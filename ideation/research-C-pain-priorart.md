# Research C — Pain Evidence & Prior Art (TBO VoyageHack 4.0)

Compiled 2026-11-07. Each claim lists a URL and the source's date where one is known. Items with no source are marked **assumption**. Vendor-reported numbers are marked *(vendor claim)*. I accessed every source on 2026-11-07. Where a page showed no publication date, the entry says "date n/a".

---

## Context: TBO scale (useful for every PS)

- TBO FY25 consolidated GTV was INR 30,832 Cr, up 16% YoY. Air GTV was INR 12,634 Cr; Hotel & Ancillary GTV was INR 18,198 Cr. Hotels and ancillaries contributed 59% of GTV and 84% of gross profit. Source: Travel Trade Journal, mid-2025 — https://traveltradejournal.com/tbo-tek-ltd-delivers-strong-performance-in-fy25-on-the-back-of-robust-growth-in-hotels-segment-revenue-up-25-per-cent-adj-ebitda-grew-22-per-cent-yoy-to-inr-329-cr-gtv-crosses-inr-30000-cr/
- In Q4 FY26, revenue was up 83% YoY to ₹814 Cr and GTV was up 29% to INR 100.79 bn. Source: indiaoutbound.info, ~May 2026 — https://indiaoutbound.info/?p=218857
- Monthly transacting buyers were 33,324, up 16% YoY. Source: TBO Feb 2026 filing as summarised in search (Business Standard / BSE attachment, 11-02-2026) — https://bsmedia.business-standard.com/_media/bs/data/announcements/bse/11022026/0a4475c2-4e29-49b7-bd9d-2567fe1596e6.pdf
- On the 29 May 2026 earnings call, TBO management said complex luxury itineraries will still be booked mostly through human advisors and agencies. They also described "Voya", which gives advisors ultra-luxury supply plus AI itinerary tools. Source: financialreports.eu transcript, 2026 — https://financialreports.eu/filings/tbo-tek-limited/call-transcript/2026/47965950/
- A secondary article says TBO connects "147,000+ buyers with 1M+ suppliers". I could not verify this against the annual report, so treat it as unverified. Source: https://blog.getrentacar.com/tbotek-financial-surge-overview (date n/a)

---

## PS1 — Inventory Optimization (pre-buy allotments / blocks / series fares)

### How wholesalers pre-buy and where the risk sits
- Bed banks buy inventory "in bulk at a discounted price for specific dates."
  - **Prepaid model:** the hotel is paid whether or not the rooms sell. Unsold prepaid inventory is a direct loss for the wholesaler, which bed banks often offload as last-minute deals to OTAs.
  - **Current practice:** wholesalers often buy only part of an allocation and sell the rest pay-on-consumption.
  - **Release periods:** typically 30–60 days before check-in.
  - Source: AltexSoft "Bed banks 101", 11 Apr 2025 — https://www.altexsoft.com/blog/bed-banks/
- Scale reference, from the same AltexSoft article:
  - Hotelbeds has about 300k properties, all directly contracted.
  - WebBeds has 500k+ hotels, with direct deals with 90k+ of them.
- Release structures of 30/21/14/7 days and "wash factors" are described in a hotel-vendor blog (date n/a) — https://www.roommaster.com/blog/hotel-allotment-management
- Airline series fares:
  - The operator locks a block of seats at a fixed rate and carries the unsold-seat risk in exchange for the discount.
  - Larger commitments get better discounts but carry more unsold risk.
  - Source: vendor blog, adivaha (date n/a) — https://www.adivaha.com/series-fare-top-trending-shows-to-watch.html
- A TripJack (Indian B2B competitor) job listing describes manual ops for series fares: "Maintain tracking sheet for blocked seats vs sold inventory. Handle ADM / debit note cases related to series bookings." This is direct evidence that the work is spreadsheet-driven. Source: (date n/a) — https://tripjack.keka.com/careers/jobdetails/59858
- Look-to-book "industry averages" are about 500 searches per booking for B2B and about 19,000 for B2C. Source: Pruvo (a WebBeds company), 25 Jun 2020, unattributed industry average — https://www.pruvo.com/blog/what-is-the-look-to-book-ratio-does-re-shopping-hotel-reservations-impact-it/

### Revenue-management methods (for the decision engine)
- **Littlewood / EMSR:** the two-class Littlewood rule is a newsvendor critical-fractile problem. Belobaba (1987 MIT thesis; Operations Research 1989) generalised it to EMSR-a. EMSR-b is the later refinement (Belobaba & Weatherford 1996), which aggregates higher classes into one virtual class. MIT DSpace — https://dspace.mit.edu/handle/1721.1/68077 ; summary — https://en.wikipedia.com/wiki/Expected_Marginal_Seat_Revenue
- EMSR-b is a static heuristic that assumes independent normal demands; bid prices and DP are its dynamic counterpart. For DP treatment, Talluri & van Ryzin, *The Theory and Practice of Revenue Management* (2004) is the standard reference. A Python package implementing these methods exists — https://pypi.org/project/revmng/
- **Assumption (not sourced here):** pre-buy under a budget maps naturally to a multi-item newsvendor with a budget constraint, solved as an LP or MILP. It can be risk-adjusted with CVaR (Rockafellar–Uryasev), using scenario demand simulated from booking, search and event features. I did not fetch a CVaR or portfolio-newsvendor citation within the time-box.

### Public datasets for a demo
- **Hotel Booking Demand** (Antonio, de Almeida, Nunes), *Data in Brief* 22 (2019) 41–49, DOI 10.1016/j.dib.2018.11.126.
  - Two hotels: 40,060 resort and 79,330 city bookings.
  - 31 variables, including lead time, ADR, cancellations, deposit type, market segment and agent.
  - Arrivals from Jul 2015 to Aug 2017.
  - It is open access and also on Kaggle.
  - Source: https://repositorio.iscte-iul.pt/handle/10071/16929
  - **Best fit for the cancellation-risk and demand-curve model.**
- **Kaggle "Flight Price Prediction"** (Shubham Bathwal): EaseMyTrip data for India's six largest metros, 300,261 rows, including the `days_left` and price fields. Good for series-fare and price-vs-lead-time curves. Source: https://baselight.app/u/kaggle/dataset/shubhambathwal_flight_price_prediction (date n/a)
- **Inside Airbnb:** per-city `listings`, `calendar` and `reviews` files under CC BY 4.0. I saw no Indian city in the part of the page I read. Source: https://insideairbnb.com/get-the-data/ (accessed 2026-11-07)
- **Assumption (not verified):**
  - Google Trends could serve as the "search" (look) signal proxy.
  - Indian public-holiday and festival calendars could serve as event signals.
  - The PredictHQ API is commercial, possibly with a trial.

### Existing products / prior art
- **PredictHQ** (event demand intelligence), all vendor-reported:
  - One hotel group's forecast accuracy improved 7.1%.
  - Another saw about 9% better accuracy on high-impact days and about 12% on low-impact days.
  - A controlled test gave a 2.2-point MAPE improvement for accommodation.
  - "Events explain >60% of demand variability."
  - Source: https://predicthq.com/blog/event-impact-analysis-how-hotels-use-event-data-to-capture-millions ; https://predicthq.com/blog/use-demand-impact-patterns-to-predict-how-events-shape-consumer-behavior
- **Duetto:** OpenSpace (formerly BlockBuster) evaluates group displacement by incremental profit. Duetto also partners with RateGain's channel manager. Sources: https://www.duettocloud.com/library/unlock-more-profit-with-every-group ; https://www.constructionworld.in/energy-infrastructure/power-and-renewable-energy/rategain-and-duetto-to-power-real-time-hotel-revenue-optimisation/93393
- **IDeaS G3 RMS:** its Group Pricing module values the business a group displaces. Source: https://www.hotel-online.com/news/giza-palace-hotel-spa-partners-with-ideas-to-implement-advanced-revenue-management-capabilities
- **Gap (assumption):** all of these RMSs are **hotel-side**, optimising one property's own inventory. I found no public product that optimises a **distributor's** pre-buy portfolio across many hotels and airlines under a budget.

### (a) Strongest sourced pain facts
1. Unsold prepaid inventory is a direct loss to the wholesaler, which is why the industry moved to partial pre-buy plus pay-on-consumption (AltexSoft, Apr 2025).
2. Larger series-fare commitments mean better discounts but higher unsold risk, and the operator bears that risk (adivaha, n/a).
3. Indian B2B competitors track blocked seats against sold seats in tracking sheets and handle ADM/debit notes manually (TripJack job post, n/a).
4. Hotels are TBO's profit engine: 84% of FY25 gross profit (Travel Trade Journal, 2025). Better hotel pre-buy decisions therefore hit the core margin.
5. Event signals are worth a few to about 12% forecast accuracy, per vendor case studies (PredictHQ).

### (b) Nearest prior art
IDeaS G3, Duetto (OpenSpace), PredictHQ, Lighthouse/RateGain for rate intelligence. All are hotel-side or signal providers. Academic: EMSR-b and newsvendor.

### (c) Credible demo with public data
- Train a cancellation and pickup model on the Antonio hotel dataset.
- Add synthetic "search" signals (look-to-book ~500:1, per the Pruvo B2B average) and Indian holiday flags.
- Run a budget-constrained newsvendor/CVaR optimiser that outputs "buy N rooms at hotel X for dates D at cost C; release by T−21; sell at P". Show expected margin and the P5 downside.
- Show series-fare pre-buy on the EaseMyTrip fare-vs-days-left curves.
- Backtest on the 2017 hold-out against naive "buy last year's volume".

---

## PS2 — Multi-Supplier Optimization (hotel/room/experience dedupe + ranking)

### Size of the mapping problem
- Without mapping, the same hotel can appear about 4 times across suppliers *(Vervotech, vendor)*. Vervotech also distinguishes "Vervotech duplicates" from "supplier duplicates". Sources: https://www.vervotech.com/hub/hotel-mapping/ ; https://support.vervotech.com/support/solutions/articles/47001235744-vervotech-duplicates-vs-supplier-duplicate-hotels
- From AltexSoft's mapping-tools review (last updated 15 Mar 2023) — https://www.altexsoft.com/blog/cloud/hotel-mapping-tools-how-giata-gimmonix-databindr-and-other-solutions-work/
  - About 2% of hotels change name, chain or phone each year (GIATA statistics).
  - An average mapping error in Germany costs about €1,500 in OTA expenses.
  - On a €2,700 tour, fixing a wrong hotel match costs about 55% of the tour price.
  - GIATA covers about 1.2M properties; Gimmonix 1.9M; Vervotech 2M+ hotels and 600+ suppliers.
  - **Room mapping is harder:** Vervotech claims about 95% for room mapping against 99.999% for hotel mapping.
- Gimmonix Mapping.Works docs *(vendor)* — https://documentation.hsp.gimmonix.com/docs/mapping-overview ; https://documentation.hsp.gimmonix.com/docs/mapping-risk-factors
  - Claims 99.99% accuracy, 98.7% hotel coverage and 100% room coverage.
  - The 100% room coverage is reached by dumping thin data such as a bare "Suite" into "secondary" categories that users can filter out. This is useful evidence that room normalisation is lossy.
- Look-to-book cost: each search costs money when vendors charge per search. Source: Zentrumhub blog (n/a) — https://www.zentrumhub.com/blog/hotel-api-aggregator-pricing/
- Experiences: one operator's tour can appear via several resellers at different prices on one results page (Recommended.app, n/a) — https://www.recommended.app/compare/best-viator-alternatives. TripAdvisor may rotate booking links when a product has multiple suppliers (PhocusWire, older article) — https://www.phocuswire.com/And-then-there-were-three-TripAdvisor-quietly-adds-more-tour-and-activity-suppliers. I found no public Viator dedup documentation.

### Academic / technical prior art
- **LLM entity matching:** GPT-4 zero-shot beats fine-tuned RoBERTa and Ditto on 3 of 5 benchmarks, with F1 around 90%. Prompts need tuning per model and dataset. Peeters, Steiner, Bizer, arXiv 2310.11244 (EDBT 2025) — https://arxiv.org/abs/2310.11244v3
- **Spatial POI entity resolution:** Grab's restaurant matching uses lat/long, name, address and distance features with tree models. Gao & Widdows, GISTAM 2020 — https://www.arxiv.org/pdf/2401.08537
- **Tourism/hotel entity matching chapter:** covers languages, transliteration and address formats. Springer LNCS, DOI 10.1007/978-3-030-88389-8_19 — https://springerlink.bibliotecabuap.elogim.com/content/pdf/10.1007/978-3-030-88389-8_19.pdf
- **GeoBench:** a spatial entity-matching benchmark builder (SIGSPATIAL 2014) — https://geobench.liris.cnrs.fr/help.html
- **Learning to rank:**
  - **Expedia ICDM 2013 / Kaggle "Personalize Expedia Hotel Searches":** about 399k search lists and 9.9M rows of training data. Includes competitor OTA prices and ~30% randomly-ranked sessions, which are useful for unbiased LTR. Sources: https://arxiv.org/pdf/1311.7679 ; https://arxiv.org/pdf/2210.16408
  - **Airbnb, "Applying Deep Learning to Airbnb Search":** KDD 2019, DOI 10.1145/3292500.3330658 — https://arxiv.org/pdf/1810.09591

### Public datasets
- **Foursquare OS Places:** 100M+ POIs under Apache 2.0, gated on Hugging Face — https://huggingface.co/datasets/foursquare/fsq-os-places
- **Overture Maps Places:** CDLA Permissive 2.0 / Apache 2.0. The Oct 2026 release has about 60.3M Meta-sourced and 3.76M Foursquare-sourced features — https://docs.overturemaps.org/guides/places
  - Overture and FSQ list the same hotels independently, so pairing them gives a **natural duplicate-pair test set**.
- The Expedia Kaggle LTR dataset (above).
- **Assumption:** OpenStreetMap `tourism=hotel` nodes could be a third source for triangulation (not fetched).

### (a) Strongest sourced pain facts
1. A single hotel mapping error costs about €1,500 in OTA expenses in Germany. Fixing a wrong match on a tour costs about 55% of its price (AltexSoft, 2023).
2. About 2% of hotels change name, chain or phone each year, so mapping decays continuously (GIATA via AltexSoft, 2023).
3. Room mapping accuracy (~95%) is far below hotel mapping (~99.99%), and "100% coverage" is achieved with coarse secondary buckets (AltexSoft 2023; Gimmonix docs).
4. Without mapping, one hotel shows up about 4× across suppliers (Vervotech).
5. Off-the-shelf GPT-4 already reaches about 90% F1 on entity matching with no training, so an LLM matcher is credible (Peeters et al., EDBT 2025).

### (b) Nearest prior art
GIATA, Gimmonix Mapping.Works, Vervotech (hotel, room and "Profit Maximizer"), DataBindR RoomMappR, TravelgateX. Academic: Ditto, Peeters LLM-EM, Grab spatial ER.

### (c) Credible demo with public data
- Pull hotels in 2–3 Indian cities from Overture and FSQ OS Places (plus OSM), and inject synthetic "supplier" noise: transliteration, abbreviations, coordinate jitter.
- Run blocking (geohash plus name trigram), then a feature model, then an LLM adjudicator for the uncertain band. Report precision and recall against hand-labelled pairs.
- **Room normalisation:**
  - Parse supplier room strings into a canonical schema: bed type, view, board, refundability, occupancy.
  - Use a confidence score with an abstain path.
  - Show a "rate parity across suppliers for the same canonical room" table.
- Train an LTR on the Expedia 2013 Kaggle data to rank the deduped offers.

---

## PS3 — Virtual Travel Agent / Agent Copilot

### Agent pain
- Leisure and business travel agents spend up to 80% of their time processing bookings (Amadeus study cited by PhocusWire, older, date n/a) — https://www.phocuswire.com/Day-Two-of-Ten-Understanding-tech-trends-in-travel
- In India, quoting often means editing Word files, converting to PDF and attaching in WhatsApp (vendor blog, n/a) — https://greentick.ai/blogs/whatsapp-api-for-travel-agencies-and-tourism/. A Peakflo claim that agencies lose 40–60% of quoted enquiries to slow quotes is a vendor claim and unverified — https://peakflo.co/blog/crm-for-travel-agents
- I found **no independent survey** of hours per itinerary for Indian B2B agents. Treat any number as an assumption.

### Why consumer AI planners fail
- **Greetwell survey**, Aug 2026, n=1,000 US leisure travellers (485 had used AI); published by Stacker on 15 Sep 2026 — https://stacker.com/stories/travel/survey-ai-hallucinated-travel-destinations-1-6-users
  - 55% of AI users hit at least one bad recommendation.
  - Failure types:

| Failure type | Share |
|---|---|
| Wrong price, hours or other details | 27% |
| Fully booked / unavailable | 21% |
| Place or activity that does not exist | 16% |
| Business permanently closed | 10% |

- **Civitatis** (Mar 2026, 7,000+ travellers): nearly half of AI users encountered incorrect or outdated info, especially prices and real-time availability (per search summary; I did not open the primary) — https://www.mightytravels.com/2026/03/why-travelers-are-still-skeptical-about-using-ai-for-trip-planning/
- **Expedia survey** (UK/US/India, 5,700+ adults): 66% would not trust an AI assistant to book for them, and only 8% would be comfortable booking via AI — https://www.phocuswire.com/news/online/ai-trust-discovery-planning-expedia-dune7
- **Phocuswright via TravelAge West**, Sep 2026: 60% of agentic-AI users aged 25–44 "completely/mostly trust" AI results — https://www.travelagewest.com/Industry-Insight/Opinion/agentic-ai-for-booking-travel

### Prior art (consumer & corporate)
- **MakeMyTrip Myra GenAI planner:** launched Aug 2025 on an agentic framework, in English and Hindi, in beta, covering planning through post-sales — https://www.businesswire.com/news/home/20250806170695/en/MakeMyTrip-Launches-Multilingual-GenAI-Trip-Planning-Assistant-Making-Travel-Booking-Conversational-and-Inclusive/
- **Expedia Romie**, an AI "travel buddy" — https://travelmarketreport.com/RetailStrategies/articles/Expedia-Unveils-Romie-an-AI-Powered-Travel-Planner
- **OpenAI Operator** (Jan 2025):
  - Partners: Booking.com, Tripadvisor, Priceline and others.
  - The demo booked a Tripadvisor Rome tour, and OpenAI warned the tool will make mistakes.
  - Sources: https://www.phocuswire.com/openai-operator-web-agent ; https://skift.com/2025/01/24/openais-travel-tool-tripadvisors-machinations-and-american-airs-earnings
- **Kayak.ai**, a conversational assistant — https://www.hospitality.today/article/kayak-pivots-from-search-to-ai-driven-travel-assistant
- **Otto**, an autonomous business-travel agent, launched 4 Dec 2025 — https://letsdatascience.com/news/otto-launches-ai-assistant-for-business-travel-ede3bd46
- **Navan:** Ava agent; AI "Executive Assistant" in Mar 2026 (Bloomberg). The CEO claims a disruption flight change takes a human about 16 minutes and the AI under 1 minute *(vendor claim)* — https://www.bloomberg.com/news/articles/2026-03-02/travel-booking-platform-navan-unveils-ai-executive-assistant ; https://www.startuphub.ai/news/navan-ceo-on-ai-travel-assistant-corporate-spending
- **Not covered:** Mindtrip, Layla, Booking AI Trip Planner and Google Gemini trips were not fetched within the time-box.

### Disruption cost
- **Europe:** air-navigation delays cost an estimated €16.1bn for airlines and passengers (2015–Oct 2025, 2024 values), of which €9.7bn fell on airlines (avweb, 2025) — https://avweb.com/aviation-news/european-air-traffic-delays-rise-high-cost/
- **US corporates:** spend $17bn+ a year on the fallout from flight cancellations (Perk/TravelPerk survey, 2025) — https://perk.com/blog/business-travel-chaos-survey/
- **Global:** Amadeus estimated the annual cost of flight disruption at $60bn across the ecosystem (date unclear) — https://www.travolution.com/news/travel-sectors/air/amadeus-study-puts-annual-cost-of-flight-disruption-at-60bn/

### (a) Strongest sourced pain facts
1. 55% of AI-planner users got at least one bad recommendation; 27% got wrong prices or details and 21% got unavailable items (Greetwell, Aug 2026).
2. 66% would not trust AI to book for them, and only 8% are comfortable (Expedia survey via PhocusWire).
3. Agents spend up to 80% of their time on booking processing rather than selling (Amadeus via PhocusWire).
4. Flight disruption costs $60bn a year globally (Amadeus), €16.1bn in European ATC delays, and $17bn+ for US corporates.
5. TBO itself says complex itineraries will stay agent-booked and is building advisor AI tools in Voya (TBO call, May 2026). This validates a **copilot for agents** over a consumer bot.

### (b) Nearest prior art
MakeMyTrip Myra (B2C, India), Navan/Otto (corporate, with post-booking), Operator/Kayak.ai (consumer), TBO Voya (luxury advisors).

### (c) Differentiation & demo
- **Differentiation (assumption):**
  - Agent-facing, not consumer-facing.
  - Every price and availability in a quote is grounded in a live or cached supplier response, with a quote-ID and timestamp. That directly targets the 27% and 21% failure modes.
  - Agent markup and white-label PDF/WhatsApp quote in under a minute.
  - Post-booking watchlist: schedule changes, LCD reminders, auto-proposed rebooking alternatives.
- **Demo:**
  - Use a mock supplier API seeded from the Kaggle EaseMyTrip fares, Overture hotels and the Antonio ADR distribution.
  - An LLM drafts the itinerary, but every line item must resolve to an inventory ID, or the system refuses.
  - Simulate a flight cancellation event and show auto-rebuild with the price delta.

---

## PS4 — OpsDesk (Zendesk replacement for B2B travel ops)

### Zendesk costs & limits (official pages)
- From the Zendesk pricing page (accessed 2026-11-07) — https://www.zendesk.com/pricing/
  - Suite Team: $55 per agent per month, paid yearly ($69 monthly).
  - Suite Professional: $115 per agent per month, paid yearly ($149 monthly).
  - Copilot add-on: $50 per agent per month, Professional and above.
  - Automated resolutions: Team includes 5 per agent per month and Professional 10. Extra resolutions cost $1.50 committed or $2.00 pay-as-you-go.
  - Side conversations are listed from Suite Professional upward.
- From Zendesk developer docs (accessed 2026-11-07) — https://developer.zendesk.com/api-reference/introduction/rate-limits/
  - API rate limits per minute: Team 200, Professional 400, Enterprise 700, Enterprise Plus 2,500. The High Volume add-on raises a plan to 2,500.
  - **Incremental Exports are capped at 10 requests per minute**, or 30 with High Volume.
  - The side-conversation events endpoint allows 600 requests per 10 minutes.
- Slack side-conversation limits (Zendesk Help, accessed 2026-11-07) — https://support.zendesk.com/hc/en-us/articles/4408844202778
  - Only comments of 1,000 characters or fewer can be inserted.
  - No direct messages.
  - A side conversation can't mix email and Slack.
  - Slack Connect channels owned by an external workspace break it.
  - An archived channel leaves the conversation read-only.

### Modern AI ticketing
- **Intercom Fin:** $0.99 per outcome or resolution (third-party summaries, 2026) — https://www.gleap.io/blog/intercom-fin-ai-pricing-2026
  - Resolution rates cited range from 51% (Anthropic case study) to 56% (AWS case study) to about 67% (late 2025).
  - Sources: https://claude.com/es/customers/intercom ; https://aws.amazon.com/solutions/case-studies/intercom-anthropic/ ; https://createwith.com/tool/intercom/updates/intercom-ships-200-updates-in-2025-fin-3-reaches-67-average-resolution-rate
- **Sierra:** outcome-based pricing, paid only when a defined outcome is achieved. Sierra blog, 10 Dec 2024 — https://www.sierra.ai/blog/outcome-based-pricing-for-ai-agents
- **Not covered:** Decagon pricing was not found within the time-box.

### Open-source alternatives
| Tool | License (third-party table, verify in repo) | GitHub stars (31 Aug 2026) |
|---|---|---|
| Zammad | AGPL-3.0 | ~5.9k |
| FreeScout | AGPL-3.0, paid modules | ~4.5k |
| Chatwoot | MIT core plus an `enterprise/` directory | ~36k |
| osTicket | GPL-2.0 | ~3.9k |

Sources: https://wz-it.com/en/blog/zammad-freescout-osticket-chatwoot-helpdesk-comparison/ ; https://dev.to/selfhostingsh/helpdesk-1681

### Travel-ops-specific pain
- Most "booking not found at check-in" calls are a search problem: the desk searches by surname instead of hotel confirmation number or wholesaler name (DMC vendor guide, n/a) — https://dmcquote.com/blog/post/hotel-cant-find-booking-check-in-travel-agents
- Helpdesks set "booking not found" to high priority and escalate to the supplier immediately (Freshdesk KB, n/a) — https://blue7tech-help.freshdesk.com/support/solutions/articles/150000195126-booking-not-found
- RateHawk keeps a dedicated help article for the case where the hotel says it has no reservation — https://help.ratehawk.com/en/articles/7918704-what-should-i-do-if-i-contact-the-hotel-and-they-say-they-don-t-have-our-reservation
- **Assumption:** urgency depends on check-in date and LCD, not ticket age. Generic helpdesk SLAs are measured from ticket creation, so they mis-prioritise travel tickets. I found no ticket-volume statistics for B2B bed banks.

### (a) Strongest sourced pain facts
1. Zendesk Incremental Export is limited to 10 requests per minute (30 with a paid add-on). Bulk export and BI over ticket history are throttled (Zendesk dev docs).
2. Slack side conversations are capped at 1,000-character inserts, have no DMs and break on external Slack Connect channels. Supplier collaboration is a weak spot (Zendesk Help).
3. An AI layer adds about $50 per agent per month for Copilot on top of $115 for Professional, plus $1.50–$2.00 per automated resolution beyond the 5–10 included per agent (Zendesk pricing).
4. Industry benchmarks put AI-agent resolution at roughly 50–67% (Intercom/Anthropic/AWS case studies). Ops tickets that need supplier action can't be closed by FAQ bots.
5. "Booking not found at check-in" is a recognised, high-priority escalation pattern across B2B travel helpdesks (multiple KBs).

### (b) Nearest prior art
Zendesk Suite + Copilot, Intercom Fin, Sierra and Decagon (outcome-priced agents), Zammad and Chatwoot (OSS base).

### (c) Credible demo
- Start from a Chatwoot or Zammad fork, or a custom build. Ingest synthetic tickets tied to bookings: TBOH booking ID, hotel, check-in date, LCD, supplier.
- **SLA = f(hours to check-in, hours to LCD, booking value)**, plus routing by region, shift, skill and live availability.
- Side conversation to the supplier by email or WhatsApp, threaded back to the ticket.
- An LLM triage extracts the booking reference and intent and drafts the supplier email.
- Dashboard of "tickets at risk of LCD breach in the next 24h", with CSV/Parquet export that has no rate limit.

---

## PS5 — AI-native HR platform (Darwinbox replacement)

### DPDP Act 2023 & DPDP Rules 2025
- **Notification:** 13 Nov 2025, gazetted 14 Nov 2025 — https://yourstory.com/2025/11/digital-personal-data-protection-dpdp-rules-2025-rollout-over-18-months
- **Phased timeline:**

| Phase | When | What applies |
|---|---|---|
| Immediate | 13/14 Nov 2025 | Rules 1, 2, 17–21: the Data Protection Board |
| 12 months | ~Nov 2026 | Rule 4: Consent Manager registration |
| 18 months | ~May 2027 | Notices, consent, data-principal rights, breach notification, security safeguards, erasure/retention, SDF duties, cross-border transfer |

  - Sources: https://www.mondaq.com/india/data-protection/1706890/a-closer-look-at-the-dpdp-rules-2025 ; https://webiis08.mondaq.com/india/data-protection/1706878/indias-digital-personal-data-protection-act-phased-rollout-and-key-compliance-milestones
  - **Timing note: as of today (7 Nov 2026), the 12-month mark is about a week away and full obligations land around May 2027.**
- **EY summary**, 15 Dec 2025 — https://www.ey.com/en_in/insights/cybersecurity/transforming-data-privacy-digital-personal-data-protection-rules-2025
  - Breaches must be reported immediately to data principals and the Board, with a detailed Board report within 72 hours.
  - Individuals must be notified at least 48 hours before their data is erased.
  - Grievances must be redressed within 90 days.
  - Notices must be itemised and plain-language.
  - Children require verifiable parental consent.
  - The EY page does not give rule numbers, the one-year log-retention figure, or penalty amounts. **Verify these against the MeitY gazette text.** The PIB PDF was not parseable.

### Labour Codes (verified: effective 21 Nov 2025)
- **Full & final settlement within 2 working days** of the last working day, under Code on Wages 2019 s.17(2). This covers resignation, termination and retrenchment. Gratuity keeps its own 30-day timeline and PF goes via EPFO. Sources (HR blogs/news, 2026): https://www.pockethrms.com/full-and-final-settlement/ ; https://www.angelone.in/news/personal-finance/new-labour-codes-2025-2-day-full-and-final-settlement-rule-for-all-employees
  - One Zee Business piece frames it as from 1 Apr 2026, so there is a date discrepancy; check the notified rules — https://www.zeebiz.com/personal-finance/news-from-april-1-2026-full-and-final-settlement-rules-change-know-key-changes-before-resigning-392993
- **Fixed-term employees** become eligible for gratuity after 1 year (Ministry of Labour FAQ) — https://labour.gov.in/en/faqs-labour-codes ; https://kredily.com/new-labour-codes-gratuity/
- **Uniform "wages" definition:** basic + DA + retaining allowance. Exclusions above 50% of total remuneration are added back. This raises the base for PF and gratuity — https://labour.gov.in/en/faqs-labour-codes
- **Gratuity formula:** 15/26 × last monthly wages × years of service (Code on Social Security s.53) — https://labourlawreporter.com/gratuity.asp
- **EPF:** 12% employee + 12% employer on wages, with a ₹15,000 statutory ceiling (secondary source; **verify with EPFO**) — https://kredily.com/new-wage-code-india-2026-payroll-impact/

### Agentic HR prior art
- **Darwinbox:**
  - Super Agent, Sept 2025, built on Sense AI with 30+ HR agents.
  - Claims to be the first HCM with an MCP server. Agents inherit existing permissions and approval chains.
  - Sources: https://darwinbox.com/blog/darwinbox-launches-super-agent ; https://www.peoplematters.in/news/hr-technology/darwinbox-becomes-first-hr-tech-platform-to-launch-its-own-mcp-server-for-ai-integration-45528
- **Workday:** Agent System of Record, announced 11 Feb 2025, for onboarding, governing, cost-tracking and orchestrating its own and third-party agents — https://newsroom.workday.com/2025-02-11-The-Next-Generation-of-Workforce-Management-is-Here-Workday-Unveils-New-Agent-System-of-Record
- **Rippling:** agents across HR, IT and finance. They encapsulate deterministic action sequences as tools the agents can call (ZenML LLMOps case study, 2025) — https://www.zenml.io/llmops-database/building-production-ai-agents-for-enterprise-hr-it-and-finance-platform
- **Leena AI:** an employee-helpdesk agent — https://leena.ai/blog/ai-in-hr-enterprise-service-delivery-2026
- **Gartner (via roundup):** 82% of CHROs plan to adopt AI agents within a year — https://resources.rework.com/tools/ai-agents/best-ai-agents-for-hr-2026 (secondary)

### Infrastructure prior art
- **Temporal:** durable execution, with human-in-the-loop handled through Signals and Updates. A LangGraph plugin lets a human approval wait for days at no cost — https://temporal.io/blog/temporal-langgraph-plugin-durable-execution ; https://temporal.io/blog/durable-flexible-multi-agent-systems
- **Inngest AgentKit:** `step.waitForEvent` for HITL and `step.ai.infer` for durable LLM calls. Still labelled early access — https://inngest.com/docs/agent-kit/overview
- **Cedar vs OPA/Rego:** the Cedar paper (arXiv 2403.04651) reports that Cedar matches or beats Rego and OpenFGA on readability and performs far better, and that it is analysable and formally verifiable — https://arxiv.org/pdf/2403.04651. AWS claims Cedar is 42–60× faster than Rego *(vendor)* — https://aws.amazon.com/blogs/security/migrating-from-open-policy-agent-to-amazon-verified-permissions

### Onboarding stats (weak sourcing)
- Structured onboarding makes employees 69% more likely to stay 3 years (SHRM Foundation-cited, secondary) — https://thirst.io/blog/employee-onboarding-statistics-for-2025/
- The widely quoted "82% retention (Brandon Hall)" is **unverified**: its attribution conflicts across sources. Do not cite it.

### (a) Strongest sourced pain facts
1. The two-working-day F&F mandate under the Code on Wages s.17(2) is effective with the codes from 21 Nov 2025. Manual exit workflows now carry a statutory deadline.
2. DPDP Rules: 72-hour Board breach report, 48-hour pre-erasure notice and 90-day grievance SLA, with full obligations around May 2027 (EY, Dec 2025; Mondaq). HR is a personal-data-heavy fiduciary.
3. The uniform 50% wage definition changes PF and gratuity bases, so every payroll and F&F calculator must be recoded (MoL FAQ).
4. Incumbents are already shipping agents with permission inheritance and MCP (Darwinbox, Sep 2025) and agent registries (Workday, Feb 2025). The bar for "AI-native" is guardrails plus auditability, not chat.
5. The Cedar paper shows policy-as-code can be formally analysed, a credible basis for provable HR guardrails.

### (b) Nearest prior art
Darwinbox Super Agent/Sense, Workday Agent System of Record, Rippling AI, Leena AI. Infra: Temporal or Inngest with Cedar or OPA.

### (c) Credible demo
- An agent-first exit flow: resignation in natural language, then a Cedar policy check (notice period, approver), then a Temporal workflow with a HITL manager approval.
- An F&F calculator that encodes the 50% wage rule and the 15/26 gratuity formula (FTE eligibility after 1 year). It enforces a 2-working-day SLA timer.
- A DPDP consent and erasure ledger: the 48-hour erasure notice, plus a breach drill that generates a 72-hour Board report.
- Per-workflow cost meter (tokens × model price), with routing of cheap models for extraction and strong models for judgement.
- "Live extension test": add a new policy (e.g. a state-specific leave rule) as a Cedar policy at runtime, with no redeploy.
- All of it runs on synthetic employees. No external dataset is needed.

---

## Gaps / not covered within time-box
- No CVaR or portfolio-newsvendor citation fetched.
- No primary pages fetched for Mindtrip, Layla, Booking AI Trip Planner, Google Gemini trips or Decagon pricing.
- No independent data on Indian B2B agent hours per quote, B2B bed-bank ticket volume, or hotel duplicate rates. All of these are vendor or qualitative only.
- The DPDP rule numbers for 72h, 48h, 90d and 1-yr log retention, and penalty amounts, must be verified against the MeitY gazette text.
