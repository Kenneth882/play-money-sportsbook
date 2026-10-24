# #10: Place a bet atomically with idempotency key

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/10
- **Phase:** Phase 1: Core backend (Weeks 1–4) (#1)
- **Blocked by:** [#7 Login and authenticated requests](07-login-and-authenticated-requests.md), [#9 Odds model (Elo) and append-only odds snapshots](09-odds-model-elo-and-append-only-odds-snapshots.md)
- **Unblocks:** [#11](11-concurrency-test-500-parallel-bets-against-1.md), [#12](12-bet-history.md), [#13](13-settle-a-finished-game-in-process.md)
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

An authenticated user places a home/away moneyline bet with a stake and a client-generated idempotency key. In a single transaction the server locks the account row (`FOR UPDATE`), validates the game is scheduled and before tip-off, checks the requested price matches the current odds snapshot (never trusting client odds), checks funds, inserts the bet with `locked_price`, writes a negative `BET_PLACED` ledger entry and decrements the balance. Repeating a request with the same idempotency key returns the original bet unchanged with no new writes. Lock ordering: account before bet.

## Acceptance criteria

- [ ] bets table with `CHECK (outcome IN ('home', 'away'))`, `idempotency_key UNIQUE`, status enum, `locked_price`, via migration
- [ ] Same request twice → exactly one bet and one ledger entry; identical response
- [ ] Insufficient funds → `InsufficientFunds` error, no writes
- [ ] Game started / not scheduled / invalid outcome (including `draw`) / stale price → rejected, no writes
- [ ] Any failure mid-transaction leaves no partial financial writes
- [ ] Structured logs include bet_id, account_id, game_id and idempotency key
- [ ] Every money-touching test ends with a ledger reconciliation assertion (`balance == SUM(ledger_entries.amount)` for every account)
- [ ] `ruff check`, `ruff format --check`, `mypy app` and `pytest` all pass
