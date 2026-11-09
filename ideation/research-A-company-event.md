# Research A: TBO Tek (the company) and VoyageHack (the event)

Researched 2026-11-07. Every claim has a URL or a local file path. Anything not backed by a source is marked **assumption**. Figures come from primary filings where I could get them: the TBO shareholder letter (BSE), the NSE press release and the AGM transcript on TBO's own S3 bucket. Third-party summaries are marked as such.

Primary docs downloaded and read in full:
- Q2 FY27 Shareholders' Letter (2 Nov 2026), BSE: https://www.bseindia.com/xml-data/corpfiling/AttachLive/25d7ab26-f6c8-457b-9be2-15d9df3455ef.pdf
- Q1 FY27 Press Release (29 Jul 2026), NSE: https://nsearchives.nseindia.com/corporate/9810411243_29072026182903_Press_Release_29072026.pdf
- AGM Transcript (8 Aug 2025), TBO IR: https://tbo-static-files.s3.eu-west-1.amazonaws.com/tbo-investor-relations/Shareholder-Communication/2025-26/AGM_Transcript_08082025.pdf
- The five local problem-statement PDFs in `D:\Projects\29. voyagehack\Problem Statement\`

---

## 1. TBO business model and key numbers

### Model
- TBO is a two-sided B2B ("B2A", business-to-agent) travel distribution platform. Suppliers are hotels, airlines, car rentals, transfers, cruises, insurance, rail and others. Buyers are travel agencies, tour operators, TMCs, OTAs, super-apps and loyalty apps. (Third-party IPO summary of the RHP: https://groww.in/ipo/tbo-tek-ipo ; Gulf News: https://gulfnews.com/business/corporate-news/b2a-travel-tech-platform-tbo-goes-public-to-further-empower-and-accelerate-growth-of-travel-agencies-in-the-middle-east-1.1716800587168)
- Products listed on tbo.com: Hotels, Air, Packages, Transfers, Sightseeing, Car Rental, Insurance, Cruise, Rail Europe, Cargo, Marine, Umrah, Platinum Collection and "Connectors (NEW)". Platforms listed: TBO APIs, TBO+, TBO Academy, Roamer (a traveller app), Paxes and others. (https://www.tbo.com/)
- **Revenue models:** the RHP-era summary names two: "commission" and "B2B rate". (Bajaj Broking summary: https://bajajbroking.in/blog/tbo-eek-limited-ipo-details)
- **Working capital (important for the inventory problem statement):** CFO Vikas Jain at the AGM said "TBO is a negative working capital business… we collect first before making payment to the suppliers." For hotels, TBO "generally" pays suppliers "at the time of check-in or after check-in". He put the overall figure at about 4 days of GTV. (AGM transcript, above)
  - Inference (**assumption**): pre-buying inventory means paying suppliers in advance, which works against this cash model. A pre-buy pitch therefore has to justify the capital it ties up and the risk of unsold stock, not just forecast demand.
- **Asset-light:** "an asset-light business model that can be readily scaled without additional Capex." (IPO note: https://reports.chittorgarh.com/ipo_notes/TBO_TEK_Ltd-IPO_Note.pdf)

### Scale (sources disagree, so the date of each figure matters)
| Metric | Value | Source |
|---|---|---|
| Buyers (marketing figure) | 159K+ travel buyers, 1M+ hotels, 100+ countries, 55+ currencies, 300+ account managers | https://www.tbo.com/ |
| Buyers (investor figure, Q3 FY25) | "around 185K Buyers across more than 150 countries", "over one million Suppliers" | https://www.outlookindia.com/amp/story/hub4business/tbo-tek-ltd-delivers-a-strong-performance-in-q3-fy25-achieves-29-yoy-revenue-growth-at-inr-422-cr-adj-ebitda-grew-26-yoy-to-inr-75-cr |
| Transacting agents / supply (FY25) | "over 50,000 plus transacting agents", "more than 1 million hotels and 750 airlines", 2,300+ staff, 15 new countries entered in FY25 | AGM transcript (Chairman) |
| Monthly transacting buyers (organic international, Q2 FY27) | 14,449, a record, +17.4% YoY | Q2 FY27 letter |
| Monthly transacting buyers (all, Q2 FY26) | 30,662, +8% YoY | https://traveltradejournal.com/tbo-tek-reports-robust-q2-fy26-performance-with-26-per-cent-revenue-growth-and-18-32-per-cent-adjusted-ebitda-margin-before-acquisition-costs/ |
| India active agents (FY25) | "more than 31,000 active agents" | AGM transcript |

### Financials
| Period | GTV | Revenue | Other | Source |
|---|---|---|---|---|
| FY25 | > ₹30,000 Cr | – | PAT ₹230 Cr; Adj. EBITDA ₹329 Cr | AGM transcript |
| Q2 FY26 | ₹8,901 Cr (+12%) | ₹568 Cr (+26%) | Hotels + Ancillaries = 64% of GTV, **87% of gross profit** | traveltradejournal (above) |
| Q1 FY27 | ₹11,154 Cr (+37%) | ~₹926 Cr (+81%) | Adj. EBITDA ₹150 Cr (+77%); organic GTV ₹9,918 Cr (+22%) | NSE press release; https://inc42.com/buzz/tbo-tek-q1-profit-surges-32-yoy-to-%E2%82%B983-3-cr/ |
| Q2 FY27 (latest) | ₹11,695 Cr (+31%; +25% constant currency) | ₹866 Cr (+53%) | GP ₹561 Cr; Adj. EBITDA ₹152 Cr (17.6% margin); cash ₹2,060 Cr; term debt $60M | Q2 FY27 letter |

- **Take rates, Q2 FY27:** implied take rate 6.0% for the organic business, 24.7% for Classic Vacations and 7.4% consolidated. Gross profit was 4.0% of GTV for the organic business and 13.8% for Classic. Organic Hotels + Ancillary gross profit was **5.5% of GTV**, up from 5.2% in Q1 FY27, when TBO made a "calibrated call… to prioritize volume preservation in the Middle East". (Q2 FY27 letter)
- **Hotels vs air:** hotels are the profit engine. They were 64% of GTV and 87% of gross profit in Q2 FY26 (above). In the RHP era, hotels were "72.47% of revenue from operations" (Bajaj Broking, above).
- **Regional growth, Q2 FY27, constant currency:** Europe +36% (36% of Hotels + Ancillary GTV, the largest source market), APAC +33%, MEA +10%, LatAm +9%. (Q2 FY27 letter)

### Acquisitions and expansion
- **Classic Vacations** (US luxury wholesaler): bought for up to $125M and completed on 1 Oct 2025. It serves "more than 10,000 travel advisors" and has direct contracts with "more than 1,500 luxury hotel properties". (https://skift.com/es/2025/09/02/tbo-tek-buys-classic-vacations-for-125-million-to-expand-in-u-s-luxury-travel-exclusive/ ; https://www.altexsoft.com/travel-industry-news/tbo-tek-expands-in-luxury-travel-buys-classic-vacations)
  - Trailing-12-month figures: $463.6M GTV and $11.5M Adj. EBITDA, a 2.5% Adj. EBITDA/GTV conversion. (Q2 FY27 letter)
- Earlier: TBO's Dubai arm Tek Travels DMCC took a 51% stake in Bookabed, Switzerland (https://www.gccbusinessnews.com/dubai-based-tek-travels-dmcc-acquires-51-stake-in-swiss-bookabed/). Jumbo Online is referenced in the Q2 FY27 letter.

### Founder strategy statements (Gaurav Bhatnagar and Ankush Nijhawan)
- "Technology remains central to how we strengthen our proposition and improve productivity. Our focus on AI, simpler workflows and greater operating efficiency supports both better service and a lower cost to serve." (Q2 FY27 letter)
- "Our strategic priorities centre on expanding this distribution, strengthening differentiated supply and consistently improving the value we deliver to our partners." (Q2 FY27 letter)
- On luxury: "combining our technology and global reach with richer content, curated supply and broader trip capabilities, we aim to help advisors serve more of their customers' travel needs through TBO." (Q2 FY27 letter)
- Self-service as the lever: "As new agents become more familiar with our self-service platform, they require less support… support a growing business without a proportionate increase in costs." Agents need less KAM time "after their first 5 to 10 transaction". (Q2 FY27 letter)
- Bhatnagar, Q1 FY27: the platform will "support progressively greater volumes of business without requiring a commensurate increase in costs". (NSE press release)
- Bhatnagar, May 2026: "Consistency in hotel data is fundamental to how we operate." (https://www.travolution.com/news/tbo-strengthens-hotel-mapping-with-vervotech-and-ai/)
- FY26 roadmap from the AGM Chairman's speech: "deepen AI across the platform to cut our service time and drive advanced monetization", scale HNext globally "supported by dynamic margin algorithms to optimize conversion", and a "one contract, many products strategy". (AGM transcript)

---

## 2. TBO's own AI and tech initiatives

| Initiative | What is said | Source |
|---|---|---|
| **AI itinerary builder** (for advisors) | Produces day-by-day itineraries in 2–3 minutes, against 4–5 days of DMC back-and-forth. Itineraries contain bookable, dynamically priced flights, rooms, transfers and excursions. | TTN interview with Bhatnagar, 1 Oct 2026: https://www.ttnworldwide.com/ArticleTTN/487135/beyond-the-bot- |
| **MCP connectors for Claude and ChatGPT** | Advisors can pull live TBO inventory into Claude or ChatGPT. This is probably the "Connectors (NEW)" item on tbo.com (**assumption** that they are the same thing). | TTN (above); https://www.tbo.com/ |
| **HNext / "H-Next"**, the next-generation hotel booking engine | "embedded with AI-powered features, including smart search, dynamic [itinerary] generation, and automated support". The transcript says "literacy". Reading it as "itinerary" is my **assumption** that it is a transcription error. | AGM transcript; Q3 FY25 release: "H-Next… being rolled-out to users in a phased manner" |
| AI smart search | "AI enabled smart search available on the platform." | Outlook Q3 FY25 (above) |
| **Supplier-notification automation** | "45% of supplier notifications being automatically handled with 99.5% accuracy" (Q3 FY25). AGM: "AI-led bots that now automate a significant portion of our supplier communications". | Outlook Q3 FY25; AGM transcript |
| **AI voice bot** for outbound calls | "5x speed at ~50% cost vs. manual process in trials" (Q3 FY25). An earlier quarter reported about 450 man-hours saved and a completion rate above 60%. | Outlook Q3 FY25; https://india.entrepreneur.com/news-and-trends/tbo-tek-limited-reports-24-growth-in-q2-fy25-gtv-28/482878 |
| **AI-led customer support** | "AI-led customer support handles 75% of global tickets". This comes from FilingReader's AI summary of the 12 Dec 2025 investor presentation. I could not open the underlying deck, so **verify before quoting**. The same summary says hotel traffic doubled and cost per search fell about 30%. | https://filingreader.com/news-wire/mumbai/2025-12-12/tbo-tek-posts-strong-h1-fy26-results-on-luxury-travel-and-ai |
| **Travel Agent 360** | "a proprietary data platform, allows deep personalization and journey orchestration across touchpoints" | AGM transcript |
| Dynamic margin algorithms / dynamic pricing | Scale HNext "supported by dynamic margin algorithms to optimize conversion" | AGM transcript |
| **Hotel mapping** | Renewed partnership with Vervotech for AI-based hotel mapping (May 2026). Vervotech maps TBO's catalogue to canonical hotel and room IDs. The 99.998% accuracy figure is Vervotech's own claim. | Travolution (above); https://indiaoutbound.info/trade-news/tbo-renews-partnership-with-vervotech-for-ai-based-hotel-mapping/ ; https://www.vervotech.com/hub/master-suppliers/tbo/ |
| Platinum Collection | A curated luxury hotel programme that "driven superior engagement and conversion" | AGM transcript |
| Hosting cost optimisation | Hosting and bandwidth costs rose only 2.3% YoY while volume grew much faster | Q2 FY27 letter |

**Where TBO says tech is heading** (Bhatnagar, TTN, Oct 2026):
- "A standard flight or hotel booking… I can totally see that happening on ChatGPT."
- "As an advisor, your relevance is locked into trips that are connected, complex, and luxury."
- The benchmark for advisors is to deliver something "markedly better, faster and more contextualised" than ChatGPT.
- "A good travel advisor never has a dearth of bookings - they have a dearth of time."

Taken together, TBO's own thesis is AI that saves advisors time on complex, multi-product, luxury trips. It is not consumer chatbots for simple bookings.

### API products and field meanings
- **Hotel API on tektravels.com:** Authenticate, CountryList, DestinationCityList, TopDestination, Hotel Search, Hotel Info, Hotel Room, Block Room, Book, Generate Voucher, GetBookingDetails, and Cancel (SendChangeRequest / GetChangeRequestStatus). Steps are chained by a shared **TraceId**. (https://apidoc.tektravels.com/hotel/)
- **TBO Holidays XML API:** methods include HotelCancellationPolicy, AvailabilityAndPricing, HotelBook and GenerateInvoice. (https://api.tbotechnology.in/AIS_HotelCancellationpolicy.aspx ; http://api.tbotechnology.in/AIS_Hotelbook.aspx ; v7 spec: https://api.tbotechnology.in/pdf/TBOHolidays_HotelAPI_v7.pdf)
- **LCD = Last Cancellation Date / Deadline. Confirmed.**
  - TBO's API returns `<LastCancellationDeadline>`, after which cancellation charges apply. Different rooms can have different LCDs, and the all-rooms call returns the nearest one. (https://api.tbotechnology.in/AIS_HotelCancellationpolicy.aspx and the v7 spec)
  - Unpaid bookings held for invoicing are auto-cancelled on the LCD unless GenerateInvoice is called. TBO's hotel page advertises holding a booking until the LCD without blocking agency funds. (https://www.tboholidays.com/hotels.aspx ; search summary of the HotelBook page)
  - The OpsDesk problem statement uses "check-in date or LCD" as a ticket-priority signal. (local `Zendesk-Darwin box Automation.pdf`)
- **TBOH:**
  - "TBOH" is TBO's own shorthand for TBO Holidays, as in the document title "TBOH Hotel API Specifications V2.1". (https://www.scribd.com/document/904333825/TBOH-Hotel-API-Specifications-V2-1)
  - In the OpsDesk problem statement, TBOH works as a booking-level key: "tickets that share the same TBOH", "Cases linked by agency, TBOH, intent". (local PDF)
  - **Assumption:** TBOH is the TBO Holidays booking reference/ID printed on vouchers. I found no public definition of it as a field.

---

## 3. Pain points mapped to the problem statements

| Problem statement | Evidence from TBO's own materials | Source |
|---|---|---|
| (a) Inventory pre-buy / allocation optimisation (`Automate Inventory Optimization.pdf`) | The problem statement says the system "analyzes historical bookings, demand trends, sold outs, look to book, seasonality" and that "TBO is expected to plan pre buy, supplier integration and pricing to maximise bookable inventory". Counterweight: TBO runs negative working capital and pays hotels "at the time of check-in or after", and the RHP risk factors cite suppliers who "withhold inventory". MEA margin was compressed to defend volume. The strategy line is "strengthening differentiated supply". | local PDF; AGM transcript; https://www.equentis.com/ipos/tbo-tek-ipo_69551 ; Q2 FY27 letter |
| (b) Multi-supplier hotel and sightseeing dedup, mapping and ranking (`Multi Supplier Optimization.pdf`) | "Consistency in hotel data is fundamental to how we operate". TBO renewed the Vervotech AI mapping deal in May 2026. 1M+ hotels sit behind the platform, and hotels produce about 87% of gross profit. Leadership talks about "richer content, curated supply" and dynamic margin algorithms to "optimize conversion". **Gap:** I found no public TBO statement on *sightseeing* deduplication. That part of the problem may be less served by vendors (**assumption**). | Travolution; Q2 FY27 letter; AGM transcript; traveltradejournal Q2 FY26 |
| (c) Virtual travel agent / agent copilot (`Virtual Travel Agent _ Travel Agent Copilot.pdf`) | TBO has **already shipped** an AI itinerary builder and MCP connectors for Claude and ChatGPT (Oct 2026). The founder's thesis is that advisors have "a dearth of time" and that complex luxury trips are the moat. A plain itinerary chatbot therefore copies what TBO already has. To stand out, focus on post-booking work (cancellations, modifications, disruptions, vouchers), which the problem statement stresses, plus multi-product orchestration. This is **assumption**/inference. | TTN interview; local PDF |
| (d) Ops ticketing, OpsDesk replacing Zendesk (`Zendesk-Darwin box Automation.pdf`) | The problem statement lists: no linkage across tickets for the same TBOH, hard-coded FIFO/LIFO routing, no LCD/check-in urgency, "AI costs extra + needs HITL", and "3K-row exports". Company side: "AI-led customer support handles 75% of global tickets" (unverified summary), 2,300+ staff, "deepen AI across the platform to cut our service time", "lower cost to serve". | local PDF; FilingReader; AGM; Q2 FY27 letter |
| (e) HR platform, AI-native HR replacing Darwinbox (same PDF, part 2) | Agent-first HR services platform. Judging weights: Governance 20%, Extensibility 20%, Automation depth 20%, Cost 15%, Engineering 15%, Experience 10%, plus a **live extension test at the finale**. Company context: 2,300+ employees across 55 countries (FY25). The Q2 FY27 merit cycle raised employee costs 12.5% YoY. MarketScreener reports CHRO turnover (Ankush Arora left Feb 2026). | local PDF; AGM; Q2 FY27 letter; https://www.marketscreener.com/quote/stock/TBO-TEK-LIMITED-169787519/company-governance/ |
| (f) Fraud / security, agentic DAST (`Fraud Prevention & Security.pdf`, a 6th problem statement not in the brief) | Very timely. In Q2 FY27 TBO booked an ₹8.1 Cr exceptional loss from "suspected collusion among certain current and former employees" at an overseas subsidiary. Suggested weights: findings and severity 30%, precision 20%, discovery/API inventory 20%, safety 10%, speed 10%, report 10%. Note that the problem statement is about **AppSec**, not transaction fraud. | Q2 FY27 letter; local PDF |

---

## 4. VoyageHack event

### VoyageHack 4.0 (current edition)
- **Platform:** Unstop. https://unstop.com/competitions/crp-voyagehack-40-tbocom-1774031 (fetched through the api.unstop.com mirror)
- **Registrations:** 13,107. Teams of 2–5, open to anyone, one team per person, free entry. Contact: voyagehacks@tbo.com (https://www.hiretoday.in/competitiondetails/40000244)
- **Timeline (IST):**
  - Registration closes **12 Nov 2026, 11:59 PM**
  - **Mandatory briefing webinar** (Microsoft Teams), where TBO leaders walk through the problem statements: **14 Nov 2026, 5:30–6:30 PM**
  - Idea submission: no dates on the page. **Assumption:** about 14–25 Nov, since prototype opens 26 Nov.
  - **Prototype submission:** 26 Nov 2026 12:00 PM to **24 Dec 2026 11:59 PM**
  - **Grand finale:** 8 Jan 2027, 10 AM–6 PM. Location not stated. 3.0's finale was at the Gurugram office, so Gurugram is likely (**assumption**).
  - The StartupGrantsIndia listing says "26 Oct 2026, online", which conflicts with Unstop. Treat Unstop as authoritative. (https://www.startupgrantsindia.com/events/voyagehack-40)
- **Round 1 (idea):**
  - A PPT/PDF covering **Potential Impact, Implementation & Technical Feasibility, Innovation, Adoption Risk/Feasibility**, plus a recorded video.
  - The Stages section says "**2-slide PPT** (excluding cover/thank-you)". One submission per team.
- **Round 2 (prototype):** a GitHub repo with run docs, an explainer video, and a 10-slide deck. Submitted as a zip.
- **Finale:** present to "jury panel and industry experts" and interact with TBO leadership.
- **Prizes:** ₹3L / ₹2L / ₹1L, each with a pre-placement interview. Finalists can interview for paid internships. Everyone gets a certificate.
- **Rubric:** no weighted overall rubric is published on Unstop. Per-problem weights appear only in some problem statement PDFs (HR and Security, see §3).

### Past editions
| Edition | Dates | Platform | Problem statement / notes | Source |
|---|---|---|---|---|
| VoyageHack (1.0) | about early 2024 (an IIIT-B story filed under Feb 2024) | – | IIIT-B team was 1st runner-up. Their problem was "Mashups – Packages, Calendar, and trip itineraries using Generative AI", built on TBO APIs. Only 7 teams reached the finale. The story calls it VoyageHack 2.0, which conflicts with 2.0 being Feb 2025, so the edition number is unclear. | https://naviiina.iiitb.ac.in/featured-story-in-february-2024/iiit-b-students-develop-award-winning-travel-solution-at-voyagehacks-hackathon/ (found by search; returned 404 when fetched) |
| VoyageHack 2.0 | Finale 13 Feb 2025, Gurugram office | – | "pan-India hackathon". Prizes included guaranteed paid internships and PPIs. | https://thejobcompany.co.in/frontend/job_details.php?job_id=2466 |
| VoyageHack 3.0 | Registration closed 21 Jan 2026; webinar 12 Jan; prototype 11 Feb–2 Mar 2026; finale ~10 Mar 2026, Gurugram | Unstop | Same format and prizes as 4.0. Problem statements were in a downloadable attachment that I could not access. | https://api.unstop.com/competitions/voyagehack-30-tbocom-1617332 |

- **Judges:** not named for any edition on any page I found. Registration counts for 1.0–3.0 were not found.
- **Theme continuity:** GenAI itineraries were a problem statement in an earlier edition, so judges have seen many itinerary bots before (inference, **assumption**).

---

## 5. Likely judges and what they have said
None are confirmed. Based on the "TBO leaders" and "leadership" wording on the event page, the likely jury is (**assumption**):

- **Akshat Varma (also spelled Verma)**, Whole-Time Director and **CTO**. (AGM transcript; https://stockanalysis.com/quote/nse/TBOTEK/company/) I found no public AI quotes from him.
- **Gaurav Bhatnagar**, Co-founder and Joint MD. He is the public voice on AI: the itinerary builder, the MCP connectors, "dearth of time", and luxury and complex trips (TTN, Oct 2026).
- **Ankush Nijhawan**, Co-founder and Joint MD. He speaks mostly about India air, cash flow and business performance. (NSE Q1 FY27 press release)
- **Nishant Misra**, listed as Chief Product Officer on Simply Wall St only, so unverified. (https://simplywall.st/stocks/in/consumer-services/bse-544174/tbo-tek-shares/management)
- Others: Vikas Jain (CFO); Deepak Khanna (listed as COO, Apr 2026); Aditi Madhok-Naarden (Global CHRO, a likely judge for the HR problem statement). (stockanalysis; MarketScreener)

Problem-statement owners may well sit on the jury: the OpsDesk PDF says "the TBO panel gives a new HR requirement on the day". They are not named.

---

## Gaps and unverified items
- I could not read the 12 Dec 2025 investor deck, so the "75% of tickets" and "~30% cost per search" figures are unverified. The Q2 FY27 earnings call transcript is paywalled (https://www.gurufocus.com/news/9172151/q2-2027-tbo-tek-limited-earnings-call-transcript).
- No public confirmation that TBO uses Zendesk or Darwinbox, other than the problem statement PDFs themselves.
- The meaning of TBOH as a booking-ID field is an assumption.
- The 4.0 finale venue and idea-round dates are not published.

## 10 most decision-relevant facts
1. **Hotels are the profit engine:** 64% of GTV and 87% of gross profit (Q2 FY26). Organic hotel gross profit is about 5.5% of GTV, and TBO is defending it under Middle East competition. Problem statements that move hotel conversion or margin, like multi-supplier dedup and ranking (PS b), touch TBO's core P&L.
2. **TBO already shipped an AI itinerary builder and Claude/ChatGPT MCP connectors** (Oct 2026), and an earlier VoyageHack already ran a GenAI itinerary problem. A virtual-agent entry must go well beyond itineraries, for example post-booking changes, disruptions and multi-product orchestration, or it will look derivative.
3. **The founders' AI thesis is advisor time-saving on complex, luxury trips** ("dearth of time"; Classic Vacations at $125M). Pitches framed as "saves agents hours on complex trips" match the leadership's language.
4. **"Lower cost to serve" plus "AI, simpler workflows"** is the main tech line in the latest shareholder letter. Ops automation (OpsDesk) and cost-per-task (HR) speak directly to it.
5. **Pre-buy runs against TBO's negative working capital model:** they pay hotels at or after check-in. Inventory optimisation must model risk and capital explicitly, and judges will likely probe adoption risk there.
6. **Hotel mapping is partly outsourced to Vervotech** (renewed May 2026). For PS (b), the differentiation is room-type mapping, sightseeing dedup that keeps inclusions apart, and supplier-reliability-aware ranking, not basic hotel matching.
7. **Round 1 is only 2 slides plus a video**, scored on Impact, Feasibility, Innovation and Adoption Risk. The briefing on 14 Nov is mandatory and registration closes 12 Nov 2026.
8. **13,107 registrations so far**, against about 7 finalists in an earlier edition. Expect a very harsh idea-round cut, so the slides must lead with a TBO-specific metric.
9. **The OpsDesk and HR problem statements publish detailed weights.** HR puts 40% on governance and extensibility and adds a live extension test at the finale. That is high engineering risk but well-specified. The ops problem statement uses real TBO concepts (TBOH, LCD, agency, refund loops) that make a domain-heavy demo easy to judge.
10. **Fraud/security is timely:** TBO just disclosed an ₹8.1 Cr insider-collusion loss and an ED/FEMA penalty in Q2 FY27. But that problem statement is agentic DAST/AppSec with its own weights, not transaction fraud, and it needs a test target environment.
