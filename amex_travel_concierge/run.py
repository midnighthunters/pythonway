"""
Convenience Runner for the Amex Travel Concierge FastAPI Application.
Starts Uvicorn server on http://localhost:8000 with hot-reloading.
"""

import sys
import os
import uvicorn

# Ensure the current directory is on PYTHONPATH
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  AMERICAN EXPRESS® TRAVEL CONCIERGE & LANGGRAPH DISRUPTION ENGINE")
    print("=" * 70)
    print("  Status: Server launching on http://localhost:8000")
    print("  Mobile UI: Open http://localhost:8000 in your browser")
    print("  Features: Multi-Modal Itinerary Tracking (Flight, Cab, Hotel, Lounge, Dinner)")
    print("  LangGraph: 8-Node Autonomous State Machine with Native HITL Interrupt")
    print("=" * 70 + "\n")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
