# #26: k6 load test and measured findings write-up

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/26
- **Phase:** Phase 3: Reliability/DevOps (Weeks 8–10) (#3)
- **Blocked by:** [#11 Concurrency test: 500 parallel bets against 1,000 credits](11-concurrency-test-500-parallel-bets-against-1.md), [#24 Prometheus metrics and Grafana dashboard](24-prometheus-metrics-and-grafana-dashboard.md)
- **Unblocks:** —
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

A k6 script exercises bet placement under load, and a write-up records measured results (throughput, latency percentiles, error rates, and confirmation that ledger reconciliation still holds after the run), with the environment and bottlenecks found. Numbers come only from real runs.

## Acceptance criteria

- [ ] k6 script for placing bets with realistic idempotency-key use
- [ ] Post-run reconciliation check passes
- [ ] Write-up lists hardware/environment, exact command, and raw results
- [ ] No illustrative or estimated numbers presented as measured
