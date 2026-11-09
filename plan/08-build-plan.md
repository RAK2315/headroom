# 08 Build plan

Read 00, 01, 04 and 11 before starting. Work in phases. Each phase ends demoable, verified and committed, and the status line in CLAUDE.md is updated.

## Calendar (hard dates)
| Date | What | Owner |
|---|---|---|
| **by 12 Nov 2026 23:59** | Register the team on Unstop (2 members). Without this nothing else matters. | owner |
| 14 Nov 17:30-18:30 | Mandatory briefing webinar. Ask: is any TBO data or API access provided for Inventory Optimization? Slide template and video length for Round 1? Note answers in `brief.md` open questions. | both |
| **20 Nov** | Round 1 deadline: 2 content slides + video, zipped (target: submit 19 Nov). Content in `12-round1-and-demo.md`. | builder + owner |
| 26 Nov - 24 Dec | Prototype round (target: submit 22 Dec). GitHub repo + README + workflow video (+ 10-slide deck per past editions). | both |
| 8 Jan 2027 | Finale, live demo + Q&A. | both |

## Phases

### Phase 0: skeleton (8-9 Nov, about 6 h)
Build:
- Repo layout exactly as 04-architecture.md section 5. The repo already exists (github.com/RAK2315/headroom, private) with a `.gitignore` covering data/raw, data/artefacts except truth_42, data/headroom.duckdb, node_modules, .venv and dist. Clone it and work on `main`.
- `pyproject.toml` with dependency groups `api` (fastapi, uvicorn, pydantic, duckdb, numpy, scipy), `pipeline` (pandas, pyarrow, holidays, chronos-forecasting, torch CPU, lightgbm), `dev` (pytest, httpx, ruff, highspy). `uv lock`. Use the versions in 02-stack.md.
- Web: `npm create vite@latest web -- --template react-ts`, then pin versions from 02-stack.md, Tailwind v4 via `@tailwindcss/vite`, tokens.css, fonts, router with 7 placeholder screens, Shell/Header/Nav (F12).
- `data/reference/*.yaml` with the seed data from 05-data-model.md; `pipeline reference` step loading `plan/schema.sql` and YAML into DuckDB (F01).
- CI: GitHub Actions running `ruff check`, `pytest -m "not slow"`, `npm run lint`, `npm run typecheck`, `npm run test`.
Done when: `uv run pytest` green (reference tests), `npm run dev` shows the shell with 7 routes and the dark tokens, CI green on the first push.
Verify: Playwright smoke `tests/e2e/shell.spec.ts` visits 7 routes, asserts no console errors.

### Phase 1: real engine on real-shaped data (9-12 Nov, about 16 h)
Two streams in parallel (two Claude Code sessions, separate worktrees: `claude -w engine`, `claude -w web`).
Stream A (engine + data):
1. TDD `engine/recourse.py`, `tables.py`, `allocate.py`, `metrics.py`, `scenarios.py` per 11-engine-spec.md sections 3-6, 9 (tests first, list in section 12). Start by porting `plan/spikes/decomp_spike.py`.
2. `test_exact_gap.py` with highspy.
3. Pipeline `signals` (S1-S5; do the manual downloads: Trends CSVs, Kaggle fares, Hotel Booking Demand CSV) and `world` and `demand` (F02-F04). Calibration report.
4. Forecast with seasonal naive + LightGBM first (fast); Chronos-2 is phase 3 unless time allows (F05 partially).
5. API: health, meta, plans, frontier (F08) with the table LRU cache.
Stream B (web, against mocks that match `web/src/api/types.ts`):
1. Plan Studio UI (F15) wired to the real API as soon as `POST /api/plans` exists.
2. Start the pressure map (F13) with mock week states: land, hubs, gauges, arcs.
Done when: Plan Studio, on pipeline data, re-solves on budget change in under 3 s and shows buy lines with contract chips and reasons; `test_exact_gap` passes; `test_perf.py` plan at most 2.5 s.
Verify: `uv run pytest`, `uv run pytest -m slow -k perf`, `npm run typecheck && npm run test`, open `/plan` in Chrome, drag budget from ₹40 Cr to ₹20 Cr and back, confirm the infeasible banner appears at ₹20 Cr (or tune defaults so it does), console clean.
Integration point: the TS types must match pydantic. Generate TS types from FastAPI's OpenAPI (`npx openapi-typescript http://localhost:8000/openapi.json -o web/src/api/types.gen.ts`) and re-export; do not hand-edit drifted types.

### Phase 2: the hero, real (12-17 Nov, about 20 h)
1. Fast re-plan first (2 h): build hull allocation (11-engine-spec.md section 5) and the in-season re-plan on remaining cells at S=64, G=10. Target under 0.6 s, aim for 0.3 s.
2. Baselines (F09), simulator (F10) with Bayesian update, shocks, releases, diff lines; tests.
3. SSE stream + sim registry + `cache-demo` step (F11).
4. Theatre: map layers (sparks, arcs + trips, haze, gauges), ledger with count-ups, lanes, controls, shock card, diff card, result line (F13, F14). Playback buffer and "Re-planning..." state.
5. Cached mode (`VITE_FORCE_CACHED=1`) and the "Cached run" badge.
Done when: from a cold start, clicking Play on `/theatre` plays the default hero run end to end in 39 s at 1x with the shock at week 9, the diff card within 1 s, and the result line; the same works with the API stopped (cached).
Verify: `test_simulate.py`, perf test for re-plan; Chrome performance recording during playback (60 fps target, at most 5% frames over 20 ms); Playwright `demo-journey.spec.ts` step 2 (asserts result line text and that the diff card appears); watch the full run once at 1920x1080 and once at 1366x768.

### Round 1 package (17-19 Nov, about 8 h)
- If time: Chronos-2 forecast + backtest swap-in (F05 complete), else state "naive + LightGBM; Chronos-2 in Round 2" honestly.
- Record the video and build the 2 slides per `12-round1-and-demo.md`. Submit on 19 Nov.

### Phase 3: depth (26 Nov - 4 Dec, about 20 h)
- Contract Lab (F16) including `lab-eval.ts` port of recourse with fixture tests exported from Python.
- Demand Lens + provenance (F17).
- Chronos-2 forecast + backtest + copula estimation (F05 complete) if not done.
- Supplier lever screen (F21).
- Proof pipeline + Proof page (F19).
Done when: demo journey steps 1, 3, 4, 5 and 7 (Proof part) work on live data.
Verify: unit tests, `lab-eval` fixture parity test, Playwright journey steps, Chrome check of each screen's correct render.

### Phase 4: adoption and play (5-12 Dec, about 16 h)
- Approvals + audit + CSV export (F18) with state machine tests.
- Beat the Desk (F22), shock picker (F23), lane drill-down (F24).
Done when: the full 7-step demo journey runs in 4:30 without touching code.
Verify: full Playwright journey; manual run-through with a timer.

### Phase 5: polish, deploy, Round 2 submission (13-22 Dec, about 20 h)
- `/impeccable` design pass on every screen; states (loading, empty, error, stale, partial, offline) everywhere.
- Deploy (F25): Vercel + Render/Fly; environment variables; cached mode verified on the deployed URL.
- README (F20): problem, GIF, run steps (uv + npm, and docker compose), demo script, PS objective checklist, assumptions, provenance and licences, AI tools used, architecture diagram.
- Quality sequence: /deslop, then /simplify, then /code-review (high). The thermo-nuclear review skill is not installed on this machine; skip it.
- Record the Round 2 workflow video (5-7 min) and the 10-slide deck if required.
Done when: a fresh clone on another machine runs with README commands; deployed URL works; video uploaded; submitted by 22 Dec.

### Phase 6: finale prep (26 Dec - 7 Jan)
- Upgrades from 09-push-further.md and STRETCH features: F29 sensitivity tornado (strong for Q&A), F26 Ask Headroom, F27 BYO data, F30 light theme, presenter mode.
- Demo kit: laptop with docker images pulled, cached runs, a screen recording of the hero, HDMI adapter.
- Rehearse the 4:30 script 5 times; prepare answers in `12-round1-and-demo.md` Q&A.

## Task ownership
- Week 1 (owner busy): the teammate builds Phases 0-2 with Claude Code, two sessions in parallel worktrees (engine/data and web).
- From 17 Nov: owner joins; suggested split: owner takes web (Theatre polish, Lab, Approvals), teammate keeps engine/pipeline/API and Proof.
- Integration points (keep these in sync): (1) OpenAPI-generated TS types, regenerate after every API change; (2) SSE event shape in 04-architecture.md, mocks must match it; (3) `recourse.py` vs `lab-eval.ts` fixtures.

## Decisions made (override if you disagree)
- PS: Inventory Optimization, product name "Headroom". Reason: one visible competitor vs four on Multi-Supplier; large uncovered space in the PS text.
- Decomposition engine instead of a MILP. Reason: spike, the MILP does not solve at size.
- 10 destinations, 3 hotel tiers, 15 flight routes, 26 weekly buckets. Reason: covers TBO-relevant outbound markets and matches the spike size.
- Calibrated synthetic data from 5 real public sources. Reason: no TBO data; provenance makes it credible.
- 2D pressure map, dark theme, no globe. Reason: differentiation and projector legibility (light theme is STRETCH backup).
- No LLM in MVP. Reason: auditability; cost; not needed for the hero.
- Default budget ₹40 Cr and target 95% on peak cells. Tune after the first pipeline run so that ₹40 Cr meets 95% with a positive capital price and ₹20 Cr does not (so the infeasible banner is demonstrable). Record final defaults here.
- Plan date 21 Sep 2026 for W26.
- Demo roles via a header switcher, no login.
- Supplier and shock names are fictional. Reason: never impersonate real companies.

## Later (after the finale)
- Real TBO data adapter: waiting on the webinar answer.
- Multi-season planning (summer): one season proves the method.
- Room-level or hotel-level decisions: pools keep the problem readable and fast.
- Overbooking/oversell strategy: adds complexity without new demo value.
- Currency risk on foreign-currency contracts: mention in Q&A only.

## Parked list (features moved later during the build; bring them back when there is time)
- (empty)

## When a phase finishes early
Pick the next upgrade from 09-push-further.md for the area just built, then move on.
