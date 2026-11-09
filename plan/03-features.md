# 03 Features

Tags: [MVP] the demo journey or hero breaks without it. [V2] build when MVP lands early. [STRETCH] impressive extras, never blocking.
Protected marks: (HERO) serves the hero moment, (USP) is a USP amplifier. Protected features are never cut without the owner's approval.
Order inside each tag = build dependency order. Feature ids are used in commits and in 08-build-plan.md.

---

## [MVP]

### F01 Reference data (USP)
- What: destinations, hubs, pools, routes, tiers, weeks of seasons W24, W25, W26, contract parameters, candidate suppliers, shocks, event calendar. Loaded from `data/reference/*.yaml` into DuckDB.
- Acceptance: `uv run headroom-pipeline reference` creates tables `destination`, `pool`, `season`, `week`, `contract_param`, `supplier`, `shock`, `event` with the exact rows in 05-data-model.md seed section; `pytest pipeline/tests/test_reference.py` passes (45 pools, 30 hotel + 15 flight, 26 weeks per season, every event has a source URL or `assumption: true`).
- Depends on: nothing.

### F02 Real signal ingestion (USP)
- What: load the five public sources into tidy Parquet: (1) Inside Airbnb `calendar.csv.gz` for Bangkok, Singapore, Istanbul, London, Paris, Hong Kong -> nightly share unavailable per city; (2) Hotel Booking Demand (Antonio et al. 2019) -> lead-time distribution and cancellation probability by lead-time bucket and deposit type; (3) Google Trends weekly interest, geo India, 5 years, one CSV per destination (manual export, committed); (4) Indian holidays via `holidays` + curated event YAML; (5) EaseMyTrip flight fares (Kaggle) -> price multiplier by days-left. Details and URLs in 10-data-pipeline.md.
- Acceptance: `uv run headroom-pipeline signals` writes `data/signals/*.parquet`; each file has the schema in 10-data-pipeline.md; a `provenance` table lists every source with URL, licence, date fetched, what it calibrates; `test_signals.py` asserts row counts > 0 and no NaN in key columns.
- Depends on: F01.
- Gotcha: Kaggle needs login to download; download once by hand into `data/raw/` (git-ignored if licence forbids redistribution; then commit only the derived curve). Inside Airbnb files are large (100-400 MB each, compressed); keep raw files git-ignored and commit only derived parquet.

### F03 Calibrated synthetic world generator (USP)
- What: generate daily history for seasons W24 and W25 and a hidden truth for W26, per pool: searches, bookings, sold-out searches, cancellations, free-sale availability per supplier, net rates by contract type, close-outs. Seasonality from Trends, peaks from events and Airbnb pressure, lead times and cancellations from Hotel Booking Demand, fares from the EaseMyTrip curve. Seeded and deterministic.
- Acceptance: `uv run headroom-pipeline world --seed 42` writes `history_daily` and `truth_daily` (500 truth seeds stored as compact arrays plus the "realistic" seed 42 in full); the calibration report `data/reports/calibration.md` shows for each calibrated parameter: source value vs generated value (e.g. cancellation rate by lead bucket within 2 pp of source); `test_world.py` checks determinism (same seed, same hash) and that sold-out searches > 0 on peak cells and about 0 on off-peak cells.
- Depends on: F01, F02.

### F04 Unconstrained demand (un-censoring)
- What: weekly `demand_unc = bookings + soldout_searches x conv_rate`, where `conv_rate` per pool = bookings / searches on non-sold-out weeks (median of last 8 such weeks). Weekly aggregation of history.
- Acceptance: `weekly_demand` table exists for W24, W25; on cells with zero sold-outs, `demand_unc == bookings`; unit test with a hand-made example.
- Depends on: F03.

### F05 Forecast (USP)
- What: weekly quantile forecasts (q 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95) of `demand_unc` for all 45 pools for the 26 weeks of the target season, with covariates: `is_holiday_in`, `event_intensity`, `airbnb_pressure` (real for 6 cities, 0 elsewhere with a flag), `trends_index`. Models: Chronos-2 (primary), LightGBM quantile, seasonal naive. Backtest: train through W24, forecast W25, score weighted quantile loss (WQL) and P10-P90 coverage; pick the best model per pool group (hotel/flight) by WQL; production forecast for W26 uses data through W25.
- Acceptance: `uv run headroom-pipeline forecast` writes `forecast_quantile` and `backtest_metric` tables; `data/reports/backtest.md` lists WQL and coverage per model; coverage of the chosen model is between 0.72 and 0.88; run time under 10 minutes on CPU.
- Depends on: F04.

### F06 Scenario generator
- What: S correlated demand scenarios for all 1,170 cells from the quantiles: per cell, interpolate the inverse CDF from the 7 quantiles (linear between quantiles, log-linear tails); correlation by a Gaussian copula with three factors (global, destination, week-cluster) estimated from backtest residuals (default loadings 0.35 / 0.5 / 0.2 if estimation is unstable). Also free-sale capacity scenarios (share of demand available, falling with pressure) and free-sale net rate scenarios.
- Acceptance: `engine.scenarios.generate(season, S, seed)` returns arrays `D[S,C]`, `Fcap[S,C]`, `c_free[S,C]`; mean of D within 3% of P50-mean; empirical quantiles within 5% of forecast quantiles for S=1024; same seed, same arrays (test).
- Depends on: F05.

### F07 Decomposition optimiser (HERO, USP)
- What: the engine in 11-engine-spec.md: value tables over (markup x hard x allotment) per cell, capital price and availability weight by bisection, risk weight from risk appetite, supplier lever greedy loop, portfolio metrics, reasons. Contract rules: hotels can use hard, allot, free; flights hard (series block) and free only.
- Acceptance:
  - `engine.optimise(PlanParams)` returns `PlanResult` (04-architecture.md contract) in at most 2.5 s for S=128 on the demo laptop (`test_perf.py`, marked slow).
  - Budget respected: capital committed at most budget, and within 1% of it when the capital price > 0.
  - When the target is reachable the plan's expected availability is at least the target minus 0.3 pp; when not, `availability_achievable` and `budget_needed_for_target` are filled.
  - Exact gap: on the tiny instance (4 pools x 4 weeks x 32 scenarios, no suppliers) the decomposition objective is within 2% of HiGHS MILP (`test_exact_gap.py`).
  - Monotonicity tests: more budget never lowers availability; higher target never lowers capital used; "cautious" never has a worse CVaR 5% than "bold".
- Depends on: F06.

### F08 Plan API
- What: `POST /api/plans`, `GET /api/plans/{id}`, `POST /api/plans/frontier`, `GET /api/meta`, `GET /api/health`.
- Acceptance: contracts exactly as 04-architecture.md; `pytest api/tests/test_plans.py` hits each endpoint with TestClient; invalid input returns 422 with a message; plans persisted in DuckDB and survive restart.
- Depends on: F07.

### F09 Baseline desks (HERO, USP)
- What: `playbook` (hard pre-buy = last season's served units x 1.10 on peak cells, signed at season start; markup 8%; free-sale top-up when margin positive), `profit_only` (hard-only newsvendor per cell maximising E[profit] - 0.5*SD under the same budget by its own capital-price bisection; markup 8%; no availability term, no allotment, no suppliers, no re-plan).
- Acceptance: both produce `PlanResult` under the same budget; `test_baselines.py` checks budget respected and that profit_only uses no allotment.
- Depends on: F07 (shares recourse code).

### F10 Season simulator + weekly re-plan (HERO)
- What: plays a season week by week for 3 or 4 desks on one truth path: at each week, realise demand from truth, serve with each desk's commitments (recourse rules), record outcomes, apply shocks revealed this week (truth already contains their effect; the reveal updates what Headroom knows), update Headroom's scenarios for remaining weeks (Bayesian scaling, 11-engine-spec.md section 6), re-plan remaining cells (increments only), auto-release allotment past cut-off. Baselines do not re-plan (playbook) or re-plan nothing (profit_only).
- Acceptance: `engine.simulate(SimParams)` yields 26 `WeekState` objects per desk; deterministic for the same inputs; per-week Headroom re-plan p95 at most 0.6 s at S=64 (`test_perf.py`); total sold-out searches and profit reconcile with the per-week sums (test).
- Depends on: F07, F09.

### F11 Season stream API + cached runs (HERO)
- What: `POST /api/sims` creates a run; `GET /api/sims/{id}/stream` streams `week` events (SSE) as the simulator produces them; `POST /api/sims/{id}/shock` (only in play mode) and `POST /api/sims/{id}/act` (Beat the Desk). Demo runs (realistic truth seed 42, scripted shock list) are precomputed by `uv run headroom-pipeline cache-demo` into `web/public/cached/*.json` so the frontend can play them with no backend.
- Acceptance: stream emits weeks in order, at most 1 event per desk per week, with `event: done` at the end; a run with the same params returns the cached result instantly; the frontend plays a cached run with the backend stopped and shows the "Cached run" badge.
- Depends on: F10.

### F12 App shell, tokens, routing (HERO)
- What: Vite React app with the layout shell, header (season, budget, target, simulated badge, role switcher), left nav (7 screens), tokens from 06-design-system.md, fonts, error boundary, toasts, empty/loading/error components.
- Acceptance: all 7 routes render a titled placeholder; tokens applied; no framework default styles visible; Playwright smoke test navigates all routes with a clean console.
- Depends on: nothing (can start on day 1 in parallel with F01-F03).

### F13 Pressure map (HERO)
- What: deck.gl map in the Theatre: land outline (world-atlas `land-50m`), equirectangular view framed lon -12 to 128, lat -12 to 58; hubs; 10 destination gauges (3 tier arcs + free-sale disc); flight arcs (ArcLayer) + animated trips (TripsLayer); sold-out sparks (ScatterplotLayer, particle system in a typed array updated per frame); pressure haze (HeatmapLayer). Picking: hover a gauge -> tooltip with the three desks' numbers for that destination this week.
- Acceptance: 60 fps at 4,000 particles on the builder's laptop (Chrome performance panel, 10 s recording, no frame over 20 ms more than 5% of frames); visual matches 06-design-system.md correct render; works offline.
- Depends on: F12. Uses mock week states until F11 lands (mock generator in `web/src/mocks/`).

### F14 Ledger + lanes + playback controls (HERO)
- What: ledger panel with 3-4 desk columns (metrics: sold-out search rate on peak cells, all-cell sold-out rate, realised profit, capital committed, capital at risk, units wasted) with count-up, per-desk sparklines; season lanes (10 x 26 cells; past = realised pressure colour, future = forecast pressure hatched with opacity = uncertainty); playhead; play/pause/step/speed; shock card drop; diff card; end-of-season result line; click a lane cell -> popover with the three desks' outcomes for that destination-week.
- Acceptance: plays a cached run end to end in 39 s at 1x with no dropped weeks; shock card pauses 2 s; diff card text equals the API diff; result line numbers equal ledger numbers.
- Depends on: F12, F11 (or cached JSON).

### F15 Plan Studio (USP)
- What: controls (budget ₹5-150 Cr slider with typed input, availability target 85-99%, risk appetite 3-way, lever toggles contracts/suppliers/pricing), summary strip (sold-out rate peak and all, expected profit, P10, CVaR 5%, capital committed, capital at risk, capital price sentence, solve ms), frontier chart (x: budget ₹ Cr 5-150 at 12 precomputed points + current; y-left: peak sold-out rate; y-right: expected profit; hover shows point), buy list (grouped by destination, rows per pool with week ranges merged, contract chips with units, markup, buy-by date, release date, reason sentence, "Open in Contract Lab" link), infeasibility banner ("Best achievable 91.8%. Needs ₹6.1 Cr more."), "Play this plan in the Theatre" and "Submit for approval" buttons.
- Acceptance: changing any control re-solves (debounced 400 ms) and shows results within 3 s; the banner appears exactly when `availability_achievable < target`; the frontier renders 12 points; buy list total capital equals the summary.
- Depends on: F08, F12.

### F16 Contract Lab (USP)
- What: pick pool and week (defaults Dubai core 4-star, week of 28 Dec 2026). Shows demand fan (P5-P95) for the cell, then a payoff panel: x = units secured, three curves for "all hard", "all allotment", "hard + allotment at Headroom's split", y = expected profit with P10-P90 band; a second small chart: P(sold out) vs units. Sliders for hard units and allotment units; live readouts: expected profit, P10, sold-out probability, capital committed, capital at risk. Button "Snap to Headroom's mix". Editable contract parameters (net rate %, release days, utilisation %, salvage %) with "assumption" tags and a reset.
- Acceptance: `GET /api/contract-lab` returns curves for the cell in under 300 ms; sliders update readouts at 30 fps from a client-side evaluation of the returned scenario sample (S=256 demand values sent to the client); snapping sets sliders to the plan's values.
- Depends on: F07, F12.

### F17 Demand Lens (USP)
- What: destination and tier picker; main chart for W25 and W26: bookings (line), unconstrained demand (line), shaded gap labelled "Searches that found sold out", forecast fan for W26 with the chosen model, event markers; side panel of signals: Trends index line, Airbnb forward pressure (real, 6 cities, with "Inside Airbnb, snapshot 2026-09" tag), holidays; Provenance panel listing the five sources (name, URL, licence, what it calibrates, date fetched); backtest badge (WQL, coverage). "Play the season" button to the Theatre.
- Acceptance: loads in under 1 s from DuckDB; for a city without Airbnb data the pressure panel shows "No public forward data for this city; using events and Trends" (not an empty chart).
- Depends on: F05, F08, F12.

### F18 Approvals and export (USP: adoption)
- What: "Submit for approval" turns a plan's buy lines into orders with state machine (05-data-model.md); role switcher: Contracting manager can submit/withdraw; Finance approver can approve/reject with a comment; approved orders can be "sent to supplier" (simulated) and then "confirmed" or "declined by supplier". Orders table with filters (state, destination, contract), totals, CSV export (all rows, no cap), audit log (who, what, when, from-to state).
- Acceptance: illegal transitions return 409; CSV contains every order with all columns; audit shows every transition; state survives restart.
- Depends on: F08, F12.

### F19 Proof page (USP)
- What: results of `uv run headroom-pipeline proof`: 500 truth seeds x 3 desks at ₹40 Cr: distribution strips of peak sold-out rate and profit per desk, win-rate table (Headroom vs each baseline on sold-outs and profit), forecast backtest table, exact-gap badge, engine timings (p50/p95), calibration report link.
- Acceptance: page renders from `GET /api/proof` (precomputed JSON); numbers match `data/reports/proof.md`.
- Depends on: F10, F05.

### F20 README and run scripts
- What: README with problem, demo GIF, how to run (uv + npm, or docker compose), demo script, feature checklist mapped to PS objectives, data provenance and licences, assumptions list, architecture diagram, AI tools used.
- Acceptance: a fresh clone runs with the documented commands on Windows and Linux (test in a clean folder).
- Depends on: all MVP.

---

## [V2]

### F21 Supplier lever screen (USP)
- What: list of 6 candidate suppliers (fictional names, see 05 seed) with integration cost, weeks to go live, cells covered; integration value bars (objective gain minus cost) from the current plan; toggle to force include/exclude; the map highlights covered destinations; summary delta (sold-out rate, profit).
- Acceptance: toggling re-solves and shows the delta; the plan's supplier decisions appear in Plan Studio.
- Depends on: F07 supplier loop (which is MVP inside the engine), F15.
- Note: if V2 time is short, the supplier lever still exists in the engine and in Plan Studio (MVP); only this dedicated screen is V2.

### F22 Beat the Desk (play mode) (HERO)
- What: "Play as me" in the Theatre replaces the playbook desk with "You". At each week the playhead pauses; the user can: top up allotment (pool, weeks at least 5 ahead, units), buy hard (weeks at least 3 ahead, worse rate), release allotment (before cut-off), change markup (weeks at least 2 ahead). "Next week" advances. Budget meter. Final scoreboard against Headroom and profit-only.
- Acceptance: actions validated server-side (409 with reason if illegal); a 2-week play takes under 60 s of presenter time; scoreboard correct.
- Depends on: F11, F14.

### F23 Shock picker
- What: in the Theatre, before Play, choose shocks from the library (6 scripted shocks) or none; each shows its effect description and "fictional scenario" label.
- Acceptance: each shock changes the truth path deterministically; the Headroom diff card appears on its reveal week.
- Depends on: F10.

### F24 Lane cell drill-down
- What: clicking a lane cell opens a side sheet: per desk, units secured by contract, demand realised, served, sold-out searches, profit for that destination-week.
- Depends on: F14.

### F25 Deployed demo
- What: web on Vercel, API on Render/Fly; env vars per 04-architecture.md; health check; cached mode serves recorded runs whenever the API is not reachable.
- Depends on: F11, F20.

---

## [STRETCH]

### F26 Ask Headroom
- What: a command bar (Ctrl+K): "What if Dubai demand drops 20% after January?" -> a small LLM maps the sentence to a structured shock or parameter change via a JSON schema; the UI shows the parsed change for confirmation; on confirm, re-plan. Model provider via env vars (OpenAI-compatible). Never edits numbers directly.
- Acceptance: 10 example sentences in tests map to the right structure (recorded responses, no live calls in CI).

### F27 Bring your own data
- What: upload a bookings/searches CSV in the documented schema; validation report; re-run forecast and plan on it.
- Acceptance: the sample CSV round-trips; bad files show row-level errors.

### F28 Weekly action digest
- What: "This week's actions" view and an email/WhatsApp-style message preview (no sending): what to sign, release, re-price this week, with deadlines.

### F29 Sensitivity tornado
- What: which assumption moves profit and sold-outs most (elasticity, salvage, release days, close-out rate), +/-20%.

### F30 Light theme for bright rooms and projectors
- What: a light token set toggled in the header, in case the venue projector washes out the dark theme.
