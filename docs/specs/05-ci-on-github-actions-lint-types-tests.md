# #5: CI on GitHub Actions: lint, types, tests

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/5
- **Phase:** Phase 1: Core backend (Weeks 1–4) (#1)
- **Blocked by:** [#4 Walking skeleton: Compose, FastAPI, Alembic, Testcontainers](04-walking-skeleton-compose-fastapi-alembic.md)
- **Unblocks:** —
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

Every pull request runs ruff (check + format check), mypy and the full pytest suite, including Testcontainers integration tests, on GitHub Actions. A red check blocks merging.

## Acceptance criteria

- [ ] Workflow runs on pull requests and pushes to main
- [ ] Testcontainers tests run in CI against real Postgres (no DB mocking)
- [ ] A deliberately failing test or lint error turns the check red
- [ ] README or CLAUDE.md notes how CI runs
