 # VoiceAI Med

Voice appointment booking MVP with a FastAPI dashboard, SQLite mock clinic data, and Pipecat-ready function tools.

## Run locally

```bash
uv sync
uv run uvicorn voiceai_med.main:app --reload
```

Open http://localhost:8000. Set `ELEVENLABS_API_KEY` and `DEEPSEEK_API_KEY` in `.env` for provider configuration. Never commit `.env`; rotate any key that has been exposed.

## Agent tools

`check_doctor_availability`, `book_appointment`, and `cancel_appointment` are defined in `voiceai_med.agent`. The dashboard WebSocket provides a deterministic demo bridge while the live Pipecat transport is connected to ElevenLabs STT/TTS and DeepSeek-compatible LLM providers.
