 # VoiceAI Med

Voice appointment booking MVP with a FastAPI dashboard, SQLite mock clinic data, and Pipecat-ready function tools.

## Run locally

```bash
uv sync
uv run uvicorn voiceai_med.main:app --reload
```

For the Vite dashboard, run a second terminal:

```bash
cd src/voiceai_med/web
npm install
npm run dev
```

Open http://localhost:5173 during development. For a production bundle, run `npm run build`; FastAPI will serve `src/voiceai_med/web/dist` automatically. Set `ELEVENLABS_API_KEY` and `DEEPSEEK_API_KEY` in `.env` for provider configuration. Never commit `.env`.

The dashboard includes a realtime WebSocket voice-session control and browser microphone fallback. The current backend WebSocket remains a deterministic demo bridge until the Pipecat WebRTC transport is wired to the provider pipeline.

## Agent tools

`check_doctor_availability`, `book_appointment`, and `cancel_appointment` are defined in `voiceai_med.agent`. The dashboard WebSocket provides a deterministic demo bridge while the live Pipecat transport is connected to ElevenLabs STT/TTS and DeepSeek-compatible LLM providers.
