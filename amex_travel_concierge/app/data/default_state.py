"""
Default travel data and user profile state for the Amex Travel Concierge Application.
Contains detailed records for: Flights, Cabs, Hotels, Lounges, and Dining.
"""

from typing import Dict, Any
import copy

INITIAL_USER_PROFILE = {
    "user_id": "usr_amex_centurion_84001",
    "name": "Alexander V. Vance",
    "card_tier": "Centurion",
    "card_name": "The Centurion® Card",
    "card_last4": "84001",
    "member_since": "17",
    "points_balance": 482910,
    "tier_status": "Centurion Member & Amex Global Dining VIP",
    "trip_protection_active": True,
    "trip_protection_limit": 10000.0,
    "concierge_phone": "1-800-525-3355",
    "avatar_initials": "AV",
}

INITIAL_ITINERARY: Dict[str, Any] = {
    "flight": {
        "id": "flt_aa1420",
        "airline": "American Airlines",
        "flight_number": "AA-1420",
        "aircraft": "Boeing 777-300ER (Flagship First)",
        "origin": "JFK",
        "origin_name": "New York John F. Kennedy",
        "origin_terminal": "Terminal 8",
        "origin_gate": "B22",
        "destination": "LAX",
        "destination_name": "Los Angeles International",
        "destination_terminal": "Terminal 4",
        "scheduled_departure": "15:45 EST",
        "scheduled_arrival": "19:10 PST",
        "seat": "2B (Flagship First Suite)",
        "pnr": "AMX7X9",
        "status": "ON_TIME",  # ON_TIME, CANCELLED, DELAYED, REBOOKED
        "status_color": "green",
        "carrier_code": "AA",
        "ticket_price": 2850.0,
        "is_disrupted": False,
        "disruption_note": None,
    },
    "cab": {
        "id": "cab_blacklane_9921",
        "service_provider": "Blacklane Executive Chauffeur",
        "vehicle_model": "Mercedes-Benz S-Class (Black Edition)",
        "pickup_location": "LAX Bradley International Arrivals - VIP Curbside",
        "pickup_time": "19:40 PST",
        "dropoff_location": "The Beverly Hills Hotel, 9641 Sunset Blvd",
        "driver_name": "Marcus Thorne",
        "driver_phone": "+1 (310) 555-0199",
        "booking_ref": "BL-LAX-88210",
        "fare": 240.0,
        "status": "CONFIRMED",  # CONFIRMED, RESCHEDULED, CANCELLED
        "status_color": "green",
        "free_cancellation_until": "18:40 PST",
    },
    "hotel": {
        "id": "htl_beverly_hills",
        "property_name": "The Beverly Hills Hotel & Bungalows",
        "brand": "Dorchester Collection",
        "room_type": "Bungalow Garden Suite with Fireplace",
        "check_in_date": "Today",
        "check_out_date": "In 3 Days",
        "scheduled_check_in_time": "20:30 PST",
        "guaranteed_late_check_in": True,
        "reservation_code": "BHH-AMX-5519",
        "nightly_rate": 1950.0,
        "total_stay_cost": 5850.0,
        "status": "CONFIRMED",  # CONFIRMED, CHECK_IN_EXTENDED, RESCHEDULED, CANCELLED
        "status_color": "green",
        "amex_benefit": "Fine Hotels & Resorts®: $100 Property Credit, Complimentary Breakfast, 4 PM Late Checkout",
    },
    "lounge": {
        "id": "lng_centurion_jfk",
        "lounge_name": "The Centurion® Lounge - JFK",
        "airport": "JFK",
        "terminal": "Terminal 4 (Post-Security, Level 2)",
        "valid_window": "13:00 - 15:45 EST",
        "barcode_code": "AMX-CENT-JFK-99824",
        "amenities": "1850 Speakeasy Cocktail Bar, Chef Ignacio Mattos Cuisine, Private Phone Booths, High-Speed Wi-Fi",
        "status": "ACTIVE",  # ACTIVE, EXPIRED, REISSUED
        "status_color": "green",
        "priority_access": True,
    },
    "dinner": {
        "id": "din_nobu_malibu",
        "restaurant_name": "Nobu Malibu",
        "reservation_time": "20:45 PST",
        "guests": 2,
        "table_type": "Prime Oceanfront Patio Terrace",
        "reservation_ref": "RSY-NOBU-7731",
        "cancellation_policy": "$100 per guest fee if cancelled under 6 hours without certified travel waiver",
        "potential_fee": 200.0,
        "status": "CONFIRMED",  # CONFIRMED, RESCHEDULED, CANCELLED_FEE_WAIVED
        "status_color": "green",
        "amex_benefit": "Global Dining Access by Resy - VIP Priority Table & Complimentary Chef Amuse-Bouche",
    }
}


def get_fresh_itinerary() -> Dict[str, Any]:
    """Returns a deep copy of the pristine itinerary."""
    return copy.deepcopy(INITIAL_ITINERARY)


def get_fresh_user_profile() -> Dict[str, Any]:
    """Returns a deep copy of the user profile."""
    return copy.deepcopy(INITIAL_USER_PROFILE)
