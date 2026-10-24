# #9: Odds model (Elo) and append-only odds snapshots

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/9
- **Phase:** Phase 1: Core backend (Weeks 1–4) (#1)
- **Blocked by:** [#8 Game ingestion from balldontlie](08-game-ingestion-from-balldontlie.md)
- **Unblocks:** [#10](10-place-a-bet-atomically-with-idempotency-key.md), [#22](22-redis-read-cache-for-games-and-odds.md)
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

For each scheduled game the system computes home/away moneyline prices from an in-house Elo model (team ratings plus a home-court advantage, converted to a win probability with the logistic Elo formula) with a bookmaker margin, and stores them as append-only odds snapshots. The API returns the latest snapshot per game. There is no draw outcome: NBA games go to overtime until there is a winner.

## Acceptance criteria

- [ ] odds table has `CHECK (outcome IN ('home', 'away'))`
- [ ] odds table is append-only (snapshots are inserted, never updated); prices stored as NUMERIC
- [ ] Unit tests: home and away probabilities sum to 1 before margin; implied probabilities exceed 1 after margin
- [ ] Unit tests cover edge cases (evenly matched teams, heavy favourite, home-court advantage moves the price toward the home team)
- [ ] Generating odds again inserts a new snapshot and the API serves the newest
- [ ] `ruff check`, `ruff format --check`, `mypy app` and `pytest` all pass
