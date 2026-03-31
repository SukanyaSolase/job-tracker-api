# Job Tracker API

![CI](https://github.com/SukanyaSolase/job-tracker-api/actions/workflows/ci.yml/badge.svg)

A production-style REST API for tracking job applications — built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. Features JWT authentication, full CRUD, status filtering, pagination, and CSV export.

---

## Features

- **JWT Auth** — register, login, and access protected routes with Bearer tokens
- **Application CRUD** — create, read, update, and delete job applications
- **Status Pipeline** — track applications through `APPLIED → INTERVIEW → OFFER → REJECTED`
- **Filters & Pagination** — filter by status or company name, paginate with `limit` and `offset`
- **CSV Export** — download all your applications as a CSV file
- **Auto Swagger Docs** — interactive API docs available at `/docs`
- **Pytest + CI** — integration tests run on every push via GitHub Actions
- **Docker Compose** — spin up the API and database with a single command

---

## Tech Stack

| Layer      | Technology                           |
| ---------- | ------------------------------------ |
| Framework  | FastAPI                              |
| Database   | PostgreSQL 16                        |
| ORM        | SQLAlchemy 2                         |
| Migrations | Alembic                              |
| Auth       | JWT (python-jose) + bcrypt (passlib) |
| Testing    | Pytest + FastAPI TestClient          |
| CI         | GitHub Actions                       |
| Container  | Docker Compose                       |

---

## Project Structure

```
job-tracker-api/
├── app/
│   ├── api/
│   │   ├── deps.py              # DB session + auth dependencies
│   │   └── routes/
│   │       ├── auth.py          # /auth/register, /auth/login
│   │       ├── users.py         # /users/me
│   │       └── applications.py  # CRUD + export
│   ├── core/
│   │   ├── config.py            # pydantic-settings env config
│   │   └── security.py          # JWT + bcrypt helpers
│   ├── db/
│   │   ├── base.py              # SQLAlchemy declarative base
│   │   └── session.py           # Engine + session factory
│   ├── models/                  # SQLAlchemy ORM models
│   └── schemas/                 # Pydantic request/response schemas
├── alembic/                     # DB migrations
├── tests/
│   ├── conftest.py              # Test DB setup + fixtures
│   ├── test_auth.py
│   └── test_applications.py
├── .github/workflows/ci.yml
├── docker-compose.yml
├── dockerfile
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- Or Python 3.11+ and PostgreSQL if running locally

### Run with Docker Compose

```bash
git clone https://github.com/SukanyaSolase/job-tracker-api.git
cd job-tracker-api

# Copy env file and fill in your values
cp .env.example .env

# Start API + database
docker-compose up --build
```

API will be live at `http://localhost:8000`
Swagger docs at `http://localhost:8000/docs`

### Run Locally (without Docker)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Set up your .env, then run migrations
alembic upgrade head

uvicorn app.main:app --reload
```

---

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/jobtracker
JWT_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## API Reference

### Auth

| Method | Endpoint         | Description            |
| ------ | ---------------- | ---------------------- |
| `POST` | `/auth/register` | Create a new account   |
| `POST` | `/auth/login`    | Get a JWT access token |

### Applications

All routes require `Authorization: Bearer <token>`

| Method   | Endpoint                   | Description                                   |
| -------- | -------------------------- | --------------------------------------------- |
| `POST`   | `/applications`            | Create a new application                      |
| `GET`    | `/applications`            | List applications (with filters + pagination) |
| `GET`    | `/applications/{id}`       | Get a single application                      |
| `PUT`    | `/applications/{id}`       | Update an application                         |
| `DELETE` | `/applications/{id}`       | Delete an application                         |
| `GET`    | `/applications/export/csv` | Download all applications as CSV              |

### Query Parameters (GET /applications)

| Param     | Type   | Description                                                    |
| --------- | ------ | -------------------------------------------------------------- |
| `status`  | string | Filter by status (`APPLIED`, `INTERVIEW`, `OFFER`, `REJECTED`) |
| `company` | string | Filter by company name (case-insensitive, partial match)       |
| `limit`   | int    | Number of results (default: 20)                                |
| `offset`  | int    | Pagination offset (default: 0)                                 |

### Example: Create an Application

```bash
curl -X POST http://localhost:8000/applications \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "company": "Google",
    "role": "Software Engineer",
    "status": "APPLIED",
    "link": "https://careers.google.com",
    "notes": "Applied via referral"
  }'
```

---

## Running Tests

```bash
# Requires a running PostgreSQL instance (or use Docker)
TEST_DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/jobtracker_test \
pytest -v
```

Tests cover: registration, login, JWT auth, CRUD operations, status filtering, and 401/404 edge cases.

---

## CI / CD

GitHub Actions runs the full test suite on every push and pull request. The workflow spins up a PostgreSQL service container, installs dependencies, and runs `pytest`.

See `.github/workflows/ci.yml` for the full pipeline.

---

## Status Values

| Status      | Meaning                            |
| ----------- | ---------------------------------- |
| `APPLIED`   | Application submitted              |
| `INTERVIEW` | Interview scheduled or in progress |
| `OFFER`     | Offer received                     |
| `REJECTED`  | Application rejected               |

---

## Future Improvements

- Redis caching on list endpoints
- Rate limiting on `/auth/login` with slowapi
- Email notifications on status change (FastAPI BackgroundTasks)
- Frontend dashboard

---

## Author

**Sukanya Solase** — [GitHub](https://github.com/SukanyaSolase)
