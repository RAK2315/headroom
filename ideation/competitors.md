# VoyageHack 4.0 public competitor repos (checked 2026-11-07)

Public repos are a small, early sample; most teams keep repos private until Round 2.

## PS2 Multi-Supplier Optimization (4 visible)
| Repo | What it has | Gaps (from its own README/ROADMAP) |
|---|---|---|
| [RaktimChandra/trueshelf](https://github.com/RaktimChandra/trueshelf) | Hotel ER (gradient boosting, 23 signals, leave-one-city-out F1 0.99+), room grammar F1 0.996, sightseeing "experience atoms", like-for-like ₹ price, ShelfRank, Review Desk, Bayesian supplier reliability, 36 tests, proof page | Synthetic data only; no image dedup/enrichment; no non-Latin scripts; ranking fixed weights (not learned); no sightseeing ranking; unseen room style recall 49%; availability signal partial; conversion not measured |
| [swarnnim/trustscore-hotels](https://github.com/swarnnim/trustscore-hotels) | Merge + room taxonomy + TrustScore with reasons; stdlib Python; 41 synthetic records | Toy scale, hotels only |
| akashhhh254/voyageiq | "duplicate hotels, room mapping, consolidation, explainable value ranking" (description only) | unknown |
| [Nishkarsh5108/voyage-4.0](https://github.com/Nishkarsh5108/voyage-4.0) | Deep research only so far: typed graph SAME_AS / VARIANT_OF / INCLUDES, room vs rate disentanglement, debiased ranking, real public datasets (Foursquare, Overture, OSM, Wikidata, Trivago RecSys 2019, Expedia 2013, Hotels-50K) | No code yet; plans to "consume Vervotech, win on sightseeing, offers, ranking" |

## PS1 Inventory Optimization (1 visible)
| Repo | What it has | Gaps |
|---|---|---|
| [shanshantanusingh113-max/allotment-atlas](https://github.com/shanshantanusingh113-max/allotment-atlas) | Synthetic 28 destinations; quantile GBM forecast + conformal bands (WAPE 9%); newsvendor sizing; buy-timing; exact grouped-knapsack DP on E[profit] − λ·SD; 10k correlated Monte Carlo seasons; shocks; 3D demand globe; NL commands ("cut 3 crore"); season replay vs simple rule; scenario compare; 59 tests; live GitHub Pages | Synthetic only; objective is profit, not **availability** (the PS headline); treats inventory as units, not **contracts with release clauses**; no **supplier-integration** lever (explicit in PS); no in-season **recourse** (release / top-up as the season unfolds); sell-outs measured per block, not across suppliers |

## Other 4.0 repos (other PS)
- arshsri0513/TBO-VoyAgent-AI (Virtual Travel Agent, includes disruption sentinel)
- shriza1991/RouteWatch (Security)
- tester248/TBO-FlightRiskRadar (flight risk, TBO Air API)
- Kaushik9560/Tbo-Hackathon-round-2 (MERN trip planner using TBO Hotel/Air APIs)

## Event facts confirmed from competitor research
- Round 1 window 26 Oct - **20 Nov 2026**: 2 content slides + video in a zip.
- Judging: impact, feasibility, innovation, adoption risk, then prototype quality and alignment with objectives.
- No data provided for either PS.
