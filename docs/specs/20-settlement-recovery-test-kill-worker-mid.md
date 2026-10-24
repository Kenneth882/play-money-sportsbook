# #20: Settlement recovery test: kill worker mid-batch

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/20
- **Phase:** Phase 2: Distributed (Weeks 5–7) (#2)
- **Blocked by:** [#18 Celery settlement consumer for game events](18-celery-settlement-consumer-for-game-events.md)
- **Unblocks:** [#23](23-kubernetes-manifests-for-kind.md)
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

Prove settlement survives crashes: kill the settlement worker partway through a batch, restart it, and verify every bet settles exactly once.

## Acceptance criteria

- [ ] Worker process is genuinely terminated mid-batch (not a simulated exception only)
- [ ] After restart, all bets are settled; none paid twice, none left pending
- [ ] Test is repeatable in CI
- [ ] Every money-touching test ends with a ledger reconciliation assertion (`balance == SUM(ledger_entries.amount)` for every account)
