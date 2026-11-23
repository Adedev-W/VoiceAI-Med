from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).with_name("appointments.db")

def connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    with connection() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS doctors (id TEXT PRIMARY KEY, name TEXT NOT NULL, specialty TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS slots (id TEXT PRIMARY KEY, doctor_id TEXT NOT NULL, date TEXT NOT NULL, time TEXT NOT NULL, available INTEGER NOT NULL DEFAULT 1);
        CREATE TABLE IF NOT EXISTS appointments (id INTEGER PRIMARY KEY AUTOINCREMENT, phone TEXT NOT NULL, slot_id TEXT NOT NULL UNIQUE, status TEXT NOT NULL DEFAULT 'booked', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
        """)
        if db.execute("SELECT COUNT(*) FROM doctors").fetchone()[0] == 0:
            db.executemany("INSERT INTO doctors VALUES (?, ?, ?)", [("d1", "Dr. Maya Pratama", "General Practitioner"), ("d2", "Dr. Budi Santoso", "Cardiologist"), ("d3", "Dr. Sari Wijaya", "Dermatologist")])
            slots = [(f"{d}-{day}-{time}", d, day, time, 1) for d, times in [("d1", ["09:00", "10:30", "13:00"]), ("d2", ["09:30", "11:00", "14:00"]), ("d3", ["10:00", "12:30", "15:00"])] for day in ("2026-11-24", "2026-11-25", "2026-11-26") for time in times]
            db.executemany("INSERT INTO slots VALUES (?, ?, ?, ?, ?)", slots)

def rows(query: str, args: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    with connection() as db:
        return [dict(row) for row in db.execute(query, args).fetchall()]
