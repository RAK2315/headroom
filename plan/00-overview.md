# 00 Overview

Read this first, then `01-hero.md`, then `08-build-plan.md` for what to do today.

## Problem
TBO must decide, before a season, which hotel rooms and flight seats to secure, under which contract, with which suppliers and at what markup, so that agents searching TBO on peak dates find bookable inventory, without burning the budget on rooms that never sell. Headroom is the decision-support platform that makes that decision, measures its risk, and re-plans weekly.

## Users and surface
| Role | Uses | Main screens |
|---|---|---|
| Contracting manager (primary) | Desktop web app | Plan Studio, Contract Lab, Approvals |
| Revenue / finance lead | Desktop web app | Plan Studio frontier, Proof, Approvals (approver) |
| Judge / presenter | Same app on a 1920x1080 projector | Season Theatre, Beat the Desk |
| B2B travel agent | Does not use Headroom; benefits from fewer sold-out searches | n/a |

No login. A role switcher in the header (Contracting manager / Finance approver) controls which approval buttons show. Demo auth is fine for a hackathon; say so in the README.

## USP (verbatim from CONTEXT.md)
Headroom is the only inventory planner that optimises availability (sold-out agent searches) as a first-class target by choosing the contract type per pool-week (hard pre-buy, allotment with release cut-off, or free sale), the supplier to integrate and the markup, under a budget and a risk limit, and re-plans every week as the season unfolds, grounded in real public demand signals.

## Requirement fit (from brief.md)
Every PS ask maps to a lever or metric: availability = headline metric and target; pre-buy / supplier integration / pricing = the three levers; bookings, sold-outs, look-to-book, seasonality, external signals = demand model inputs; budget across hotels, flights, destinations, periods = 45 pools x 26 weeks under one budget; cancellations and unsold risk = scenario profit distribution and CVaR; "maximum input budget" = first input of Plan Studio.

## Scope rule
A feature is in only if it makes one of these more convincing to a TBO judge: availability gain, contract choice, supplier lever, weekly re-planning, risk in ₹, or the realism of the data. Everything else waits.

## Scope cut line
In:
- Data pipeline: real public signals -> calibrated synthetic TBO-shaped history and hidden truth seasons.
- Forecast: unconstrained weekly demand quantiles per pool with covariates; backtest.
- Optimiser: decomposition engine with three levers, availability target, risk appetite; exact-check test.
- Simulator: 4 desks, shocks, weekly re-plan, SSE streaming, cached demo runs, Monte Carlo proof.
- Screens: Season Theatre (hero), Plan Studio, Contract Lab, Supplier lever, Demand Lens, Approvals, Proof.
Out (and why):
- Real TBO API or data: not available; CSV import seam instead (STRETCH).
- Accounts, SSO, multi-tenant: no demo value.
- Mobile layout: judged on a laptop/projector.
- LLM in the decision path: numbers must be traceable. Optional "Ask Headroom" is STRETCH and never changes numbers directly.
- Live external APIs at demo time: everything is pre-fetched and committed, so the demo runs anywhere.
- Transfers, sightseeing, cruise: PS names hotels and flights.

## Hard constraints
- No real personal data. No scraping of TBO.
- Every shipped library and dataset must allow commercial use, listed in README with licence. Research-only data may be used for calibration only and must be marked.
- Every simulated number in the UI carries a "Simulated, calibrated on public data" badge.
- The demo must run fully offline from a laptop (docker compose or two terminals) and also from a deployed URL.

## Success metric
Measured on 500 simulated seasons at the same budget (₹40 Cr default):
1. Headroom's peak-date sold-out search rate is at least 3x lower than Last year's playbook and at least 2x lower than the profit-only optimiser. (Target; report the measured value, whatever it is.)
2. Headroom's expected profit is not worse than profit-only by more than 5%, and its CVaR 5% is better than playbook.
3. Weekly re-plan p95 latency at most 0.6 s; initial plan at most 2.5 s on the demo laptop.
4. Forecast P10-P90 coverage between 72% and 88% on the backtest season.
Report the measured values on screen. Parameter changes go in data/reports/calibration.md with a reason. Ways to push the results further are in 09-push-further.md.

## Demo journey (target 4:30, hero at 0:20)
1. 0:00 Demand Lens, Dubai premium, last New Year: bookings line vs unconstrained demand line; gap shaded "searches that found sold out". One sentence: "Bookings hide the demand you could not serve."
2. 0:20 HERO. Season Theatre, season W26, budget ₹40 Cr. Press Play. Three desks race. Week 9: shock card "UAE eases visa on arrival for Indians". Headroom re-plans (diff card, under 1 s). Week 26: ledger freeze-frame and result line.
3. 1:30 Plan Studio. Change budget to ₹25 Cr: availability target 95% turns amber "Best achievable 91.8%. Needs ₹6.1 Cr more." Drag back to ₹40 Cr. Open a buy line reason. Show capital price.
4. 2:30 Contract Lab. Dubai core 4-star, week of 28 Dec. Drag hard units; see profit fan and sold-out probability; click "Headroom's mix".
5. 3:00 Supplier lever. Toggle "Supplier Andaman"; map highlights Bangkok and Bali; sold-out rate drops; integration value in ₹.
6. 3:30 Beat the Desk. Judge takes "You" desk for two weeks (top up Bangkok, release Singapore). Fast-forward to result.
7. 4:00 Approvals. Submit the plan's buy orders; switch role to Finance approver; approve two; export CSV; audit trail. Close on Proof (500 seasons distribution, forecast backtest).
