# 13 Screens (wireframes at 1920x1080)

Tokens and states: 06-design-system.md. Data: 04-architecture.md contracts. The Theatre wireframe is in 01-hero.md.

## Common
Header 56 px and left nav 64 px on every screen (06). Content area = 1856 x 1024 px.

## Plan Studio `/plan`
```
+--------------------+----------------------------------------------------------------------+
| CONTROLS 360px     | SUMMARY STRIP (8 stats, mono numbers)                     solve 1,420 ms|
| Budget  ₹[ 40 ] Cr | Peak sold-out 4.9% | All 2.1% | E[profit] ₹23.1 Cr | P10 ₹19.8 Cr |  |
| [-----o---------]  | CVaR5 ₹17.2 Cr | Committed ₹38.7 Cr | At risk ₹6.1 Cr | Capital price  |
| Target   95%       |  "Next ₹1 Cr: -0.4 pp sold-outs, +₹9 L profit"                       |
| [--------o------]  +----------------------------------------------------------------------+
| Scope (Peak | All) | (warn banner only when infeasible) Best achievable 91.8%. Needs ₹6.1 Cr |
| Risk (Cautious|    +-----------------------------------+----------------------------------+
|  Balanced | Bold)  | FRONTIER 900x340                  | SUPPLIERS (compact)              |
| Levers             |  x budget ₹5-150 Cr, y-left peak  |  Sahara Beds   +₹2.4 Cr  [on]    |
|  [x] Contracts     |  sold-out %, y-right E[profit];   |  Andaman DMC   +₹1.9 Cr  [on]    |
|  [x] Suppliers     |  12 points + current marker        |  ...                             |
|  [x] Pricing       |                                   |  link: Suppliers screen          |
| [Play this plan]   +-----------------------------------+----------------------------------+
| [Submit for        | BUY LIST (scroll)  filter: destination | contract | weeks             |
|  approval]         | Dubai                                                    ₹14.2 Cr   |
|                    |  Core 4*  wk 10-13  [Allot 900] [Hard 300] 8%  buy by 28 Sep  rel 7 Dec |
|                    |   "Forecast 1,480 (P90 2,050); free sale closes out in 64% ..."  [Lab]|
|                    |  Premium  wk 12     [Hard 120] 12% ...                                |
|                    | Bangkok ...                                                          |
+--------------------+----------------------------------------------------------------------+
```
Week ranges: merge consecutive weeks with the same contract mix and markup into one row (display only).

## Contract Lab `/lab`
```
+---------------------------------------------------------------------------------------------+
| Cell: [Dubai v] [Core 4* v] [Week of 28 Dec 2026 v]   plan: pl_xxx (Headroom's mix: H 300 A 900 m 8%) |
+---------------------------------------------+-----------------------------------------------+
| DEMAND FAN for the cell (P5-P95 band,       | PAYOFF 860x380                                |
| P25-P75 band, P50 line) over weeks 8-16,    |  x units secured 0..q95                       |
| this week highlighted                       |  curves: all hard (violet), all allot (mint), |
|                                             |  Headroom split (lime) with P10-P90 bands     |
+---------------------------------------------+  vertical marker = slider position            |
| SLIDERS                                     +-----------------------------------------------+
|  Hard units   [----o------]  300            | P(SOLD OUT) vs units 860x200                  |
|  Allot units  [--------o--]  900            |                                               |
|  Markup  (4% | 8% | 12%)                    +-----------------------------------------------+
| READOUTS (mono, live)                       | ASSUMPTIONS (editable, each with "assumption")|
|  E[profit] ₹1.42 Cr  P10 ₹0.98 Cr           |  Hard rate 78% · Allot rate 90% · Fee 2%      |
|  P(sold out) 6%  Committed ₹2.2 Cr          |  Release 21 d · Utilisation 70% · Salvage 25% |
|  At risk ₹0.31 Cr                           |  Late cancel 7.8% (real, Hotel Booking Demand)|
|  [Snap to Headroom's mix]                   |  [Reset]                                      |
+---------------------------------------------+-----------------------------------------------+
```
Slider changes evaluate client-side with `lab-eval.ts` on the 256 returned samples; assumption edits re-fetch the curves.

## Suppliers `/suppliers`
```
+------------------------------------------------------+--------------------------------------+
| SUPPLIER ROWS                                        | MINI MAP (same projection as Theatre)|
| name / description         cost   live  cells value  | covered destinations glow lime when  |
| Sahara Beds (GCC bed bank) ₹1.2Cr wk4   78  +₹2.4Cr [on]| the row is hovered or on            |
| Andaman DMC                ₹0.9Cr wk5   52  +₹1.9Cr [on]|                                     |
| Bosporus Consolidator      ₹1.5Cr wk8  117  -₹0.3Cr [off]|                                    |
| ... (6 rows; value bar right-aligned, negative grey)  +--------------------------------------+
| Toggle = force include/exclude, re-solves the plan    | DELTA: peak sold-out 6.8% -> 4.9%    |
|                                                       | E[profit] +₹3.1 Cr, capital +₹2.1 Cr |
+------------------------------------------------------+--------------------------------------+
```

## Demand Lens `/demand`
```
+---------------------------------------------------------------------------------------------+
| [Dubai v] [Premium 5* v]  [W25 | W26]                         backtest: LightGBM WQL 0.11, 81% |
+---------------------------------------------------------------------------------------------+
| MAIN CHART 1400x420: weeks on x (W25 then W26). Bookings line (text-2), unconstrained demand   |
| line (text-1), gap shaded --danger at 25% "Searches that found sold out". W26: forecast fan.   |
| Event markers as thin vertical lines with labels (Diwali, Christmas, New Year, DSF).           |
+------------------------------------------------+----------------------------------------------+
| SIGNALS                                        | PROVENANCE                                   |
|  Google Trends India "Dubai" (5 y, weekly)     |  Inside Airbnb calendars (6 cities)  real    |
|  Inside Airbnb forward pressure (or the        |  Hotel Booking Demand (2019)         real    |
|   "No public forward data" note)               |  Google Trends India                 real    |
|  Indian holidays in window                     |  Holidays + events calendar          real    |
|                                                |  EaseMyTrip fares (curve only)       derived |
|                                                |  Volumes, rates, contract terms      assumption |
|                                    [Play the season ->]                                       |
+------------------------------------------------+----------------------------------------------+
```

## Approvals `/approvals`
```
+---------------------------------------------------------------------------------------------+
| Role: (Contracting manager | Finance approver)     filters: state, destination, contract  [Export CSV] |
+---------------------------------------------------------------------------------------------+
| ORDERS TABLE: order id · cell · hard · allot · markup · committed ₹ · state chip · actions     |
| rows grouped by plan; totals row at bottom; actions shown only for the current role            |
+---------------------------------------------------------------------------------------------+
| AUDIT DRAWER (toggle): time · role · action · from -> to · comment                             |
+---------------------------------------------------------------------------------------------+
```

## Proof `/proof`
```
+---------------------------------------------------------------------------------------------+
| "500 simulated seasons, ₹40 Cr, same budget for every desk"            [Simulated]           |
+------------------------------------------------+----------------------------------------------+
| PEAK SOLD-OUT RATE strip plot: 3 rows (desks), | PROFIT strip plot: 3 rows, 500 dots each,    |
| 500 jittered dots each, median tick            | median tick, CVaR5 marker                    |
+------------------------------------------------+----------------------------------------------+
| WIN RATES table: Headroom vs playbook / vs profit-only, on sold-outs and on profit              |
| FORECAST BACKTEST table: model x pool kind, WQL, coverage                                      |
| EXACT CHECK badge: "Decomposition within 1.3% of exact MILP (4 pools x 4 weeks)"              |
| TIMINGS: plan p50/p95, re-plan p50/p95                                                         |
+---------------------------------------------------------------------------------------------+
```
