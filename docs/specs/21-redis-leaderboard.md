# #21: Redis leaderboard

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/21
- **Phase:** Phase 2: Distributed (Weeks 5–7) (#2)
- **Blocked by:** [#18 Celery settlement consumer for game events](18-celery-settlement-consumer-for-game-events.md), [#16 Frontend: browse games, place bets, view history](16-frontend-browse-games-place-bets-view-history.md)
- **Unblocks:** [#23](23-kubernetes-manifests-for-kind.md)
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

Users see a leaderboard ranked by balance (or net winnings — decide and document), served from a Redis sorted set updated from settlement events and rebuildable from Postgres, which remains the source of truth. Includes a leaderboard page in the frontend.

## Acceptance criteria

- [ ] Leaderboard API and UI page
- [ ] Updates after settlement; duplicate events don't double-count
- [ ] A rebuild command reconstructs it from Postgres and matches
- [ ] Redis outage degrades the leaderboard only, never betting or settlement
- [ ] `ruff check`, `ruff format --check`, `mypy app` and `pytest` all pass
