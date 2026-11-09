# 07 Assets

Most visuals are data-driven and built in code. There are no stock photos. The few files below are the full list; anything not listed is deliberately none.

## Manifest
| id | screen / component | purpose | source | dims / aspect | format | path | prompt or search query | license | status |
|---|---|---|---|---|---|---|---|---|---|
| A01 | Map (all) | land outline | data: `world-atlas/land-50m.json` | vector | TopoJSON | npm package import | n/a | ISC (Natural Earth, public domain) | needed |
| A02 | Header | wordmark + glyph | procedural SVG in code: a horizontal bar "gauge" glyph (three stacked arcs in contract colours) next to "Headroom" in Plex Sans Condensed 600 | 24 px high | SVG component | `web/src/components/Logo.tsx` | n/a | ours | needed |
| A03 | Favicon | tab icon | same glyph | 32x32, 180x180 | SVG + PNG | `web/public/favicon.svg`, `apple-touch-icon.png` | n/a | ours | needed |
| A04 | Map | spark particle | procedural (ScatterplotLayer circle, radius 2 px, alpha fade) | n/a | code | `web/src/map/layers/sparks.ts` | n/a | ours | needed |
| A05 | Lanes | future fog hatch | procedural SVG pattern (45 degree, 1 px `--line`, 6 px spacing) | n/a | code | `web/src/charts/Lanes.tsx` | n/a | ours | needed |
| A06 | Theatre | shock card icons | Lucide `plane`, `music`, `cloud-fog`, `indian-rupee`, `building-2`, `plane-takeoff` | 16 px | React icons | lucide-react | n/a | ISC | needed |
| A07 | README / Round 1 slides | demo GIF | screen recording of the Theatre hero (week 0-12, shock) | 1280x720, 12 fps, at most 8 MB | GIF + MP4 | `docs/media/theatre.gif`, `docs/media/theatre.mp4` | record with OBS or ScreenToGif at 1920x1080 then scale | ours | needed |
| A08 | Round 1 slides (optional) | background for slide 1 | generated image, owner generates | 16:9, 1920x1080 | PNG | `docs/media/slide-bg-1.png` | see prompt P1 below | per tool terms | needed |
| A09 | Architecture diagram | README + slide 2 | export Mermaid from 04-architecture.md | 1600 px wide | SVG | `docs/media/architecture.svg` | `npx @mermaid-js/mermaid-cli` | ours | needed |

Status values: needed, placeholder, delivered, wired. Claude moves to placeholder and wired; the owner moves to delivered by dropping the file at its path.

## Prompt P1 (A08, optional, 2 variants)
Shared style suffix: "dark operations-room aesthetic, deep blue-black background #07090C, single warm accent of muted orange and red glow, fine grain, no text, no logos, no people, no glossy plastic look, no lens flare, documentary photo feel."
- Variant a: "Night view from high above a dense city by the sea, lights of hotel towers, a faint radar-like haze of orange over one district suggesting crowding, wide 16:9 composition with empty dark space on the left third for text, 35mm lens, long exposure." + suffix
- Variant b: "Abstract top-down view of an airport apron at night with a few aircraft and light trails forming arcs, soft orange haze around one gate area, generous negative space on the left for text, 16:9." + suffix
If no image tool is available, use a plain `--ink-0` slide with the Theatre screenshot instead. The product screenshot is stronger than any generated image.

## Done check
Every screen in 06-design-system.md has its slots resolved: map (A01, A04), header (A02), lanes (A05), shock cards (A06). All other screens: deliberately no imagery (charts are the visuals).
