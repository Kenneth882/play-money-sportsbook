# #16: Frontend: browse fixtures, place bets, view history

- **Issue:** https://github.com/Kenneth882/play-money-sportsbook/issues/16
- **Phase:** Phase 1: Core backend (Weeks 1–4) (#1)
- **Blocked by:** [#12 Bet history](12-bet-history.md), [#15 Frontend skeleton: sign up, log in, see balance](15-frontend-skeleton-sign-up-log-in-see-balance.md)
- **Unblocks:** [#21](21-redis-leaderboard.md)
- **Status:** ready-for-agent

Must uphold the financial invariants and critical flows in [CLAUDE.md](../../CLAUDE.md).

## What to build

A logged-in user browses upcoming fixtures with current odds, places a bet from a bet slip, and sees bet history and their updated balance. The client generates the idempotency key once per bet attempt so retries and double-clicks don't create duplicate bets.

## Acceptance criteria

- [ ] Placing a bet updates the balance and appears in history
- [ ] Double-clicking submit creates one bet
- [ ] Insufficient-funds and stale-price errors are shown clearly
- [ ] The client never sends its own price as authoritative; the server's locked price is displayed
