# Headroom

Inventory procurement planner for TBO VoyageHack 4.0 (PS: Inventory Optimization). The demo must show the Season Theatre: three buying desks race the same season on the same budget, a shock lands at week 9, Headroom re-plans in under a second, and ends with far fewer sold-out agent searches.

Status: plan pack written, nothing built yet. Next: Phase 0 in plan/08-build-plan.md. Updated 2026-11-07.

## Read first
brief.md, CONTEXT.md (vocabulary), plan/00-overview.md, plan/01-hero.md, plan/08-build-plan.md (what to do now). Engine maths: plan/11-engine-spec.md. Data: plan/10-data-pipeline.md. Contracts and layout: plan/04-architecture.md. Spike code to port: plan/spikes/decomp_spike.py.

## Stack (locked, see plan/02-stack.md; changes need a decision record and owner approval)
Python 3.12.15 via uv, numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, pyarrow 26.0.0, duckdb 1.5.6, fastapi 0.162.0, uvicorn 0.54.0, pydantic 2.14.1, holidays 0.107, chronos-forecasting 2.3.2 + torch 2.14.1 CPU (pipeline group only), lightgbm 4.7.0, highspy 1.15.1 (dev), pytest 9.1.1, httpx 0.28.1, ruff 0.17.2.
Node 24, react 19.3.1, vite 8.3.5, @vitejs/plugin-react 6.1.2, typescript 6.0.3, tailwindcss 4.3.3, deck.gl 9.4.0, world-atlas 2.0.2, topojson-client 3.1.0, d3 7.9.0, motion 14.6.0, zustand 5.0.16, @tanstack/react-query 5.104.5, react-router 8.5.0, vitest 4.1.12, @playwright/test 1.64.1, eslint 10.13.0, typescript-eslint 8.72.0.

## Commands (create these in Phase 0; keep this list exact)
- install: `uv sync --all-groups` and `npm --prefix web ci`
- pipeline: `uv run python -m pipeline all` (steps: reference, signals, world, demand, forecast, proof, cache-demo)
- api dev: `uv run uvicorn api.main:app --reload --port 8000`
- web dev: `npm --prefix web run dev` (http://localhost:5173)
- test: `uv run pytest -m "not slow"` and `npm --prefix web run test`
- perf: `uv run pytest -m slow`
- e2e: `npm --prefix web run e2e`
- typecheck: `npm --prefix web run typecheck`
- lint: `uv run ruff check .` and `npm --prefix web run lint`
- types from API: `npx openapi-typescript http://localhost:8000/openapi.json -o web/src/api/types.gen.ts`
- demo offline: `docker compose up` (or set `VITE_FORCE_CACHED=1`)

## Scope cut line
In: the seven screens (Season Theatre, Plan Studio, Contract Lab, Suppliers, Demand Lens, Approvals, Proof), the data pipeline, forecast, optimiser, simulator, baselines, Beat the Desk. Out: real TBO integration, accounts/SSO, multi-tenant, mobile, LLM in the decision path, live external APIs at demo time, transfers/sightseeing/cruise.

## Protected (never cut without asking the owner)
- USP: Headroom is the only inventory planner that optimises availability (sold-out agent searches) as a first-class target by choosing the contract type per pool-week (hard pre-buy, allotment with release cut-off, or free sale), the supplier to integrate and the markup, under a budget and a risk limit, and re-plans every week as the season unfolds, grounded in real public demand signals.
- Hero moment: At 0:20 of the demo the Season Theatre plays the 2026-27 winter season week by week. Three desks run the same budget on the same hidden season: Last year's playbook, a profit-only optimiser, and Headroom. At week 9 a shock card drops; Headroom re-plans in under a second and shows the diff; the ledger ends with sold-out searches, profit and peak capital for each desk.
- Showpiece: Contract-aware, availability-constrained, risk-adjusted procurement over 1,170 pool-weeks and 128-256 correlated demand scenarios, solved by Lagrangian decomposition, with weekly re-planning that stays ahead of a 1.5 s/week playback.

## Writing rules
Apply to code comments, docs, commit messages, PR descriptions, and user-facing copy.
- Never use em dashes. Use a comma, a colon, parentheses, or a plain hyphen.
- No ALL-CAPS in user-facing text or UI labels. Sentence case, always.
- No emoji unless asked.
- Plain, direct language. No marketing voice, no "seamlessly", no "delve into", no "it's not just X, it's Y".
- Comments explain why, not what. Match the density of the surrounding code. Don't narrate obvious lines.
- Keep comments to one line. If it needs a paragraph, the code is wrong or it belongs in a doc. No banner blocks, no ASCII dividers, no boxed headers.
- No decorative symbols in comments or copy: no backticks, tildes, arrows, asterisks, or box-drawing characters.
- Every simulated number in the UI carries the "Simulated, calibrated on public data" context. Supplier and shock names stay fictional.

## Code style
- Simple and boring over clever. No abstraction until needed twice. No config systems, plugin layers, or premature generality.
- Seams (plan/04-architecture.md section 5): only `api/store.py` touches DuckDB and artefact files; `engine/` is pure numpy (no pandas, DuckDB or FastAPI) and never sees truth arrays when planning; `engine/recourse.py` is the only outcome calculator and `web/src/lib/lab-eval.ts` is its tested port; routes validate, call and persist, nothing more; reasons and diff lines come from `engine/reasons.py` templates, never an LLM; the web never computes plans.
- TDD on core logic only: `engine/recourse.py`, `tables.py`, `allocate.py`, `scenarios.py`, `metrics.py`, `suppliers.py`, `simulate.py`, `api/orders.py` state machine, `pipeline/uncensor.py`, `web/src/lib/lab-eval.ts`. Tests before implementation. Not on glue, UI or throwaway code.
- Determinism: every random draw goes through a seeded `numpy.random.Generator`; same inputs, same numbers.
- Money is integer rupees in JSON; format with `web/src/lib/format.ts` (₹ Cr, ₹ L, Indian digit grouping).
- Typecheck and test as you go.
- Visuals follow plan/06-design-system.md; assets follow plan/07-assets.md. Never ship a framework-default look.

## Build mindset
Build the best version of every feature. Think about what makes it more impressive, faster and clearer, not about what could go wrong. Plan numbers are floors, not ceilings. When a feature works, take the next upgrade from plan/09-push-further.md. Use every tool to its full capability.

## Build rules
- MVP-first: something demoable at every point. The hero moment is real by phase 2.
- Phase done means: verification passes, status above updated, committed.
- Explicit user requests are decisions: state the cost in one line, then build.
- Features moved later go in the parked list in plan/08-build-plan.md.
- Never invent a requirement. If guessing, say so.
- Never tune the truth generator or baselines to make Headroom look better. Parameter changes go in data/reports/calibration.md with a reason.
- UI: never claim it works without opening it (Chrome, or Playwright when Chrome is off). Check loading, empty and error states, and 1920x1080 plus 1366x768.
- Commit messages: `F07: allocate bisection with warm start` style (feature id first). End with the attribution lines the session provides.

## Skills - when to reach for what
Reach for these yourself when the moment matches; don't wait to be told. If you're about to do something a skill covers, use the skill instead of improvising it.

Planning:
  /prototype        spike the riskiest unknown BEFORE committing to it (phase 2 re-plan spike)
  /research         any API or SDK I haven't used before; hits primary sources (deck.gl TripsLayer/HeatmapLayer, Chronos-2 predict_df, FastAPI SSE)
  /domain-modeling  new vocabulary goes into CONTEXT.md first
  /codebase-design  choosing module seams
  /grill-me         when a requirement is unclear and the owner is available

Building:
  /tdd              the verifiable core only - recourse, tables, allocation, scenarios, simulator, order state machine, lab-eval.
                    Never on glue, UI, or throwaway code.
  /diagnose         the moment something breaks - reproduce, minimise, fix.
                    Not shotgun debugging.
  /verify-this      when I need evidence something works, not your summary
  /impeccable       design pass on screens (phase 5) and token refinement
  /handoff          before context gets tight, not after

Before the demo, in this order:
  1. /deslop
        Strips the AI residue: pointless comments, defensive try/catch on
        trusted paths, `any` casts that only silence the compiler. Fast, safe,
        run it any time after a big generated chunk.
  2. /simplify then /code-review
        Final pass.

## Context and sessions
- One task per session. Run /context before anything big; past ~40%, say so and suggest a fresh session.
- If auto-compact happens mid-task, that session is over. Say so.
- Before every /handoff: say what we figured out this session that isn't written down, then write it down (a line here, a note in plan/, or a comment where the surprise lives). Then commit.
- No research tangents. If files or sources are named, use those.
- Plan in Opus. Once the plan is locked and the work is mechanical, suggest switching to Sonnet.
- Two parallel sessions in phase 1-2: `claude -w engine` (engine, pipeline, api) and `claude -w web` (web). Merge often; regenerate API types after every API change.
