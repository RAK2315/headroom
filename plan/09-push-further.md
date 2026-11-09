# 09 Push further

Build the best version of every feature. The numbers in this plan are floors, not ceilings. When a feature works, come here and make it more impressive, faster or clearer. Each list is in priority order: take from the top whenever a phase finishes early.

## How to build
- Build the ambitious version first. Pick the approach that looks best in the demo and is true.
- Use every tool to its full capability: deck.gl GPU layers and transitions, motion springs, vectorised numpy, Chronos-2 covariates, DuckDB for instant queries.
- Make the product feel alive: every control responds within a frame or two, every number counts up, every change animates into place.
- Real measured results with provenance are part of the wow. Show them proudly, labelled "Simulated, calibrated on public data".
- New feature ideas that come up while building: add them here or to 03-features.md with an F number, then build them.

## Engine
1. Hull allocation for every solve (11-engine-spec.md section 5): keep each cell's upper concave hull of options, binary search on the hull slope. Aim for a full plan under 1 s and a weekly re-plan under 0.3 s, so sliders feel instant.
2. Warm-start the bisection from the previous capital price and availability weight on every re-plan.
3. S=256 scenarios for the initial plan, 128 in-season.
4. Wider exact check: 6 pools x 6 weeks against HiGHS, shown on the Proof page.
5. Marginal value per destination: "next ₹1 Cr here buys -0.6 pp sold-outs" for each destination, not just the total.
6. Lever ablation: run the plan with contracts only, plus suppliers, plus pricing, plus weekly re-planning, and show what each lever adds. Strong judge piece for the Proof page.

## Season Theatre (hero)
1. 60 fps with 4,000 sparks, then push to 8,000 if the frame budget allows.
2. Shock ripple: when the shock lands, a pressure wave spreads from the affected destination across the map before the card drops.
3. Diff card that animates each changed buy line into place (FLIP animation), with the ₹ delta counting up.
4. Speed control 0.5x to 4x and scrub back through played weeks.
5. Desk focus: click a desk column and the map shows only that desk's sold-out sparks, so the contrast between desks becomes visible on the map itself.
6. "Replay the shock" button at the end jumps back to week 8.
7. End card: the three desks plotted as dots on the budget vs sold-out plane, with Headroom's frontier behind them.
8. Keyboard shortcuts for presenting: space play/pause, right arrow step, R reset, F desk focus.

## Plan Studio
1. Drag the marker along the frontier to set the budget.
2. Buy lines that change after a re-solve flash lime and slide into their new position.
3. Compare mode: pin a plan, change controls, and see the diff in buy lines and metrics side by side.
4. Hover any summary number to see how it was computed, with the actual values.

## Contract Lab
1. Payoff surface: a heatmap of expected profit over hard units x allotment units, Headroom's choice as a dot, the slider position as a crosshair.
2. Scenario strip: the 256 demand samples as thin sorted bars, each coloured by how it was served (hard, allotment, free sale, lost).
3. Assumption edits recompute client-side through `lab-eval.ts` wherever the change does not need new scenarios.

## Demand Lens
1. Un-censoring toggle: the gap between bookings and true demand fills in with animated search sparks.
2. Forecast model toggle (Chronos-2, LightGBM, seasonal naive) with live backtest scores.
3. Lag view: how many weeks Google Trends leads bookings, per destination.

## Suppliers
1. Coverage arcs on the mini map for the hovered supplier.
2. Value waterfall: each supplier's contribution to sold-outs and profit, stacked.

## Proof
1. Strip plots animate in as the 500 seasons drop in as dots.
2. Small multiples: win rate per destination.
3. Lever ablation chart (engine item 6).
4. Calibration report rendered as a section of the page, each check with its measured value.

## Beat the Desk
1. Leaderboard of everyone who played (judges at the finale), stored in DuckDB.
2. After the run, show the judge's plan next to Headroom's on the same lanes so they see exactly where they lost searches.

## Data
1. All 6 Inside Airbnb cities, and more than one snapshot per city for a forward-pressure time series.
2. BYO-data CSV upload (F27): a judge can drop in a bookings CSV and see a plan for it.
3. More destinations (Goa, Phuket, Bali villas) if the pipeline is fast.

## Presentation
1. Presenter mode: hides the nav, enlarges type and numbers for the projector.
2. Light theme (F30) tuned for bright rooms.
3. Sensitivity tornado (F29): which assumption moves the result most.
4. Ask Headroom (F26): plain-language questions answered from the engine's numbers.
5. Demo kit: docker compose runs everything offline from the laptop, cached runs load instantly, and a recording of the hero sits ready in a second tab.
6. Loading states that match the final layout, empty states with a clear next action.

## Turn judge questions into screens
Every hard question gets a visual answer on screen, not just a spoken one (spoken answers are in 12-round1-and-demo.md):
- "The data is synthetic": provenance panel plus the calibration section on Proof.
- "TBO is asset-light": capital committed vs capital at risk split in Plan Studio and the ledger.
- "Why not a MILP": the exact check badge on Proof.
- "What if the forecast is wrong": the shock in the Theatre and the weekly re-plan.
- "Your assumptions are guesses": editable assumptions in the Contract Lab and the sensitivity tornado.
