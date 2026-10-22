# #6: Sign up with 1,000-credit signup bonus

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/6
- **Phase:** Phase 1: Core backend (Weeks 1–4) (#1)
- **Blocked by:** [#4 Walking skeleton: Compose, FastAPI, Alembic, Testcontainers](04-walking-skeleton-compose-fastapi-alembic.md)
- **Unblocks:** [#7](07-login-and-authenticated-requests.md)
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

A new user signs up with email and password. In one transaction the system creates the user, their account and a `SIGNUP_BONUS` ledger entry of 1,000 credits; the balance is derived from that entry, never set directly. The user can read their balance. This ticket also introduces the shared ledger-reconciliation test helper every later money test uses.

## Acceptance criteria

- [ ] Migrations create users, accounts (`balance BIGINT CHECK (balance >= 0)`) and ledger_entries; constraints live in migrations
- [ ] Money is integer credit units (BIGINT); no floats anywhere
- [ ] Signup is atomic: a failure mid-signup leaves no user, account or ledger row
- [ ] Duplicate email is rejected cleanly
- [ ] Passwords are stored hashed
- [ ] A test proves the DB CHECK rejects a negative balance even when application code is bypassed
- [ ] Shared reconciliation helper exists and is used
- [ ] Every money-touching test ends with a ledger reconciliation assertion (`balance == SUM(ledger_entries.amount)` for every account)
- [ ] `ruff check`, `ruff format --check`, `mypy app` and `pytest` all pass
