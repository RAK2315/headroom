# Obvious set (banned as-is)

These are the ideas most teams will submit. A candidate may reuse one only if its twist is the reason it wins.

## PS1 Inventory Optimization (pre-buy)
1. Prophet / XGBoost demand forecast on the Kaggle "Hotel Booking Demand" dataset + a Streamlit dashboard of charts.
2. Knapsack / LP budget allocation that outputs a table of "buy X rooms at hotel Y".
3. "AI analyst" chatbot that answers questions over the booking data (text-to-SQL).
4. Heatmap of destinations by demand.

## PS2 Multi-Supplier Optimization
1. Fuzzy string match (name + address) + lat/long distance threshold to dedupe hotels, shown as a merged table.
2. Send pairs to an LLM: "are these the same hotel?"
3. Weighted-score ranking (price, rating, cancellation) on a listing page.
4. Image dedupe with CLIP embeddings.

## PS3 Virtual Travel Agent
1. ChatGPT-style chat that writes a day-by-day itinerary (thin wrapper, hallucinated prices).
2. LangGraph/CrewAI multi-agent "flight agent + hotel agent + planner agent" on mock JSON.
3. Voice travel assistant.
4. Itinerary on a map with drag-to-reorder.
5. Post-booking FAQ chatbot over a voucher PDF.

## PS4 OpsDesk (Zendesk replacement)
1. CRUD ticket app (Kanban + list) with LLM intent classification.
2. Same + SLA countdown timers + dashboard charts.
3. "AI summarise ticket" button.

## PS5 AI-native HR (Darwinbox replacement)
1. LangGraph onboarding agent + approval inbox + chat UI.
2. HR policy RAG helpdesk chatbot.
3. Resume screening ranker.

## Expected crowding (guess, organizer has not published counts)
PS3 Virtual Travel Agent: highest (every team knows "AI trip planner").
PS4 OpsDesk / PS5 HR: medium; detailed specs make submissions converge on the same feature list, so execution and polish decide.
PS1 Inventory: medium; data/ML teams.
PS2 Multi-Supplier: lowest; least glamorous-sounding, but closest to TBO's core economics.
