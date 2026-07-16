# AI Hospital Voice Receptionist

An intelligent, voice-driven AI receptionist designed for healthcare facilities. This application enables patients to seamlessly book, reschedule, cancel, and review their appointments through natural, real-time voice conversations. 

Built using a modern stack featuring React, FastAPI, LiveKit, and Google Gemini, it provides a highly responsive, human-like interaction experience with support for both English and Hindi.

## Table of Contents

- [Features](#features)
- [Architecture & Tech Stack](#architecture--tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Deployment](#deployment)
- [Future Enhancements](#future-enhancements)
- [Author](#author)

## Features

- **Voice-Based Appointment Management:** Book, reschedule, or cancel appointments using natural voice commands.
- **Multilingual Support:** Communicate fluently in English and Hindi.
- **Real-Time Doctor Availability:** Automatically checks and suggests available time slots and doctors.
- **Appointment History:** Patients can query their past and upcoming appointments.
- **Low-Latency Voice Interactions:** Powered by LiveKit, Deepgram, and ElevenLabs for real-time speech-to-text and text-to-speech capabilities.
- **Intelligent Conversations:** Uses Google Gemini for context-aware, empathetic, and professional healthcare interactions.

## Architecture & Tech Stack

The system is composed of three main microservices: a frontend client, a backend API, and an AI voice agent.

### Tech Stack
- **Frontend:** React, Vite, Tailwind CSS
- **Backend:** FastAPI, PostgreSQL, SQLAlchemy
- **AI & Voice Services:** 
  - LiveKit (Real-time WebRTC infrastructure)
  - Deepgram (Fast Speech-to-Text)
  - Google Gemini (Large Language Model)
  - ElevenLabs (High-quality Text-to-Speech)
  - Silero VAD (Voice Activity Detection)

### System Flow
1. **User Interaction:** Patient speaks to the React frontend.
2. **Audio Streaming:** Audio is streamed via LiveKit to the AI Agent.
3. **Transcription & Processing:** Deepgram transcribes the audio; Google Gemini determines the user's intent.
4. **Action Execution:** If an action is required (e.g., booking), the AI Agent triggers a function call to the FastAPI backend.
5. **Database Operation:** FastAPI interacts with PostgreSQL to read/write data.
6. **Voice Synthesis:** Gemini's text response is converted to speech by ElevenLabs and streamed back to the patient.

## Prerequisites

Before starting, ensure you have the following installed on your system:
- Node.js (v18 or higher)
- Python (3.10 or higher)
- PostgreSQL
- API Keys for LiveKit, Deepgram, ElevenLabs, and Google Gemini

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/vishmithapoojary84/ai-hospital-voice-agent.git
cd ai-hospital-voice-agent
```

### 1. Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Frontend Setup

```bash
cd frontend
npm install
```

### 3. AI Agent Setup

```bash
cd ai_agent
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the `ai_agent` directory and populate it with your API keys:

```env
# Google Gemini
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-1.5-flash

# LiveKit
LIVEKIT_URL=your_livekit_url
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret

# Voice Services
DEEPGRAM_API_KEY=your_deepgram_api_key
ELEVEN_API_KEY=your_elevenlabs_api_key

# Backend API
BACKEND_URL=http://localhost:8000
```

*Note: You may also need a `.env` file in the `backend` directory containing your PostgreSQL database URL, depending on your database configuration.*

## Running the Application

To run the full stack locally, you need to start all three services in separate terminal windows.

### Start the Backend
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

### Start the Frontend
```bash
cd frontend
npm run dev
```

### Start the AI Agent
```bash
cd ai_agent
source .venv/bin/activate
python voice_agent.py dev
```

The frontend should now be accessible at `http://localhost:5173`.

## Project Structure

```text
ai-hospital-voice-agent/
├── frontend/                 # React UI for the voice client
│   ├── src/
│   ├── public/
│   └── package.json
├── backend/                  # FastAPI server handling business logic
│   ├── app/
│   │   ├── api/
│   │   ├── database/
│   │   └── models/
│   ├── requirements.txt
│   └── main.py
├── ai_agent/                 # LiveKit worker running the voice pipeline
│   ├── voice_agent.py
│   ├── tools.py              # Function calling tools for Gemini
│   ├── prompts.py            # System prompts and instructions
│   ├── config.py
│   └── requirements.txt
└── README.md
```

## Deployment

The application is designed to be easily deployed to modern cloud platforms:

- **Frontend:** [https://ai-hospital-voice-agent-1.onrender.com/](https://ai-hospital-voice-agent-1.onrender.com/)
- **Backend:** [https://ai-hospital-voice-agent.onrender.com](https://ai-hospital-voice-agent.onrender.com)
- **AI Agent:** Can be deployed to a standard VPS or containerized platform.

## Future Enhancements

- Implementation of patient authentication and authorization.
- Support for multiple hospital branches and varied clinic schedules.
- A comprehensive doctor/admin dashboard for managing appointments.
- Automated SMS and Email appointment confirmations and reminders.
- Calendar integration (Google Calendar/Outlook).
- Electronic Health Record (EHR) integration.

## Author

**Vishmitha Poojary**
- AI | Backend | Full Stack Development
- GitHub: [vishmithapoojary84](https://github.com/vishmithapoojary84)
