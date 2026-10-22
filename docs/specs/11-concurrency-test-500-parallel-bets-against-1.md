# #11: Concurrency test: 500 parallel bets against 1,000 credits

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/11
- **Phase:** Phase 1: Core backend (Weeks 1–4) (#1)
- **Blocked by:** [#10 Place a bet atomically with idempotency key](10-place-a-bet-atomically-with-idempotency-key.md)
- **Unblocks:** [#26](26-k6-load-test-and-measured-findings-write-up.md)
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

Prove bet placement is safe under contention: an account with 1,000 credits receives 500 simultaneous 100-credit bets with distinct idempotency keys.

## Acceptance criteria

- [ ] Exactly 10 bets succeed; the rest get insufficient-funds
- [ ] Final balance is exactly 0; never negative at any point
- [ ] Runs against real Postgres via Testcontainers with genuine parallelism (not serialized in-process)
- [ ] Test is deterministic across repeated runs
- [ ] Every money-touching test ends with a ledger reconciliation assertion (`balance == SUM(ledger_entries.amount)` for every account)
