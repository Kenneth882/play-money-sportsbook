# #22: Redis read cache for games and odds

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/22
- **Phase:** Phase 2: Distributed (Weeks 5–7) (#2)
- **Blocked by:** [#9 Odds model (Elo) and append-only odds snapshots](09-odds-model-elo-and-append-only-odds-snapshots.md)
- **Unblocks:** —
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

Game and odds reads are served from Redis with sensible TTLs/invalidation. Bet placement continues to validate price against the database snapshot, never the cache.

## Acceptance criteria

- [ ] Cache hit/miss behaviour tested
- [ ] New odds snapshot invalidates or refreshes the cached odds
- [ ] A test proves bet validation ignores a stale cached price
- [ ] Redis outage falls back to Postgres
- [ ] `ruff check`, `ruff format --check`, `mypy app` and `pytest` all pass
