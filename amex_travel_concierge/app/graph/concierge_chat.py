"""
Amex Travel Concierge Conversational Agent.
Allows cardmembers to converse with an AI Travel Concierge powered by Groq LLM,
with deep contextual knowledge of the current LangGraph state, flight disruption,
hotel holds, lounge privileges, and fine dining reservations.
"""

from typing import Dict, Any, List
import datetime
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

try:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
    from config import get_llm
    LLM_AVAILABLE = True
except Exception:
    LLM_AVAILABLE = False


CONCIERGE_SYSTEM_PROMPT = """You are the American Express Centurion & Platinum Travel Concierge, an elite executive AI travel counselor.
You are assisting Mr. Alexander V. Vance (Centurion Cardmember since 2017, Member #•••• 84001).
His travel itinerary includes:
- Flight: American Airlines AA-1420 (JFK ➔ LAX) - Recently Cancelled due to weather/ATC
- Chauffeur: Blacklane Executive Mercedes-Benz S-Class at LAX
- Hotel: The Beverly Hills Hotel & Bungalows (Fine Hotels & Resorts® VIP booking)
- Lounge: The Centurion® Lounge at JFK Terminal 4
- Dining: Nobu Malibu (Global Dining Access by Resy VIP table)

Tone & Style:
- Professional, ultra-refined, confident, empathetic, and exceptionally clear.
- Always reassure the cardmember of their Amex Centurion & Platinum protections ($10,000 trip protection, waived fees, guaranteed inventory).
- Clearly explain downstream impacts on their chauffeur, hotel room hold, lounge access, and dinner reservation.
- Guide them through their 3 recovery options (Option 1: Express Delta One Same-Day; Option 2: Luxury Overnight Rest at JFK TWA Hotel + Flagship First tomorrow; Option 3: Full Trip Cancellation & $8,940 Refund).
- Format responses cleanly with concise bullet points where appropriate.
"""


def chat_with_concierge(user_message: str, current_state: Dict[str, Any], chat_history: List[Dict[str, str]] = None) -> str:
    """
    Sends user query to Groq LLM with full LangGraph itinerary context.
    Provides intelligent fallback if LLM is unavailable or encounters error.
    """
    if chat_history is None:
        chat_history = []

    itinerary = current_state.get("itinerary", {})
    flight = itinerary.get("flight", {})
    cab = itinerary.get("cab", {})
    hotel = itinerary.get("hotel", {})
    lounge = itinerary.get("lounge", {})
    dinner = itinerary.get("dinner", {})
    disruption = current_state.get("disruption", {})
    options = current_state.get("options", [])
    workflow_status = current_state.get("workflow_status", "IDLE")

    context_summary = f"""
Current Itinerary Snapshot:
- Flight: {flight.get('airline')} {flight.get('flight_number')} ({flight.get('origin')} ➔ {flight.get('destination')}), Status: {flight.get('status')}
- Cab: {cab.get('service_provider')} ({cab.get('pickup_time')}), Status: {cab.get('status')}
- Hotel: {hotel.get('property_name')} ({hotel.get('scheduled_check_in_time')}), Status: {hotel.get('status')}
- Lounge: {lounge.get('lounge_name')} ({lounge.get('valid_window')}), Status: {lounge.get('status')}
- Dinner: {dinner.get('restaurant_name')} ({dinner.get('reservation_time')}), Status: {dinner.get('status')}
- Disruption Reason: {disruption.get('reason', 'None')}
- Workflow Status: {workflow_status}
- Number of Recovery Options Ready: {len(options)}
"""

    if LLM_AVAILABLE:
        try:
            llm = get_llm(temperature=0.3)
            messages = [
                SystemMessage(content=CONCIERGE_SYSTEM_PROMPT + "\n\n" + context_summary)
            ]
            for msg in chat_history[-6:]:
                if msg.get("role") == "user":
                    messages.append(HumanMessage(content=msg.get("content", "")))
                elif msg.get("role") == "assistant":
                    messages.append(AIMessage(content=msg.get("content", "")))

            messages.append(HumanMessage(content=user_message))
            response = llm.invoke(messages)
            return response.content
        except Exception as e:
            print(f"[CONCIERGE_CHAT] LLM Error: {e}, using heuristic response.")

    # Graceful high-quality heuristic response
    user_lower = user_message.lower()
    if "dinner" in user_lower or "nobu" in user_lower:
        return (
            "Regarding your reservation at Nobu Malibu: because your flight was cancelled due to carrier weather delays, "
            "your Global Dining Access by Resy policy completely waives the $200 late cancellation fee. "
            "If you select Option 1 (Express Re-route), we have secured a late VIP seating for you at 22:45 PST. "
            "Alternatively, with Option 2, we will cancel tonight without fee and reserve prime seating at Spago Beverly Hills for tomorrow evening."
        )
    elif "hotel" in user_lower or "beverly" in user_lower:
        return (
            "Your stay at The Beverly Hills Hotel & Bungalows is protected under Amex Fine Hotels & Resorts®. "
            "We have placed an automatic VIP late arrival lock on your Bungalow Suite so your room will not be released. "
            "If you prefer to fly tomorrow morning (Option 2), your reservation dates will be shifted at zero penalty."
        )
    elif "cab" in user_lower or "driver" in user_lower or "blacklane" in user_lower:
        return (
            "Your Blacklane chauffeur, Marcus Thorne, has been notified of the flight disruption. "
            "Under our executive transfer guarantee, the driver dispatch is on hold with zero waiting charges, "
            "and will automatically adjust curbside pickup to match your confirmed replacement flight."
        )
    elif "refund" in user_lower or "cancel" in user_lower or "insurance" in user_lower:
        return (
            "Under your Centurion Card Comprehensive Trip Protection, you are covered up to $10,000 for unexpected cancellations. "
            "Selecting Option 3 will immediately initiate a full refund of $8,940 back to your Centurion Card ending in 84001, "
            "plus a courtesy credit of 25,000 Membership Rewards points."
        )
    else:
        return (
            f"Mr. Vance, I am continuously monitoring your journey. With Flight {flight.get('flight_number')} cancelled, "
            f"your 3 multi-modal recovery options are ready in the Disruption Hub. "
            f"Option 1 gets you to Los Angeles tonight on Delta One (dep 18:30 EST) with all cab, hotel, and dining synchronized. "
            f"Would you like me to confirm Option 1 for you?"
        )
