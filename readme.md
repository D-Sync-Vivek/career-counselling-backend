# 🌟 Harmony: AI-Powered Career Counselor

Harmony is a comprehensive, full-stack career counseling platform designed to guide students and professionals through their career journeys. It leverages advanced AI to provide personalized career roadmaps, interactive aptitude assessments, and intelligent mentor matching via vector embeddings.

![Harmony Dashboard](https://img.shields.io/badge/Status-Active_Development-success)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![React](https://img.shields.io/badge/React_Vite-Frontend-61DAFB?logo=react)

---

## 🚀 Key Features

* **🧠 AI Career Journey:** Automated, step-by-step career roadmapping powered by DeepSeek and Groq LLMs.
* **📊 Comprehensive Assessments:** Built-in quantitative, logical, and verbal aptitude tests, alongside personality profiling.
* **🤝 Smart Mentor Matching:** Semantic search engine matching users to industry mentors based on career goals using local HuggingFace embeddings (`all-MiniLM-L6-v2`).
* **📹 Real-Time Sessions:** Seamless 1-on-1 video mentoring integrated directly into the platform via the Dyte SDK.
* **⚡ Highly Optimized Architecture:** CPU-only optimized PyTorch dependencies to drastically reduce container size and cloud hosting costs.

---

## 🛠️ Technology Stack

### Frontend
* **Framework:** React + Vite
* **Routing/State:** React Router, Zustand (Optimized for performance)
* **Deployment:** Nginx (Alpine-based multi-stage Docker build)

### Backend
* **Framework:** FastAPI (Python 3.11)
* **Database & ORM:** PostgreSQL (Neon.tech) + SQLAlchemy
* **Authentication:** JWT (JSON Web Tokens) via `python-jose[cryptography]`
* **AI & Machine Learning:** LangChain, HuggingFace (`sentence-transformers`), PyTorch (CPU-Optimized)

### Infrastructure
* **Containerization:** Docker & Docker Compose
* **Reverse Proxy/SSL:** Traefik (Optional/Supported)

---

## ⚙️ Environment Variables

To run this project, you will need to create a `.env` file in the root directory. **Do not commit this file to GitHub.**

```env
# Database (IMPORTANT: Do not use quotation marks around the URL)
DATABASE_URL=postgresql://user:password@ep-your-database.neon.tech/dbname?sslmode=require

# Security
SECRET_KEY=your_generated_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# AI API Keys
DEEPSEEK_API_KEY=your_deepseek_key
GROQ_API_KEY=your_groq_key

# Video Integration
DYTE_ORG_ID=your_dyte_org_id
DYTE_API_KEY=your_dyte_api_key

# Frontend Configuration (Required for Frontend Docker Build)
VITE_API_BASE_URL=http://your-server-ip:8000
