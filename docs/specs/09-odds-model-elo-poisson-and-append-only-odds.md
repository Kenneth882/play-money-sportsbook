# #9: Odds model (Elo/Poisson) and append-only odds snapshots

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/9
- **Phase:** Phase 1: Core backend (Weeks 1–4) (#1)
- **Blocked by:** [#8 Fixture ingestion from football-data.org](08-fixture-ingestion-from-football-data-org.md)
- **Unblocks:** [#10](10-place-a-bet-atomically-with-idempotency-key.md), [#22](22-redis-read-cache-for-fixtures-and-odds.md)
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

For each scheduled fixture the system computes home/draw/away prices from an in-house Elo/Poisson model with a bookmaker margin, and stores them as append-only odds snapshots. The API returns the latest snapshot per fixture.

## Acceptance criteria

- [ ] odds table is append-only (snapshots are inserted, never updated); prices stored as NUMERIC
- [ ] Unit tests: model probabilities sum to ~1 before margin; implied probabilities exceed 1 after margin
- [ ] Unit tests cover edge cases (evenly matched teams, heavy favourite)
- [ ] Generating odds again inserts a new snapshot and the API serves the newest
- [ ] `ruff check`, `ruff format --check`, `mypy app` and `pytest` all pass
