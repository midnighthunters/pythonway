"""
Mock Travel and Amex Concierge Services API.
Simulates real-world integration with Airline GDS, Chauffeur APIs, Hotel Property Management Systems,
Centurion Lounge Access Gateways, Resy/OpenTable Dining, and Amex Trip Protection Underwriting.
"""

from typing import Dict, Any, List
import datetime
import uuid


class FlightService:
    """Mock Airline GDS & Flight Operations Engine"""

    @staticmethod
    def search_alternative_flights(origin: str, destination: str) -> List[Dict[str, Any]]:
        return [
            {
                "id": "flt_dl482",
                "airline": "Delta Air Lines",
                "flight_number": "DL-482",
                "aircraft": "Airbus A350-900 (Delta One Suites)",
                "origin": origin,
                "origin_terminal": "Terminal 4",
                "destination": destination,
                "destination_terminal": "Terminal 3",
                "departure_time": "18:30 EST",
                "arrival_time": "21:45 PST",
                "cabin": "Delta One Suite (Lie-Flat)",
                "seat_assigned": "3A",
                "stops": 0,
                "fare_difference": 0.0,  # Amex Centurion waiver
                "source": "Amex Guaranteed Seat Inventory",
                "available_seats": 2,
            },
            {
                "id": "flt_ua1904",
                "airline": "United Airlines",
                "flight_number": "UA-1904",
                "aircraft": "Boeing 787-10 Dreamliner (Polaris)",
                "origin": origin,
                "origin_terminal": "Terminal 7",
                "destination": destination,
                "destination_terminal": "Terminal 7",
                "departure_time": "20:15 EST",
                "arrival_time": "23:25 PST",
                "cabin": "United Polaris Business",
                "seat_assigned": "4D",
                "stops": 0,
                "fare_difference": 0.0,
                "source": "Star Alliance Priority Desk",
                "available_seats": 4,
            },
            {
                "id": "flt_aa003_morning",
                "airline": "American Airlines",
                "flight_number": "AA-003",
                "aircraft": "Boeing 777-300ER (Flagship First)",
                "origin": origin,
                "origin_terminal": "Terminal 8",
                "destination": destination,
                "destination_terminal": "Terminal 4",
                "departure_time": "08:00 EST (Tomorrow)",
                "arrival_time": "11:20 PST (Tomorrow)",
                "cabin": "Flagship First Suite",
                "seat_assigned": "1A (VIP)",
                "stops": 0,
                "fare_difference": 0.0,
                "source": "Carrier Protected Next-Day Priority",
                "available_seats": 1,
            }
        ]

    @staticmethod
    def rebook_flight(pnr: str, new_flight: Dict[str, Any]) -> Dict[str, Any]:
        new_pnr = f"AMX{uuid.uuid4().hex[:4].upper()}"
        return {
            "status": "SUCCESS",
            "old_pnr": pnr,
            "new_pnr": new_pnr,
            "rebooked_flight": new_flight,
            "e_ticket_number": f"006-{uuid.uuid4().int % 1000000000:09d}",
            "carrier_confirmation": "CONFIRMED_GDS_SYNCHRONIZED",
            "rebooked_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


class ChauffeurService:
    """Mock Blacklane & Executive Ground Transportation API"""

    @staticmethod
    def adjust_pickup_time(booking_ref: str, new_pickup_time: str, flight_number: str) -> Dict[str, Any]:
        return {
            "status": "SUCCESS",
            "booking_ref": booking_ref,
            "new_pickup_time": new_pickup_time,
            "tracked_flight": flight_number,
            "chauffeur_status": "DISPATCH_SYNCHRONIZED",
            "fee_charged": 0.0,
            "message": f"Chauffeur pickup successfully shifted to {new_pickup_time} to match flight {flight_number} arrival."
        }

    @staticmethod
    def cancel_ride_with_waiver(booking_ref: str, reason: str) -> Dict[str, Any]:
        return {
            "status": "CANCELLED_FEE_WAIVED",
            "booking_ref": booking_ref,
            "refund_amount": 240.0,
            "fee_penalty": 0.0,
            "reason": reason,
            "waiver_authority": "Amex Centurion Premium Transport Coverage"
        }


class HotelService:
    """Mock Luxury Hotel & Amex Fine Hotels & Resorts (FHR) PMS API"""

    @staticmethod
    def extend_arrival_window(reservation_code: str, new_eta: str) -> Dict[str, Any]:
        return {
            "status": "GUARANTEED_LATE_ARRIVAL_LOCKED",
            "reservation_code": reservation_code,
            "guaranteed_arrival_time": new_eta,
            "room_hold_status": "SECURED_ALL_NIGHT",
            "amenities_alert": "Welcome bottle of Krug Champagne & fruit presentation placed in suite",
            "fee": 0.0
        }

    @staticmethod
    def shift_checkin_date(reservation_code: str, new_date: str) -> Dict[str, Any]:
        return {
            "status": "DATES_MODIFIED",
            "reservation_code": reservation_code,
            "new_check_in": new_date,
            "penalty_waived": True,
            "waiver_reason": "Amex Fine Hotels & Resorts Flight Disruption Guarantee"
        }

    @staticmethod
    def cancel_stay_with_full_refund(reservation_code: str) -> Dict[str, Any]:
        return {
            "status": "CANCELLED_FULL_REFUND",
            "reservation_code": reservation_code,
            "refund_issued": 5850.0,
            "cancellation_fee": 0.0,
            "insurance_code": "AMX-FHR-DISRUPTION-CLAIM"
        }


class LoungeService:
    """Mock Amex Centurion Lounge Access System"""

    @staticmethod
    def extend_or_reissue_pass(airport: str, terminal: str, new_window: str) -> Dict[str, Any]:
        return {
            "status": "PASS_EXTENDED",
            "lounge_name": f"The Centurion® Lounge - {airport}",
            "terminal": terminal,
            "valid_window": new_window,
            "new_barcode": f"AMX-CENT-{airport}-{uuid.uuid4().hex[:6].upper()}",
            "access_tier": "Centurion Member Priority (Complimentary Speakeasy & Private Studio)",
            "guest_allowance": 2
        }


class DiningService:
    """Mock Global Dining Access by Resy / VIP Dining API"""

    @staticmethod
    def reschedule_or_hold_table(reservation_ref: str, new_time: str) -> Dict[str, Any]:
        return {
            "status": "TABLE_RESCHEDULED",
            "reservation_ref": reservation_ref,
            "new_time": new_time,
            "table_type": "VIP Chef's Tasting Table / Oceanfront Hold",
            "penalties_waived": 200.0,
            "host_notes": "Guest flight delayed - Amex Platinum Concierge Priority Hold applied"
        }

    @staticmethod
    def cancel_dining_with_full_waiver(reservation_ref: str, reason: str) -> Dict[str, Any]:
        return {
            "status": "CANCELLED_FEE_WAIVED",
            "reservation_ref": reservation_ref,
            "waived_penalty_amount": 200.0,
            "waiver_code": "AMX-RESY-CONCIERGE-DISRUPTION-PROTECTION",
            "note": "Late cancellation fee ($100/guest) completely waived via Global Dining Access policy."
        }


class AmexInsuranceService:
    """Amex Trip Delay & Cancellation Protection Underwriting Engine"""

    @staticmethod
    def file_trip_interruption_claim(card_last4: str, items_impacted: List[str], claim_amount: float) -> Dict[str, Any]:
        claim_id = f"CLM-AMX-{uuid.uuid4().hex[:6].upper()}"
        return {
            "claim_id": claim_id,
            "card_account": f"•••• {card_last4}",
            "status": "APPROVED_INSTANT_CREDIT",
            "coverage_type": "Amex Centurion Comprehensive Trip Delay & Cancellation Protection",
            "approved_amount": claim_amount,
            "items_covered": items_impacted,
            "statement_credit_eta": "Within 24 business hours"
        }
