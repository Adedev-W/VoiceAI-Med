"""VoiceAI Med appointment booking application."""

__version__ = "0.2.0"

def main() -> None:
    import uvicorn
    uvicorn.run("voiceai_med.main:app", host="127.0.0.1", port=8000, reload=False)
