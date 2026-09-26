# 💳 American Express Travel Concierge: Advanced Multi-Modal Disruption Graph

The complete, advanced LangGraph project with the **American Express Mobile App UI** has been created in the dedicated directory:
👉 **[`amex_travel_concierge/`](file:///c:/Users/azureuser/PycharmProjects/Langraph/amex_travel_concierge)**

Detailed Architecture & Mermaid Diagrams are documented in:
👉 **[`amex_travel_concierge/LANGGRAPH_ARCHITECTURE.md`](file:///c:/Users/azureuser/PycharmProjects/Langraph/amex_travel_concierge/LANGGRAPH_ARCHITECTURE.md)**

---

## ⚡ Quick Start

To launch the FastAPI server and experience the Amex Mobile App:

```bash
# In the terminal (from project root):
.\.venv\Scripts\python.exe amex_travel_concierge\run.py
```

Then open your browser to:
**http://localhost:8000**

---

## 🧭 System Capabilities
- **Multi-Modal Tracking**: Real-time tracking of **Flights**, **Cabs**, **Hotels**, **Lounges**, and **Dinner**.
- **Autonomous Crisis Intervention**: Detects flight cancellation and evaluates cascaded impacts across all 4 downstream services.
- **LangGraph Pro 8-Node State Machine**:
  1. `itinerary_monitor_node`
  2. `downstream_impact_node`
  3. `amex_policy_node`
  4. `option_generator_node`
  5. `human_in_the_loop_node` (Native `interrupt()` breakpoint)
  6. `rebooking_orchestrator_node`
  7. `notification_synthesizer_node`
  8. `audit_telemetry_node`
- **Amex Mobile App UI**: Authentic Centurion & Platinum card design, embossed typography, Membership Rewards counter, bottom tab navigation, and live visual graph inspector.
