# ⚡ Notes Backend

The backend API for the Notes App, built with **FastAPI, SQLAlchemy, PostgreSQL, and JWT authentication**.

> A REST API designed around a layered architecture, database migrations, and protected endpoints.

---

## 🧩 What it does

|     | Feature                                                      |
| --- | ------------------------------------------------------------ |
| 👤  | **Users** — Registration and user management                 |
| 🔐  | **Authentication** — JWT-based login and protected endpoints |
| 📝  | **Notes** — Create, read, update, and delete notes           |
| 👥  | **Ownership** — Notes belong to authenticated users          |
| 🗄️ | **Database** — PostgreSQL with SQLAlchemy 2.x                |
| 🔄  | **Migrations** — Schema changes managed with Alembic         |
| 📖  | **API Docs** — Interactive Swagger / OpenAPI documentation   |

---

## 🏗️ Architecture

```text id="qg6s4j"
                    ┌─────────────────┐
                    │     Frontend    │
                    └────────┬────────┘
                             │
                         HTTP / JSON
                             │
                             ▼
                    ┌─────────────────┐
                    │     Routers     │
                    │   API Endpoints │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     Services    │
                    │ Business Logic  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    SQLAlchemy   │
                    │      Models     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    └─────────────────┘
```

Authentication utilities handle password hashing and JWT creation/validation.

Alembic manages the database schema independently from the application startup logic.

---

## 🛠️ Built With

`Python` · `FastAPI` · `SQLAlchemy 2.x` · `Pydantic` · `PostgreSQL` · `Alembic` · `JWT` · `Uvicorn`

---

## 📁 Project Structure

```text id="z2b1qe"
notes-backend/
│
├── alembic/                 # Database migrations
│   └── versions/
│
├── database/                # Database configuration
│
├── models/                  # SQLAlchemy models
│
├── routers/                 # API endpoints
│
├── schemas/                 # Pydantic request/response schemas
│
├── services/                # Application/business logic
│
├── utils/                   # Authentication & JWT utilities
│
├── config.py                # Application configuration
├── main.py                  # FastAPI application
├── alembic.ini              # Alembic configuration
├── requirements.txt         # Python dependencies
└── Dockerfile
```

---

## 🚀 Running Locally

### Prerequisites

* Python 3.x
* PostgreSQL
* Git

### 1. Create a virtual environment

From `notes-backend`:

```bash id="q8d7wm"
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash id="1s7n5b"
pip install -r requirements.txt
```

### 3. Configure environment variables

Create:

```text id="k0b5r8"
.env
```

Example:

```env id="8t0j3w"
DATABASE_URL=postgresql+psycopg://postgres:<password>@localhost:5432/notes
JWT_SECRET_KEY=<your-secret>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 4. Run database migrations

```bash id="f8z1sl"
alembic upgrade head
```

### 5. Start the API

```bash id="r6t4ju"
uvicorn main:app --reload
```

The API will be available at:

```text id="2q0jla"
http://localhost:10000
```

---

## 📖 API Documentation

FastAPI automatically provides interactive API documentation.

**Swagger UI**

```text id="k6y3pp"
http://localhost:10000/docs
```

**OpenAPI schema**

```text id="7v6n5p"
http://localhost:10000/openapi.json
```

---

## 🗄️ Database Migrations

Alembic is responsible for managing database schema changes.

### Check the current migration

```bash id="g1h5c4"
alembic current
```

### Create a migration

After modifying a SQLAlchemy model:

```bash id="j3f7az"
alembic revision --autogenerate -m "describe change"
```

### Apply migrations

```bash id="p9d2rx"
alembic upgrade head
```

The application does not rely on `Base.metadata.create_all()` for schema management. Database changes are handled through Alembic migrations.

---

## 🐳 Docker

The backend can be run as part of the complete Notes App using Docker Compose.

From the project root:

```bash id="v4j1rx"
docker compose up -d --build
```

The backend container:

```text id="d6s9eu"
PostgreSQL becomes healthy
          ↓
Alembic migrations run
          ↓
Uvicorn starts FastAPI
```

Inside Docker, PostgreSQL is accessed through the Compose service name:

```text id="e8v3mq"
db:5432
```

rather than `localhost`.

---

## ⚙️ Environment Variables

| Variable                      | Purpose                      |
| ----------------------------- | ---------------------------- |
| `DATABASE_URL`                | PostgreSQL connection string |
| `JWT_SECRET_KEY`              | Secret used to sign JWTs     |
| `JWT_ALGORITHM`               | JWT signing algorithm        |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime        |

Never commit `.env` or other files containing secrets.

---

## 🔮 Future Improvements

* Refresh token authentication
* Note sharing and collaboration
* Viewer / editor permissions
* Better API error handling
* Monitoring and logging
