# CLAUDE.md

This file guides Claude Code when working in this repository.

## Project

**HoopsExchange** — a play-money NBA sportsbook built as a backend/infrastructure engineering project. Users get virtual credits, bet on real NBA games (home/away moneyline; there is no draw) at locked odds, and compete on a leaderboard.

The betting is the use case; the real goal is **correctness under concurrency, duplicate messages, and failures**. No lost credits, no double payouts, no negative balances — ever. When a trade-off arises between speed/convenience and financial correctness, choose correctness.

## Stack

| Layer | Choice |
|---|---|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.x, Alembic, Pydantic v2 |
| Database | PostgreSQL (source of truth) |
| Cache / rate limiting / leaderboard | Redis |
| Messaging | RabbitMQ |
| Workers | Celery (game ingestion, odds, settlement, outbox publisher) |
| Frontend | Next.js + TypeScript (keep it functional, not fancy) |
| Testing | pytest, Testcontainers (real Postgres), k6 for load |
| Infra | Docker Compose first → Kubernetes (kind/minikube) → AWS later |
| CI | GitHub Actions |
| Observability | Prometheus, Grafana, OpenTelemetry |
| Data | balldontlie API free tier; odds generated in-house (Elo with home-court advantage) |

## Architecture rules

- **Betting and Wallet live in the same FastAPI app and the same Postgres database.** Placing a bet must debit the wallet and record the wager atomically. Do not split them into separate services or databases.
- Workers (games, odds, settlement) run as separate processes and may scale horizontally.
- Events leave the database via a **transactional outbox**: write the outbox row in the same transaction as the state change; a publisher process forwards it to RabbitMQ. Never publish to RabbitMQ directly from inside a business transaction.
- Assume **at-least-once delivery** everywhere. Every consumer must be idempotent.
- Add infrastructure (RabbitMQ, K8s, observability) incrementally, only once the layer below it works and is tested.

## Data model

```
users            id, email, password_hash, created_at
accounts         id, user_id, balance BIGINT CHECK (balance >= 0)
ledger_entries   id, account_id, amount, type, bet_id, created_at
                 partial UNIQUE (bet_id, type) for BET_PAYOUT / BET_REFUND
games            id, external_id UNIQUE, home_team, away_team, tip_off, status
                 (scheduled|in_progress|final|postponed|cancelled),
                 home_score, away_score
odds             id, game_id, outcome, price, created_at   (append-only snapshots)
bets             id, account_id, game_id, outcome, stake, locked_price,
                 status (pending|won|lost|void), idempotency_key UNIQUE, created_at
outbox           id, event_type, payload JSONB, created_at, published_at
```

Ledger entry types: `SIGNUP_BONUS`, `BET_PLACED`, `BET_PAYOUT`, `BET_REFUND`.

Outcomes are `home` or `away` only, enforced by `CHECK (outcome IN ('home', 'away'))` on `odds` and `bets`.

## Financial invariants (non-negotiable)

1. `balance >= 0` — enforced by a DB `CHECK` constraint, not just application code.
2. `accounts.balance == SUM(ledger_entries.amount)` for every account.
3. A bet is settled at most once.
4. A payout never exceeds `stake * locked_price` (per the documented rounding rule).
5. Failed transactions leave no partial financial writes.

Rules that follow from these:

- **The ledger is append-only.** Never `UPDATE` or `DELETE` ledger rows. Corrections are new entries.
- Every balance change writes a ledger entry **in the same transaction**.
- Money is **integer credit units** (`BIGINT`). Never use `float` for stakes, prices-applied-to-stakes, or balances. Odds prices are `NUMERIC`; payout = `floor(stake * locked_price)` — round down, document it, test it.
- Enforce invariants with DB constraints wherever possible; tests verify the rest.
- New users get 1,000 credits via a `SIGNUP_BONUS` ledger entry, not by setting the balance directly.

## Critical flows

### Placing a bet (single transaction)
1. Request carries a client-generated **idempotency key**. If a bet with that key exists, return it unchanged (same response, no new writes).
2. `SELECT ... FROM accounts WHERE id = :id FOR UPDATE`.
3. Validate on the server: game exists, status is scheduled, `now() < tip_off`, outcome valid, price matches the current odds snapshot. Never trust client-supplied odds.
4. Check `balance >= stake`; otherwise raise `InsufficientFunds`.
5. Insert bet (with `locked_price`), insert `BET_PLACED` ledger entry (negative amount), decrement balance.
6. Commit, or roll back everything.

Lock ordering: always lock account rows before bet rows to avoid deadlocks.

### Settling a game
1. Game worker detects final score → in one transaction update the game and write a `GAME_FINISHED` outbox row.
2. Settlement worker consumes the event and processes pending bets in batches.
3. Per bet, in one transaction: lock the bet, skip if not `pending`, mark `won`/`lost` (higher final score wins), for winners insert a `BET_PAYOUT` ledger entry and credit the balance.
4. The unique `(bet_id, type)` constraint is the backstop: a duplicate payout must fail and roll back, not double-pay.
5. Postponed/cancelled games → bets `void`, `BET_REFUND` of the stake. A game reported final with tied scores (should never happen) is voided the same way.
6. Rerunning settlement for the same game must be a no-op.

## Repository layout (target)

```
backend/
  app/
    api/          # FastAPI routers (thin: validation + call service)
    services/     # business logic: betting, wallet, settlement, odds
    models/       # SQLAlchemy models
    schemas/      # Pydantic request/response models
    db/           # session, transaction helpers
    workers/      # Celery tasks: games, odds, settlement, outbox publisher
  alembic/
  tests/
    unit/  integration/  concurrency/  idempotency/  recovery/
frontend/         # Next.js
infra/
  docker-compose.yml
  k8s/
load/             # k6 scripts
.github/workflows/
```

## Commands

> Update this section as the real tooling lands.

Python tooling is managed by **uv** (`backend/pyproject.toml` + `uv.lock`). Run backend
commands from `backend/`; run `docker compose` from the repo root (root `compose.yaml`
includes `infra/docker-compose.yml`).

```bash
# repo root
docker compose up --build                     # Postgres + backend on :8000 (GET /health)
docker compose run --rm backend alembic upgrade head

# backend/
uv sync                                       # install deps incl. dev tools
uv run pytest                                 # all tests; integration ones need Docker running
uv run pytest tests/unit                      # fast, no DB
uv run pytest tests/integration               # real Postgres via Testcontainers
uv run ruff check . && uv run ruff format --check .
uv run mypy app tests alembic
uv run alembic revision --autogenerate -m "msg"   # needs DATABASE_URL; always review the file
```

Tests run on the host, not in the backend container: Testcontainers needs the host Docker
daemon. The shared `postgres_url` / `engine` / `session_factory` fixtures in
`backend/tests/conftest.py` start one migrated Postgres per test run.

CI (`.github/workflows/ci.yml`) runs on every pull request and every push to `main`, as two
jobs: **Lint & types** (ruff check, ruff format --check, mypy) and **Tests** (full pytest,
including Testcontainers against real Postgres using the runner's Docker). Merging needs
both checks green once `main` branch protection requires them (Settings → Branches). To
reproduce CI locally, run the backend commands above, installing with `uv sync --frozen`
instead of `uv sync`.

## Testing expectations

- Integration, concurrency, and idempotency tests run against **real Postgres** (Testcontainers). Never mock the database for anything touching money.
- Required concurrency test: account with 1,000 credits, 500 simultaneous 100-credit bets with distinct idempotency keys → exactly 10 succeed, the rest get insufficient-funds, final balance 0, ledger reconciles.
- Idempotency tests: same HTTP request twice → one bet; same settlement message twice → totals unchanged.
- Recovery tests: kill the settlement worker mid-batch, restart, verify every bet settles exactly once.
- Every test touching money ends with a ledger reconciliation assertion.
- Unit-test odds math (home + away probabilities sum to 1 before margin) and payout rounding.

## Coding conventions

- Routers stay thin; logic goes in `services/`. Services take an explicit session; transaction boundaries are explicit (`with session.begin():`), never implicit autocommit.
- Type hints everywhere; `mypy` clean. Pydantic models at API boundaries.
- Migrations via Alembic only — never hand-edit the schema. Constraints (CHECK, UNIQUE, FK) belong in migrations.
- Celery tasks must be safe to retry: idempotent, no side effects outside the DB transaction except via the outbox.
- Use structured logging with `bet_id`, `account_id`, `game_id`, and idempotency key where relevant.
- Secrets come from env vars; never commit `.env` or API keys.

## Things to avoid

- Read-modify-write of balances without `FOR UPDATE`.
- Floats for money.
- Updating balances without a matching ledger entry.
- Publishing messages outside the outbox.
- Mocking Postgres in money-path tests.
- Adding Kubernetes, new services, or extra betting markets before the transactional core and its tests are solid.
- Presenting illustrative metrics as measured results (README/resume numbers must come from real k6 runs).

## Roadmap

1. **Weeks 1–4 — core backend:** auth, accounts, ledger, game ingestion, odds model, bet placement with locking + idempotency, settlement, voids/refunds, bet history, integration tests.
2. **Weeks 5–7 — distributed:** Celery + RabbitMQ settlement, Redis leaderboard/caching, outbox, worker recovery, K8s manifests.
3. **Weeks 8–10 — reliability/DevOps:** CI/CD, Prometheus/Grafana/OTel, k6 load tests, documented performance findings.

Stretch (only after the above): dynamic odds, Redis token-bucket rate limiting, failure-injection experiments, more markets, admin settle/void dashboard.

## Agent skills

### Issue tracker

Issues and specs are tracked as GitHub Issues on Kenneth882/play-money-sportsbook (via `gh`). See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary: needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one root `GLOSSARY.md` plus `docs/adr/`. See `docs/agents/domain.md`.
