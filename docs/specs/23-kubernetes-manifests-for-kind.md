# #23: Kubernetes manifests for kind

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/23
- **Phase:** Phase 2: Distributed (Weeks 5–7) (#2)
- **Blocked by:** [#19 Scheduled fixture ingestion and odds refresh on Celery beat](19-scheduled-fixture-ingestion-and-odds-refresh.md), [#20 Settlement recovery test: kill worker mid-batch](20-settlement-recovery-test-kill-worker-mid.md), [#21 Redis leaderboard](21-redis-leaderboard.md)
- **Unblocks:** —
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

The full stack (API, workers, publisher, Postgres, Redis, RabbitMQ, frontend) runs on a local kind cluster, with workers scalable horizontally. Secrets via K8s Secrets, not committed.

## Acceptance criteria

- [ ] Documented steps bring the stack up on kind
- [ ] Scaling the settlement worker to multiple replicas keeps settlement exactly-once
- [ ] Migrations run as a Job before the API starts
- [ ] No secrets committed
