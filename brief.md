# Brief: Headroom

## Event
- Name / link: TBO VoyageHack 4.0, https://unstop.com/competitions/crp-voyagehack-40-tbocom-1774031
- Format: ps
- Track / PS id and title: "Automate Inventory Optimization" (Hackathon Challenge: Inventory Optimization for TBO.com). Verbatim text:

  > How can data-driven intelligence help TBO.com maximize availability by making smarter travel inventory procurement decisions?
  > Build an intelligent system that analyzes historical bookings, demand trends, sold outs, look to book, seasonality and external signals to identify inventory to target to maximize expected profit.
  > The solution should optimize budget allocation across hotels, flights, destinations, and travel periods, while accounting for demand fluctuations, pricing changes, cancellations, and unsold inventory risks.
  > Basis on this TBO is expected to plan pre buy, supplier integration and pricing to maximise bookable inventory.
  > Key Objectives
  > - Predict Demand: Forecast travel demand using booking trends, search data, and external market signals.
  > - Identify Opportunities: Discover high-potential inventory, destination, travel time and favorable procurement prices.
  > - Optimize Investments: Allocate a given budget to maximize expected returns.
  > - Maximize Profitability: Recommend optimal purchase timing, inventory quantities, and selling prices.
  > - Manage Risk: Minimize potential losses from uncertain demand and unsold inventory.
  > Expected Outcome
  > Develop a decision-support platform that transforms travel and market data into actionable inventory investment recommendations, helping TBO.com buy the right inventory, at the right time, within the right budget, to maximize risk-adjusted profits. System will be provided with maximum input budget.

- Judging criteria: Round 1 slides must cover Potential Impact, Implementation and Technical Feasibility, Innovation, Adoption Risk/Feasibility. No weights published. Round 2 judged on prototype quality and alignment with objectives (GitHub repo + docs + workflow video). Finale: live jury at TBO.
- Prize category targeted: overall (₹3L / ₹2L / ₹1L + PPI).
- Deadlines: registration 12 Nov 2026; mandatory briefing webinar 14 Nov 2026 17:30; idea submission 20 Nov 2026 (2 content slides + video, zipped); prototype round 26 Nov - 24 Dec 2026; finale 8 Jan 2027.
- Time budget: about 6 weeks total, generous. Round 1 is idea-only, so the deck must be very clear.
- Team: 2 full-stack generalists. Builder this week: teammate with Claude Code. Owner (user) reviews and joins later.
- Hard constraints: no TBO data is provided (assumption based on competitor README; re-check at the 14 Nov webinar). Use only public or synthetic data. Licences must allow commercial use for anything shipped.

## Problem
- User (named group): TBO's contracting and procurement team (who sign hotel allotments and flight series blocks) and the revenue/finance lead who owns the budget. Beneficiaries: TBO's B2B travel agents, who search TBO and lose bookings when results show sold out.
- Pain, concretely: on peak dates (Diwali, Christmas to New Year, long weekends, destination events) supplier free-sale inventory closes out, agents searching TBO find nothing bookable, and the booking goes to a competitor. Meanwhile prepaying for rooms that do not sell is a direct loss. Today the decision of what to lock in, under which contract, at what price, is made on last year's numbers and spreadsheets.
- Evidence:
  - Hotels are 64% of TBO TTV and 87% of gross profit in Q2 FY26; hotel take rate about 5.5% under competitive pressure (research-A, TBO shareholder letters).
  - A bed bank that prepays for rooms takes the full loss on rooms it cannot resell, which is why the industry moved to partial pre-buy and allotments (AltexSoft, Apr 2025, research-C).
  - Larger series-fare seat blocks earn bigger discounts but raise unsold risk; competitors track blocked vs sold seats in spreadsheets (TripJack job ad, research-C).
  - TBO collects from agents before paying suppliers and pays hotels at or after check-in, so capital tied up in pre-buy is a real cost to justify (research-A).
  - TBO's actual sold-out search rate: unknown. Every sold-out number in the demo is an estimate on calibrated synthetic data and is labelled so.

## Idea
Headroom tells TBO which hotel rooms and flight seats to lock in, under which kind of contract (hard pre-buy, allotment with a release date, or free sale), which new supplier to integrate, and at what markup, so that agents stop seeing "sold out" on peak dates within a fixed budget and a stated risk limit, and it re-plans every week as the season unfolds.

## Requirement fit
Every PS ask is load-bearing:
- "maximize availability": the headline metric is the sold-out search rate, with an availability target the planner must hit.
- "pre buy, supplier integration and pricing": the optimiser has exactly these three levers (contract mix, supplier integration, markup level).
- "historical bookings, demand trends, sold outs, look to book, seasonality and external signals": demand is un-censored with sold-out searches, forecast with known-future covariates (holidays, events, forward market pressure, search interest).
- "optimize budget allocation across hotels, flights, destinations, and travel periods": 45 pools (30 hotel pools, 15 flight routes) x 26 weeks under one budget.
- "cancellations, unsold inventory risks", "risk-adjusted profits": scenario-based profit distribution, CVaR, cancellations from real lead-time data.
- "System will be provided with maximum input budget": budget is the first input.
Removal test: remove the budget, demand forecast, contracts or risk model and nothing is left. Pass.

## USP
- Nearest real prior art:
  - Allotment Atlas (https://github.com/shanshantanusingh113-max/allotment-atlas), a VoyageHack 4.0 entry: quantile forecast, newsvendor sizing, budget knapsack on E[profit] - lambda*SD, Monte Carlo, 3D demand globe, plain-English commands, season replay.
  - IDeaS, Duetto, PredictHQ: single-hotel revenue management and demand intelligence, not distributor procurement (research-C).
- What we do that it does not:
  1. Optimises availability (sold-out searches) as a first-class target, not only profit.
  2. Chooses the contract type per pool-week: hard pre-buy vs allotment with release cut-off and utilisation clause vs free sale. This is how hotels actually sell inventory, and it directly answers TBO's cash concern.
  3. Has the supplier-integration lever the PS names.
  4. Re-plans every week as the season unfolds (release before cut-off, top up, re-price), shown live against two baseline desks on the same season.
  5. Grounded in five real public datasets with a provenance panel, and reports the shadow price of capital ("the next ₹1 Cr buys X pp fewer sold-outs").
- Why other teams on this PS will not have it: the obvious build is forecast-then-knapsack on units. Contract options, availability targets and in-season recourse need a decomposition approach (our spike showed the joint stochastic MILP does not solve in 60 s at demo size; the decomposition plans in about 1.4 s).

## Hero moment
At 0:20 of the demo the Season Theatre plays the 2026-27 winter season week by week (1.5 s per week). Three desks run the same budget on the same hidden season: Last year's playbook, a profit-only optimiser, and Headroom. Destinations on a dark pressure map fill with secured inventory; when demand overflows, red sold-out sparks spill. At week 9 a shock card drops ("UAE eases visa on arrival for Indians: Dubai demand +25%"). Headroom re-plans in under a second and shows the diff (top up Dubai allotment, release Singapore rooms before cut-off, raise Bali markup). The ledger ends: sold-out searches 31% vs 18% vs 5% (target numbers, to be replaced with measured ones), with profit and peak capital beside them.

## Showpiece
- The hardest real technical thing: contract-aware, availability-constrained, risk-adjusted procurement over 1,170 pool-weeks and 128-256 correlated demand scenarios, solved by Lagrangian decomposition (capital price, availability weight, risk weight found by bisection over per-cell value tables), with weekly re-planning that stays ahead of a 1.5 s/week playback.
- One-sentence plain explanation: "We turn the budget and the availability target into prices, which lets us solve over a thousand small buying decisions exactly and still re-plan the whole season in about a second."

## Demo journey (draft)
1. 0:00 One line: "Last Diwali, how many agent searches on TBO found Dubai sold out?" Demand Lens shows bookings vs true demand (sold-out searches added back).
2. 0:20 HERO: Season Theatre plays; three desks; shock at week 9; Headroom re-plans; ledger result.
3. 1:30 Plan Studio: budget ₹40 Cr, availability target 95%, risk Balanced. Buy list with contract chips and reasons; shadow price of capital; drag along the frontier.
4. 2:30 Contract Lab: one pool-week (Dubai 4-star, New Year week): why 120 allotment + 40 hard + free-sale top-up beats 160 hard.
5. 3:00 Supplier lever: integrating "Supplier Andaman" closes 62% of Bali/Thailand Christmas sold-outs (target number).
6. 3:30 Beat the Desk: a judge plays two weeks against Headroom.
7. 4:00 Approvals: send buy orders for approval, export CSV, audit trail. Close on proof page (500 simulated seasons, forecast backtest).

## Visual concept
- 2D, data-driven. Deliberately not a 3D globe (the strongest competitor already has one).
- Style direction: Windy.com (animated weather-radar fields and colour ramps: "availability weather"), Flightradar24 (dark live map with moving objects and arcs), Bloomberg Terminal (dense monospaced numerics, ledger columns).
- Assets: Natural Earth land outline (world-atlas), procedural particle "spill", code-built wordmark. No stock photos. Optional generated imagery for the Round 1 slide background only.

## Enabling tech (candidates only, architect decides)
- Probabilistic demand forecasting with known-future covariates: Chronos-2 (Apache-2.0), LightGBM quantile baseline, seasonal naive.
- Correlated scenario generation: Gaussian copula on forecast quantiles.
- Optimisation: numpy-vectorised value tables + bisection (decomposition); HiGHS (highspy) as exact check on small instances.
- Map and particles: deck.gl without a tile basemap; charts: D3.
- Streaming season playback: Server-Sent Events.

## Feasibility
- Riskiest bet: interactive solve and weekly re-plan speed at demo size. Spiked 2026-11-07: joint MILP and its LP relaxation time out at 60 s; decomposition builds tables in 2.2 s (S=128) and allocates in 1.35 s, hitting budget exactly. Details in plan/spikes/.
- Next 2-hour spike: in-season re-plan on remaining cells at S=64 must be at most 0.6 s.

## Impact
- TBO's hotel business is 87% of gross profit (sourced). Every peak-date search that ends in "sold out" is a lost booking for an agent and for TBO. TBO's own sold-out rate is unknown; demo numbers are estimates on calibrated synthetic data and are labelled "simulated".
- Capital efficiency: the planner reports how much capital each pp of availability costs, so finance can approve pre-buy with a number rather than a feeling.

## Surprise
A typical team builds a forecast dashboard plus a knapsack table. Headroom plays the season like a live race between three buying desks, lets a judge try to beat it, and treats contracts as options rather than units.

## Red team results
- Three other teams on this PS: (1) Allotment-Atlas-style profit optimiser with a globe, (2) Prophet forecast + LP dashboard in Streamlit, (3) LLM "inventory analyst" chatbot over a CSV. Ours wins on Innovation (contracts, availability, supplier lever, weekly recourse) and on Impact framed in TBO's own words ("maximize availability"), and on Adoption (allotments reduce capital at risk; human approval queue).
- Judge's first skeptical question: "TBO is asset-light and pays hotels after check-in. Why tie up cash?" Answer: Headroom usually recommends allotments and supplier integration, which commit little or no cash; it only buys hard where the expected sold-out loss beats the capital price, and it shows that price in ₹. Second question: "Your data is synthetic." Answer: calibrated on five real public datasets with a provenance panel; a CSV seam takes TBO's real bookings; shadow mode first.
- Removal test: passes (see Requirement fit).
- One-sentence explanation for a non-technical judge: "It tells TBO which rooms and seats to lock in, and on what kind of contract, so agents never see sold out on Diwali or New Year, and it keeps re-planning every week."
- Hero in first 60 s: yes, at 0:20.
- Impact claims: hotel GP share sourced; sold-out rates labelled simulated.

## Rejected
- Multi-Supplier Optimization "Room Genome": 4 visible competitors including TrueShelf (F1 0.99+, like-for-like price, ranking); TBO already pays Vervotech for mapping.
- Virtual Travel Agent "Disruption Twin": most crowded PS; TBO already shipped an AI itinerary builder and Claude/ChatGPT connectors (Oct 2026).
- OpsDesk: the spec fixes the feature list, so entries converge.
- HR platform: 8 mandatory objectives plus a live extension test; heavy for 2 people; weak travel link.
- 3D globe as hero: the strongest competitor already has one.
- LLM in the decision path: judges must trust numbers; reasons are generated from engine numbers only.

## Open questions
- Will TBO share any data or API access at the 14 Nov webinar? If yes, add a real-data adapter before Round 2.
- Exact Round 1 slide template and video length (check at the webinar).
- Real TBO contract terms (typical allotment release days, utilisation clauses, series-block deposits). Until known, parameters are labelled assumptions and are editable in the UI.
