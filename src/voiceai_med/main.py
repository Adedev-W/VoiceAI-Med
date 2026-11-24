from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .agent import call_tool, config_status
from .db import init_db, rows
from .services import appointments, doctors
load_dotenv(); init_db()
app = FastAPI(title="VoiceAI Med")
WEB = Path(__file__).parent / "web"; DIST = WEB / "dist"
if DIST.exists(): app.mount("/assets", StaticFiles(directory=DIST / "assets"), name="assets")
else: app.mount("/static", StaticFiles(directory=WEB), name="static")
@app.get("/")
def index(): return FileResponse((DIST / "index.html") if DIST.exists() else WEB / "index.html")
@app.get("/api/doctors")
def get_doctors(): return doctors()
@app.get("/api/slots")
def get_slots(): return rows("SELECT s.*, d.name doctor, d.specialty FROM slots s JOIN doctors d ON d.id=s.doctor_id ORDER BY s.date,s.time")
@app.get("/api/appointments")
def get_appointments(): return appointments()
@app.get("/api/status")
def status(): return config_status()
@app.websocket("/ws")
async def voice_session(socket: WebSocket):
    await socket.accept(); await socket.send_json({"type":"status","message":"Connected. Pipecat session ready."})
    try:
        while True:
            message = await socket.receive_json()
            if message.get("type") == "tool_call":
                result = call_tool(message["name"], message.get("arguments", {})); await socket.send_json({"type":"tool_result","name":message["name"],"result":result}); await socket.send_json({"type":"data_refresh"})
            elif message.get("type") == "transcript": await socket.send_json({"type":"transcript","role":"assistant","text":"I heard you. Please choose a doctor or ask about available slots."})
    except Exception: await socket.close()
