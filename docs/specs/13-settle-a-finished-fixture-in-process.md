# #13: Settle a finished fixture (in-process)

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/13
- **Phase:** Phase 1: Core backend (Weeks 1–4) (#1)
- **Blocked by:** [#10 Place a bet atomically with idempotency key](10-place-a-bet-atomically-with-idempotency-key.md)
- **Unblocks:** [#14](14-void-and-refund-bets-on-postponed-cancelled.md), [#17](17-transactional-outbox-and-rabbitmq-publisher.md)
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

When ingestion sees a fixture's final score, the fixture is updated and its pending bets are settled. Each bet is settled in its own transaction: lock the bet, skip if not pending, mark won/lost, and for winners insert a `BET_PAYOUT` ledger entry of `floor(stake * locked_price)` and credit the balance. A partial UNIQUE `(bet_id, type)` constraint for payout/refund entries is the backstop against double payment. Settlement is triggered directly in this phase; the outbox replaces the trigger in Phase 2.

## Acceptance criteria

- [ ] Partial UNIQUE `(bet_id, type)` for BET_PAYOUT/BET_REFUND added via migration
- [ ] Unit tests for payout rounding (`floor`) including fractional cases; rounding rule documented
- [ ] Payout never exceeds `stake * locked_price`
- [ ] Re-running settlement for the same fixture is a no-op (totals unchanged)
- [ ] A forced duplicate payout insert fails and rolls back rather than double-paying
- [ ] Account locked before bet (lock ordering)
- [ ] Every money-touching test ends with a ledger reconciliation assertion (`balance == SUM(ledger_entries.amount)` for every account)
- [ ] `ruff check`, `ruff format --check`, `mypy app` and `pytest` all pass
