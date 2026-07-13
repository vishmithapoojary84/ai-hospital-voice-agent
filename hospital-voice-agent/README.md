# Hospital Voice Agent

A modern voice agent application designed for hospitals, facilitating appointment bookings, checking availability, and managing doctor interactions.

## Project Structure

```text
hospital-voice-agent/
│
├── backend/                  # FastAPI & Python AI Agent
│   ├── .venv/                # Python Virtual Environment
│   ├── app/
│   │   ├── agent/            # Agent logic, tools, and prompts
│   │   │   ├── voice_agent.py
│   │   │   ├── prompt.py
│   │   │   └── tools.py
│   │   ├── api/              # API endpoints and routers
│   │   │   └── routes.py
│   │   ├── database/         # Database models, schemas, and connection setup
│   │   │   ├── database.py
│   │   │   ├── models.py
│   │   │   └── schemas.py
│   │   ├── services/         # Business logic services
│   │   │   ├── booking_service.py
│   │   │   ├── availability_service.py
│   │   │   └── doctor_service.py
│   │   ├── utils/            # Helper utilities
│   │   │   └── helpers.py
│   │   ├── config.py         # Application configuration
│   │   └── main.py           # FastAPI entrypoint
│   ├── .env                  # Backend environment configurations (git-ignored)
│   └── requirements.txt      # Python dependencies list
│
├── frontend/                 # React & Vite frontend application
│   ├── public/               # Public assets
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Page layouts and views
│   │   ├── hooks/            # Custom React hooks
│   │   ├── services/         # Frontend API services
│   │   ├── App.jsx           # Main App component
│   │   └── main.jsx          # Frontend entrypoint
│   ├── package.json          # Node dependencies and scripts
│   └── vite.config.js        # Vite bundler config
│
└── .gitignore                # Project-wide gitignore config
```

## Tech Stack

* **Backend**: Python 3.12, FastAPI, SQLAlchemy, `uv` package manager.
* **AI Engine**: Google Gemini API via `google-genai` package.
* **Frontend**: React, Vite, Vanilla CSS.

## Getting Started

### Backend Setup

1. Make sure you have `uv` installed. If not, install it using:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. Navigate to the backend directory:
   ```bash
   cd backend
   ```
3. Initialize the environment and install dependencies:
   ```bash
   uv sync
   ```
4. Copy the environment variables and set your Gemini API key:
   ```bash
   cp .env.example .env  # configure keys
   ```
5. Run the FastAPI development server:
   ```bash
   uv run uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Run the Vite development server:
   ```bash
   npm run dev
   ```
