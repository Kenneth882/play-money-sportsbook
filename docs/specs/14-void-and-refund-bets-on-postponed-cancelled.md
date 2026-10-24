# #14: Void and refund bets on postponed/cancelled games

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/14
- **Phase:** Phase 1: Core backend (Weeks 1–4) (#1)
- **Blocked by:** [#13 Settle a finished game (in-process)](13-settle-a-finished-game-in-process.md)
- **Unblocks:** [#18](18-celery-settlement-consumer-for-game-events.md)
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

When a game is postponed or cancelled, its pending bets become `void` and each receives a `BET_REFUND` ledger entry equal to its stake, credited to the balance, one transaction per bet.

## Acceptance criteria

- [ ] Refund equals the stake exactly
- [ ] Re-running is a no-op; the unique `(bet_id, type)` backstop prevents double refunds
- [ ] Already-settled bets are untouched
- [ ] Every money-touching test ends with a ledger reconciliation assertion (`balance == SUM(ledger_entries.amount)` for every account)
- [ ] `ruff check`, `ruff format --check`, `mypy app` and `pytest` all pass
