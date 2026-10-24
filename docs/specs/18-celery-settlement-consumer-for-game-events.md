# #18: Celery settlement consumer for game events

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/18
- **Phase:** Phase 2: Distributed (Weeks 5–7) (#2)
- **Blocked by:** [#14 Void and refund bets on postponed/cancelled games](14-void-and-refund-bets-on-postponed-cancelled.md), [#17 Transactional outbox and RabbitMQ publisher](17-transactional-outbox-and-rabbitmq-publisher.md)
- **Unblocks:** [#19](19-scheduled-game-ingestion-and-odds-refresh-on.md), [#20](20-settlement-recovery-test-kill-worker-mid.md), [#21](21-redis-leaderboard.md), [#24](24-prometheus-metrics-and-grafana-dashboard.md)
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

Settlement and voiding move from the in-process trigger to a Celery worker that consumes game events from RabbitMQ and processes pending bets in batches, reusing the per-bet settlement transaction. The consumer is idempotent under at-least-once delivery.

## Acceptance criteria

- [ ] Delivering the same GAME_FINISHED message twice leaves totals unchanged (idempotency test)
- [ ] Batches: a large number of pending bets settles correctly
- [ ] Workers can run as multiple concurrent instances without double payouts
- [ ] Task retries are safe
- [ ] Every money-touching test ends with a ledger reconciliation assertion (`balance == SUM(ledger_entries.amount)` for every account)
- [ ] `ruff check`, `ruff format --check`, `mypy app` and `pytest` all pass
