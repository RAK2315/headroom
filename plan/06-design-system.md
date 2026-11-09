# 06 Design system

Builders: before building screens, run `/impeccable` with this file as input to refine tokens and motion. Keep the art direction and the rejected-look list; refine values, do not replace the concept.

## Art direction: "availability weather"
Headroom shows inventory pressure the way a weather radar shows rain: calm dark ground, a colour ramp that intensifies toward sold-out, motion that means something (sparks = lost searches, arcs = seats moving). It should feel like an operations room at an airline or a trading desk, not like a startup landing page.

References and what to take:
1. **Windy.com**: animated fields over a dark map, a single sequential colour ramp with a visible legend, thin type over data. Take: the pressure ramp and haze, legend placement bottom-left, restraint in chrome.
2. **Flightradar24**: live dark map, small bright moving objects, hover cards with dense facts. Take: arcs with moving dashes, compact tooltip cards, density.
3. **Bloomberg Terminal**: monospaced tabular numbers, columns of ledgers, amber-on-black emphasis, function-key-like controls. Take: the ledger panel, mono numerals everywhere numbers appear, tight 4 px grid.

Rejected default look (never ship these by accident): purple-to-blue gradients, glassmorphism cards, an untouched component kit, centred hero with blurred blobs, emoji icons, Inter for everything, drop-shadow-heavy cards, rounded "pill everything", a 3D globe (the strongest competitor uses one), generic KPI tiles with big icons.

## Tokens (`web/src/styles/tokens.css`)
### Colour (dark theme, default)
| Token | Hex | Role |
|---|---|---|
| `--ink-0` | #07090C | app background behind the map |
| `--ink-1` | #0D1117 | panels |
| `--ink-2` | #141A22 | raised rows, inputs |
| `--ink-3` | #1C2430 | hover, selected rows |
| `--line` | #253041 | hairlines, grid |
| `--land` | #10161E | land fill on the map |
| `--land-edge` | #2A3646 | coastlines |
| `--text-1` | #E7ECF2 | primary text |
| `--text-2` | #9BA8B7 | secondary text |
| `--text-3` | #5F6C7C | tertiary, axis labels |
| `--pressure-0` | #12324A | calm |
| `--pressure-1` | #1F6F8B | building |
| `--pressure-2` | #D8B44A | tight |
| `--pressure-3` | #EE7B33 | closing out |
| `--pressure-4` | #FF4D5E | sold out (also `--danger`) |
| `--danger` | #FF4D5E | sold-out searches, errors, losses. Reserved for state. |
| `--ok` | #5BD69A | target met, approved. Reserved for state. |
| `--warn` | #F2C14E | target at risk, assumptions. Reserved for state. |
| `--c-hard` | #C9A7FF | hard pre-buy / series block |
| `--c-allot` | #7FE3CF | allotment |
| `--c-free` | #8FB4FF | free sale |
| `--desk-headroom` | #D4F25A | Headroom (brand accent; the only lime in the app) |
| `--desk-profit` | #F2A7CB | profit-only optimiser |
| `--desk-playbook` | #8C99A8 | last year's playbook |
| `--desk-you` | #FFFFFF | the judge in Beat the Desk |
Light theme (STRETCH F30) mirrors roles with `--ink-*` light greys and darker ramps; define later.
Rules: status colours (`--danger`, `--ok`, `--warn`) never decorate. Contract colours appear only on contract chips, lab curves and gauge arcs. Desk colours appear only where a desk is identified.

### Type
- Families (self-hosted via @fontsource): `IBM Plex Sans Condensed` (labels, headings, nav), `IBM Plex Sans` (body copy), `IBM Plex Mono` (every number, ids, dates in tables). Numbers always `font-variant-numeric: tabular-nums`.
- Scale (px / line-height): 11/14 micro (axis ticks, badges), 12/16 small, 13/18 body, 15/20 emphasis, 18/24 panel title, 24/28 screen title, 40/44 ledger hero numbers, 64/68 result line number (Theatre end).
- Weights: 400 body, 500 labels, 600 titles. No italics except quotes of sources.
- Case: sentence case everywhere. No ALL-CAPS labels (the wordmark "Headroom" is sentence case too).

### Space, radius, lines, elevation
- 4 px base grid. Spacing tokens: 4, 8, 12, 16, 24, 32, 48.
- Radius: 2 px for inputs and chips, 4 px for panels, 0 for the map and ledger. No pills.
- Lines: 1 px `--line` hairlines separate panels; no card shadows. Elevation is shown by `--ink-2/3` steps only.

### Motion (motion 14)
- Durations: 120 ms (hover), 200 ms (controls), 300 ms (count-ups, chart transitions), 400 ms (shock card drop, panel enter), 1,500 ms per week at 1x playback.
- Easing: `cubic-bezier(0.2, 0.8, 0.2, 1)` for enters; linear for playback; spring (stiffness 300, damping 30) only for the shock card.
- Respect `prefers-reduced-motion`: sparks become a static count badge per destination, count-ups become instant, playback still advances.

## Layout shell
- Header (56 px): wordmark "Headroom" + glyph (left), context strip: season, budget, target, risk (click to edit in Plan Studio), the "Simulated, calibrated on public data" badge (warn colour outline, always visible), "Cached run" badge when applicable, role switcher (Contracting manager / Finance approver) right.
- Left nav (64 px collapsed, icons + tooltips; 200 px expanded on hover): Theatre, Plan Studio, Contract Lab, Suppliers, Demand Lens, Approvals, Proof. Lucide icons: `play-circle`, `sliders-horizontal`, `flask-conical`, `plug`, `activity`, `check-square`, `shield-check`.
- Main area: full-bleed panels separated by hairlines; no page scroll on the Theatre at 1920x1080; other screens scroll vertically.
- Minimum supported width 1366 px. Demo width 1920 px. Below 1366 show a "Best viewed on a laptop or larger" notice (no mobile layout).

## Component states (every main screen implements all)
| State | Look |
|---|---|
| Loading | skeleton bars in `--ink-2` with a 1.2 s shimmer; map shows land and hubs immediately |
| Empty | one sentence of what to do + one action button (e.g. "No orders yet. Submit a plan from Plan Studio.") |
| Error | `--danger` left rule, plain message from the API error, "Retry" and, where possible, "Use cached run" |
| Stale | when params changed but re-solve is pending: numbers dim to `--text-3` with a "Re-solving..." label |
| Partial | Demand Lens for cities without Airbnb data: "No public forward data for this city; using events and Trends" |
| Offline / API down | header badge "Cached run", Theatre plays cached JSON, Plan Studio shows the cached default plan and disables controls with a tooltip |
| Infeasible target | Plan Studio banner `--warn`: "Best achievable 91.8%. Needs ₹6.1 Cr more." |

## Accessibility
- Contrast: text at least 4.5:1 against its panel (check `--text-2` on `--ink-1`), large numbers at least 3:1.
- Never colour alone: contract chips carry text (HARD, ALLOT, FREE are the only uppercase-like labels; write them as "Hard", "Allot", "Free" to respect sentence case); desks carry names; pressure has a legend with numbers; sold-out sparks also counted in the ledger.
- Keyboard: Space = play/pause, Right arrow = step a week, 1/2/4 = speed, P = play as me, Tab order through controls; sliders operable with arrows (1 step) and Shift+arrows (10 steps).
- Focus ring: 2 px `--desk-headroom` outline offset 2 px.

## Screen inventory (maps to 03-features.md)
| Screen | Route | Features |
|---|---|---|
| Season Theatre | `/theatre` (default) | F13, F14, F22, F23, F24 |
| Plan Studio | `/plan` | F15, F21 (supplier summary) |
| Contract Lab | `/lab` | F16 |
| Suppliers | `/suppliers` | F21 |
| Demand Lens | `/demand` | F17 |
| Approvals | `/approvals` | F18 |
| Proof | `/proof` | F19 |

## Correct render per screen (check in Chrome at 1920x1080 and 1366x768, console clean)
### Season Theatre
- Visible without scroll: header, map (land outline, 3 hubs labelled DEL BOM BLR, 10 destination gauges labelled with 3-letter codes), ledger with 3 desk columns and 6 metric rows, lanes strip with 10 rows and 26 columns, controls row.
- Before play: lanes show forecast pressure (hatched), ledger shows zeros and "Ready", play button focused.
- During play: playhead moves one column per week; sparks appear only at destinations with sold-out searches for the selected desk; arcs animate; ledger counts up.
- Shock: card visible above lanes at its week, playback paused 2 s, diff card in the ledger under the Headroom column.
- End: result line with numbers matching the ledger; Replay and "Open plan" buttons.
- Clickable: desk chips, gauges (tooltip), lane cells (drill-down), all controls.
### Plan Studio
- Visible: controls column (360 px), summary strip (8 stats, solve ms), frontier chart (12 points + current marker), buy list (grouped, contract chips, reasons truncated to 2 lines with expand).
- Changing budget shows "Re-solving..." then new numbers in under 3 s; banner appears only when infeasible.
### Contract Lab
- Visible: cell picker, demand fan, payoff chart with 3 curves and bands, sold-out probability chart, sliders, readouts, assumptions panel with "assumption" tags, "Snap to Headroom's mix".
- Dragging a slider updates readouts every frame without network calls.
### Suppliers
- Visible: 6 supplier rows with cost, live week, cells covered, value bar (positive in `--ok`, negative in `--text-3`), toggle; mini map highlighting covered destinations; delta summary.
### Demand Lens
- Visible: picker, main chart with bookings line, unconstrained demand line, shaded sold-out gap, forecast fan for W26, event markers; signals panel; provenance list with 5 sources; backtest badge; "Play the season" button.
### Approvals
- Visible: role switcher state, orders table with state chips, filters, totals row, action buttons allowed for the role only, export button, audit drawer.
### Proof
- Visible: distribution strips per desk (500 dots each, jittered) for peak sold-out rate and profit, win-rate table, forecast backtest table, exact-gap badge, timings.
