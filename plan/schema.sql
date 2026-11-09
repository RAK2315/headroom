-- Headroom DuckDB schema. Keep in sync with plan/05-data-model.md (change both in the same commit).
-- Run: duckdb data/headroom.duckdb < plan/schema.sql  (the pipeline runs it automatically in step `reference`)

CREATE TABLE IF NOT EXISTS destination (
  dest_id TEXT PRIMARY KEY, name TEXT NOT NULL, lat DOUBLE NOT NULL, lon DOUBLE NOT NULL,
  region TEXT NOT NULL, weight DOUBLE NOT NULL, airbnb_city TEXT, trends_term TEXT NOT NULL, airport TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS hub (
  hub_id TEXT PRIMARY KEY, name TEXT NOT NULL, lat DOUBLE NOT NULL, lon DOUBLE NOT NULL, share DOUBLE NOT NULL
);
CREATE TABLE IF NOT EXISTS pool (
  pool_id TEXT PRIMARY KEY,
  kind TEXT NOT NULL CHECK (kind IN ('hotel','flight')),
  dest_id TEXT NOT NULL REFERENCES destination(dest_id),
  tier TEXT CHECK (tier IN ('value','core','premium')),
  hub_id TEXT REFERENCES hub(hub_id),
  ref_rate_inr INTEGER NOT NULL,
  label TEXT NOT NULL,
  CHECK ((kind = 'hotel' AND tier IS NOT NULL AND hub_id IS NULL) OR (kind = 'flight' AND tier IS NULL AND hub_id IS NOT NULL))
);
CREATE TABLE IF NOT EXISTS season (
  season_id TEXT PRIMARY KEY, start_date DATE NOT NULL, end_date DATE NOT NULL, plan_date DATE
);
CREATE TABLE IF NOT EXISTS week (
  season_id TEXT NOT NULL REFERENCES season(season_id), k INTEGER NOT NULL CHECK (k BETWEEN 0 AND 25),
  week_start DATE NOT NULL, PRIMARY KEY (season_id, k)
);
CREATE TABLE IF NOT EXISTS contract_param (
  param TEXT NOT NULL, pool_kind TEXT NOT NULL CHECK (pool_kind IN ('hotel','flight')),
  value DOUBLE NOT NULL, assumption BOOLEAN NOT NULL, note TEXT, PRIMARY KEY (param, pool_kind)
);
CREATE TABLE IF NOT EXISTS supplier (
  supplier_id TEXT PRIMARY KEY, name TEXT NOT NULL, description TEXT NOT NULL, cost_inr INTEGER NOT NULL,
  live_weeks INTEGER NOT NULL, rate_factor DOUBLE NOT NULL, fictional BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE TABLE IF NOT EXISTS supplier_coverage (
  supplier_id TEXT NOT NULL REFERENCES supplier(supplier_id), pool_id TEXT NOT NULL REFERENCES pool(pool_id),
  boost_share DOUBLE NOT NULL, PRIMARY KEY (supplier_id, pool_id)
);
CREATE TABLE IF NOT EXISTS shock (
  shock_id TEXT PRIMARY KEY, title TEXT NOT NULL, effect_text TEXT NOT NULL,
  reveal_week INTEGER NOT NULL CHECK (reveal_week BETWEEN 0 AND 25), fictional BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE TABLE IF NOT EXISTS shock_effect (
  shock_id TEXT NOT NULL REFERENCES shock(shock_id), dest_id TEXT NOT NULL, pool_kind TEXT, tiers TEXT,
  week_from INTEGER NOT NULL, week_to INTEGER NOT NULL,
  target TEXT NOT NULL CHECK (target IN ('demand','free_cap')),
  announced_mult DOUBLE NOT NULL, true_mult DOUBLE NOT NULL
);
CREATE TABLE IF NOT EXISTS event (
  event_id TEXT PRIMARY KEY, name TEXT NOT NULL, dest_ids TEXT NOT NULL, start_date DATE NOT NULL, end_date DATE NOT NULL,
  intensity DOUBLE NOT NULL CHECK (intensity BETWEEN 0 AND 1), source_url TEXT, assumption BOOLEAN NOT NULL,
  CHECK (source_url IS NOT NULL OR assumption)
);
CREATE TABLE IF NOT EXISTS provenance (
  source_id TEXT PRIMARY KEY, name TEXT NOT NULL, url TEXT NOT NULL, licence TEXT NOT NULL, fetched_on DATE NOT NULL,
  used_for TEXT NOT NULL, kind TEXT NOT NULL CHECK (kind IN ('real','derived','assumption'))
);

CREATE TABLE IF NOT EXISTS history_daily (
  season_id TEXT NOT NULL, pool_id TEXT NOT NULL REFERENCES pool(pool_id), date DATE NOT NULL,
  demand_true INTEGER NOT NULL, searches INTEGER NOT NULL, bookings_gross INTEGER NOT NULL, cancellations INTEGER NOT NULL,
  served INTEGER NOT NULL, soldout_searches INTEGER NOT NULL, secured_hard INTEGER NOT NULL, free_cap INTEGER NOT NULL,
  ref_rate_inr INTEGER NOT NULL, free_rate_inr INTEGER NOT NULL, pressure DOUBLE NOT NULL,
  PRIMARY KEY (season_id, pool_id, date)
);
CREATE TABLE IF NOT EXISTS truth_daily AS SELECT * FROM history_daily WHERE FALSE;
CREATE TABLE IF NOT EXISTS weekly_demand (
  season_id TEXT NOT NULL, pool_id TEXT NOT NULL REFERENCES pool(pool_id), k INTEGER NOT NULL,
  searches INTEGER NOT NULL, bookings INTEGER NOT NULL, soldout_searches INTEGER NOT NULL, served INTEGER NOT NULL,
  demand_unc DOUBLE NOT NULL, conv_rate DOUBLE NOT NULL, is_peak BOOLEAN NOT NULL,
  PRIMARY KEY (season_id, pool_id, k)
);
CREATE TABLE IF NOT EXISTS covariate_week (
  season_id TEXT NOT NULL, dest_id TEXT NOT NULL REFERENCES destination(dest_id), k INTEGER NOT NULL,
  holiday_in INTEGER NOT NULL, event_intensity DOUBLE NOT NULL, airbnb_pressure DOUBLE NOT NULL,
  has_airbnb BOOLEAN NOT NULL, trends_index DOUBLE NOT NULL, PRIMARY KEY (season_id, dest_id, k)
);
CREATE TABLE IF NOT EXISTS forecast_quantile (
  season_id TEXT NOT NULL, pool_id TEXT NOT NULL REFERENCES pool(pool_id), k INTEGER NOT NULL, model TEXT NOT NULL,
  q05 DOUBLE NOT NULL, q10 DOUBLE NOT NULL, q25 DOUBLE NOT NULL, q50 DOUBLE NOT NULL,
  q75 DOUBLE NOT NULL, q90 DOUBLE NOT NULL, q95 DOUBLE NOT NULL, chosen BOOLEAN NOT NULL,
  PRIMARY KEY (season_id, pool_id, k, model)
);
CREATE TABLE IF NOT EXISTS backtest_metric (
  model TEXT NOT NULL, pool_kind TEXT NOT NULL, wql DOUBLE NOT NULL, coverage_80 DOUBLE NOT NULL, n_cells INTEGER NOT NULL,
  PRIMARY KEY (model, pool_kind)
);
CREATE TABLE IF NOT EXISTS copula_param (name TEXT PRIMARY KEY, value DOUBLE NOT NULL);

CREATE TABLE IF NOT EXISTS plan (
  plan_id TEXT PRIMARY KEY, params_json JSON NOT NULL, metrics_json JSON NOT NULL, created_at TIMESTAMP NOT NULL
);
CREATE TABLE IF NOT EXISTS buy_line (
  plan_id TEXT NOT NULL REFERENCES plan(plan_id), pool_id TEXT NOT NULL, k INTEGER NOT NULL,
  hard_units INTEGER NOT NULL, allot_units INTEGER NOT NULL, markup DOUBLE NOT NULL,
  buy_by DATE NOT NULL, release_by DATE, capital_committed_inr BIGINT NOT NULL, capital_at_risk_inr BIGINT NOT NULL,
  exp_demand DOUBLE NOT NULL, exp_served DOUBLE NOT NULL, p_soldout DOUBLE NOT NULL, exp_profit_inr BIGINT NOT NULL,
  reason TEXT NOT NULL, PRIMARY KEY (plan_id, pool_id, k)
);
CREATE TABLE IF NOT EXISTS supplier_decision (
  plan_id TEXT NOT NULL REFERENCES plan(plan_id), supplier_id TEXT NOT NULL, integrate BOOLEAN NOT NULL,
  forced BOOLEAN NOT NULL, value_inr BIGINT NOT NULL, cells_helped INTEGER NOT NULL, live_week INTEGER NOT NULL,
  PRIMARY KEY (plan_id, supplier_id)
);
CREATE TABLE IF NOT EXISTS order_line (
  order_id TEXT PRIMARY KEY, plan_id TEXT NOT NULL REFERENCES plan(plan_id), pool_id TEXT NOT NULL, k INTEGER NOT NULL,
  hard_units INTEGER NOT NULL, allot_units INTEGER NOT NULL, markup DOUBLE NOT NULL, capital_committed_inr BIGINT NOT NULL,
  state TEXT NOT NULL CHECK (state IN ('pending_approval','approved','rejected','withdrawn','sent_to_supplier','confirmed','declined_by_supplier')),
  submitted_by TEXT NOT NULL, decided_by TEXT, comment TEXT, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL,
  UNIQUE (plan_id, pool_id, k)
);
CREATE SEQUENCE IF NOT EXISTS audit_seq START 1;
CREATE TABLE IF NOT EXISTS audit_log (
  entry_id BIGINT PRIMARY KEY DEFAULT nextval('audit_seq'), occurred_at TIMESTAMP NOT NULL, actor_role TEXT NOT NULL,
  entity TEXT NOT NULL, entity_id TEXT NOT NULL, action TEXT NOT NULL, from_state TEXT, to_state TEXT, comment TEXT
);
