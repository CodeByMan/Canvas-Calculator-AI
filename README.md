<div align="center">

# 🧮 AI Canvas Calculator — Multimodal Math Assistant

A FastAPI + Next.js portfolio application for interpreting user-drawn mathematical expressions and diagrams with Google Gemini.

![Python](https://img.shields.io/badge/Python-3.11%2B-3776ab?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Frontend-Next.js%2015-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![React](https://img.shields.io/badge/UI-React%2019-61dafb?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/Types-TypeScript-3178c6?style=for-the-badge&logo=typescript&logoColor=white)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285f4?style=for-the-badge&logo=google&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-13%20Backend-22c55e?style=for-the-badge)

</div>

---

## 📌 Project Overview

**AI Canvas Calculator** is a full-stack drawing calculator that lets users write mathematical expressions or draw graphical problems on a browser canvas. The FastAPI backend sends the submitted image to Google Gemini and returns validated, structured answers to the Next.js interface.

The project demonstrates multimodal AI integration, strict response validation, bounded API requests, and a responsive React canvas workflow. It is intentionally focused: there are no user accounts, database records, symbolic-math engine, or autonomous tool execution.

## ✨ Features

### 🎨 Drawing Workspace

- ✍️ Draw expressions, equations, and diagrams on a responsive canvas.
- 📱 Support pointer and touch drawing interactions.
- 🎨 Select drawing colors and clear the canvas.
- ↩️ Undo, redo, and reset the current drawing.
- 📋 Keep assigned variables available for later calculations in the current session.

### 🧠 AI-Assisted Calculation

- 🖼️ Send canvas images to a multimodal Google Gemini model.
- ➕ Interpret simple arithmetic expressions and variable assignments.
- 📐 Handle equation and graphical-math prompts according to the configured AI instructions.
- 🧾 Request structured `expr`, `result`, and `assign` fields.
- ✅ Validate AI output with Pydantic before returning it to the frontend.

### 🛡️ Reliability and Security Controls

- 🔐 Keep the Gemini API key on the backend only.
- 🚦 Apply per-client request rate limiting and bounded concurrent AI work.
- 📏 Enforce image byte, pixel, variable-count, and AI-response-size limits.
- 🌐 Allow only configured frontend origins through CORS.
- 🧹 Return stable public errors without exposing provider or internal exception details.
- 🧩 Parse structured AI responses without executing arbitrary code.

### 🖥️ Next.js Interface

- ⚛️ Responsive React 19 interface built with TypeScript.
- 🔄 Loading, success, and failure states for API requests.
- 🔔 User feedback through toast notifications.
- 👨‍💻 Developer attribution for Muhammad Ali Nawaz 2026.

## 🧰 Tech Stack

### Frontend

- Next.js 15
- React 19
- TypeScript
- Tailwind CSS
- Axios
- Lucide React
- Sonner

### Backend

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic
- Pillow

### AI and Validation

- Google Gemini API
- Multimodal image-and-prompt requests
- Pydantic response models
- Bounded structured-output parsing

### Quality Assurance

- Python `unittest`
- ESLint through Next.js
- TypeScript compiler checks
- Next.js production build checks
- pnpm production dependency audit
- GitHub Actions CI

## 📁 Folder Structure

```text
ai-canvas-calculator/
├── .github/workflows/ci.yml
├── backend/
│   ├── main.py
│   ├── schema.py
│   ├── constants.py
│   ├── requirements.txt
│   ├── src/calculator/
│   │   ├── route.py
│   │   └── utils.py
│   ├── tests/
│   │   ├── test_route.py
│   │   ├── test_schema.py
│   │   └── test_utils.py
│   └── vercel.json
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── package.json
│   ├── pnpm-lock.yaml
│   └── .env.example
├── README.md
└── .gitignore
```

## 🔐 Environment Variables

Never commit a real `.env` or `.env.local` file. Use the example files and keep provider credentials in the backend environment only.

### Backend `.env`

Copy `backend/.env.example` to `backend/.env` and set:

```env
GEMINI_API_KEY=your_gemini_api_key
FRONTEND_ORIGINS=http://localhost:3000
```

### Frontend `.env.local`

Copy `frontend/.env.example` to `frontend/.env.local`:

```env
NEXT_PUBLIC_BASE_API_URL=http://localhost:8000/api
```

`NEXT_PUBLIC_BASE_API_URL` is a public backend URL. Never place `GEMINI_API_KEY` in a `NEXT_PUBLIC_*` variable.

## 🚀 Getting Started on Windows

### Prerequisites

- Windows 10 or 11
- Python 3.11 or newer
- Node.js 20 or newer
- Internet access for Gemini API requests
- A Google Gemini API key

The project does not require a database, Docker, or a separate local model download.

## ▶️ Run the Complete Project

Use Windows PowerShell from the project root.

### 1. Set up the FastAPI backend

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `backend/.env` and add your Gemini API key, then start the API:

```powershell
py -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

The health response is available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

### 2. Set up the Next.js frontend

Open a second PowerShell window:

```powershell
cd frontend
Copy-Item .env.example .env.local
npx --yes pnpm@9.15.0 install --frozen-lockfile
npx --yes pnpm@9.15.0 dev
```

Open [http://localhost:3000](http://localhost:3000).

The `npx --yes pnpm@9.15.0` form avoids requiring a global pnpm installation and also avoids Corepack permission issues on Windows.

## 🧪 Test the Project

The automated backend tests use mocks and do not require a live Gemini request.

### Backend quality checks

Run from the `backend` directory:

```powershell
py -m unittest discover -s tests -p "test_*.py"
py -m compileall -q .
```

### Frontend quality checks

Run from the `frontend` directory:

```powershell
npx --yes pnpm@9.15.0 install --frozen-lockfile
npx --yes pnpm@9.15.0 audit --prod
npx --yes pnpm@9.15.0 lint
npx --yes pnpm@9.15.0 exec tsc --noEmit
npx --yes pnpm@9.15.0 build
```

The expected dependency-audit result for the current lockfile is `No known vulnerabilities found`; registry advisories can change over time.

## 📜 Available Commands

| Command | Description |
| --- | --- |
| `py -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload` | Start the FastAPI backend |
| `npx --yes pnpm@9.15.0 dev` | Start the Next.js frontend |
| `py -m unittest discover -s tests -p "test_*.py"` | Run backend unit tests |
| `npx --yes pnpm@9.15.0 lint` | Run frontend lint checks |
| `npx --yes pnpm@9.15.0 exec tsc --noEmit` | Run frontend type checks |
| `npx --yes pnpm@9.15.0 build` | Validate the frontend production build |
| `npx --yes pnpm@9.15.0 audit --prod` | Audit production frontend dependencies |

## 🔌 Main API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/` | Return basic backend service status |
| `POST` | `/api/calculate-results` | Analyze a submitted canvas image and return structured results |

### `POST /api/calculate-results`

Request body:

```json
{
  "image": "data:image/png;base64,...",
  "dict_of_vars": {
    "x": 4
  }
}
```

Successful responses contain a `data` array with `expr`, `result`, and `assign` fields. Invalid image data receives a client error. AI provider failures receive a server error without exposing provider details.

## 🎯 Project Flow

```text
User draws an expression or diagram
└── Next.js canvas creates a bounded image data URL
    └── FastAPI validates the request and applies limits
        └── Gemini receives the image and calculation prompt
            └── Pydantic validates the structured response
                └── Next.js displays results and stores assignments
```

## 🤖 AI Processing Flow

```text
Canvas image + assigned variables
└── Prompt construction with calculation rules
    ├── Multimodal Gemini request
    ├── Response-size and answer-count limits
    ├── Python literal parsing without code execution
    └── Pydantic schema validation
        └── Structured results returned to the UI
```

## 🛡️ Security and Limitations

- The calculation API is intentionally unauthenticated for this local/public calculator; it does not provide user accounts, sessions, passwords, JWTs, or authorization roles.
- The backend keeps the Gemini credential private and applies explicit CORS, request validation, size limits, response limits, rate limiting, concurrency limits, and request timeouts.
- Rate-limit state is in memory and is therefore process-local; a multi-instance deployment would need a shared limiter.
- AI output is validated before use, but mathematical correctness is not independently proven by a symbolic mathematics engine.
- Submitted canvas images are sent to Google Gemini for analysis.
- The application does not execute AI-generated code, shell commands, database queries, or external tools.
- Do not commit `.env`, `.env.local`, virtual environments, dependency folders, caches, or build metadata.

## 🧑‍💻 Author

**Muhammad Ali Nawaz 2026**  
Python Developer / AI Developer

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  <b>⭐ If this project helps you, consider starring the repository!</b>
</p>

