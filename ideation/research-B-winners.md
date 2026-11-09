# Research B — Past VoyageHack winners & comparable travel-tech hackathons

Compiled 2026-11-07. Every claim carries a URL. Items without a source are labelled **assumption**. LinkedIn pages were mostly rate-limited (HTTP 429/999), so some LinkedIn facts come from search-engine snippets of those pages and are marked "(via search snippet)".

---

## 0. Edition timeline (corrects the brief's year guesses)

| Edition | Run dates | Finale | Prizes | Source |
|---|---|---|---|---|
| VoyageHacks 1.0, branded "hackathon2024" | 3 Nov 2023 – 20 Jan 2024 | Jan 2024; IIIT-B news item dated 7 Jan (via snippet) | ₹5L or a Maldives trip / ₹2L / ₹1L | https://www.tbo.com/engagement/hackathon2024/ |
| VoyageHack 2.0 | Registration closed 18 Dec 2024 | 13 Feb 2025, TBO Gurugram | ₹3L or an international trip / ₹2L / ₹1L; finalists "guaranteed paid internships" | https://api.unstop.com/competitions/voyagehack-20-tbocom-1251347 , https://thejobcompany.co.in/frontend/job_details.php?job_id=2466 |
| VoyageHack 3.0 | Registration closed 21 Jan 2026; prototypes due 11 Feb – 2 Mar 2026 | Listed as 10 Mar 2026 (tentative); TBO staff posts say it was held on **16 March** | ₹3L / ₹2L / ₹1L, each with a PPI | https://api.unstop.com/competitions/voyagehack-30-tbocom-1617332 ; finale date from https://www.linkedin.com/in/bisma-rais-a772a3aa/ (via snippet) |
| VoyageHack 4.0 (current) | A TBO post says "Registrations close on 12 November 2026" | — | ₹6L total pool (₹3L / ₹2L / ₹1L) | https://in.linkedin.com/in/mohammad-afsar-0877b28b , https://unstop.com/competitions/crp-voyagehack-40-tbocom-1774031 |

**Format, the same in 2.0 and 3.0:**
- **Round 1:** a 2-slide deck (cover and thank-you slides excluded) plus a video. The deck covers Potential Impact, Implementation & Technical Feasibility, Innovation, and Adoption Risk/Feasibility.
- **Round 2:** a 10-slide deck, a GitHub repo with run docs, and an explainer video showing the workflow.
- **Finale:** the team presents to TBO leadership and a jury.

No scoring weights are published. Source: https://api.unstop.com/competitions/voyagehack-20-tbocom-1251347

**Funnel:** for 3.0, TBO posted "800+ ideas, 46 working prototypes, and 5 finalist teams" from 11,000+ registrations. For 2.0, a search snippet reports 13,000+ registrations and 800+ ideas. Sources: https://in.linkedin.com/in/bisma-rais-a772a3aa (fetched), https://www.linkedin.com/in/mohammad-afsar-0877b28b/ (via snippet). In 3.0, roughly 46 of 800 ideas (about 6%) became working prototypes, and 5 reached the finale.

---

## 1. Winners and finalists by edition

### VoyageHacks 1.0 (Nov 2023 – Jan 2024)
- **Winner:** not found.
- **1st runner-up:** IIIT-Bangalore iMTech students Shivankar Pilligundla, Hardik Khandelwal and Chaitanya Manas Cheedella. The IIIT-B story says only 7 teams reached the finale (via snippet): https://naviiina.iiitb.ac.in/featured-story-in-february-2024/iiit-b-students-develop-award-winning-travel-solution-at-voyagehacks-hackathon/ (the page now returns 404).
  - **Project:** a search snippet of that story says it "used real-time TBO APIs to fetch relevant and up-to-date data related to the user's refined itinerary", combining TBO APIs with GenAI. I could not confirm this on the live page.
  - **Probable repo:** https://github.com/CManas03/VoyageHacks (owner name matches Chaitanya Manas; Create-React-App boilerplate README; last updated 24 Dec 2023). The link between this repo and the winning team is an **assumption**.
- **Finale video:** "TBO Voyage Hacks 2024 Final!" https://www.youtube.com/watch?v=rSfPan30-g8. The content could not be extracted.
- **Theme known from a non-winning team:** "Mashups – Packages, Calendar, Itineraries (Generative AI)".
  - Team Unleashers built "Travel Buddy", a Gemini Pro itinerary generator aimed at travel agents: https://github.com/ashu-rb/Unleashers_Voyagehacks-TBO-Hackathon

### VoyageHack 2.0 (finale 13 Feb 2025)
- **Winners:** not found. One LinkedIn profile claims "National Winner, VoyageHack 2.0" but names no team (via snippet; page rate-limited): https://www.linkedin.com/in/amaldeep-patra-246bb8247/
- **Official problem statements:** not public (they sit in a PDF on Unstop). The submissions below suggest the themes were AI itinerary planning, agent recommendation, and group planning (**assumption** drawn from the repos).
  - **Swizzle**: AI itinerary planner with community and group-chat planning. Flutter + FastAPI + LangChain + Ollama, and it calls TBO flight-search APIs. https://github.com/Hackmey/VoyageHack2.0-public
  - **TBO SmartConnect**: package recommendations for travel agents, using logistic regression to rank packages by booking probability. Flask + React. https://github.com/Shubhamm1211/VoyageHack-TBO-SmartConnect
  - **Code-Voyagers**: https://github.com/solanki505/Code-Voyagers

### VoyageHack 3.0 (finale 16 Mar 2026) — podium confirmed by TBO staff
Source: https://in.linkedin.com/in/bisma-rais-a772a3aa and https://in.linkedin.com/in/mohammad-afsar-0877b28b (both fetched). Exact text:
"Team Travelers – Winner, IIIT Dards – 1st Runner-up, 404 Not Found – 2nd Runner-up".

| Place | Team | What we know |
|---|---|---|
| Winner | **Team Travelers** | No project found. A finalist on another team, Aditya Chavan (SPIT), posted that he heard "our name as winners", but the post gives no team or project (via snippet): https://www.linkedin.com/in/aditya-chavan-482ac/ . Whether he was on Team Travelers is **unverified**. |
| 1st runner-up | **IIIT Dards** (IIIT Delhi; Aditya Rai) | Fully documented below. Aditya Rai's portfolio lists "VOYAGEHACK 3.0 — First Runner-Up … top 2 of 11,000+": https://warhawkadi.github.io/ . He later interned at TBO (May–Jul 2026) on an "Enterprise Data Graph" team (same page). |
| 2nd runner-up | **404 Not Found** | No project found. |

**IIIT Dards — "TBO Assemble: The Operating System for Group Travel"**
- Repo: https://github.com/WarHawkADI/tbo-assemble
- Live demo: https://tbo-assemble-production.up.railway.app
- **Problem statement taken:** group inventory management for MICE events, destination weddings and corporate retreats, i.e. hotel room blocks.
- **One-line idea:** upload a hotel contract PDF and an invitation, and AI extracts room blocks, rates and attrition rules in under 60 seconds. The tool then auto-generates a branded guest microsite and tracks bookings and attrition live.
- **Tech:**
  - Frontend: Next.js 16, React 19, TypeScript, Tailwind v4, Radix
  - Data: Prisma + SQLite
  - AI and parsing: GPT-4o, plus `pdf-parse` with a tesseract.js OCR fallback
  - UI libraries: Recharts, @dnd-kit
  - Hosting: deployed on Railway
- **What the demo showed:**
  - Five pre-loaded sample contracts (Taj Lake Palace wedding, Marriott MICE, ITC Grand Chola, and others) for a "no-upload instant demo"
  - Drag-and-drop room allocator that honours proximity requests, with AI auto-allocation that explains its reasoning
  - Attrition tracker showing "at-risk revenue in ₹" with WhatsApp nudges (simulated)
  - QR check-in, GST invoices, cross-tab real-time sync, Hindi i18n
  - 42+ API routes
- **Notable claims:**
  - "What takes 3 days manually, TBO Assemble does in 30 minutes"
  - Attrition penalties of "10–30% of block value"
  - "4–6 hours wasted per event" on manual allocation
- **Does it use the TBO API?** The README does not mention it. The value story is ops automation and money at risk, not inventory search.

**Other 3.0 submissions (placement unknown — treat as non-winners unless proven otherwise)**

The repos point to at least two 3.0 tracks (**assumption**): a "Virtual Travel Agent Copilot" and "MICE / group event travel".

- **Khoj — Virtual Travel Agent Copilot** (Akash Mondal & Hitakshi): https://github.com/akash-mondal/khoj
  - Live TBO staging hotel API covering 307,640 Dubai hotel codes, with a full Search → PreBook → Book flow.
  - Client-preference memory, proactive alerts, and voice via Groq Whisper/Orpheus.
  - Ships a 3-minute DEMO_SCRIPT and states "100% live APIs — zero mocked data".
  - Its `TBO_API_FINDINGS.md` documents that the staging API field names differ from the official docs (`CheckIn`, `PaxRooms`, `HotelSearchResults`). This is very useful for 4.0 if the same API is supplied.
- **Smart Group Tour Platform** (MICE/weddings): https://github.com/divyanshupatel17/Smart-Group-Tour-Platform-VoyageHack
  - Claims "85% reduction in planning time, 3x conversion, 92% satisfaction", with no evidence given.
- **Roameo** (team Prakhar): https://github.com/OmkarLolage21/Prakhar-VoyageHack3.0
  - AI itinerary planner using phidata + Groq, TBO hotel/air APIs, and Sarvam voice in 10+ Indian languages.
- **Voyara**, budget-aware group itinerary planner: https://github.com/avirals14/voyage
- **Eastern Tigers** and **SigmaFigma.AI**, "TBO TravelAgent" assistants: https://github.com/subhchandan-003/VOYAGEHACK-3.0_Prototype_Eastern-Tigers , https://github.com/subhchandan-003/VOYAGEHACK-3.0_Prototype_SIgmaFigma.AI_IIM-Sambalpur

**Observation:** the only 3.0 project confirmed on the podium is a deep, ops-heavy B2B workflow tool (contracts → room blocks → attrition money at risk). Several well-built consumer and agent itinerary chatbots exist in the repo pool, but none is confirmed as a winner. This is suggestive, not proof (n=1 known podium project).

### VoyageHack 4.0 — competitor repos already public
These show the 4.0 tracks: Multi-Supplier Optimization, Inventory Optimization, and travel copilot.
- **TrueShelf** (Multi-Supplier Optimization track; README says all data is generated because "no TBO data is available to teams"): https://github.com/RaktimChandra/trueshelf
- **STOCKSHOCK** (Inventory Optimization track; demand forecasting on simulated history): https://github.com/aadityambk-del/stockshock
- **TBO-VoyAgent-AI** (multi-agent B2B copilot and multi-supplier bundler): https://github.com/arshsri0513/TBO-VoyAgent-AI
- **TrustScore Hotels** ("explainable data-trust layer over multi-supplier hotel search"): https://github.com/swarnnim/trustscore-hotels
- **Eventra**: https://github.com/swayamdharsingh/Eventra-Voyagehack

---

## 2. Theme recurrence

| Theme | 1.0 | 2.0 | 3.0 | 4.0 | Evidence |
|---|---|---|---|---|---|
| GenAI itinerary / packages "mashups" | ✔ (official theme name) | ✔ (repos) | ✔ (repos) | — | Unleashers README; Swizzle; Roameo |
| Travel-agent copilot / B2B agent assistant | ✔ ("Travel Buddy … our travel agents") | ✔ (SmartConnect) | ✔ ("Virtual Travel Agent Copilot", Khoj) | ✔ (VoyAgent) | repos above |
| Group / MICE / wedding inventory | — | partly (group itinerary) | ✔ (1st runner-up) | — | tbo-assemble |
| Multi-supplier / hotel data quality and mapping | — | — | — | ✔ (TrueShelf, TrustScore) | 4.0 repos |
| Inventory / demand forecasting | — | — | partly (Smart Group Tour "no-show prediction") | ✔ (STOCKSHOCK) | repos |
| Ops ticketing | not seen | not seen | not seen | ? | — |

The travel-agent copilot has appeared in every edition, so judges have seen many of them. A plain chatbot over TBO search is therefore a crowded category. (The crowding conclusion is an inference from the repo counts, i.e. an **assumption**.)

---

## 3. Comparable corporate travel hackathons

- **Amadeus Trav-Tech Hackathon 2025, Bangkok** (agentic AI; teams had to use at least one Amadeus Self-Service API plus Google Gemini/ADK; 11 industry teams): https://www.ttgasia.com/2025/10/06/agentic-ai-takes-centre-stage-at-amadeus-trav-tech-hackathon-2025/ , https://amadeus.com/en/newsroom/press-releases/travel-hackathon-to-boost-innovation-with-agentic-ai
  - **Winner:** Trip.com, "Click & Go", a personalised AI assistant to search, book and manage trips.
  - **1st runner-up:** Cleartrip, "MyTravel.ai", tailored inspiration.
  - **2nd runner-up:** Richmond Travels, "RABBIT", business-travel assistant.
  - **Hackers' Favorite:** AsiaOneClick, "FareSmart AI", an autonomous agent handling booking inquiries across channels for small operators.
  - **What the judge said:** Jerome Daniel (Amadeus) said Trip.com stood out for "innovation, dynamism, and near-market readiness" and that "intelligence without understanding the rules simply won't work". In other words, domain rules matter more than raw LLM ability.
- **MakeMyTrip Hackathon (HackerEarth, 2016):** the theme was apps for search, compare and book. No winners are published. https://www.hackerearth.com/challenges/hackathon/makemytrip-hackathon
- **Hotel dedup / entity matching:** I found no hackathon winners. The industry and academic state of the art is:
  - string + image similarity ML at 99.12% accuracy on 132k rows: https://acikerisim.isikun.edu.tr:443/xmlui/handle/11729/2248?show=full
  - Levenshtein + geo-clustering + a tree classifier (Quantiphi): https://quantiphi.com/case-study/hotel-content-delivery
  - false positives flagged as the main risk: https://travolution.com/news/guest-post-how-ai-can-offset-the-costs-of-hotel-supply-data-duplication

  These are useful benchmark claims if the team picks a mapping or dedup problem statement.
- **Expedia, Booking, Sabre, Agoda, Skyscanner, Flipkart GRiD, Amazon HackOn:** I found no theme-overlapping winners within the time-box. The Expedia story page (https://www.expedia.com/stories/building-new-travel-concepts-in-48-hours) was rate-limited.

---

## 4. Patterns — what these judges reward

1. **A working, deployed demo that judges can click, not slides.**
   - TBO Assemble shipped a live Railway URL and five pre-loaded sample contracts for a "no-upload instant demo": https://github.com/WarHawkADI/tbo-assemble
   - The Round 2 brief asks for a functional GitHub project plus a workflow video: https://api.unstop.com/competitions/voyagehack-20-tbocom-1251347
   - The funnel (800 ideas → 46 working prototypes → 5 finalists) suggests a working prototype is the main filter.
2. **A B2B, operator-side workflow with money at stake, ahead of consumer trip planning.**
   - The 3.0 1st runner-up quantified "at-risk revenue in ₹" and attrition penalties of "10–30% of block value". TBO is a B2B distributor serving agents and hotels.
   - At Amadeus, the peer favourite was an agent for operators' booking inquiries: https://www.ttgasia.com/2025/10/06/agentic-ai-takes-centre-stage-at-amadeus-trav-tech-hackathon-2025/
3. **One quantified headline claim**, such as "3 days → 30 minutes" (tbo-assemble). The Round 1 rubric starts with "Potential Impact" and also asks for "Adoption Risk/Feasibility": https://api.unstop.com/competitions/voyagehack-30-tbocom-1617332 . Back the claim with something real. Unbacked figures like "92% satisfaction" (Smart Group Tour) did not reach the known podium (**assumption** about cause).
4. **Domain-rule depth: model the industry's actual mechanics.**
   - Attrition rules, release dates, GST invoices, room blocks, Indian locale and WhatsApp in tbo-assemble.
   - Amadeus judge: "intelligence without understanding the rules simply won't work" (TTG Asia, above).
5. **Near-market readiness and polish.** Trip.com won partly on "near-market readiness" (TTG Asia). TBO Assemble invested in design-system polish: dark mode, i18n, validation, atomic transactions.
6. **GenAI turning messy documents into structured data that drives a workflow, not chat for its own sake.**
   - Contract PDF + OCR → structured event (tbo-assemble).
   - The 1.0 runner-up refined itineraries and pulled live TBO data (IIIT-B snippet, above).
7. **Using the sponsor's own platform/API, which counts but is not sufficient.**
   - The Amadeus hackathon required at least one Amadeus API.
   - Khoj's "100% live TBO APIs" is impressive but not confirmed as a podium entry: https://github.com/akash-mondal/khoj
   - The 3.0 1st runner-up did not foreground the TBO API.
   - For 4.0, teams report that no TBO data is provided (TrueShelf README), so realistic synthetic data plus a clean adapter seam is the norm.
8. **India-specific realism**, e.g. ₹, GST, WhatsApp, Hindi, Indian hotel brands and scenarios (tbo-assemble). Roameo also used Sarvam for Indic voice. Judges are TBO leadership in Gurugram. That this matters to them is an **assumption**, though plausible.

### Caveats
- The evidence base is thin: only one podium project (IIIT Dards, 3.0) is documented in detail. Team Travelers (the 3.0 winner), 404 Not Found, and all 1.0/2.0 winners have no public project write-up.
- Pattern 2 vs. "copilot" is a weak signal (n=1).
