from __future__ import annotations
import re
from typing import Any
from .db import connection, rows

def normalize_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone)
    return f"+{digits}" if digits else phone.strip()

def doctors() -> list[dict[str, Any]]: return rows("SELECT * FROM doctors ORDER BY name")

def availability(doctor: str | None = None, date: str | None = None) -> list[dict[str, Any]]:
    query = "SELECT s.id, s.date, s.time, d.id doctor_id, d.name doctor, d.specialty FROM slots s JOIN doctors d ON d.id=s.doctor_id WHERE s.available=1"
    args: list[str] = []
    if doctor:
        query += " AND (d.id=? OR lower(d.name) LIKE lower(?) OR lower(d.specialty) LIKE lower(?))"; args += [doctor, f"%{doctor}%", f"%{doctor}%"]
    if date: query += " AND s.date=?"; args.append(date)
    return rows(query + " ORDER BY s.date, s.time", tuple(args))

def appointments() -> list[dict[str, Any]]:
    return rows("SELECT a.id, a.phone, a.status, s.id slot_id, s.date, s.time, d.name doctor, d.specialty FROM appointments a JOIN slots s ON s.id=a.slot_id JOIN doctors d ON d.id=s.doctor_id ORDER BY a.created_at DESC")

def book_appointment(phone: str, slot_id: str) -> dict[str, Any]:
    phone = normalize_phone(phone)
    with connection() as db:
        slot = db.execute("SELECT s.*, d.name doctor FROM slots s JOIN doctors d ON d.id=s.doctor_id WHERE s.id=? AND s.available=1", (slot_id,)).fetchone()
        if not slot: return {"success": False, "message": "Slot is no longer available."}
        db.execute("INSERT INTO appointments(phone, slot_id) VALUES (?, ?)", (phone, slot_id)); db.execute("UPDATE slots SET available=0 WHERE id=?", (slot_id,))
        return {"success": True, "message": f"Booked with {slot['doctor']} on {slot['date']} at {slot['time']}", "phone": phone}

def cancel_appointment(phone: str) -> dict[str, Any]:
    phone = normalize_phone(phone)
    with connection() as db:
        item = db.execute("SELECT a.id, a.slot_id, s.date, s.time, d.name doctor FROM appointments a JOIN slots s ON s.id=a.slot_id JOIN doctors d ON d.id=s.doctor_id WHERE a.phone=? AND a.status='booked' ORDER BY a.created_at DESC LIMIT 1", (phone,)).fetchone()
        if not item: return {"success": False, "message": "No active appointment found for that phone number."}
        db.execute("UPDATE appointments SET status='cancelled' WHERE id=?", (item["id"],)); db.execute("UPDATE slots SET available=1 WHERE id=?", (item["slot_id"],))
        return {"success": True, "message": f"Cancelled {item['doctor']} on {item['date']} at {item['time']}", "phone": phone}
