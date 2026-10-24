# #25: OpenTelemetry tracing from API to settlement

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/25
- **Phase:** Phase 3: Reliability/DevOps (Weeks 8–10) (#3)
- **Blocked by:** [#24 Prometheus metrics and Grafana dashboard](24-prometheus-metrics-and-grafana-dashboard.md)
- **Unblocks:** —
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

A single trace follows a request from the API through the outbox publisher and RabbitMQ to the settlement worker, with bet_id/game_id attributes, viewable in a local trace backend.

## Acceptance criteria

- [ ] Trace context propagates across the outbox and message broker
- [ ] Spans carry bet_id, account_id, game_id where relevant
- [ ] Tracing failure never affects request or settlement outcomes
