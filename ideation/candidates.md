# Candidates (generated before evaluation)

Format: id. user | pain | what it does | hero moment | technique

## PS1 Inventory Optimization
1. TBO contracting team | blind pre-buy decisions, unsold-room losses | "Allotment Trading Desk": every hotel×month allotment is an asset with a P10/P50/P90 demand forecast; a CVaR optimizer allocates the budget; efficient frontier of profit vs risk | drag the risk slider, the globe re-lights with buys and the ₹ expected profit/downside update live | 3 (trading terminal), 6
2. Contracting team | sell-outs discovered too late | "Sell-Out Radar": look-to-book spikes + event calendar flag hotels about to sell out and recommend pre-buy now | map pulses red 3 weeks before a sell-out in backtest | 2 (proactive), 6
3. Contracting team | prepaid allotments become dead money | price each allotment's release clause as a real option; recommend partial pre-buy + release date | "this 40-room block is worth ₹1.2L more with a 21-day release clause" | 3 (options pricing)
4. Contracting team | demand shocks (concerts, IPL, Diwali) | event-shock simulator: type "Coldplay Mumbai Jan 18" and see recommended buys | 3-second recommendation after event entry | 9
5. Finance | can't see capital tied up | backtest replay: replay last year with the plan vs actual, ₹ profit and sell-outs avoided | year replays as a time-lapse | 6
6. Contracting | no explanation for buys | LLM "investment memo" per recommendation | obvious set-ish | 1

## PS2 Multi-Supplier Optimization
7. TBO content team / agents | same room priced differently but names differ ("Dlx Dbl SV RO NR") | "Room Genome": decompose room names into structured attributes, match equivalent rooms across suppliers, reveal true cheapest bookable option | "same room, ₹2,300 cheaper from supplier C, previously invisible" | 5, 6
8. Agents booking sightseeing | duplicates hide real differences | "Experience Diff": cluster equivalent tours and show a git-style diff of inclusions (transfer, level 148 vs 124, meal, cancellation) | two "Burj Khalifa" tickets diffed line by line | 3 (code diff)
9. Agents | 14 listings of one Dubai hotel clutter results | multimodal golden record (photo+name+geo embeddings, Overture IDs as neutral anchor) | 14 cards collapse into one with the best rate | 6
10. Search team | ranking ignores supplier reliability | "bookability" rank: probability the price/room actually confirms at checkout per supplier | ranking reorders, failed-booking rate drops in replay | 2
11. Content team | poor images/descriptions | content enrichment picks best images across suppliers, flags mismatched photos | wrong-hotel photo flagged | 6
12. Product | can't measure ranking changes | counterfactual ranking replay on Expedia 2013 logs, conversion lift | before/after NDCG + ₹ | 3

## PS3 Virtual Travel Agent
13. B2B travel agent | messy client WhatsApp / Hinglish voice note -> hours building a quote | voice note -> priced, bookable itinerary + quote PDF with agent margin | 30-second quote from a voice note | 8, 5
14. Traveller + agent | a cancelled flight breaks hotel, transfer and tour | "Disruption Twin": itinerary as a dependency graph; on disruption the cascade turns red, agent proposes 3 repaired plans with cost deltas, asks confirmation, executes in Duffel test mode | live cancel -> red cascade -> repaired in 20s | 6, 5
15. Agent | hallucinated prices | price-verified itinerary with live badges | badge flips when price changes | 1
16. Agent | lives in Claude/ChatGPT | TBO MCP server + MCP Apps widgets | TBO already shipped connectors -> weak | 4

## PS4 OpsDesk
17. Ops agents / escalation managers | SLAs ignore travel urgency | "₹-at-risk queue": priority = cancellation penalty that kicks in at LCD × probability of miss; cases auto-linked by TBOH | queue reorders as the LCD clock runs; 3 refund tickets collapse into one case | 6
18. Ops lead | can't prove the new system is better | "Ops day replay": simulate 5,000 tickets under FIFO vs OpsDesk routing side by side; SLA breaches and ₹ penalties avoided | split-screen simulation | 3 (air traffic control), 9
19. Product | insights trapped | theme clusters auto-filed to backlog | cluster map | 6
20. Ops agents | side conversations break | supplier thread that survives transfer | spec item; low wow | 5

## PS5 AI-native HR
21. HR + exiting employee | new Labour Codes require F&F in 2 working days | exit workflow: Slack resignation -> rules compute F&F/gratuity/leave encashment -> named human accepts -> IT/Admin loops closed; ₹ cost per workflow meter | live "2-day F&F countdown" closes | 8 (regulation as user)
22. HR | can't extend HRMS | "workflow in YAML, live": add a new service line in 2 minutes during the demo | extension test rehearsal | 10

## Crosses
23. 7 + 8 + 9 + 10: "One Truth" unified multi-supplier layer: hotel golden record + Room Genome + Experience Diff + bookability ranking.
24. 1 + 2 + 4 + 5: Allotment Trading Desk with sell-out radar, event shocks and backtest replay.
25. 14 + 17: disruption detected -> OpsDesk case auto-opened with LCD ₹ exposure (cross-PS; risks being adjacent to both).
