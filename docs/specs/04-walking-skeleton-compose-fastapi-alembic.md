# #4: Walking skeleton: Compose, FastAPI, Alembic, Testcontainers

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/4
- **Phase:** Phase 1: Core backend (Weeks 1–4) (#1)
- **Blocked by:** None (can start immediately)
- **Unblocks:** [#5](05-ci-on-github-actions-lint-types-tests.md), [#6](06-sign-up-with-1-000-credit-signup-bonus.md), [#8](08-game-ingestion-from-balldontlie.md)
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

A developer can run `docker compose up` and get Postgres plus the FastAPI backend, with a health endpoint returning 200. The backend has a SQLAlchemy session with explicit transaction boundaries, an Alembic baseline migration, and a Testcontainers-backed real-Postgres fixture that later integration tests reuse. Lint and type checking are configured. Follow the repository layout in CLAUDE.md.

## Acceptance criteria

- [ ] `docker compose up --build` starts Postgres and the backend; health endpoint returns 200
- [ ] `alembic upgrade head` runs cleanly against the Compose database
- [ ] One integration test runs against real Postgres via Testcontainers and passes
- [ ] ruff and mypy are configured and pass on the skeleton
- [ ] CLAUDE.md Commands section updated to match the real tooling
