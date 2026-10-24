# #8: Game ingestion from balldontlie

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/8
- **Phase:** Phase 1: Core backend (Weeks 1–4) (#1)
- **Blocked by:** [#4 Walking skeleton: Compose, FastAPI, Alembic, Testcontainers](04-walking-skeleton-compose-fastapi-alembic.md)
- **Unblocks:** [#9](09-odds-model-elo-and-append-only-odds-snapshots.md)
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

A runnable job fetches NBA games from the balldontlie API and upserts them keyed by `external_id`, recording home and away teams, tip-off time, status and scores. Provider statuses are mapped to `scheduled`, `in_progress`, `final`, `postponed` or `cancelled`. Running it twice changes nothing. Games are listable through the API. Tests use recorded API payloads so they need no API key; running against the live API needs the maintainer's key from env.

## Acceptance criteria

- [ ] games table with `external_id UNIQUE`, created via migration
- [ ] Provider statuses map to scheduled / in_progress / final / postponed / cancelled; unknown statuses are logged and leave the game unchanged
- [ ] Re-running ingestion on the same payload is a no-op (no duplicates, no spurious updates)
- [ ] Status and score changes in a newer payload update the existing game
- [ ] API lists upcoming games
- [ ] Tests run against recorded payloads with real Postgres; no network in tests
- [ ] API key read from env; never committed
- [ ] Human step: maintainer supplies a balldontlie API key to verify one live run
- [ ] `ruff check`, `ruff format --check`, `mypy app` and `pytest` all pass
