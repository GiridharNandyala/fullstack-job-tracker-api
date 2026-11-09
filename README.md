#1. Project Overview
The **Enterprise Job Application Tracker** is a production-grade, full-stack web application designed to streamline and manage career pipelines efficiently. Built with a modern **React** frontend and a high-performance **FastAPI** backend, the system allows candidates to track job applications, update recruitment statuses in real-time, and store records securely in a persistent cloud-hosted **Supabase PostgreSQL** database.
---

💼 Enterprise Job Application Tracker Links

[![Live Demo](https://img.shields.io/badge/Live_Demo-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://fullstack-job-tracker-boumjgp9f-giridharnandyala.vercel.app)
[![Backend API](https://img.shields.io/badge/Backend_API-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://fullstack-job-tracker-api.onrender.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/giridhar-nandyala/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/GiridharNandyala/fullstack-job-tracker-api)


---

## 2. Live Application
* **Frontend Web Application (Vercel)**: [https://fullstack-job-tracker-boumjgp9f-giridharnandyala.vercel.app](https://fullstack-job-tracker-boumjgp9f-giridharnandyala.vercel.app)
* **Backend REST API (Render)**: [https://fullstack-job-tracker-api.onrender.com](https://fullstack-job-tracker-api.onrender.com)
* **API Documentation (Swagger UI)**: [https://fullstack-job-tracker-api.onrender.com/docs](https://fullstack-job-tracker-api.onrender.com/docs)

---

## 3. Project Objectives
* **Pipeline Management**: Provide an intuitive interface to add, view, filter, and delete job applications.
* **Secure User Data**: Implement robust user authentication to isolate candidate data per account.
* **Decoupled Architecture**: Maintain a clear separation of concerns between client-side rendering and backend service layers.
* **Cloud Persistence**: Deploy continuous, scalable cloud architecture utilizing Vercel, Render, and Supabase PostgreSQL.

---

## 4. Key Features
* **Authentication & Authorization**: Secure user registration and login flows using JWT (JSON Web Tokens) and passlib salted bcrypt password hashing.
* **Dynamic CORS Integration**: Fully configured backend CORS policy supporting dynamic Vercel preview environments (`allow_origin_regex`).
* **Real-time Pipeline Filtering**: Filter tracked job applications instantly by status (`Applied`, `Interviewing`, `Offered`, `Rejected`).
* **Interactive UI**: Responsive, dark-themed dashboard featuring modern UI controls and smooth asynchronous state management.
* **Robust Database Management**: Integrated Alembic schema migrations ensuring smooth database operations across environments.

---

## 5. How It Works
1. **User Authentication**: The client submits credentials to `/register` or `/login`. Upon verification, the FastAPI backend responds with a JWT bearer access token.
2. **Session Storage**: The React application securely stores the JWT in browser `localStorage` and includes it in the `Authorization` header for subsequent API requests.
3. **Data Operations**: CRUD requests are sent via Axios to FastAPI endpoints, where SQLAlchemy ORM executes queried operations on the Supabase PostgreSQL database.
4. **State Refresh**: Visual pipelines refresh automatically after successful database transactions.

---

## 6. Architecture
┌──────────────────────────────────────────────────────────┐
│                   React Frontend (Vercel)                │
│    (State Management, Dark Theme UI, Axios HTTP Client)   │
└────────────────────────────┬─────────────────────────────┘
│
REST API Requests (JWT Auth)
│
▼
┌──────────────────────────────────────────────────────────┐
│                   FastAPI Backend (Render)               │
│   (OAuth2 Auth, Pydantic Schemas, CORS Middleware)       │
└────────────────────────────┬─────────────────────────────┘
│
SQLAlchemy ORM Queries
│
▼
┌──────────────────────────────────────────────────────────┐
│               Supabase PostgreSQL Cloud DB               │
│       (Relational Storage: Users & Jobs Tables)          │
└──────────────────────────────────────────────────────────┘

---

## 7. Technologies Used
* **Frontend**: React.js, Axios, HTML5, CSS3
* **Backend**: Python 3.14, FastAPI, Uvicorn, Pydantic, SQLAlchemy ORM
* **Authentication**: Passlib (Bcrypt), Python-JOSE (JWT)
* **Database & Migration**: Supabase PostgreSQL, Alembic, Psycopg
* **Hosting & Deployment**: Vercel (Frontend), Render (Backend)

---

## 8. Project Structure
fullstack-job-tracker-api/
│
├── app/                        # FastAPI Backend Application
│   ├── init.py
│   ├── auth.py                 # Password Hashing & JWT Logic
│   ├── database.py             # SQLAlchemy DB Session Config
│   ├── main.py                 # FastAPI Routes & CORS Config
│   ├── models.py               # Database Models (User & Job)
│   └── schemas.py              # Pydantic Request/Response Models
│
├── job-tracker-ui/             # React Frontend Application
│   ├── public/                 # Static Assets
│   └── src/                    # React Components & Logic
│       ├── App.jsx             # Main UI Component & API Integration
│       └── main.jsx            # React App Entry Point
│
├── alembic/                    # Database Migrations
├── requirements.txt            # Python Dependencies
├── README.md                   # Project Documentation
└── .env                        # Environment Variables Configuration


---

## 9. Local Installation

### Prerequisites
* Python 3.10+
* Node.js & npm
* PostgreSQL Instance (or Supabase account)

### Backend Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/GiridharNandyala/fullstack-job-tracker-api.git](https://github.com/GiridharNandyala/fullstack-job-tracker-api.git)
   cd fullstack-job-tracker-api

   1.Create and activate a virtual environment:
   
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate

   2.Install backend dependencies:
   pip install -r requirements.txt

   3.Configure environment variables in a .env file:
   
    DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<dbname>
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30

   4.Start the FastAPI server:
   uvicorn app.main:app --reload

Frontend Setup

    1.Navigate to the frontend directory:
    cd job-tracker-ui

    2.Install npm dependencies:
    npm install

    3.Start the Vite/React development server:
    npm run dev

   
