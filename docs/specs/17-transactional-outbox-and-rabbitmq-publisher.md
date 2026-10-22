# #17: Transactional outbox and RabbitMQ publisher

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/17
- **Phase:** Phase 2: Distributed (Weeks 5–7) (#2)
- **Blocked by:** [#13 Settle a finished fixture (in-process)](13-settle-a-finished-fixture-in-process.md)
- **Unblocks:** [#18](18-celery-settlement-consumer-for-fixture-events.md)
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

Fixture-finished (and postponed/cancelled) state changes write an outbox row in the same transaction as the fixture update. A separate publisher process forwards unpublished rows to RabbitMQ and sets `published_at`. Nothing publishes to RabbitMQ from inside a business transaction. RabbitMQ is added to Compose.

## Acceptance criteria

- [ ] outbox table via migration; row written atomically with the fixture update
- [ ] Rolling back the fixture update leaves no outbox row
- [ ] Publisher crash between publish and marking published results in a re-publish (at-least-once), never a loss
- [ ] Multiple publisher instances don't lose events
- [ ] `ruff check`, `ruff format --check`, `mypy app` and `pytest` all pass
