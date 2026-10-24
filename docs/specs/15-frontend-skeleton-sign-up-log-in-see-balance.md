# #15: Frontend skeleton: sign up, log in, see balance

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/15
- **Phase:** Phase 1: Core backend (Weeks 1–4) (#1)
- **Blocked by:** [#7 Login and authenticated requests](07-login-and-authenticated-requests.md)
- **Unblocks:** [#16](16-frontend-browse-games-place-bets-view-history.md)
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

A functional (not fancy) Next.js + TypeScript app where a user can sign up, log in and see their credit balance, talking to the real backend. Added to Docker Compose.

## Acceptance criteria

- [ ] Sign up → logged in → balance shows 1,000
- [ ] Login errors are shown to the user
- [ ] Runs under `docker compose up`
- [ ] TypeScript type check passes
