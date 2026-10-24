# #24: Prometheus metrics and Grafana dashboard

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/24
- **Phase:** Phase 3: Reliability/DevOps (Weeks 8–10) (#3)
- **Blocked by:** [#18 Celery settlement consumer for game events](18-celery-settlement-consumer-for-game-events.md)
- **Unblocks:** [#25](25-opentelemetry-tracing-from-api-to-settlement.md), [#26](26-k6-load-test-and-measured-findings-write-up.md)
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

The API and workers expose Prometheus metrics, and a provisioned Grafana dashboard shows bet placement latency and error rates (including insufficient-funds), outbox lag (oldest unpublished row), and settlement throughput.

## Acceptance criteria

- [ ] Prometheus and Grafana run in Compose with the dashboard provisioned
- [ ] Outbox lag metric rises when the publisher is stopped and recovers when restarted
- [ ] Metrics have bounded label cardinality (no per-user labels)
