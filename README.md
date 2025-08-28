
<div align="center">

# 📅 AI Calendar Scheduler (MCP Server + Agent)  
### Schedule events in Google Calendar directly from natural language prompts

</div>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI"/>
  <img src="https://img.shields.io/badge/Google%20Calendar-4285F4?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Google Calendar"/>
</p>

---

## 📌 Overview

This project connects **OpenAI GPT** with **Google Calendar API** through a lightweight **MCP server**.  
It enables natural language scheduling, so you can simply type commands like:

> "Schedule a meeting for tomorrow at 4 PM to discuss the project launch for an hour."

The agent parses the intent → calls the MCP server → schedules it on Google Calendar.

---

## ✨ Features

- 🤖 **AI Agent** that understands natural language and extracts event details  
- 📅 **Google Calendar Integration** using OAuth2  
- ⚡ **FastAPI MCP Server** for event scheduling  
- 🔑 **Secure authentication flow** (`/login` & `/oauth2callback`)  
- 📂 Minimal, extensible project structure  

---

## 🛠️ Tech Stack

| Layer | Technologies | Purpose |
|------|--------------|---------|
| **Agent** | OpenAI GPT-4 Turbo | Natural language → structured event data |
| **Server** | FastAPI | REST API for scheduling |
| **Calendar API** | Google Calendar | Event creation & management |
| **Auth** | OAuth2.0 | Secure login with Google |

---

## ⚙️ How It Works

1. **Authenticate** with Google using `/login` → `/oauth2callback`.  
2. **Store credentials** in `credentials.json`.  
3. **Agent (`agent.py`)** sends structured scheduling requests to MCP server.  
4. **Server (`mcp_server.py`)** creates events in Google Calendar.  
5. ✅ Done! Your event is live in the calendar.

---

## 📂 Folder Structure

```
AI-Calendar-Scheduler/
├── agent.py         # AI scheduling agent (OpenAI tool call → MCP server)
├── mcp_server.py    # FastAPI server (Google Calendar integration)
├── credentials.json # Generated after login (OAuth tokens)
└── .gitignore
```

---

## 🚦 Getting Started

### 1️⃣ Clone & Setup
```bash
git clone https://github.com/your-username/ai-calendar-scheduler.git
cd ai-calendar-scheduler
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Add Google Credentials
- Download `client_secret.json` from Google Cloud Console.  
- Place it in the project root.  

### 4️⃣ Run the Server
```bash
uvicorn mcp_server:app --reload
```

### 5️⃣ Login with Google
Visit:
```
http://localhost:8000/login
```
Copy the credentials printed in the terminal into `credentials.json`.

### 6️⃣ Run the Agent
```bash
python agent.py
```
Example prompt:
```
"Schedule a meeting for tomorrow at 4 PM to discuss the project launch for an hour"
```

---

## 📌 Roadmap

- [ ] Add recurring event support  
- [ ] Support multiple calendars  
- [ ] Natural language event modifications  
- [ ] Web dashboard for event management  

---

## 🙌 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)  
- [OpenAI](https://openai.com/)  
- [Google Calendar API](https://developers.google.com/calendar)  

---

<div align="center">
  Built with ❤️ by <a href="https://github.com/your-username">Your Name</a>
</div>
