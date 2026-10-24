# #19: Scheduled game ingestion and odds refresh on Celery beat

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/19
- **Phase:** Phase 2: Distributed (Weeks 5–7) (#2)
- **Blocked by:** [#18 Celery settlement consumer for game events](18-celery-settlement-consumer-for-game-events.md)
- **Unblocks:** [#23](23-kubernetes-manifests-for-kind.md)
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

Game ingestion and odds generation run as periodic Celery tasks rather than manual jobs, safe to retry and safe to run concurrently.

## Acceptance criteria

- [ ] Periodic schedule configured; intervals respect balldontlie free-tier rate limits
- [ ] Overlapping or retried runs produce no duplicate games and correct snapshots
- [ ] Final-score detection flows through the outbox to settlement end to end
- [ ] `ruff check`, `ruff format --check`, `mypy app` and `pytest` all pass
