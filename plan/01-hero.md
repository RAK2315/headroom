# 01 Hero (the offense)

Everything in the plan exists to make this file real. If a trade-off is unclear, choose whatever makes the Season Theatre more convincing.

## Hero moment spec: Season Theatre

### Screen at 1920x1080 (the projector size; design for it first)
```
+--------------------------------------------------------------------------------------------+
| HEADROOM  Season W26 (5 Oct 2026 - 4 Apr 2027)  Budget ₹40 Cr  Target 95%  [Simulated]   |  header 56px
+------------------------------------------------------------+-------------------------------+
|                                                            | LEDGER          wk 9 / 26     |
|          PRESSURE MAP (deck.gl, no tiles)                  |                               |
|   Europe ........................ Gulf ...... SE Asia      |  Playbook  Profit-only Headroom|
|   LON  PAR  IST          DXB   MLE            BKK  KUL     |  sold-out  31.2%  18.4%  4.9% |
|                    DEL BOM BLR (hubs, arcs)   SIN  HKG DPS |  profit ₹  ...    ...    ...  |
|   Each destination = reservoir gauge (3 tier rings)        |  capital   ...    ...    ...  |
|   red sparks spill when demand overflows                   |  wasted    ...    ...    ...  |
|   radar haze = sell-out pressure this week                 |  sparkline per desk           |
|                                                            |  [Re-plan diff card appears]  |
+------------------------------------------------------------+-------------------------------+
| SEASON LANES: 10 destination rows x 26 week columns. Past = realised, future = fog/hatch.  |  260px
| Playhead. Shock cards drop at their week.   [Play] [Pause] [Step] [1x 2x 4x] [Play as me]  |
+--------------------------------------------------------------------------------------------+
```
- Map panel: 1240x764 px. Ledger: 680x764 px. Lanes strip: 1920x260 px.
- Desk selector on the map: chips `Playbook | Profit-only | Headroom` (default Headroom). The map shows the selected desk; the ledger always shows all desks.

### Exact numbers
- 26 weeks at 1x = 1.5 s per week, so a full season plays in 39 s. 2x = 0.75 s, 4x = 0.375 s.
- Map renders at 60 fps on the demo laptop (integrated GPU) with: 10 destination gauges, 15 flight arcs, up to 4,000 live spark particles, 1 heatmap layer.
- Spark particles: each sold-out search batch of 25 searches = 1 spark (so 4,000 sparks = 100,000 sold-out searches on screen at most). Spark life 1.2 s, falls 40 px with slight drift, colour `--danger`.
- Gauge: outer ring 3 arcs (value, core, premium tier). Arc fill = secured units (hard + allot) / forecast P50 demand for the current week, capped at 120%. Inner disc = free-sale availability (dims as close-outs rise).
- Flight arcs: width 1-8 px proportional to series-block seats for the current week; animated dash along the arc at a speed proportional to bookings.
- Radar haze: HeatmapLayer weight = P(sold out this week) per destination from the scenarios, ramp `--pressure-0` to `--pressure-4`.
- Ledger numbers update every week with a 300 ms count-up animation; mono tabular numerals; the leading desk per metric gets a small marker.
- Shock at week 9: card slides down from the lanes strip over 400 ms; the playhead pauses for 2.0 s; the re-plan request fires; Headroom's diff card shows in the ledger within 1.0 s of the card appearing (measured: replan p95 at most 0.6 s plus render).
- Diff card content (max 5 lines): e.g. "+180 Dubai core allotment (wk 10-13) · +60 Dubai premium hard (wk 12) · release 90 Singapore value before cut-off (wk 11) · Bali markup 8% to 12% (wk 12-13) · capital +₹1.9 Cr". Lines are generated from the plan diff, never by an LLM.
- End state (week 26): playback stops, ledger freezes, a result line fades in under the lanes: "Same ₹40 Cr. Headroom: 4.9% sold-out searches on peak dates vs 31.2% (playbook) and 18.4% (profit-only). Profit ₹x Cr vs ₹y Cr." (numbers from the actual run).

### Trigger and timing in the demo
- Presenter clicks Play at 0:20 (the screen is already open from the Demand Lens via the "Play the season" button).
- 0:20-0:33 weeks 0-8 play (1.5 s each); presenter narrates the map.
- 0:33 shock lands at week 9; 2 s pause; diff card.
- 0:36-1:00 weeks 10-17 at 1x, then presenter presses 4x; season ends about 1:05.
- 1:05-1:30 presenter reads the result line and clicks a lane cell to show "what happened in Dubai at New Year" (tooltip with the three desks' outcomes).

### The 2 seconds before and after
- Before: Demand Lens shows the gap between bookings and true demand for Dubai premium New Year 2025. Presenter: "Now watch three desks buy for this coming season with the same budget." Click "Play the season".
- After the shock: the presenter points at the diff card: "It just moved ₹1.9 Cr while the others are still on last month's plan."

## Showpiece spec: the decomposition engine
- What: for each of 1,170 cells, the engine evaluates every option on a grid of (markup level 3 x hard units 12 x allotment units 12) = 432 options against S correlated demand scenarios (S=128 default, 256 for proof runs) using the exact recourse logic (serve hard first, then allotment, then free sale up to the scenario's free-sale capacity, else sold out; utilisation penalty; salvage; cancellations). This builds value tables of expected profit, expected served units, capital and per-scenario profit.
- The budget and availability target are turned into prices (capital price lambda, availability weight mu) found by nested bisection; each cell then picks its best option independently in vectorised numpy. A risk weight beta penalises each option's downside (mean shortfall below its scenario median), and portfolio P10 and CVaR 5% are computed exactly by summing per-scenario profits of the chosen options.
- Supplier lever: greedy outer loop. For each candidate supplier, recompute only the affected cells with boosted free-sale capacity, re-allocate, and keep the supplier if the objective gain exceeds its cost and it goes live before the cells it helps.
- In-season re-plan: commitments already made are sunk offsets; the grid is over increments (top up, release, re-price) for the remaining cells, with S=64.
- Why it is hard: a joint two-stage stochastic MILP at this size (1.17 M variables at S=128) did not solve in 60 s with HiGHS, nor did its LP relaxation (spike, 2026-11-07, plan/spikes/RESULTS.md). The decomposition is what makes it interactive.
- Judge sentence: "We turn the budget and the availability target into prices, which lets us solve over a thousand small buying decisions exactly and still re-plan the whole season in about a second."
- Proven real in the demo:
  - The Plan Studio shows solve time in ms on every run, and changing the budget re-solves live.
  - An "Exact check" badge in Proof shows the decomposition objective vs the exact HiGHS MILP on a 4-pool x 4-week instance (gap printed, target at most 2%).
  - Tests in `engine/tests/` run in CI.

## USP amplifiers (each proves one USP claim)
| Amplifier | USP claim it proves | Where |
|---|---|---|
| Sold-out ledger as the first metric everywhere | Availability is first-class | Theatre ledger, Plan Studio header |
| Availability target that can be infeasible ("Needs ₹6.1 Cr more") | Availability is a constraint, not a decoration | Plan Studio |
| Contract chips on every buy line (HARD / ALLOT / FREE) and the Contract Lab | Contract type per pool-week | Plan Studio, Contract Lab |
| Capital-at-risk vs capital-committed split | Answers TBO's cash concern | Plan Studio, ledger |
| Supplier lever toggles with ₹ value | Supplier integration lever | Supplier screen, diff card |
| Shock + diff card + release before cut-off | Weekly re-planning | Theatre |
| Profit-only desk in the race | Profit-only optimisation is not enough | Theatre, Proof |
| Provenance panel with 5 real sources | Grounded in real public signals | Demand Lens, footer badge |
| Shadow price of capital line | Finance-ready reasoning | Plan Studio |

## Wow inventory per demo step
| Step | What impresses | Notes |
|---|---|---|
| 1 Demand Lens | The shaded gap between bookings and true demand, with the real Inside Airbnb forward-pressure curve overlaid | 20 s, transition to hero |
| 2 Theatre | Live race, sparks, shock, sub-second re-plan, ledger | the hero |
| 3 Plan Studio | Re-solve in ~1.5 s while dragging budget; infeasibility message with ₹ gap; frontier | strong second beat |
| 4 Contract Lab | The payoff fan bending as you drag; "Headroom's mix" snapping in | teaches the core idea in 30 s |
| 5 Supplier | Map lights up covered cells; sold-out drops | short |
| 6 Beat the Desk | A judge plays; the scoreboard | fun, optional on time |
| 7 Approvals + Proof | Human-in-the-loop, CSV, 500-season distribution, exact-check badge | adoption + rigour |

## Stack requirements (inputs to 02-stack.md)
1. Optimiser: initial plan at most 2.5 s (tables + allocation) for 1,170 cells x 432 options x S=128 on a 4-core laptop CPU; weekly re-plan at most 0.6 s p95 at S=64 on remaining cells.
2. Season stream: server pushes one week-state per desk per week; client buffer at least 2 weeks ahead at 1x (1.5 s/week), so compute per week must stay under 1.5 s including 3 baseline desks (cheap).
3. Map: 60 fps with 4,000 animated particles + 15 animated arcs + heatmap; no tile server (offline); land outline from a local TopoJSON.
4. Charts: fan charts, frontier, lanes (10x26 cells), sparklines; all SVG/canvas with full control of styling; no chart-kit default look.
5. Data: about 2.5 M daily rows of history (45 pools x 3 seasons x 365 days x few columns) queried by pool; analytical store that loads in-process, zero server.
6. Forecast: quantile forecasts with known-future covariates, run offline in the pipeline (minutes are fine), results stored.
7. Everything runs offline; deployed demo tolerates a cold backend by falling back to cached runs with a visible "cached run" badge.
8. Determinism: a given (plan params, truth seed, shocks) produces identical numbers every time, so the recorded video and live demo match.
