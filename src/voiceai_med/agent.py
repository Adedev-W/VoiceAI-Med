from __future__ import annotations
import os
from typing import Any
from .services import availability, book_appointment, cancel_appointment

def appointment_tools() -> list[dict[str, Any]]:
    return [{"type":"function","function":{"name":"check_doctor_availability","description":"Find available doctor slots","parameters":{"type":"object","properties":{"doctor":{"type":"string"},"date":{"type":"string"}}}}},{"type":"function","function":{"name":"book_appointment","description":"Book a slot after confirming the spoken phone number","parameters":{"type":"object","required":["phone","slot_id"],"properties":{"phone":{"type":"string"},"slot_id":{"type":"string"}}}}},{"type":"function","function":{"name":"cancel_appointment","description":"Cancel using the confirmed spoken phone number","parameters":{"type":"object","required":["phone"],"properties":{"phone":{"type":"string"}}}}}]

def call_tool(name: str, args: dict[str, Any]) -> dict[str, Any]:
    if name == "check_doctor_availability": return {"slots": availability(args.get("doctor"), args.get("date"))}
    if name == "book_appointment": return book_appointment(args["phone"], args["slot_id"])
    if name == "cancel_appointment": return cancel_appointment(args["phone"])
    return {"success": False, "message": f"Unknown tool: {name}"}

def config_status() -> dict[str, bool]:
    return {"elevenlabs": bool(os.getenv("ELEVENLABS_API_KEY")), "deepseek": bool(os.getenv("DEEPSEEK_API_KEY"))}
