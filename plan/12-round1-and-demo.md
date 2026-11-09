# 12 Round 1 submission, demo script, Q&A

## Round 1 format (from past editions; re-check at the 14 Nov webinar)
Zip with: a deck of **2 content slides** (cover and thank-you slides do not count) covering Potential Impact, Implementation and Technical Feasibility, Innovation, Adoption Risk/Feasibility; plus a recorded video explaining the idea. Deadline 20 Nov 2026; submit 19 Nov.

Rules for both slides: one big number, one picture, one mechanism. 16:9, `--ink-0` background, Plex fonts, product screenshots rather than illustrations. Every simulated number labelled "simulated". No paragraph longer than two lines.

### Cover slide (does not count)
"Headroom: never sold out when agents are searching." Team name, PS: Inventory Optimization. Background: Theatre screenshot (or A08 image).

### Slide 1: Problem, impact, innovation
- Title: "Bookings hide the demand TBO could not serve."
- Left half: Demand Lens screenshot, Dubai premium New Year: bookings line flat at capacity, true demand line above it, the gap shaded red "searches that found sold out".
- Right half, three blocks:
  1. Impact: "Hotels are 87% of TBO's gross profit (Q2 FY26). Every sold-out search on a peak date is a lost booking for an agent and for TBO." + simulated headline from the proof run, e.g. "Same budget: 6x fewer sold-out searches on peak dates (simulated, 500 seasons)."
  2. Innovation, the three levers the PS names, done properly: "Contract per week (hard pre-buy, allotment with release date, free sale) · supplier to integrate · markup", "Availability is a target, not a by-product", "Re-plans every week as the season unfolds".
  3. "Not a forecast dashboard: a buying desk that races last year's playbook and a profit-only optimiser on the same season."

### Slide 2: How it works, feasibility, adoption risk
- Title: "Turn the budget into a price, then solve 1,170 buying decisions exactly."
- Top: the architecture strip (A09 simplified): real signals (Inside Airbnb forward availability, Hotel Booking Demand cancellations, Google Trends India, holidays and events, fare curves) -> un-censored demand -> Chronos-2 quantile forecast -> 128 correlated scenarios -> decomposition optimiser (capital price, availability weight, risk) -> plan + weekly re-plan -> approval queue.
- Middle: Theatre screenshot at the shock moment with the diff card visible.
- Bottom, two columns:
  - Feasibility: "Working prototype today: plans in ~1.5 s, re-plans in < 0.6 s; exact-solver check within 2%; spike showed a joint MILP does not solve at this size, so we built the decomposition." (Use measured numbers only.)
  - Adoption risk: "Allotments and supplier integration need little capital, so pre-buy only where the sold-out loss beats the capital price, shown in ₹. Human approval for every order, CSV export, audit trail. Runs in shadow mode first on TBO's own bookings via a CSV seam."

### Video (target 2:30-3:00; record at 1920x1080 from cached runs)
1. 0:00-0:15 Hook over the Demand Lens: "Last New Year, how many agent searches for Dubai found nothing to book? Bookings will never tell you, because you cannot book a sold-out room."
2. 0:15-1:15 The Theatre hero: play, narrate the three desks, the shock, the diff card, the result line.
3. 1:15-1:45 Plan Studio: budget slider, infeasible banner "Needs ₹X Cr more", one buy line reason with contract chips.
4. 1:45-2:15 How it works (slide 2 diagram on screen): real signals, forecast, scenarios, decomposition, weekly re-plan; one line on the spike result.
5. 2:15-2:45 Adoption: approvals, shadow mode, CSV seam; close: "Headroom: buy the right inventory, on the right contract, at the right time, and never be sold out when agents are searching."
Record everything from the running product, at 1920x1080, using cached runs so the numbers match the live app.

## Finale demo script (4:30)
Follows 00-overview.md demo journey. Presenter A drives, presenter B narrates and takes the judge to Beat the Desk. Keep a backup MP4 of the hero ready in a second tab.

## Q&A preparation (write short, numeric answers; update with measured numbers)
1. "TBO is asset-light and pays hotels after check-in. Why tie up cash?" Headroom mostly recommends allotments (no upfront payment, release by cut-off) and supplier integration; it buys hard only where the expected sold-out loss is larger than the capital price, which it shows in ₹ per ₹. Show the capital-committed vs capital-at-risk split.
2. "Your data is synthetic." Calibrated on five real public datasets with a pass/fail calibration report; every on-screen number labelled simulated; the CSV seam takes TBO's bookings and searches; rollout starts in shadow mode comparing Headroom's plan against what contracting actually did.
3. "How do you know demand when hotels were sold out?" We add back sold-out searches times the conversion rate observed in non-sold-out weeks (un-censoring); tested to recover true demand within 10% on 90% of cells.
4. "Why not a MILP solver?" Spike numbers: 1.2 M variables, no solution in 60 s with HiGHS even relaxed; the decomposition is exact per cell and within 2% of the MILP on a small instance in our tests.
5. "What if the forecast is wrong?" The plan uses 128 correlated scenarios, not a point forecast; risk appetite trades profit for downside; weekly re-plan corrects with observed demand; the shock demo shows it.
6. "Why should availability be a target instead of just maximising profit?" Agents remember sold-out results and move volume to competitors; the profit-only desk in the race shows the trade-off; the frontier shows how much profit each pp of availability costs.
7. "How would this plug into TBO?" Inputs: bookings, searches (deduplicated), sold-out flags, contract terms, supplier capacity. Outputs: buy orders to contracting with approval. Weekly batch, not real-time.
8. "What about cancellations?" Late-cancellation rates from real hotel booking data reduce the value of hard rooms; allotment cancellations return to the hotel.
9. "Elasticity and contract terms are assumptions." Yes, editable in the Contract Lab and listed as assumptions; the sensitivity view (if built) shows which ones matter.
10. "Which AI did you use?" Chronos-2 for forecasting; no LLM in decisions; Claude Code as a coding assistant (say so in README).
