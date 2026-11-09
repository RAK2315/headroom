# 10 Data pipeline

Goal: TBO-shaped history and hidden truth seasons whose shape comes from real public data, with every calibration traceable. CLI: `uv run python -m pipeline <step>`; steps in order: `reference`, `signals`, `world`, `demand`, `forecast`, `proof`, `cache-demo`; `all` runs everything. Each step is idempotent and overwrites its outputs.

Key dates:
- Seasons: W24 = 7 Oct 2024 to 6 Apr 2025, W25 = 6 Oct 2025 to 5 Apr 2026, W26 = 5 Oct 2026 to 4 Apr 2027 (26 Monday-start weeks each; checked with Python on 2026-11-07).
- Plan date for W26: 21 Sep 2026. History available to the forecaster: up to the end of W25 plus the off-season gap (we only model the 26 winter weeks; off-season is not generated).
- Diwali: 31 Oct 2024 (W24 week 3), 20 Oct 2025 (W25 week 2), 8 Nov 2026 (W26 week 4). Christmas in week 11, New Year in weeks 12-13. Holi 4 Mar 2026 (W25 week 21), 22 Mar 2027 (W26 week 24). Republic Day 26 Jan (weeks 15-16). Source: `holidays` 0.107 `holidays.India` (checked 2026-11-07).

## Step `reference`
Writes from `data/reference/*.yaml` (seed content in 05-data-model.md): destinations, hubs, pools, seasons + weeks, contract params, suppliers, shocks, events. Validates: 45 pools, unique ids, every event has `source_url` or `assumption: true`.

## Step `signals` (real data)
Raw files go to `data/raw/` (git-ignored). Derived parquet goes to `data/signals/` (committed when the licence allows redistribution of derived data; otherwise commit only the small derived curves and document how to rebuild).

### S1 Inside Airbnb forward availability (real, 6 cities)
- Source: https://insideairbnb.com/get-the-data/ . Calendar files available on 2026-11-07 (verified by listing the page):
  - Bangkok `data.insideairbnb.com/thailand/central-thailand/bangkok/2026-09-22/data/calendar.csv.gz`
  - Singapore `.../singapore/sg/singapore/2026-09-23/data/calendar.csv.gz`
  - Istanbul `.../turkey/marmara/istanbul/2026-09-25/data/calendar.csv.gz`
  - London `.../united-kingdom/england/london/2026-09-17/data/calendar.csv.gz`
  - Paris `.../france/ile-de-france/paris/2026-09-16/data/calendar.csv.gz`
  - Hong Kong `.../china/hk/hong-kong/2026-09-20/data/calendar.csv.gz`
  Not available: Dubai, Bali, Kuala Lumpur, Maldives (no Inside Airbnb coverage).
- Columns used: `listing_id, date, available` (`t`/`f`).
- Derivation: per city per night, `unavail_share = share of listings with available == 'f'`. Then `pressure_night = clip((unavail_share - p50) / (p95 - p50), 0, 1)` using the city's own distribution over the 365 nights. Weekly `airbnb_pressure` = mean of the 7 nights.
- Caveat (show in UI tooltip): "Unavailable includes nights blocked by hosts, so this is a pressure proxy, not occupancy."
- Output: `data/signals/airbnb_pressure.parquet` (`city_id, date, unavail_share, pressure`), plus `airbnb_pressure_week` aggregated to W26 weeks.
- Use: real forward covariate for W26 forecasts and the free-sale close-out model. For history seasons (W24, W25) the generator reuses the same day-of-year pressure shape aligned by weekday and holiday dates (assumption, documented).
- Licence: check the footer of the page at download time (Inside Airbnb publishes under Creative Commons Attribution 4.0 as far as we know; record what the page says in `provenance`).

### S2 Hotel Booking Demand (real lead times and cancellations)
- Source: Antonio, de Almeida, Nunes (2019), "Hotel booking demand datasets", Data in Brief 22, https://doi.org/10.1016/j.dib.2018.11.126 . Convenient CSV mirror: TidyTuesday 2020-02-11 `hotels.csv` (https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-02-11). 119,390 bookings, two Portuguese hotels, 2015-2017. Verify the licence statement on the article page when downloading.
- Columns used: `hotel, is_canceled, lead_time, arrival_date_year, arrival_date_month, arrival_date_day_of_month, deposit_type, adr, stays_in_weekend_nights, stays_in_week_nights`.
- Derivations:
  - Lead-time distribution: empirical CDF of `lead_time` for non-cancelled bookings, separately for "City Hotel" (use for city destinations) and "Resort Hotel" (use for Bali, Maldives).
  - Cancellation probability by lead bucket (0-7, 8-21, 22-60, 61-120, 121+ days) and deposit type.
  - Late-cancel rate `rho`: share of eventually-cancelled bookings whose cancellation came within 21 days of arrival. The dataset has `reservation_status_date` for cancellations; late = arrival date minus reservation_status_date at most 21 days.
- Output: `data/signals/lead_cancel.parquet` (`hotel_type, lead_bucket, deposit_type, p_cancel, p_late_cancel, lead_cdf...`).

### S3 Google Trends (real seasonality of Indian outbound interest)
- Manual export (pytrends is archived; do not use it): https://trends.google.com/trends/explore , Geo = India, Time = past 5 years, Category = Travel, one search term per destination: "Dubai", "Bangkok", "Singapore", "Bali", "Kuala Lumpur", "Maldives", "Istanbul", "London", "Paris", "Hong Kong". Export CSV for each, save as `data/raw/trends/<DEST>.csv`. Also export one comparison chart with all five largest together (Dubai, Bangkok, Singapore, London, Bali) to get relative scale; save as `data/raw/trends/compare.csv`.
- Derivation: weekly index per destination, normalised to mean 1.0 over 5 years; seasonal profile = median by ISO week across years; YoY growth slope from the last 3 years.
- Output: `data/signals/trends_week.parquet` (`dest_id, week_start, index, seasonal_profile`). Commit the raw CSVs too (they are small; Trends allows citing the data; we use only the derived index).

### S4 Holidays and events (real dates)
- `holidays.India(years=2024..2027)` for Indian public holidays.
- `data/reference/events.yaml`: curated list, each with `id, name, dest_ids (or "all"), start, end, intensity 0-1, source_url`. Minimum list to fill (verify each date from the official or Wikipedia page and paste the URL):
  - Diwali window (Dhanteras to Bhai Dooj) each year: all destinations, intensity 0.6 (Dubai, Bangkok, Singapore 0.8).
  - Indian school winter break (about 24 Dec - 2 Jan): all, 0.9.
  - Christmas - New Year: all, 1.0 (London, Paris, Dubai 1.0; others 0.8).
  - Republic Day long weekend: Gulf and SE Asia, 0.5.
  - Dubai Shopping Festival (mid Dec - mid Jan; check dates per year on visitdubai.com): DXB, 0.5.
  - Chinese New Year (29 Jan 2025, 17 Feb 2026, 6 Feb 2027): SIN, KUL, HKG, BKK, 0.4.
  - Holi long weekend: Gulf and SE Asia, 0.3.
  - Eid al-Fitr: DXB, KUL, IST, 0.3.
- Output: `data/signals/event_intensity_day.parquet` (`dest_id, date, intensity`), max over overlapping events.

### S5 Flight fares by days-left (real shape)
- Source: Kaggle "Flight Price Prediction" (EaseMyTrip, about 300k rows), https://www.kaggle.com/datasets/shubhambathwal/flight-price-prediction . Columns `days_left, price, class, airline, source_city, destination_city`.
- Derivation: for economy, median price by `days_left` (1-49) normalised to the 49-day value -> `fare_multiplier(days_left)`. This is domestic India data; we use only its shape (how fares rise as departure nears) for international routes (assumption, documented).
- Licence: read the dataset page. If it is not commercial-friendly, keep the raw file out of git and commit only the 49-number curve with attribution, and mark it "research use" in provenance.
- Output: `data/signals/fare_curve.parquet`.

### Provenance table
`provenance(source_id, name, url, licence, fetched_on, used_for, real_or_assumption)`. Shown in the Demand Lens and README.

## Step `world` (calibrated synthetic TBO-shaped data)
Deterministic given `--seed` (default 42). For each pool and each day of W24, W25 and W26:

1. Base volume. Destination weight (A): DXB 1.00, BKK 0.70, SIN 0.55, LON 0.35, DPS 0.35, KUL 0.30, PAR 0.25, MLE 0.20, IST 0.20, HKG 0.15. Hotel weekly room-nights at season average for the core tier = 5,000 x weight; tier shares value 0.35, core 0.45, premium 0.20 (core = 0.45 of the destination total, so scale accordingly). Flight weekly seats per route = 1,500 x weight of the destination x hub share (DEL 0.4, BOM 0.35, BLR 0.25). All marked "TBO-shaped scale (assumption)".
2. Seasonality: multiply by the Trends seasonal profile of the destination (S3) for that week.
3. Growth: +12% per year (A), so W26 is about 1.25 x W24.
4. Events: multiply by `1 + intensity(date)` (S4).
5. Weekday shape: hotels Fri-Sat x1.15, Sun-Thu x0.94 (A).
6. Daily unconstrained demand `~ NegBin(mean, dispersion k = 20)` (A).
7. Free-sale capacity: `cap = demand_mean x clip(0.95 - 0.6 x pressure + N(0, 0.12), 0.05, 1.3)` where pressure = Airbnb pressure (S1) for the 6 cities, else `min(1, event intensity)`; flights use 1.05 - 0.4 x pressure.
8. Secured inventory in history: the historical TBO desk followed the playbook (hard = previous season served x 1.1 on peak cells; for W24 use 0.8 x mean demand on peak cells). This makes history realistic: some peaks were covered, many were not.
9. Served, bookings, sold-outs: `served = min(demand, secured + cap)`; `bookings_gross = served / (1 - p_cancel_avg)`; cancellations by lead bucket using S2; `lost = demand - served`; searches `= demand x l2b` with `l2b = 8` (A); `soldout_searches = lost x l2b x 1.5` (people retry when sold out, A).
10. Rates: reference net rate `r` per pool (05 seed) x `(1 + 0.3 x pressure)`; free-sale rate ratio per S2 of 11-engine-spec; fares x fare_multiplier for flights by booking lead.
11. Truth for W26: seed 42 "realistic" path including the true effects of scripted shocks (shock library in 05 seed), stored in full in `truth_daily` and as weekly arrays `data/artefacts/truth_42.npz` (D, Fcap, cf per cell). Proof truths: seeds 0-499 without shocks, weekly arrays only, `truth_proof.npz` (500 x 1,170 x 3 float32, about 7 MB).
12. Write `history_daily` (W24, W25), `truth_daily` (W26 seed 42), and `data/reports/calibration.md` with a table: parameter, real source value, generated value, tolerance, pass/fail. Required rows: lead-time median per hotel type (within 10%), cancellation rate by lead bucket (within 2 pp), late-cancel rate (within 2 pp), Trends seasonal correlation between generated weekly demand and the Trends profile (at least 0.8), Airbnb pressure correlation with generated close-out rate (at least 0.6 for the 6 cities).

## Step `demand`
Weekly aggregation and un-censoring (F04): `weekly_demand(pool_id, season_id, week, searches, bookings, soldout_searches, served, demand_unc, is_peak, conv_rate)`. Validation test: on W25, `demand_unc` is within 10% of the generator's true weekly demand for at least 90% of cells.

## Step `forecast`
- Input series: weekly `demand_unc` per pool for W24 and W25 (52 points per pool; the 26-week off-season gap is bridged by treating the two winters as consecutive with a `season_break` covariate, assumption) plus covariates per week: `holiday_in` (count of Indian holidays in the week), `event_intensity` (max), `airbnb_pressure` (0 when missing, plus `has_airbnb` flag), `trends_index`.
- Backtest: fit or condition on W24 only, forecast W25's 26 weeks; compute WQL and P10-P90 coverage per model. Models: Chronos-2 (`Chronos2Pipeline` from chronos-forecasting 2.3.2, `amazon/chronos-2`, CPU, `predict_df` with `future_df` covariates; read the model card examples before coding), LightGBM quantile (one model per quantile, features: lags 1, 2, 26, covariates, pool categorical), seasonal naive (same week last season x growth).
- Production: condition on W24 + W25, forecast W26 with W26 covariates.
- Output: `forecast_quantile(season_id, pool_id, week, model, q05, q10, q25, q50, q75, q90, q95)`, `backtest_metric(model, pool_kind, wql, coverage_80)`, `copula_param` (from W25 residual correlations), `data/reports/backtest.md`.
- Chosen model per pool kind = lowest WQL; record the choice.

## Step `proof`
For truth seeds 0-499 at ₹40 Cr, 95% peak target, balanced, S=128: optimise once per desk (plans do not depend on truth), simulate each truth without shocks (no re-plan needed for the plan-quality proof; a second smaller proof with re-plan on 50 seeds measures re-planning value). Output `data/reports/proof.md` and `web/public/cached/proof.json`: per desk distributions of peak sold-out rate, profit, CVaR; win rates; exact-gap result; engine timings.

## Step `cache-demo`
Runs the scripted demo sims and saves the full event streams to `web/public/cached/sim_<hash>.json`, where hash = sha1 of the canonical JSON of `{params, truth_seed, shocks, desks}`. Scripted runs:
1. Default hero: W26, ₹40 Cr, 95% peak, balanced, all levers, truth 42, shocks `["visa_uae"]`, desks playbook/profit_only/headroom.
2. Same with shocks `["visa_uae", "bkk_concert"]`.
3. Same with no shocks.
Also caches `plan_<hash>.json` for the default Plan Studio state and the 12 frontier points.
