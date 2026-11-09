# CONTEXT: Headroom

Shared vocabulary for everyone building Headroom. Use these words exactly in code, UI copy and docs. If a new concept appears, add it here first.

## Protected (copied verbatim from brief.md; never cut without the owner's approval)

- **usp:** Headroom is the only inventory planner that optimises availability (sold-out agent searches) as a first-class target by choosing the contract type per pool-week (hard pre-buy, allotment with release cut-off, or free sale), the supplier to integrate and the markup, under a budget and a risk limit, and re-plans every week as the season unfolds, grounded in real public demand signals.
- **hero_moment:** At 0:20 of the demo the Season Theatre plays the 2026-27 winter season week by week. Three desks run the same budget on the same hidden season: Last year's playbook, a profit-only optimiser, and Headroom. At week 9 a shock card drops; Headroom re-plans in under a second and shows the diff; the ledger ends with sold-out searches, profit and peak capital for each desk.
- **showpiece:** Contract-aware, availability-constrained, risk-adjusted procurement over 1,170 pool-weeks and 128-256 correlated demand scenarios, solved by Lagrangian decomposition, with weekly re-planning that stays ahead of a 1.5 s/week playback.

## Scope cut line

In: the seven demo screens (Season Theatre, Plan Studio, Contract Lab, Supplier lever, Demand Lens, Approvals, Proof), the data pipeline, the forecast, the optimiser, the simulator, baselines, Beat the Desk.
Out: real TBO integration, user accounts and SSO, multi-tenant, mobile layout, LLM in the decision path, live external APIs at demo time, cruise/transfers/sightseeing inventory.

## Domain terms

| Term | Meaning | Code name |
|---|---|---|
| Destination | One of 10 cities: Dubai, Bangkok, Singapore, Bali, Kuala Lumpur, Maldives, Istanbul, London, Paris, Hong Kong | `destination`, id like `DXB` |
| Hub | Indian origin airport for flight routes: DEL, BOM, BLR | `hub` |
| Pool | A unit of inventory we plan for. Hotel pool = destination x tier (value 3-star, core 4-star, premium 5-star). Flight pool = route hub to destination (economy). 30 hotel pools + 15 flight routes = 45 pools | `pool`, id like `H-DXB-4` or `F-DEL-DXB` |
| Week | Planning bucket, Monday-start ISO week inside a season | `week` (int 0..25 inside a season) |
| Season | A 26-week planning window. Planning season: `W26` (5 Oct 2026 to 4 Apr 2027). Backtest season: `W25` (6 Oct 2025 to 5 Apr 2026) | `season_id` |
| Cell | One pool-week. The optimiser decides per cell. 45 x 26 = 1,170 cells | `cell` |
| Unit | Room-night (hotels) or seat (flights) | `units` |
| Contract | How inventory is secured. Exactly three types below | `contract_type` |
| Hard pre-buy (`hard`) | Units bought upfront at the cheapest net rate. Paid at signing. Unsold units are dumped at a salvage rate. For flights this is a series block | `hard` |
| Allotment (`allot`) | Units held by the hotel for TBO at a mid net rate. Paid only when sold, plus a small holding fee. Unsold units return to the hotel at the release cut-off. A utilisation clause charges a penalty if less than the agreed share is used. Hotels only | `allot` |
| Free sale (`free`) | Units bought from suppliers' dynamic availability at booking time. Most expensive net rate. Availability can close out on peak dates | `free` |
| Release cut-off | Days before the stay week after which unsold allotment returns to the hotel. Default 21 days | `release_days` |
| Utilisation clause | Minimum share of allotment that must be used. Default 70% | `util_min` |
| Close-out | A supplier stops selling free-sale units for a date (stop-sell) | `closeout` |
| Search | A de-duplicated agent search session for a pool-week (not raw API calls) | `searches` |
| Sold-out search | A search where no supplier and no secured inventory had a bookable unit | `soldout_searches` |
| Look-to-book | searches / bookings for a cell | `l2b` |
| Unconstrained demand | Bookings plus the bookings lost to sold-out searches (sold-out searches x conversion rate). The thing we forecast | `demand_unc` |
| Availability | Share of unconstrained demand that found a bookable unit. Headline metric is its complement, the sold-out search rate | `availability`, `soldout_rate` |
| Peak cell | A cell flagged peak by the event calendar (Diwali, Christmas-New Year, long weekends, destination events) | `is_peak` |
| Markup level | TBO's markup over net rate: 4%, 8% or 12% | `markup` |
| Scenario | One sampled demand path for all cells (correlated) | `scenario`, axis `S` |
| Truth path | The hidden actual season used by the simulator. Never visible to the optimiser | `truth` |
| Value table | Per cell, expected profit / served units / capital for every option on the grid | `value_table` |
| Capital price | Shadow price of the budget (₹ of objective per ₹ of capital) found by bisection | `capital_price` (lambda) |
| Availability weight | Multiplier on served units, raised until the availability target is met | `avail_weight` (mu) |
| Risk appetite | cautious, balanced, bold. Maps to the downside penalty weight beta | `risk` |
| CVaR 5% | Average profit of the worst 5% of scenarios | `cvar5` |
| Plan | One optimiser result: buy lines + metrics | `plan` |
| Buy line | One cell's decision: hard units, allotment units, markup, buy-by date, release date, reason | `buy_line` |
| Buy order | A buy line sent for human approval | `order` |
| Supplier lever | Decision to integrate a new supplier (one-time cost, live after N weeks, adds free-sale capacity in some cells) | `supplier`, `integrate` |
| Desk | A buying policy in the simulator: `playbook`, `profit_only`, `headroom`, `you` | `desk` |
| Shock | A scripted change to the truth path revealed at a given week | `shock` |
| Re-plan | Headroom's weekly re-optimisation of remaining cells given what has happened | `replan` |
| Calibrated synthetic | Our generated TBO-shaped data whose parameters come from real public datasets | label shown in UI: "Simulated, calibrated on public data" |
