# #7: Login and authenticated requests

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/7
- **Phase:** Phase 1: Core backend (Weeks 1–4) (#1)
- **Blocked by:** [#6 Sign up with 1,000-credit signup bonus](06-sign-up-with-1-000-credit-signup-bonus.md)
- **Unblocks:** [#10](10-place-a-bet-atomically-with-idempotency-key.md), [#15](15-frontend-skeleton-sign-up-log-in-see-balance.md)
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

A registered user logs in and receives a token; protected endpoints (e.g. balance) require it and reject missing, invalid or expired tokens. Secrets come from env vars.

## Acceptance criteria

- [ ] Login with correct credentials returns a token; wrong credentials are rejected without revealing which field was wrong
- [ ] Protected endpoints return 401 without a valid token
- [ ] A user can only read their own account
- [ ] Signing secret is read from env, not committed
- [ ] `ruff check`, `ruff format --check`, `mypy app` and `pytest` all pass
