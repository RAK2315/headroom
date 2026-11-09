# 02 Stack (locked 2026-11-07)

Principle: boring where it does not matter, best-in-class where the hero lives (optimiser speed, map animation, charts).

Versions were checked on 2026-11-07 against PyPI (`https://pypi.org/pypi/<pkg>/json`) and the npm registry (`npm view <pkg> time`). Rule used: the newest release that is at least two weeks old (before 2026-10-24), unless noted. Lockfiles (`uv.lock`, `package-lock.json`) are committed at scaffold time and are the source of truth after that.

## Requirements (from 01-hero.md)
R1 Initial plan at most 2.5 s, weekly re-plan at most 0.6 s p95. R2 Season stream at 1.5 s/week with at least 2 weeks buffered. R3 Map 60 fps, 4,000 particles, offline (no tiles). R4 Fully styled custom charts. R5 About 2.5 M history rows in-process. R6 Quantile forecasts with known-future covariates, offline. R7 Offline demo plus deployed URL with cached mode. R8 Deterministic runs.

## Decision records

### Engine language and numerics: Python 3.12 + numpy 2.5.4 + scipy 1.18.1
- Requirement: R1, R6, R8.
- Candidates: Python/numpy; TypeScript in the browser (as Allotment Atlas did); Rust/WASM.
- Scores: Python wins on R6 (Chronos-2 and LightGBM are Python), on vectorised speed (spike: tables 2.2 s, allocation 1.35 s) and on Claude Code familiarity. Browser TS would duplicate the engine and lose the forecasting stack. Rust is too slow to write for a 2-person team.
- Chosen because: the spike proved numpy meets R1 at S=128.
- Gives us: one language for data, forecast, optimiser, simulator. Costs us: a backend must run for live solves (mitigated by cached runs).
- Verified: https://pypi.org/project/numpy/ (2.5.4, 2026-10-10), https://pypi.org/project/scipy/ (1.18.1, 2026-08-21), 2026-11-07.
- Spike: done (plan/spikes/RESULTS.md).

### Environment and packaging: uv 0.13.x, Python 3.12.15
- Candidates: uv, pip+venv, poetry. uv: fastest, lockfile, installs Python itself (the owner's machine has only Python 3.10; `uv venv -p 3.12` worked in the spike). One line.

### API: FastAPI 0.162.0 + uvicorn 0.54.0 + pydantic 2.14.1
- Requirement: R2 (SSE streaming), typed contracts.
- Candidates: FastAPI, Litestar, Flask.
- Chosen because: typed request/response models generate the OpenAPI docs judges can open; native `StreamingResponse` for SSE; most familiar to Claude Code.
- Gives us: `/docs` page for free. Costs us: single process; we run one worker (DuckDB single writer).
- Verified: https://pypi.org/project/fastapi/ (0.162.0, 2026-10-23), https://pypi.org/project/uvicorn/ (0.54.0, 2026-09-25), https://pypi.org/project/pydantic/ (2.14.1, 2026-10-11).
- Spike: not needed.

### Data store: DuckDB 1.5.6 (file `data/headroom.duckdb`) + Parquet + `.npy` artefacts
- Requirement: R5, zero ops.
- Candidates: DuckDB, SQLite, Postgres (Supabase).
- Scores: DuckDB reads Parquet natively and handles analytical queries over millions of rows in-process; SQLite is slower for aggregates; Postgres adds a server and network for no demo value.
- Chosen because: in-process, offline, fast group-bys, one file to ship.
- Costs us: one writer at a time, so the API holds one connection behind a lock. 1.5.6 chosen over 2.0.0 (released 2026-10-21, a new major, too fresh).
- Verified: https://pypi.org/project/duckdb/ (1.5.6, 2026-09-28; 2.0.0, 2026-10-21), 2026-11-07.
- Large arrays (scenario tensors S x 1,170) live as `.npy` files in `data/artifacts/`, not in the DB, because they are read whole into numpy.

### Dataframes: pandas 3.1.0 + pyarrow 26.0.0
- pandas is required by chronos-forecasting; use it in the pipeline only. The engine works on numpy arrays. One line.
- Verified: https://pypi.org/project/pandas/ (3.1.0, 2026-10-22), https://pypi.org/project/pyarrow/ (26.0.0, 2026-10-09).

### Forecasting: Chronos-2 via chronos-forecasting 2.3.2 (+ torch 2.14.1 CPU), LightGBM 4.7.0 quantile baseline, seasonal naive baseline
- Requirement: R6 (quantiles, known-future covariates).
- Candidates: Chronos-2; TimesFM 2.5/3.0; LightGBM quantile regression; Prophet.
- Scores: Chronos-2 natively supports known-future real and categorical covariates and outputs quantiles, Apache-2.0, CPU inference supported (model card). TimesFM 3.0 downloadable weights are non-commercial (research-D), so it fails the licence rule. Prophet has no native quantile output beyond intervals and is in the obvious set. LightGBM quantile is a strong, cheap baseline and our comparison model.
- Chosen because: zero-shot quantile forecasts with covariates, licence-clean, and "foundation model forecast" is a credible innovation line; LightGBM keeps us safe if Chronos-2 underperforms in backtest (pick the better on backtest WQL, report both).
- Gives us: covariate-aware fans without training. Costs us: torch is heavy (about 1 GB), so it is a pipeline-only dependency group, never in the API image.
- Verified: https://huggingface.co/amazon/chronos-2 (licence apache-2.0, last modified 2026-06-05; covariates table on the card), https://pypi.org/project/chronos-forecasting/ (2.3.2, 2026-09-08), https://pypi.org/project/torch/ (2.14.1, 2026-09-30), https://pypi.org/project/lightgbm/ (4.7.0, 2026-07-18), 2026-11-07.
- Spike: 1 hour in phase 1: run Chronos-2 on 45 weekly series with 3 covariates on CPU; must finish under 10 minutes.

### Holidays: holidays 0.107
- Indian public holidays per year (`holidays.India`). Event calendar beyond that is a curated YAML with source URLs. One line. Verified https://pypi.org/project/holidays/ .

### Exact-check solver (tests only): highspy 1.15.1
- Used only in `engine/tests/test_exact_gap.py` to solve a tiny instance exactly. Verified https://pypi.org/project/highspy/ (1.15.1, 2026-07-02).

### Python tooling: pytest 9.1.1, ruff 0.17.2, httpx 0.28.1 (TestClient), mypy not used (pydantic models + tests are enough)
- Verified on PyPI 2026-11-07.

### Frontend framework: React 19.3.1 + Vite 8.3.5 + TypeScript 6.0.3
- Requirement: R3, R4, fast dev loop, static deploy.
- Candidates: React + Vite; Next.js; SvelteKit.
- Scores: deck.gl has first-class React bindings; Vite builds a static SPA that deploys anywhere and runs offline; Next.js adds server features we do not need (our server is Python). SvelteKit has weaker deck.gl integration.
- Chosen because: static SPA + Python API is the simplest shape that meets R3 and R7.
- TypeScript pinned to 6.0.3, not 7.x: typescript-eslint 8.72.0 supports TypeScript `>=4.8.4 <6.1.0`.
- Verified: npm `react` 19.3.1 (2026-10-14), `vite` 8.3.5 (2026-10-21), `@vitejs/plugin-react` 6.1.2 (2026-10-05, peer vite ^8), `typescript` 6.0.3 (2026-04-16), `typescript-eslint` peer range checked 2026-11-07.

### Map and particles: deck.gl 9.4.0 (no basemap) + world-atlas 2.0.2 + topojson-client 3.1.0
- Requirement: R3 (60 fps, 4,000 particles, arcs, heatmap, offline).
- Candidates: deck.gl; MapLibre GL + custom layers; plain Canvas2D/PixiJS.
- Scores: deck.gl gives ScatterplotLayer (particles), ArcLayer, TripsLayer, HeatmapLayer, GeoJsonLayer on the GPU with transitions; no tile server needed if we draw land from a local TopoJSON. MapLibre needs a style and tiles (offline risk). PixiJS would mean hand-building projection and heatmap.
- Chosen because: all four visual layers we need exist and run on WebGL2 at the target counts.
- Costs us: deck.gl's API surface is large; Claude must read docs for TripsLayer and HeatmapLayer before coding (use /research).
- Verified: npm `deck.gl` 9.4.0 (2026-09-05), peer `@deck.gl/core ~9.4.0`; `world-atlas` 2.0.2 (ISC), `topojson-client` 3.1.0 (ISC), 2026-11-07.
- Spike: 1 hour in phase 2: 4,000 particles + 15 arcs + heatmap at 60 fps on the builder's laptop.

### Charts: D3 7.9.0 (scales, shapes, axes) rendered as React SVG
- Requirement: R4.
- Candidates: D3 in React; visx 4; Recharts/ECharts.
- Scores: D3 gives total control and is extremely well known to Claude; visx 4.0.0 is new (risk of stale APIs); Recharts/ECharts bring a default look we would fight.
- Verified: npm `d3` 7.9.0, `@types/d3` 7.4.3, 2026-11-07.

### Styling: Tailwind CSS 4.3.3 (+ @tailwindcss/vite 4.3.3) with CSS custom-property tokens
- One line: utility classes on top of our own tokens in `web/src/styles/tokens.css`; no component kit. Verified npm 4.3.3 (2026-07-16).

### Motion: motion 14.6.0
- Panel transitions, count-ups, shock card drop. Verified npm (2026-10-22).

### State and data fetching: zustand 5.0.16 + @tanstack/react-query 5.104.5
- zustand for UI state (selected desk, playhead, sliders); react-query for API calls with caching. Verified npm (2026-10-22, 2026-10-19).

### Routing: react-router 8.5.0
- Seven screens with shareable URLs. Verified npm (2026-10-19). Use the library ("declarative") mode only, no framework mode.

### Icons and fonts: lucide-react (pin at scaffold), @fontsource/ibm-plex-sans, @fontsource/ibm-plex-sans-condensed, @fontsource/ibm-plex-mono (pin at scaffold)
- Self-hosted fonts work offline. One line.

### Frontend tests: vitest 4.1.12 (unit), @playwright/test 1.64.1 (demo-journey e2e + screenshots)
- vitest 4.1.12 peer vite `^6 || ^7 || ^8` (checked). Verified npm 2026-11-07.

### Lint: eslint 10.13.0 + typescript-eslint 8.72.0; ruff 0.17.2 for Python

### Realtime transport: Server-Sent Events (FastAPI `StreamingResponse`, browser `EventSource`)
- Candidates: SSE, WebSocket, polling.
- Chosen because: one-way server-to-client stream of week states is exactly SSE; works through proxies; no extra library. Player actions in Beat the Desk go over normal POSTs.

### Hosting: frontend on Vercel (static), backend on Render (Docker web service, paid Starter so it does not sleep) or Fly.io; local docker compose for the live demo
- Candidates: Vercel + Render; Vercel + Fly.io; single VPS.
- Chosen because: static SPA on Vercel is free and fast; Render runs a Dockerfile with no config. The live finale demo runs from the laptop (no venue wifi dependency); the deployed URL is for judges in Round 2.
- Costs us: about $7/month for a non-sleeping backend (Render Starter; verify current price before buying). If not bought, the frontend falls back to cached runs with a visible badge.

### LLM: none in MVP. STRETCH "Ask Headroom" uses a small model through an OpenAI-compatible endpoint configured by env vars
- Why: numbers must be traceable; reasons are generated from engine numbers. If built, the model only translates a sentence into a shock or parameter change that the user confirms. Candidate cheap models (research-D, checked 2026-11): Claude Haiku 5.5 ($0.10/$0.50 per 1M tokens), Gemini 2.5 Flash-Lite ($0.10/$0.40).

## Compatibility matrix
| Pair | Status |
|---|---|
| react 19.3.1 / react-dom 19.3.1 | react-dom peer `^19.3.1` OK |
| vite 8.3.5 / @vitejs/plugin-react 6.1.2 | plugin peer `vite ^8.0.0` OK |
| vite 8.3.5 / vitest 4.1.12 | vitest peer `^6 or ^7 or ^8` OK |
| typescript 6.0.3 / typescript-eslint 8.72.0 | TS `<6.1.0` OK |
| deck.gl 9.4.0 / @deck.gl/react 9.4.0 | same minor required (`~9.4.0`) |
| deck.gl / react 19 | peer `react >=16.3` OK |
| tailwindcss 4.3.3 / @tailwindcss/vite 4.3.3 / vite 8 | same version pair; check plugin peer at scaffold |
| Python 3.12 / torch 2.14.1 CPU / chronos-forecasting 2.3.2 | resolved together by uv on 2026-11-07 (dry run) |
| numpy 2.5.4 / pandas 3.1.0 / pyarrow 26.0.0 / duckdb 1.5.6 | resolve together with uv; confirm at scaffold |

## Capability exploitation map
| Tool | Strongest capabilities | Used by | Deliberately not used |
|---|---|---|---|
| numpy | broadcasting over (cells, options, scenarios); float32 | value tables, allocation, Monte Carlo | numba/JIT (not needed after spike) |
| HiGHS | exact MIP | exact-gap test oracle | main engine (too slow at size) |
| Chronos-2 | zero-shot quantiles, known-future covariates, cross-series group attention | demand forecast with holiday/event/pressure/trends covariates | fine-tuning (no real data to justify it) |
| LightGBM | quantile objective, fast | baseline forecaster and comparison | classification uses |
| DuckDB | Parquet scans, window functions | Demand Lens queries, aggregates, plan/orders persistence | extensions (spatial, httpfs) |
| FastAPI | typed models, OpenAPI, StreamingResponse | all endpoints, SSE season stream, `/docs` shown to judges | background task queues |
| deck.gl | GPU layers, transitions, picking | ScatterplotLayer sparks, ArcLayer + TripsLayer flights, HeatmapLayer radar, GeoJsonLayer land, custom gauge via SolidPolygonLayer arcs | tile/basemap, 3D globe view (competitor has one) |
| D3 | scales, area/line shapes, quantile fan bands | fans, frontier, lanes, sparklines | d3-transition (motion handles animation) |
| motion | layout animations, springs | panel enter, card drop, count-ups | page-wide scroll effects |
| SSE | ordered one-way stream | season playback buffer | n/a |

## Judge-ready justifications
- Why decomposition instead of a MILP solver? "A joint stochastic MILP at our size, 1.2 million variables, did not solve in 60 seconds with HiGHS, even relaxed. Turning the budget and availability target into prices splits it into 1,170 small exact problems that numpy solves in about a second, and we check the gap against the exact MILP on a small instance in our tests."
- Why Chronos-2 and not Prophet or LSTM? "Chronos-2 forecasts quantiles zero-shot and takes known future covariates like Diwali dates and forward market pressure natively. We still backtest it against LightGBM quantile and seasonal naive and use whichever wins; both numbers are in the repo."
- Why deck.gl without a basemap? "We need thousands of animated particles, arcs and a heatmap at 60 fps, offline. deck.gl does all of that on the GPU; drawing land from a local TopoJSON removes any tile server from the demo."
- Why no LLM in decisions? "Procurement numbers have to be auditable. Every reason sentence is generated from engine outputs; an LLM would add cost and a way to be wrong."
- Why DuckDB? "Analytical queries over a few million rows, in-process, one file, no server to fail on stage."

## Locked stack (flat list)
Python 3.12.15 (uv 0.13.x), numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, pyarrow 26.0.0, duckdb 1.5.6, fastapi 0.162.0, uvicorn 0.54.0, pydantic 2.14.1, holidays 0.107, chronos-forecasting 2.3.2, torch 2.14.1 (CPU, pipeline group only), lightgbm 4.7.0, highspy 1.15.1 (dev), pytest 9.1.1 (dev), httpx 0.28.1 (dev), ruff 0.17.2 (dev).
Node 24 LTS, react 19.3.1, react-dom 19.3.1, vite 8.3.5, @vitejs/plugin-react 6.1.2, typescript 6.0.3, tailwindcss 4.3.3, @tailwindcss/vite 4.3.3, deck.gl 9.4.0 (+ @deck.gl/react, /layers, /geo-layers, /aggregation-layers 9.4.0), world-atlas 2.0.2, topojson-client 3.1.0, d3 7.9.0, motion 14.6.0, zustand 5.0.16, @tanstack/react-query 5.104.5, react-router 8.5.0, lucide-react (pin at scaffold), @fontsource IBM Plex Sans / Sans Condensed / Mono (pin at scaffold), vitest 4.1.12, @playwright/test 1.64.1, eslint 10.13.0, typescript-eslint 8.72.0.
Hosting: Vercel (web), Render or Fly.io (api, Docker), docker compose (local demo).

## Decision log
- 2026-11-07 Joint MILP rejected after spike; decomposition chosen.
- 2026-11-07 TypeScript 6.0.3 instead of 7.x for typescript-eslint compatibility.
- 2026-11-07 DuckDB 1.5.6 instead of 2.0.0 (too fresh).
- 2026-11-07 pytrends rejected (repository archived, last push 2024-08-10); Google Trends via manual CSV export committed to the repo.
- 2026-11-07 No 3D globe; 2D pressure map to look unlike the strongest competitor.

## Change-control rule
After lock, any stack change needs a new decision record in this file (same format, with the reason and the spike result) and the owner's approval. No "let me just try X" mid-build.
