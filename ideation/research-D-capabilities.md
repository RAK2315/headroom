# Research D — Capability scan (late 2025 → Nov 2026)

**For:** TBO VoyageHack 4.0 team · **Scan date:** 2026-11-07 · **Method:** ~45 web searches and fetches. Every claim has a URL. A claim that comes only from a secondary or aggregator source is marked **(secondary)**. Anything without a source is marked **assumption**.

**PS key:** PS1 = inventory pre-buy / demand forecasting · PS2 = multi-supplier dedup, room mapping, content enrichment, ranking · PS3 = agentic virtual travel agent and disruption rebooking · PS4 = AI ops ticketing for B2B support · PS5 = agent-first HR platform with guardrails and cheap model routing.

**Difficulty scale (2–4 week student prototype):** 🟢 a day or less · 🟡 a few days · 🔴 a week or more, or gated access.

---

## 0. Things that changed and could catch a team out

| Fact | Source | Implication |
|---|---|---|
| **Amadeus Self-Service APIs are gone.** Amadeus confirmed the decommission in Feb 2026, and all self-service keys were disabled on **17 Jul 2026**. The Enterprise portal is unaffected. | AirLabs, a vendor with a stake in alternatives (secondary): https://airlabs.co/amadeus-self-service-api-shutdown ; PhocusWire: https://www.phocuswire.com/amadeus-shut-down-self-service-apis-portal-developers ; https://ignav.com/docs/amadeus-self-service-shutdown | Many old tutorials and student repos depend on Amadeus test keys, and those keys now fail. Use Duffel, LiteAPI or Hotelbeds instead (§3). |
| **Amadeus × Anthropic (3 Sep 2026):** Amadeus is building a toolkit that brings its connectivity, docs, auth and content into AI dev environments (Claude Code), plus a Claude Cowork plug-in. The coverage does not call it an MCP server. | https://globetrender.com/2026/09/03/amadeus-and-anthropic-collaborate-on-ai-agents-for-travel/ ; https://www.travolution.com/news/technology/amadeus-pairs-up-with-anthropic-for-developers-access-to-content/ | Good pitch line ("GDSs are going agent-native"). It is not usable for a demo. |
| **ChatGPT Instant Checkout (ACP) was pulled back.** OpenAI is moving checkout into apps, and one secondary source says it was discontinued around Mar 2026. Booking.com and Expedia ChatGPT apps (launched with the Apps SDK, 6 Oct 2025) still hand off to the partner site to book. | Skift: https://skift.com/?p=806691 ; https://www.hospitality.today/article/chatgpt-opens-to-third-party-apps-and-travel-brands-are-first-in-line ; https://www.businesstoday.in/technology/news/story/openai-brings-bookingcom-spotify-canva-and-more-into-chatgpt-with-new-in-app-experiences-497031-2025-10-07 | Consumer chat apps don't own the transaction. A B2B agent tool with real booking, servicing and rebooking, which is TBO's position, is the gap. |
| **Google UCP (Universal Commerce Protocol)** is expanding into hotel booking, with partners Amadeus, Booking.com, Expedia, Hilton, IHG, Marriott, Trip.com and Wyndham. AP2 can act as its payment layer. | AltexSoft, 3 Nov 2026: https://www.altexsoft.com/blog/ai-agentic-commerce-travel/ | Mentioning UCP/AP2 compatibility makes PS3 look current. |
| **TBO itself:** the public page markets "integration-ready APIs" with real-time pricing, links a PDF doc (`img/TBO_API.pdf`), and has a "Register Now" call to action. **No public sandbox and no MCP server were found.** | https://www.tbo.com/tbo-api | **Assumption:** organisers will give hackathon credentials. Ask for them on day 1. A "TBO MCP server" wrapper is a credible, novel deliverable. |

---

## 1. Time-series foundation models (PS1)

| Item | What / version / date | Why it matters | Difficulty |
|---|---|---|---|
| **Chronos-2** (Amazon) | 120M encoder-only model. Zero-shot univariate, multivariate **and covariate-informed** forecasting (past-only or known-future, real or categorical) via in-context group attention. Arxiv 2510.15821, Oct 2025. Install with `pip install "chronos-forecasting>=2.0"`. Covers no static covariates (secondary). | Forecast demand per destination × hotel using known-future covariates such as holidays, events, fare and promo calendars, with **quantile outputs** for risk-aware pre-buy. A single retail case study cut WMAPE from about 56% to about 33% with covariates (anecdotal, secondary). | 🟢 |
| | Sources: https://arxiv.org/html/2510.15821v1 ; https://www.amazon.science/blog/introducing-chronos-2-from-univariate-to-universal-forecasting ; https://huggingface.co/amazon/chronos-2 ; https://aihorizonforecast.substack.com/p/chronos-2-multivariate-zero-shot | | |
| **TimesFM 2.5 / 3.0** (Google) | 2.5 released 15 Sep 2025: 200M parameters, 16k context, continuous quantile head up to a 1k horizon. XReg covariates were restored on 29 Oct 2025. **3.0 (Aug 2026)** adds native multivariate forecasting and past and future covariates, and claims #1 on fev-bench, TIME and GIFT-Eval. **Downloaded 3.0 weights are non-commercial only.** Commercial use goes through BigQuery ML (Sep 2026). Fine-tuning (LoRA) example added Apr 2026. | Strong alternative. Use 2.5 locally, or `AI.FORECAST` in BigQuery for a "no-ML-infra" story. | 🟢 for 2.5; 🟡 for 3.0 on BigQuery |
| | Source: https://github.com/google-research/timesfm (README update log) | | |
| **Toto 2.0** (Datadog) | Open weights from about 4M to 2.5B parameters, **Apache 2.0**, on Hugging Face (`Datadog/Toto-2.0-*`). Arxiv 2605.20119, May 2026. Claims SOTA on GIFT-Eval, BOOM and TIME (self-reported). Trained on observability metrics and synthetic data. | Fits PS4 best: forecast ticket volume and API error rates, and detect anomalies in booking-failure metrics. Usable for PS1 too. | 🟢–🟡 |
| | Sources: https://arxiv.org/html/2605.20119 ; https://datadoghq.com/blog/ai/toto-2/ ; https://huggingface.co/Datadog/Toto-2.0-2.5B | | |
| **Moirai 2.0** (Salesforce) | Decoder-only quantile model, Nov 2025. Ranks 5th of 37 foundation models on GIFT-Eval. The small checkpoint is about 11M parameters (secondary). | Light enough for CPU inference in a demo. | 🟢 |
| | Source: https://arxiv.org/html/2511.11698v2 | | |
| **TiRex** (NX-AI) | xLSTM-based zero-shot forecaster, described as top of GIFT-Eval in late 2025. Its standing after Toto 2.0 and TimesFM 3.0 is unclear. | Option for a comparison table only. | 🟢 |
| | Source: https://nx-ai.github.io/tirex/benchmarks | | |

**Takeaway for PS1:** a zero-shot probabilistic forecast (P10/P50/P90) per hotel-night feeds a stochastic pre-buy optimiser (§2). Students typically use Prophet or ARIMA, so this is a clear differentiator. Ship a **backtest chart against seasonal naive** to prove the lift.

---

## 2. Optimisation and revenue management (PS1)

| Item | Detail | Difficulty |
|---|---|---|
| **revmng / revmng-mcp** (arikanatakan, GitHub, updated Jun 2026) | Python RM library covering seat protection (Littlewood, EMSR, exact DP), overbooking, pricing, group displacement, **length-of-stay** and **network bid prices**, validated against published worked examples. An **MCP server** exposes these as agent tools. Small project with 2–3 stars, so vet it before relying on it. https://github.com/arikanatakan/revmng , https://github.com/arikanatakan/revmng-mcp , listed at https://github.com/topics/emsr | 🟢 |
| **RevPy** (flix-tech) | Older EMSRb and LP bid-price reference implementation, v0.1.1. https://github.com/flix-tech/RevPy (forks: https://github.com/sash-ko/RevPy) | 🟢 |
| **hotel-revenue-management-engine** (Sep 2026) | EMSR-b, an XGBoost cancellation model (AUC 0.84) and a Streamlit dashboard. A useful reference for "pre-buy minus expected cancellations". https://github.com/jdautell/hotel-revenue-management-engine | 🟢 |
| **LLM + solver pattern (OptiMUS, ICML 2024)** | Manager, Formulator, Programmer and Evaluator agents turn natural-language constraints into a MILP. Code: https://github.com/teshnizi/OptiMUS ; paper: https://proceedings.mlr.press/v235/ahmaditeshnizi24a.html | 🟡 |
| OR-Tools / HiGHS / CVXPY | Established solvers, with no news found in this window (**assumption:** stable and pip-installable). Suggested model: a scenario-based (sample-average approximation) two-stage stochastic program. Choose room-night quantities before demand is known using Chronos-2 quantile samples as scenarios, with recourse = sell at a markdown or release unsold rooms at the allotment cutoff. | 🟡 |

---

## 3. Travel APIs usable for a demo (PS2, PS3)

| API | Status (date) | Free/sandbox? | Use | Difficulty |
|---|---|---|---|---|
| **Duffel** (flights) | Test mode with `duffel_test_` tokens and **Duffel Airways (ZZ)** test airline: search, seat maps, ancillaries, order, **cancel with refund, change to alternative flights**. Test cards cover 3DS and insufficient funds. Webhook `order.airline_initiated_change_detected` with at-least-once delivery, 72h retries and `idempotency_key` (no documented way found to *trigger* it in test). | Yes, free (docs). | **Best PS3 disruption demo backbone:** book on ZZ, simulate a schedule change in your own layer, rebook with the order-change API. | 🟢 |
| | https://duffel.com/docs/api/overview/test-mode ; https://duffel.com/docs/api/webhooks/schema ; https://hookdeck.com/webhooks/platforms/guide-to-duffel-webhooks-features-and-best-practices.md | | | |
| **LiteAPI (Nuitee)** (hotels) | Sandbox mirrors production. The docs publish an example `sand_` key. **Official MCP server** (hosted docs MCP, plus an OSS Next.js MCP generated from OpenAPI with `post_hotels_rates` and `post_bookings`). | Yes. | Hotel search and booking for PS3, and a second hotel feed for PS2 dedup. | 🟢 |
| | https://docs.liteapi.travel/docs/mcp ; https://glama.ai/mcp/servers/liteapi-travel/mcp-server ; https://dev.liteapi.travel/ | | | |
| **Hotelbeds APItude** | Free evaluation keys, **50 requests/day**, test host `api.test.hotelbeds.com`, X-Signature auth (SHA256 of key + secret + timestamp). Hotels, Activities and Transfers suites. | Yes, low quota. | A third supplier for the PS2 dedup corpus. **Cache aggressively.** | 🟡 |
| | https://developer.hotelbeds.com/documentation/ | | | |
| **Viator Partner API** | Basic Access is the default for affiliates and needs no pre-authorisation. Read-only content; bookings redirect to viator.com. A sandbox is mentioned. | Yes (affiliate signup). | Sightseeing content for PS2 sightseeing dedup. | 🟡 |
| | https://partnerresources.viator.com/travel-commerce/technical-guide/ ; https://docs.viator.com/partner-api/ | | | |
| **Booking.com Demand API 3.3 + MCP server** | Sandbox host `demandapi-sandbox.booking.com`, 50 requests/min. Requires Managed Affiliate status. **Official hosted MCP server** (Streamable HTTP, `accommodations_search`, flights, **MCP Apps widgets**), limited to approved partners. | Gated. | Cite as an industry signal. Not realistic for students. | 🔴 |
| | https://developers.booking.com/demand/docs/open-api/3.3/demand-api ; https://developers.booking.com/demand/docs/getting-started/sandbox.md ; https://developers.booking.com/mcp-server/docs/about | | | |
| **Kiwi.com MCP** | Prototype with Alpic, Aug 2025. Remote URL `mcp.kiwi.com` (per third parties), no key needed, flexible-date search (±3 days), returns a booking link only. | Yes. | Zero-setup flight search inside an agent. | 🟢 |
| | https://media.kiwi.com/company-news/kiwi-com-releases-mcp-server-prototype/?cat=491 ; https://alpic.ai/blog/behind-the-kiwi-com-mcp-server-deploying-an-agentic-flight-booking-service | | | |
| **Expedia** | B2B MCP server on its Intelligent Experience Platform, announced May 2026 ("coming months"). GA not confirmed. Expedia also has an OSS **Travel Recommendations MCP** that needs an Expedia API key. | Gated. | Industry signal. | 🔴 |
| | https://skift.com/2026/05/21/expedia-to-launch-agentic-ai-tools-for-b2b-partners/ ; https://pypi.org/project/expedia-travel-recommendations-mcp/ | | | |
| **Sabre** | Agentic APIs on a proprietary MCP server (Sep 2025): flights, hotels, post-booking. Sabre Mosaic platform (ITB 2026, secondary). | Gated. | Industry signal. | 🔴 |
| | https://investors.sabre.com/node/19356 ; https://www.travelmole.com/news/sabre-stakes-claim-in-agentic-ai-for-travel/ | | | |
| **SerpApi** (Google Flights and Hotels engines) | Free plan of 250 searches/month at 50/hour. Starter costs $25 for 1,000. | Yes. | Real price signals for PS1 and PS2 enrichment (reviews, photos). | 🟢 |
| | https://serpapi.com/pricing | | | |
| **FlightAware AeroAPI** | Personal tier waives query fees up to **$5/month** (or $10 for ADS-B feeders), personal and academic use only. | Yes, small. | Real delay and cancel status for PS3 disruption triggers. | 🟢 |
| | https://www.flightaware.com/commercial/aeroapi/ ; https://supergood.ai/api-report-card/flightaware | | | |
| **AviationStack** | Free plan of 100 requests/month, HTTP only. | Yes, tiny. | Fallback. | 🟢 |
| | https://aviationstack.com/product | | | |
| **OpenSky** | **OAuth2 client-credentials now required** (basic auth dropped. New accounts need it since Mar 2025, and the Python client since 18 Mar 2026). 429 responses carry a retry-after header. About 1h of history (secondary). | Yes. | Live aircraft positions on a globe (§6). | 🟢 |
| | https://github.com/openskynetwork/opensky-api | | | |

---

## 4. Entity resolution, room mapping and content enrichment (PS2)

| Item | Detail | Why / how | Difficulty |
|---|---|---|---|
| **Gemini Embedding 2** | First natively multimodal Google embedding model, preview **10 Mar 2026** (`gemini-embedding-2-preview`): text, image, video, audio and docs in one space, up to 6 images per request, **interleaved image + text** input, 3072-d Matryoshka (1536 and 768 also good). Text costs $0.20 per 1M tokens and it is in the free tier. | Embed `hotel name + address + photo` as **one vector**, so photo similarity and name similarity are fused natively. Supports blocking and dedup of sightseeing products. | 🟢 |
| | https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-embedding-2/ ; pricing: https://aistudio.google.com/docs/pricing | | |
| **SigLIP 2 / jina-clip-v2 / jina-embeddings-v4** | Open multimodal encoders. jina-clip-v2 (about 0.9B parameters, 89 languages). jina-embeddings-v4 (3.8B, single and multi-vector, arxiv 2506.18902). SigLIP 2 beats SigLIP at all scales and has a NaFlex dynamic-resolution variant. | Local or offline image–text similarity, e.g. "is this photo the *Deluxe King* room?" | 🟡 |
| | https://jina.ai/models/jina-clip-v2/ ; https://arxiv.org/html/2506.18902v3 ; https://www.analyticsvidhya.com/blog/2025/02/boosting-image-search-capabilities-using-siglip-2/ | | |
| **imagededup** | Apache 2.0. PHash, DHash, WHash, AHash and CNN. CNN suits near-duplicates (crops, re-compression). | First pass to collapse identical supplier photos before the expensive model runs. | 🟢 |
| | https://github.com/skysense/imagededup | | |
| **Splink 4** | Probabilistic Fellegi–Sunter record linkage on DuckDB (laptop) or Spark, scaling past 100M records. Splink 4 was released Jul 2024, and a 5.0 dev build is on PyPI. Won the 2025 Civil Service Award for Innovation. | Interpretable match weights per field (name, geo distance, phone, stars). Judges like explainability. | 🟡 |
| | https://github.com/moj-analytical-services/splink ; https://pypi.org/project/splink | | |
| **Overture Maps Places + GERS** | Monthly releases. **2026-08-19.0** has 73.6M places and schema v1.18.0. `categories` was deprecated in favour of `basic_category` + `taxonomy` (removal planned for the Sep 2026 release). The **GERS** global stable IDs (GA Jun 2025) come with registry and bridge files on AWS and Azure. | Use as a neutral **"golden ID" spine**: map each supplier's hotel or POI to a GERS ID, then dedup in GERS space. | 🟡 |
| | https://docs.overturemaps.org/blog/2026/08/19/release-notes/ ; https://docs.overturemaps.org/blog/2026/06/17/release-notes/ ; https://www.geoweeknews.com/articles/overture-maps-foundation-global-entity-reference-system-gers/ | | |
| **Foursquare OS Places** | Apache 2.0. Latest snapshot found is `dt=2026-02-12`. **Since Oct 2025, new releases come only via the Places portal, Snowflake and a gated Hugging Face dataset**, not the public S3 bucket. | Second open POI reference for sightseeing and attractions. | 🟡 |
| | https://huggingface.co/datasets/foursquare/fsq-os-places ; https://foursquare.com/resources/blog/data/evolving-fsq-open-source-places/ | | |
| **Grounding with Google Maps (Gemini API)** | GA **17 Oct 2025**, covering more than 250M places (hours, ratings, reviews, coordinates) plus an interactive map widget, and combinable with Search grounding. Pricing: Gemini 3+ models get **5,000 requests/month free**, then $14 per 1,000. Gemini 2.5 models get 1,500/day free (500/day on the free tier for Flash and Flash-Lite), then $25 per 1,000. | Enrich and verify supplier content (opening hours, descriptions, review themes). Also a strong PS3 itinerary feature. **Check Maps ToS on storing results (assumption).** | 🟢 |
| | https://blog.google/innovation-and-ai/technology/developers-tools/grounding-google-maps-gemini-api/ ; https://aistudio.google.com/docs/pricing | | |
| **Commercial room-mapping benchmarks** | TourMind MappingMind (DL + LLM, claims 99.6% accuracy). Vervotech (property mapping from $499/month, room mapping from $599/month). ANIXE Resfinity. Boomi Hotel Matcher (embeddings + LLM). | Real market rates to quote in the pitch ("we replace a $599/month SaaS"). **No open-source LLM room-mapping project was found.** That gap is your opening. | — |
| | https://hotelguestexperience.co.uk/news/tourmind-launches-mappingmind-a-breakthrough-in-hotel-room-type-mapping-powered-by-deep-learning-and-llms ; https://www.vervotech.com/hub/hotel-mapping/ ; https://marketplace.boomi.com/solutions/ai-agent-hotel-matcher | | |
| H3 hex indexing | Not researched in this scan (**assumption:** H3 v4 is stable on pip). Use the cell plus its neighbours as a geo-blocking key before pairwise matching. | | 🟢 |

**Suggested PS2 pipeline (assumption: a design, not a sourced claim).** The stages run in this order:
1. H3/geo blocking.
2. Splink features plus Gemini Embedding 2 cosine similarity on name, address and photo.
3. A cheap LLM adjudicates only the uncertain band, with a JSON verdict and a reason.
4. Clusters are assigned a GERS ID.
5. Room-name normalisation into a canonical schema (bed type, view, board, refundability) by a cheap LLM.
6. An image dedup pass with imagededup, then aesthetic and quality ranking.

---

## 5. Agent tech (PS3, PS4, PS5)

| Item | Detail | Difficulty |
|---|---|---|
| **MCP Apps extension** | Stable spec **2026-01-26** (`io.modelcontextprotocol/ui`, `ui://` resources, MIME `text/html;profile=mcp-app`). Builds on MCP-UI and the OpenAI Apps SDK. Supported in Claude, ChatGPT, VS Code and Goose (secondary). Booking.com's MCP already ships MCP Apps widgets. → A **TBO MCP server with interactive hotel cards and rebooking widgets** works in both Claude and ChatGPT. https://github.com/modelcontextprotocol/ext-apps (spec path `specification/2026-01-26/apps.mdx`) ; https://www.mcpbundles.com/guides/what-are-mcp-apps | 🟡 |
| **A2A + AP2** | A2A was donated to the Linux Foundation. **AP2 v0.2 (Apr 2026)** was contributed to the **FIDO Alliance** and adds "Human Not Present" pre-authorised payments via Intent, Cart and Payment mandates (W3C Verifiable Credentials). x402 Foundation launched under the LF on 14 Jul 2026. All secondary sources; verify before quoting. → PS3: the agent rebooks within a pre-signed **Intent mandate** ("up to ₹5k extra, same day"). https://ap2-protocol.org/topics/ap2-a2a-and-mcp ; https://ecorpit.com/x402-linux-foundation-agent-payments-adopt-decision-2026/ | 🟡 (mock the mandate) |
| **OpenAI Realtime (gpt-realtime)** | GA with **SIP phone calling**, remote MCP tools and image input. Audio costs $32 per 1M input tokens and $64 per 1M output. `gpt-realtime-mini` costs $10/$20 (secondary). Needs a Twilio or Telnyx SIP trunk for a phone number. https://www.theneuron.ai/explainer-articles/openai-just-made-it-super-easy-to-build-voice-apps-that-actually-work ; https://www.forasoft.com/blog/article/openai-realtime-api-webrtc-sip-websockets-integration | 🟡 |
| **ElevenLabs Agents** | About $0.08 per call-minute platform fee plus LLM and telephony (secondary, mid-2026). https://www.getmacha.com/blog/elevenlabs-agents-pricing-explained | 🟢 |
| **Gemini Live** | Note: the Gemini 3.1 Flash Live Preview and 2.5 Flash Native Audio previews **shut down 17 Nov 2026** in the Developer API (secondary). Don't build on them. https://www.cekura.ai/blogs/gemini-live-api-pricing | — |
| **Computer use** | Gemini 2.5 Computer Use (preview **7 Oct 2025**, browser-only, leads Online-Mind2Web per Google). OpenAI added computer use to its Agents API around Sep–Oct 2026 (secondary, unverified). → PS4: the agent operates legacy supplier extranets that have no API. https://blog.google/technology/google-deepmind/gemini-computer-use-model/ ; https://windowsreport.com/openai-expands-agents-api-with-computer-use-and-aws-support-at-devday-2026/ | 🔴 |

### Cheap models (official prices, per 1M tokens, checked 2026-11-07)

| Model | In / Out | Source |
|---|---|---|
| **Claude Haiku 5.5** (prompts ≤100k) | **$0.10 / $0.50**; cache hit $0.01. Over 100k tokens: $0.50 / $2.50 | https://platform.claude.com/docs/en/about-claude/pricing |
| Claude Haiku 4.5 | $1 / $5 | same |
| Claude Sonnet 5.5 / Sonnet 5 | $2 / $10 | same |
| **GPT-5 nano** | **$0.05 / $0.40** | https://developers.openai.com/api/docs/models/gpt-5-nano |
| GPT-5 mini | $0.25 / $2.00 | https://developers.openai.com/api/docs/models/gpt-5-mini |
| **Gemini 2.5 Flash-Lite** | $0.10 / $0.40 (free tier) | https://aistudio.google.com/docs/pricing |
| Gemini 3.1 Flash-Lite | $0.25 / $1.50 (free tier) | same |
| Gemini 3.5 Flash-Lite | $0.30 / $2.50 (free tier). Gemini 2.5 Flash requests reroute here from 1 Dec 2026 | same |
| Gemini 3.6 / 3.8 Flash | $0.75 / $3.75 until 31 Dec 2026, then double | same |
| **Qwen3.5 small** (0.8B, 2B, 4B, 9B) | Open weights, Apache 2.0 (secondary), natively multimodal, around 2 Mar 2026. Run locally for free. | https://llm-stats.com/models/qwen3.5-4b ; https://www.orcarouter.ai/blog/qwen-3-5 |

→ **PS5 demo number:** a routine HR query costs fractions of a cent on Haiku 5.5, GPT-5 nano or Flash-Lite. Escalate to Sonnet or Opus only on low confidence or a policy-sensitive intent. Show a **per-request cost ledger.**

---

## 6. Visualisation (all PS, demo "wow")

| Item | Detail | Difficulty |
|---|---|---|
| **deck.gl 9.3 / 9.4** | 9.3 released 13 Apr 2026. In 9.4, **globe supports pitch and bearing**, trackpad gestures and elastic bounds. 9.1 added MapLibre v5 globe support. https://deck.gl/docs/whats-new ; https://github.com/visgl/deck.gl/releases/tag/v9.4.0 | 🟡 |
| **Google Photorealistic 3D Tiles** | OGC 3D Tiles format, renderable in CesiumJS and deck.gl. GA since Oct 2023 (old, but students rarely use it). https://mapsplatform.google.com/resources/blog/build-immersive-maps-at-scale-with-photorealistic-3d-2d-and-street-view-tiles-now-in-ga | 🟡 |
| **Maps JS 3D (`<gmp-map-3d>`, Map3DElement)** | Photorealistic 3D directly in the Maps JS API. GA status is unclear in what we found, and `mode` (HYBRID/SATELLITE) is now required. Google Maps now offers a "Maps Demo Key" (no credit card) per its site banner. https://developers.google.cn/maps/documentation/javascript/3d/overview?hl=en ; https://mapsplatform.google.com/resources/blog/3d-maps-for-javascript-api-now-in-preview-start-building-your-own-immersive-maps-experience-today/ | 🟢 |
| globe.gl, kepler.gl, Cesium | No 2026 release info found (**assumption:** stable and usable). | 🟢 |

Ideas: PS3 shows a disrupted flight live (OpenSky) on a deck.gl globe with rebooking options as arcs. PS1 shows a demand heat hexmap of P90 risk per city. PS2 shows a 3D-tile fly-to for a matched hotel cluster with its photo strip.

---

## 7. Governance, durability and observability (PS4, PS5)

| Item | Detail | Difficulty |
|---|---|---|
| **Cedar + Bedrock AgentCore Policy** | GA **3 Mar 2026**. **Natural-language → Cedar** policy authoring. The policy engine sits on the AgentCore Gateway and checks every agent→tool call. Default deny; forbid overrides permit. Open-source Cedar can be used without AWS (**assumption:** `cedarpy` or Cedar WASM bindings exist). → PS5: "manager may approve leave ≤ 5 days. Agent may *never* change salary." https://aws.amazon.com/about-aws/whats-new/2026/03/policy-amazon-bedrock-agentcore-generally-available ; https://xebia.com/blog/cedar-policies-for-amazon-bedrock-agentcore-gateway/ | 🟡 |
| OPA | Not researched in this window (**assumption:** stable). | 🟡 |
| **Temporal × OpenAI Agents SDK** | **GA 23 Mar 2026** (Python, package `temporalio-openai-agents`, `temporalio.openai_agents`). The agent loop runs in the Workflow and model calls run as Activities. MCP servers are *not* durable. A TypeScript integration exists. → Crash-safe multi-day disruption rebooking and HR approval flows. https://temporal.io/blog/announcing-openai-agents-sdk-partnership ; https://docs.temporal.io/develop/python/integrations/openai-agents | 🟡 |
| **Inngest durable agents + AgentKit** | Each LLM or tool call is a durable step. **`step.waitForEvent()` provides human-in-the-loop approval** (handle approved, rejected and timeout). Lighter than Temporal for a Next.js team. https://www.inngest.com/docs/durable-execution/durable-agents ; https://www.inngest.com/docs/durable-execution/durable-agents/human-in-the-loop.md | 🟢 |
| **Idempotency** | Duffel webhooks are at-least-once, so dedupe on `idempotency_key`. Use the same pattern for ticket and HR actions. https://hookdeck.com/webhooks/platforms/guide-to-duffel-webhooks-features-and-best-practices.md | 🟢 |
| **Routing** | Not Diamond reportedly powers **OpenRouter auto**. RouteLLM claims about 85% cost saving at about 95% of GPT-4 quality on MT-Bench. LiteLLM is an OSS gateway with cost tracking and fallbacks. Routers are a decision layer that sits in front of a gateway. All secondary sources. https://holori.com/best-llm-routers/ ; https://zylos.ai/research/2026-01-29-llm-routing-intelligent-model-selection | 🟢 |
| **Langfuse** | **Acquired by ClickHouse (16 Jan 2026)**, still MIT and self-hostable. v4 server around Jul 2026, with new SDKs (Python v5, JS v6) needing self-hosted ≥4.59 (secondary). Use for per-trace cost dashboards. https://langfuse.com/blog/joining-clickhouse ; https://www.orrick.com/en/news/2026/01/open-source-llm-observability-langfuse-acquired-by-clickhouse-inc | 🟢 (cloud free tier: **assumption**) |
| Helicone | Not researched. | — |

---

## 8. Top 10 surprising enablers (ranked)

| # | Enabler | PS | Why most student teams will miss it |
|---|---|---|---|
| 1 | **Amadeus Self-Service shutdown (17 Jul 2026) → Duffel test mode with Duffel Airways order-change and cancel, plus the airline-initiated-change webhook** | PS3 | Teams will waste a day on dead Amadeus tutorials. Duffel gives a *real* bookable, changeable and refundable flight sandbox, which makes a full disruption-rebooking loop demoable. |
| 2 | **Chronos-2 / TimesFM 2.5–3.0 zero-shot forecasting with covariates and quantiles** | PS1 (and PS4) | Probabilistic demand with holiday and event covariates and no training. Feeds a stochastic pre-buy optimiser (OR-Tools/HiGHS) directly, so it shows risk instead of a point guess. |
| 3 | **MCP Apps (spec 2026-01-26), with Booking.com and Sabre shipping MCP while TBO has none found** | PS3, PS4 | Build a "TBO MCP server" with interactive UI widgets that runs in Claude *and* ChatGPT. It positions TBO as agent-native B2B distribution, the way Expedia announced in May 2026. |
| 4 | **Gemini Embedding 2: interleaved image + text in one vector** | PS2 | Fuses photo and name/address similarity for hotel and sightseeing dedup in one API call, at $0.20 per 1M text tokens or the free tier. |
| 5 | **Overture GERS IDs + Places (Aug 2026, 73.6M places) as a neutral golden-ID spine** | PS2 | Turns N×N supplier matching into N→1 mapping to an open stable ID. Foursquare OS Places is a second reference, now on gated Hugging Face. |
| 6 | **Haiku 5.5 at $0.10/$0.50, GPT-5 nano at $0.05/$0.40, Flash-Lite free tier, Qwen3.5 small local** | PS5, PS4, PS2 | Cheap-model routing can show cents-per-1,000-requests economics. Use the cheap LLM only in the uncertain band of the PS2 matcher. |
| 7 | **Cedar policies via AgentCore Policy (GA Mar 2026) with natural-language → Cedar authoring** | PS5, PS4 | Formal, auditable guardrails (default deny, forbid wins) instead of prompt-only "please don't". HR admins write policy in English and the agent can't bypass it. |
| 8 | **Durable agents: Temporal × OpenAI Agents SDK (GA Mar 2026) or Inngest `waitForEvent` HITL** | PS3, PS4, PS5 | Crash-safe multi-day flows (rebooking awaiting customer OK, ticket escalation, leave approval) with idempotency. This is what production graders look for. |
| 9 | **Grounding with Google Maps in Gemini (Oct 2025; 5,000 requests/month free on Gemini 3+)** | PS3, PS2 | Live hours, ratings and reviews for itinerary and content enrichment without scraping, with a ready-made map widget. |
| 10 | **AP2 v0.2 "Human Not Present" mandates (FIDO, Apr 2026) and Google UCP hotel partners** | PS3 | Lets the agent rebook autonomously within a pre-signed spend limit. Shows awareness of where agentic payments are heading, especially since ChatGPT Instant Checkout retreated. |

Honourable mentions: **Toto 2.0** (Apache 2.0) for PS4 ticket-volume forecasting · **revmng-mcp** RM tools as agent tools (PS1) · **gpt-realtime SIP** for a phone-in support agent (PS3/PS4) · **deck.gl 9.4 globe** with OpenSky live flights · **Langfuse** cost traces (PS5).

## Open verification items

- TBO hackathon API credentials and sandbox scope (ask the organisers).
- Whether Duffel test mode can emit `order.airline_initiated_change_detected`. If it can't, simulate it in your own layer.
- GA status of Expedia's B2B MCP and of Maps JS 3D.
- Primary-source confirmation of the AP2→FIDO move and of Qwen3.5 licences.
