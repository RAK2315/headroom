# 11 Engine spec (the showpiece)

This is the maths the `engine/` package implements. Build it test-first (TDD) in the order of the sections. Every default parameter marked (A) is an assumption: it lives in `data/reference/contracts.yaml`, shows an "assumption" tag in the UI, and is editable in the Contract Lab.

The working prototype of sections 4-6 is `plan/spikes/decomp_spike.py`. Read it before starting; the production code is a cleaned-up, tested version of it.

## 1. Notation
- Cells `c = 0..C-1`, `C = 45 pools x 26 weeks = 1,170`. Cell order: pool-major (`c = pool_idx * 26 + week`).
- Scenarios `s = 0..S-1`.
- `D[s,c]` net demand in units at the reference markup 8% (after un-censoring, before cancellations).
- `r[c]` reference free-sale net rate per unit (₹) for the cell (from the world generator; reported per pool-week).
- `Fcap[s,c]` free-sale units available from suppliers in the cell (close-outs make it small on peaks).
- `cf[s,c]` free-sale net rate per unit in the scenario, as a multiple of `r[c]` times `r[c]`.
- `is_peak[c]` boolean from the event calendar.
- Options per cell `o = (m, ih, ia)`: markup index `m` in 0..2, hard grid index `ih` in 0..G-1, allotment grid index `ia` in 0..G-1. `G = 12` for plans, `G = 10` for in-season re-plans.

## 2. Contract economics (defaults per unit, relative to `r[c]`)
| Parameter | Hotel default | Flight default | Notes |
|---|---|---|---|
| `hard_rate` | 0.78 r (A) | 0.80 r (A) | hard pre-buy / series block net |
| `allot_rate` | 0.90 r (A) | n/a (flights have no allotment) | paid only when sold |
| `allot_fee` | 0.02 r per held unit (A) | n/a | holding fee at signing (counts as capital) |
| `release_days` | 21 (A) | n/a | allotment returns to hotel 21 days before the stay week |
| `util_min` | 0.70 (A) | n/a | utilisation clause |
| `util_pen` | 0.10 r per unit below `util_min * a` (A) | n/a | |
| `salvage` | 0.25 of hard_rate (A) | 0.15 of hard_rate (A) | resale of unsold hard units through last-minute channels |
| `late_cancel` `rho[c]` | from Hotel Booking Demand: share of bookings cancelled within 21 days of arrival, by lead bucket, mapped to the cell's lead mix | same as hotels x 0.5 (A) | real calibration |
| `free_rate` `cf/r` | lognormal around 1.03, sd 0.05, rising to 1.12 on peaks (A, calibrated so peak free-sale is 8-12% dearer) | from EaseMyTrip days-left curve | |
| Markups | 0.04, 0.08, 0.12 | same | |
| Elasticity `eps` | 1.6 (A) | 1.2 (A) | demand multiplier `((1+m)/1.08)^(-eps)` |
| Allotment cap `Amax[c]` | 0.8 x P50 demand (A) | 0 | hotels will not give more |
| Hard lead | at plan time (plan date 21 Sep 2026, two weeks before W26 starts) every cell can be contracted at the listed rates; in-season at least 3 weeks ahead, rate +8% | same | |
| Allot lead | in-season top-up at least 5 weeks before stay, rate +3% | n/a | |

Selling price `p[c,m] = r[c] * (1 + markup[m])`. Demand at markup m: `Dm[s,c] = D[s,c] * ((1+markup[m])/1.08)^(-eps)`.

## 3. Recourse (single source of truth: `engine/recourse.py`)
Given hard `h`, allotment `a`, markup `m`, and one scenario:
```
dem   = Dm[s,c]
sh    = min(h, dem)                      # hard is sunk, serve it first
rem   = dem - sh
sa    = min(a, rem); rem -= sa           # then allotment
f     = min(Fcap[s,c], rem) if p > cf[s,c] else 0   # then free sale if it has margin
lost  = rem - f                          # sold-out demand
k     = 1 - rho[c]                       # share of served units that actually stay and pay
profit = p*sh*k + salvage*(h - sh*k) - hard_rate*h
       + (p - allot_rate)*sa*k - allot_fee*a - util_pen*max(0, util_min*a - sa*k)
       + (p - cf)*f*k
served = sh + sa + f
capital_committed = hard_rate*h + allot_fee*a
unsold_hard = h - sh*k
```
Implement vectorised over arbitrary leading axes with numpy broadcasting (exactly like `value_tables` in the spike). Write the scalar version first as the test oracle, then the vectorised one, and test that they agree on random inputs.

## 4. Value tables (`engine/tables.py`)
Grids per cell:
- `hgrid[c, :] = linspace(0, q95(D[:,c]), G)`; for flights the same.
- `agrid[c, :] = linspace(0, min(Amax[c], q95(D[:,c])), G)`; flights: all zeros (or a single 0 level).
- Levers off: `contracts=False` -> `agrid = 0`; `pricing=False` -> only markup 0.08.
For every cell and option, over all scenarios, compute:
- `EP[c,o]` expected profit, `ES[c,o]` expected served, `ED[c,m]` expected demand at markup m,
- `CAP[c,o]` capital committed, `CAR[c,o]` capital at risk = E[(hard_rate - salvage)*unsold_hard + util_pen*max(0, util_min*a - sa*k)],
- `DS[c,o]` downside = E[max(0, median_s(profit) - profit)] (mean shortfall below the scenario median),
- `PS_sd[c,o]` standard deviation of profit (for the profit_only baseline).
Do not store per-scenario profit for all options (1,170 x 432 x 128 x 4 bytes = 259 MB). Recompute per-scenario profit only for the chosen options when computing portfolio metrics.
Process cells in chunks of 64 to bound memory; use float32.
Committed offsets (in-season): options are increments on top of `h0[c], a0[c]`; release is a negative allotment increment allowed only for weeks before cut-off; `CAP` counts only new capital.

## 5. Allocation (`engine/allocate.py`)
Per cell and option:
```
score[c,o] = EP[c,o] - beta*DS[c,o] + mu * w[c] * ES[c,o] - lam * CAP[c,o]
w[c] = 0.15 * r[c] * (1.0 if is_peak[c] else 0.25)   if target_scope == "peak"
w[c] = 0.15 * r[c]                                     if target_scope == "all"
choice[c] = argmax_o score[c,o]
```
- `beta` by risk appetite: cautious 1.0, balanced 0.4, bold 0.0.
- Inner loop: bisection on `lam` in [0, lam_hi] (start lam_hi = 200, double until spend at most budget) for 22 iterations; keep the feasible side (spend at most budget).
- Outer loop: bisection on `mu` in [0, 20] for 14 iterations so that availability on the scope (sum ES over scope / sum ED over scope at chosen markup) is at least the target. If availability at mu = 20 is below target, return `target_met = false`, `availability_achievable` = that value.
- `budget_needed_for_target`: only when the target is not met; bisection on budget in [budget, ₹150 Cr] (10 iterations, each with mu fixed at 20 and the inner lam loop) for the smallest budget meeting the target; `None` if even ₹150 Cr does not.
- Warm start: reuse the last `lam`, `mu` as the initial midpoint when only the budget or target changed.
- Table cache: `tables` depend on (season, S, seed, levers, contract params, committed). Keep an in-memory LRU of 4 entries in the API process so slider changes to budget, target or risk only re-run allocation (target: at most 0.5 s).
- Hull allocation (build it in phase 2 for the re-plan, then use it everywhere; the spike's plain version took 1.35 s for 14 x 22 iterations): pre-sort each cell's options by capital and keep only the upper concave hull of (CAP, EP - beta*DS + mu*w*ES); then for a given lam each cell's choice is found by binary search on the hull slope. Keep the plain version as the test oracle for it.
- Marginal value: after the final solve, re-run allocation at budget + ₹1 Cr with warm start; report `soldout_pp_per_cr` and `profit_inr_per_cr`.

## 6. Scenarios and updates (`engine/scenarios.py`)
- Inverse CDF per cell from forecast quantiles q in {0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95}: linear interpolation in probability between given quantiles; below 0.05 and above 0.95 extrapolate log-linearly using the 0.05-0.1 and 0.9-0.95 slopes; floor at 0.
- Correlated uniforms by Gaussian copula: `z = a_g*Zg[s] + a_d*Zd[s,dest(c)] + a_w*Zw[s,weekcluster(c)] + sqrt(1 - a_g^2 - a_d^2 - a_w^2)*e[s,c]`, `u = Phi(z)`, `D = invcdf_c(u)`. Defaults `a_g = 0.35, a_d = 0.5, a_w = 0.2` (A), or estimated from backtest residual correlations in the pipeline and stored in `copula_param`.
- Free-sale capacity share: `Fcap = D * clip(base_share[c] - 0.6*pressure[c] + noise, 0.05, 1.2)` where `pressure[c]` in [0,1] is the event/Airbnb pressure index; `noise ~ N(0, 0.15)`. Peak cells therefore close out often.
- Free-sale rate: `cf = r * exp(N(log(1.03 + 0.09*pressure), 0.05))`.
- Determinism: one `numpy.random.Generator(PCG64(seed))` per call; never global state.
- In-season Bayesian update after week k, per destination: `ratio = sum(observed demand, last up to 3 weeks) / sum(P50 forecast, same weeks)`, `n` = weeks observed (max 3), `kappa = n/(n+2)`, `scale = 1 + kappa*(ratio - 1)`; multiply remaining scenario demand of that destination by `scale`. On a shock reveal, multiply the affected cells' remaining scenario demand by the announced multiplier times `U(0.85, 1.15)` per scenario.

## 7. Supplier lever (`engine/suppliers.py`)
- Candidate supplier k: one-time cost `cost_k` (counts against the budget), live week `L_k` (relative to plan time; only helps cells with week at least `L_k`), boost: extra free-sale units `B_k[c]` for covered pools (per-scenario factor `U(0.6, 1.0)`), net rate `cf * rate_factor_k`.
- Greedy: base plan without suppliers. Loop up to 6 times: for each not-yet-chosen k, rebuild tables only for cells k covers (Fcap boosted, rate adjusted), re-allocate with budget minus cost_k (warm start), compute `J = sum(EP - beta*DS + mu_base*w*ES)` over all cells; `gain_k = J_with - J_current`. Add the best k if `gain_k > 0`. Forced include/exclude from `PlanParams.force_suppliers` override the greedy choice.
- Output `SupplierDecision` with `value_inr = round(gain_k)`, `cells_helped` = covered cells with any change in choice.

## 8. Reasons and diffs (`engine/reasons.py`)
Deterministic templates filled from the cell's numbers. Choose the first matching template:
1. Nothing secured: "{Dest} {tier}, week of {date}: free sale covers demand in {pct_free_ok}% of scenarios; securing rooms would only add risk."
2. Allotment-led: "{Dest} {tier}, week of {date}: forecast {p50} units (P90 {p90}); free sale closes out in {pct_closeout}% of scenarios. {a} on allotment (release by {release_by}) covers the likely range with no upfront cash{hard_clause}."  where hard_clause = "; {h} hard at {disc}% below free sale for the floor that sells in {pct_hard_sold}% of scenarios" if h > 0.
3. Hard-led (flights, or hotels where allotment is capped): "{Route or Dest tier}, week of {date}: {h} {seats or rooms} on a {series block or hard pre-buy} at {disc}% below the market rate; they sell in {pct_hard_sold}% of scenarios, expected unsold {unsold} (₹{risk} at risk)."
4. Markup clause appended when markup is not 8%: " Markup {m}%: {why}." with why = "demand exceeds secured supply in {x}% of scenarios" (12%) or "price-sensitive week, 4% keeps {y} more bookings" (4%).
Diff lines for re-plans (max 5, sorted by absolute capital change): "+{n} {Dest} {tier} allotment (wk {a}-{b})", "+{n} {Dest} {tier} hard (wk {a})", "release {n} {Dest} {tier} before cut-off (wk {a})", "{Dest} markup {old}% to {new}% (wk {a}-{b})", "integrate {supplier}". Final line "capital {+/-}₹{x} Cr".
Number formats: ₹ in Indian style (₹1.9 Cr, ₹45 L, ₹8,400). Units with thousands separators.

## 9. Portfolio metrics (`engine/metrics.py`)
- Re-run recourse for chosen options to get `profit[s]` summed over cells -> `exp_profit = mean`, `p10 = quantile 0.10`, `cvar5 = mean of profit[s] <= quantile 0.05`, `prob_loss = mean(profit < 0)`.
- `soldout_rate_peak = 1 - sum(served over peak cells) / sum(demand over peak cells)` (expected over scenarios); `soldout_rate_all` likewise.
- `capital_committed = sum CAP`; `capital_at_risk = sum CAR`.

## 10. Baselines (`engine/baselines.py`)
- `playbook`: for peak cells, `h = 1.10 * served_last_season[c]` (from W25 history mapped by week), markup 0.08, no allotment, no suppliers; if total capital exceeds budget, scale all `h` down proportionally. Off-peak: nothing secured (free sale only).
- `profit_only`: tables restricted to markup 0.08 and allotment 0; score = `EP - 0.5*PS_sd - lam*CAP`, bisection on lam to the budget; no availability term, no suppliers, no re-plan.
- Both evaluated with the same recourse and metrics.

## 11. Simulator (`engine/simulate.py`)
State per desk: commitments `h[c], a[c], m[c]`, remaining budget, cumulative outcomes.
For week k = 0..25:
1. Reveal shocks with `reveal_week == k` (emit `shock` events).
2. For each desk, realise cells of week k using `truth.D[c]`, `truth.Fcap[c]`, `truth.cf[c]` (single path) through `recourse`; accumulate profit, served, lost, wasted.
3. Headroom only: Bayesian update + shock multipliers on its remaining scenarios (section 6); re-plan increments for cells with week in (k, 25] using G = 10, S = 64, remaining budget; apply automatic releases at cut-off; emit `diff` if any line changed by at least 1% of capital or at least 50 units in a cell. "You" desk: apply validated user actions (play mode).
4. Emit `week` with per-destination aggregates and running totals.
Truth: the pipeline's world generator produces `truth_seed` paths (seed 42 = "realistic" with the scripted shocks' true effects, which may differ from the announced ones, e.g. announced +25%, true +21%). The optimiser never sees truth arrays; tests assert that `optimise` has no access to them (the engine inputs object does not contain truth).

## 12. Tests to write first (TDD list)
- `test_recourse.py`: hand-worked cases (no demand, demand below hard, demand between hard and hard+allot, free-sale closed, free-sale unprofitable, utilisation penalty), scalar vs vectorised agreement.
- `test_tables.py`: tables match brute-force loops on a 3-cell, 4-scenario instance.
- `test_allocate.py`: budget respected; monotonicity (budget up -> availability not down; target up -> capital not down); infeasible flag; budget_needed correct on a tiny instance where it is computable by hand.
- `test_exact_gap.py`: decomposition vs HiGHS MILP on 4 pools x 4 weeks x 32 scenarios, no suppliers, fixed markup; gap at most 2% on expected profit at the same budget and availability.
- `test_scenarios.py`: quantile reproduction, determinism, copula correlation within tolerance.
- `test_suppliers.py`: a supplier with zero cost and positive boost is always chosen; one with huge cost never.
- `test_simulate.py`: determinism, reconciliation of totals, truth isolation, releases happen only before cut-off.
- `test_perf.py` (marked slow, run before demo): plan at most 2.5 s (S=128), re-plan p95 at most 0.6 s (S=64).
