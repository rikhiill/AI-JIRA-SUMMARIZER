🔷 Project Overview

# AI-Based Jira Summarizer 🧠📊

An AI-powered tool that fetches Jira issues, generates intelligent summaries using NLP, and produces downloadable reports (PDF, CSV, JSON). Includes user authentication, status filters, smart dashboards, and beautiful UI.


🔧 Tech Stack

- 🧠 GPT/NLP (summarization)
- ⚙️ Flask + JWT (backend)
- 💾 JSON File Storage
- 🎨 React + Tailwind (frontend)
- 🔐 Authentication with JWT
- ☁️ Hosted on Render + Vercel

| Layer        | Tech                     |
|--------------|--------------------------|
| Frontend     | React, Tailwind, Vercel  |
| Backend      | Flask, JWT, Render       |
| Auth         | JWT + bcrypt             |
| Storage      | JSON + FileSystem        |
| NLP/AI       | LSA (or GPT via API)     |
| Reporting    | PDF, CSV, JSON, ZIP      |



🚀 Live Demo Links

- 🌐 Frontend: [ai-jira-summarizer.vercel.app](https://ai-jira-summarizer.vercel.app)
- 🔗 Backend API: [ai-jira-summarizer1.onrender.com](https://ai-jira-summarizer1.onrender.com)


✨ Features

- 🔐 **JWT-based Login/Signup**
- 🧠 **AI Summary Generation (LSA or GPT)**
- 🎨 **Smart Dashboard with Status Filters**
- ✏️ **Edit/Delete/Search Summaries**
- 📥 **Download Reports in PDF, CSV, JSON, ZIP**
- 📊 **Smart Summary Analytics**
- 🌙 **Dark/Light Theme Toggle**
- 📱 **Mobile Responsive UI**



👨‍💻 Local Setup Instructions


git clone https://github.com/rikhiill/AI-JIRA-SUMMARIZER.git
cd AI-JIRA-SUMMARIZER

# Setup backend
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

# Create .env and add:
# JIRA_API_TOKEN=your-token-here
# Run
python app.py

# Setup frontend
cd ../frontend
npm install
# .env file
REACT_APP_BACKEND_URL=http://localhost:5000s
npm start


