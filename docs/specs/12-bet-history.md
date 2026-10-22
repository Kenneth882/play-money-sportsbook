# #12: Bet history

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/12
- **Phase:** Phase 1: Core backend (Weeks 1–4) (#1)
- **Blocked by:** [#10 Place a bet atomically with idempotency key](10-place-a-bet-atomically-with-idempotency-key.md)
- **Unblocks:** [#16](16-frontend-browse-fixtures-place-bets-view.md)
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

An authenticated user lists their own bets, newest first, with fixture, outcome, stake, locked price, status and payout (once settled).

## Acceptance criteria

- [ ] Users see only their own bets
- [ ] Pagination or a sensible limit
- [ ] Status reflects pending/won/lost/void
- [ ] `ruff check`, `ruff format --check`, `mypy app` and `pytest` all pass
