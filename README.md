# AI Hospital Voice Receptionist

An AI-powered voice receptionist that allows patients to book, reschedule, cancel appointments, and view appointment history using natural voice conversations.

The application provides a phone-call-like experience by combining speech recognition, large language models, text-to-speech, and backend appointment management.

---

## Features

- Voice-based appointment booking
- Appointment rescheduling
- Appointment cancellation
- Appointment history retrieval
- Doctor availability checking
- English and Hindi conversation support
- Natural voice interaction
- AI-powered conversation handling

---

## Tech Stack

### Frontend
- React
- Vite
- Tailwind CSS

### Backend
- FastAPI
- PostgreSQL

### AI & Voice Services
- LiveKit
- Deepgram (Speech-to-Text)
- Google Gemini
- ElevenLabs (Text-to-Speech)
- Silero Voice Activity Detection (VAD)

---

## Project Architecture

```
Patient
    │
    ▼
React Frontend
    │
    ▼
LiveKit
    │
    ▼
Deepgram STT
    │
    ▼
Google Gemini LLM
    │
    ▼
Function Calling
    │
    ├── Check Doctor Availability
    ├── Book Appointment
    ├── Reschedule Appointment
    ├── Cancel Appointment
    └── Appointment History
    │
    ▼
FastAPI Backend
    │
    ▼
PostgreSQL Database
    │
    ▼
ElevenLabs TTS
    │
    ▼
Voice Response
```

---

## Project Structure

```
ai-hospital-voice-agent/

├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── backend/
│   ├── app/
│   ├── routes/
│   ├── database/
│   └── main.py
│
├── ai_agent/
│   ├── voice_agent.py
│   ├── tools.py
│   ├── prompts.py
│   ├── config.py
│   └── logger.py
│
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/vishmithapoojary84/ai-hospital-voice-agent.git

cd ai-hospital-voice-agent
```

---

## Backend Setup

```bash
cd backend

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

## AI Agent Setup

```bash
cd ai_agent

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

python voice_agent.py dev
```

---

## Environment Variables

Create a `.env` file inside the AI Agent directory.

```env
GEMINI_API_KEY=

GEMINI_MODEL=

LIVEKIT_URL=

LIVEKIT_API_KEY=

LIVEKIT_API_SECRET=

DEEPGRAM_API_KEY=

ELEVEN_API_KEY=

BACKEND_URL=
```

---

## Demo

The project demonstrates:

- Voice appointment booking
- Doctor selection
- Appointment rescheduling
- Appointment cancellation
- Appointment history
- English and Hindi conversations
- Natural AI voice responses

---

## Deployment

### Frontend

https://ai-hospital-voice-agent-1.onrender.com/

### Backend

https://ai-hospital-voice-agent.onrender.com

---

## GitHub Repository

https://github.com/vishmithapoojary84/ai-hospital-voice-agent

---

## Future Improvements

- Patient authentication
- Multiple hospital support
- Doctor dashboard
- SMS/Email appointment reminders
- Calendar integration
- Medical record integration

---

## Author

**Vishmitha Poojary**



AI | Backend | Full Stack Development
