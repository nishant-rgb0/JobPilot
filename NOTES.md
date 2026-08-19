# JobPilot — Build Notes

## Environment Setup
- Python 3.12.3, pip 24.0, Git 2.53.0 — already installed
- Docker Desktop 29.6.1 — needed WSL 2 first (`wsl --install` as admin, restart)
- Verified Docker works via `docker run hello-world`
- Using VS Code with Python + Pylance + Docker extensions

## Concepts Learned
(One line per concept, in your own words — add as we go)
- Virtual environment: isolated package box per project, so different projects don't conflict on package versions
- FastAPI: framework that turns Python functions into API endpoints, async-first
- Pydantic: library FastAPI uses to validate incoming data — e.g., checking an email field is actually an email format, automatically, without me writing manual checks
- Starlette: the lower-level toolkit FastAPI is actually built on top of (handles the core web request/response mechanics)
- @app.get("/") is a decorator — tells FastAPI "run this function when someone visits this URL with a GET request"
- uvicorn main:app --reload → main = filename, app = the FastAPI() variable, --reload = auto-restart server on code changes
- Returning a Python dict from a route function auto-converts to JSON — this is how APIs communicate
- /docs gives free interactive API documentation (Swagger UI), auto-generated from my code — no extra work needed. Good resume/interview point.
- Foreign key: a column in one table that points to another table's ID — this is how databases link related data (e.g., linking each application to the user who owns it)
- JOIN: combines rows from two tables based on a matching column, so you can query related data together in one result.
- ORM: lets me write Python classes/objects instead of raw SQL strings; SQLAlchemy translates my Python into SQL behind the scenes
- asyncpg: the actual low-level driver SQLAlchemy uses to talk to Postgres asynchronously
- python-dotenv: loads secrets (like DB password) from a separate .env file instead of hardcoding in code
- A SQLAlchemy model class (inheriting Base) maps directly to a Postgres table — one class = one table, one instance = one row
- nullable=False means the field can't be empty; unique=True prevents duplicate values (like two users with the same email)
- Passwords must never be stored as plain text — always hashed first (we'll implement this next when building auth)
- Alembic: migration tool that tracks database schema changes as versioned scripts, so I can evolve tables (add columns, etc.) without losing existing data — like Git but for database structure
- psql: Postgres's own command-line client — useful for verifying data directly, independent of the app code
- alembic_version table: Alembic's internal tracking table, records which migration the database is currently at
- In PowerShell, `curl` is aliased to Invoke-WebRequest (different syntax/behavior than real curl) — use `curl.exe` to get actual curl behavior
- Enum in SQLAlchemy: restricts a column to a fixed set of valid values (applied/screening/interview/offer/rejected) — prevents invalid/typo status values
- ForeignKey("users.id") on Application.user_id links each application to its owning user — same foreign key concept from SQL basics, now in Python
- Two login endpoints can coexist: /auth/login (JSON, for real frontend/API clients) and /auth/token (form-encoded, specifically for Swagger UI's OAuth2 flow) — common real-world pattern

## Decisions & Why
(Every time you choose X over Y, write it here — this is your interview ammo)
- Chose Docker for Postgres/Redis instead of installing natively → keeps my PC clean, matches real team setups
- Storing DB connection string in .env file, added .gitignore to exclude .env and venv/ from Git — prevents leaking secrets to GitHub

## Problems I Hit & How I Fixed Them
(Your best interview stories come from here — don't skip this section)
- WSL install: password prompt shows nothing typed, had to type blind and retype exactly
- First venv\Scripts\activate failed because I was in the wrong folder / venv wasn't created yet. Fixed by running python -m venv venv inside the jobpilot folder first, then activating.
- First docker run attempt failed because Docker Desktop app wasn't open — the CLI needs the Desktop app's engine running in the background. Fixed by opening Docker Desktop and waiting for it to fully start before retrying.
- Port 5432 had two processes listening (conflict with another Postgres instance already on the system) — caused "password authentication failed" even though Docker password was correct. Fixed by remapping Docker Postgres container to port 5433 instead, and updating .env accordingly.
- EmailStr in Pydantic needs email-validator package separately — got ImportError until installing pydantic[email]
- Installed passlib/python-jose without venv active by mistake — went to global Python instead of project venv. Always check for (venv) in prompt before running pip install.
- 500 error on login was actually a database connection failure — Docker Postgres container had stopped (likely after a restart). Fixed with `docker start jobpilot-postgres`. Lesson: containers don't survive PC restarts unless started manually (or run with --restart flag).
- passlib 1.7.4 incompatible with bcrypt 5.0.0 — threw "AttributeError: module bcrypt has no attribute __about__" and "password cannot be longer than 72 bytes" errors when hashing. Known version conflict. Fixed by pinning bcrypt==4.0.1.

## Progress Log
(Short dated entries — just a sentence or two per session)
-  Set up environment (Python, Docker, WSL, VS Code), created venv
- Installed FastAPI 0.139.0 + Uvicorn 0.51.0 in venv
- Wrote first FastAPI app (main.py) with a single GET / endpoint
- Ran it with uvicorn, confirmed working at http://127.0.0.1:8000 — returned {"message":"JobPilot API is alive"}
- Have only basic/limited SQL background — starting SQL fundamentals before touching SQLAlchemy
- Ran Postgres in Docker container (jobpilot-postgres), exposed on port 5432, database name "jobpilot"
- Confirmed jobpilot-postgres container running via `docker ps` — Postgres live on port 5432
- Installed sqlalchemy, asyncpg, python-dotenv
- Created .env (DATABASE_URL) and .gitignore (excludes venv/, .env, __pycache__/)
- Installed Alembic, ran `alembic init alembic` — created alembic/ folder with env.py, script.py.mako, and alembic.ini
- Fixed port conflict by moving Postgres container to port 5433, updated .env
- Ran first Alembic migration successfully — generated b2772ba2e899_create_users_table.py, correctly detected users table + indexes on email and id
- Ran `alembic upgrade head` — users table created in live Postgres database
- Verified users table exists in Postgres via psql directly — confirmed columns (id, email, hashed_password, created_at), 0 rows as expected
- Milestone: full chain working — Docker, Postgres, SQLAlchemy models, Alembic migrations, all connected
- Fixed passlib install by reinstalling with venv active — server now starts cleanly with auth routes loaded
- Restarted jobpilot-postgres container with `docker start jobpilot-postgres` — was exited after PC/Docker restart
- Milestone: Auth working end-to-end — register creates user with hashed password, login verifies password and returns JWT token
- Verified via Swagger UI: POST /auth/register → 200, POST /auth/login → 200 with access_token
- Milestone: Stage 1 (Auth) fully complete — register, login, and protected /auth/me all working end-to-end. Verified JWT validation via curl: GET /auth/me with Bearer token returned {"id":1,"email":"test@example.com"}
- Added Application model (with ApplicationStatus enum, foreign key to users) to models.py
- Ran migration successfully — applications table created in Postgres
- Fixed circular import by moving get_current_user into auth.py; rebuilt main.py cleanly with app.include_router(applications_router)
- Server starts cleanly with applications router wired in

- Milestone: Stage 2 (Application CRUD) fully complete — create, list, and update-status all tested and working correctly via curl
- Confirmed last_updated auto-refreshes on update while applied_date stays fixed — onupdate=func.now() working as intended
- Added /auth/token endpoint (OAuth2PasswordRequestForm-based) alongside existing JSON-based /auth/login — Swagger UI's Authorize button now works directly in the browser
- Confirmed browser-based testing works end-to-end via Swagger Authorize — created 2nd application (HCLTech) directly from /docs

- Milestone: Stage 3 (Analytics) complete — /analytics/summary and /analytics/by-source both tested and correct
- Verified: 2 applications, 1 applied + 1 interview = 50% response rate, correctly split by source (LinkedIn/Naukri)
## Explain-back check (for interview prep)
- Can explain: why passwords are hashed not stored plain, what a JWT contains and why it's signed, why /auth/me needs a dependency (get_current_user) instead of checking manually in each route
- Can explain: GROUP BY groups rows sharing a value so func.count can tally each group — same concept as an Excel pivot tabl