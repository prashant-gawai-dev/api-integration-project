# API Integration Project

A FastAPI backend service with full CRUD operations, backed by PostgreSQL (hosted on Neon), built as a hands-on project to learn backend engineering fundamentals — request validation, database persistence, error handling, and third-party API integration.

## Tech Stack

- **FastAPI** — web framework
- **PostgreSQL** (Neon) — database
- **SQLAlchemy** — ORM
- **Pydantic** — request/response validation
- **httpx** — third-party API integration (Open-Meteo)

## Features

- Full CRUD on API configuration records (create, read, update, delete)
- Proper error handling — 404 for missing records, 500 with rollback on failed writes
- Live weather data proxy via Open-Meteo, with error handling for connection/timeout/upstream failures
- Environment-based configuration (no secrets in code)

## API Endpoints

| Method | Path                          | Description                          |
|--------|-------------------------------|---------------------------------------|
| GET    | `/`                            | Health check                          |
| POST   | `/configs`                     | Create a new API config record        |
| GET    | `/configs`                     | List all API config records           |
| GET    | `/getConfig/{config_id}`       | Get a single config by ID (404 if missing) |
| PUT    | `/configUpdate/{config_id}`    | Update an existing config (404 if missing) |
| DELETE | `/configDelete/{config_id}`    | Delete a config (404 if missing)      |
| GET    | `/weather?lat={lat}&lon={lon}` | Fetch live weather data from Open-Meteo |

## Setup

1. Clone the repo:
```bash
   git clone <your-repo-url>
   cd api-integration-project
```

2. Create and activate a virtual environment:
```bash
   python3 -m venv venv
   source venv/bin/activate
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
DATABASE_URL=postgresql://<user>:<password>@<host>/<dbname>?sslmode=require

5. Run the server:
```bash
   uvicorn main:app --reload
```

6. Open the interactive API docs at `http://127.0.0.1:8000/docs`

## What This Project Is For

Built as a hands-on learning project — deliberately built, broken, and fixed piece by piece rather than following a tutorial end-to-end, to build real understanding of FastAPI, SQLAlchemy sessions, and API error handling rather than just working code.

## Next Steps

- [ ] Automated tests (pytest)
- [ ] Docker containerization
- [ ] Deployment (AWS EC2 + nginx)
- [ ] CI/CD (GitHub Actions)
