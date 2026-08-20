# JobPilot — Job Application Tracker API

A REST API built with FastAPI for tracking job applications — status updates, source tracking, and analytics on response rates. Built as a hands-on project to strengthen Python backend + async development skills.

## Features (working)
- JWT-based authentication (register, login, protected routes)
- Full CRUD for job applications (create, list with filters, update status, delete) — scoped per user
- Analytics endpoints: status breakdown, response rate, breakdown by application source

## Tech Stack
- **FastAPI** — async REST API framework
- **PostgreSQL + SQLAlchemy (async)** — database layer
- **Alembic** — database migrations
- **JWT (python-jose) + Passlib (bcrypt)** — authentication & password hashing
- **Docker** — containerized PostgreSQL for local development

## Planned / In Progress
- Celery + Redis background jobs for automated follow-up reminders
- GenAI integration (Gemini API) — AI-drafted follow-up emails, JD parsing
- pytest test suite
- Full Docker Compose setup (API + DB + Redis + worker)
- Deployment

## Running Locally

1. Clone the repo
2. Create a virtual environment and install dependencies:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

3. Start PostgreSQL via Docker:

docker run --name jobpilot-postgres -e 
POSTGRES_PASSWORD=yourpassword -e POSTGRES_DB=jobpilot -p 5433:5432 -d postgres

4. Create a `.env` file with your `DATABASE_URL` (see `.env.example`)
5. Run migrations:

alembic upgrade head

6. Start the server:

uvicorn main:app --reload

7. Visit `http://127.0.0.1:8000/docs` for interactive API documentation



