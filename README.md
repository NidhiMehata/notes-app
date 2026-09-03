# 📝 Notes App

A full-stack notes application built with **React, TypeScript, FastAPI, PostgreSQL, and Docker**.

> A personal project built to explore modern full-stack development, authentication, database design, and containerization.

---

## ✨ What it does

|     | Feature                                                    |
| --- | ---------------------------------------------------------- |
| 🔐  | **Authentication** — User registration and JWT-based login |
| 📝  | **Notes** — Create, view, edit, and delete personal notes  |
| 🗄️ | **Database** — PostgreSQL with SQLAlchemy                  |
| 🔄  | **Migrations** — Database schema managed with Alembic      |
| 🎨  | **Frontend** — React + TypeScript + Vite                   |
| 🐳  | **Containerization** — Docker + Docker Compose             |
| 🌐  | **Production Frontend** — React build served through Nginx |

---

## 🏗️ Architecture

```text
                         ┌─────────────────┐
                         │     Browser     │
                         └────────┬────────┘
                                  │
                           :5173  │
                                  ▼
                    ┌──────────────────────┐
                    │  React + TypeScript  │
                    │       + Nginx        │
                    └──────────┬───────────┘
                               │
                         API requests
                               │
                           :8000
                               ▼
                    ┌──────────────────────┐
                    │   FastAPI Backend    │
                    │      + SQLAlchemy    │
                    └──────────┬───────────┘
                               │
                               │
                               ▼
                    ┌──────────────────────┐
                    │      PostgreSQL      │
                    │    Docker Volume     │
                    └──────────────────────┘
```

The entire stack can be started with a single Docker Compose command.

---

## 🛠️ Built With

**Frontend**

`React` · `TypeScript` · `Vite` · `Nginx`

**Backend**

`Python` · `FastAPI` · `SQLAlchemy` · `Pydantic` · `JWT`

**Database**

`PostgreSQL` · `Alembic`

**Infrastructure**

`Docker` · `Docker Compose`

---

## 📁 Project Structure

```text
notes-app/
│
├── notes-backend/          # FastAPI application
│
├── notes-frontend/        # React application
│
├── docker-compose.yml     # Runs the complete stack
│
├── .env.example            # Environment variable template
│
└── README.md
```

Each application also contains its own README with component-specific development instructions.

---

## 🚀 Getting Started

### Prerequisites

* [Docker](https://www.docker.com/)
* Git

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd notes-app
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Update `.env` with your local values:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<your-password>
POSTGRES_DB=notes
JWT_SECRET_KEY=<your-secret>
```

### 3. Start the application

```bash
docker compose up -d --build
```

That's it. Docker Compose starts:

* PostgreSQL
* FastAPI
* React + Nginx

---

## 🌐 Access

| Service          | URL                        |
| ---------------- | -------------------------- |
| **Frontend**     | http://localhost:5173      |
| **Backend API**  | http://localhost:8000      |
| **Swagger Docs** | http://localhost:8000/docs |

---

## 💻 Development

The project can also be run without Docker when developing the frontend or backend independently.

### Backend

See [`notes-backend/README.md`](notes-backend/README.md) for:

* Python environment setup
* PostgreSQL configuration
* Alembic migrations
* Running FastAPI locally

### Frontend

See [`notes-frontend/README.md`](notes-frontend/README.md) for:

* Node.js setup
* Vite development server
* Environment configuration
* Production builds

---

## 🐳 Docker

The application is split into three containers:

```text
┌──────────────┐
│   Frontend   │
│ React + Nginx│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Backend    │
│   FastAPI    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  PostgreSQL  │
└──────────────┘
```

### Common commands

```bash
# Start
docker compose up -d

# Rebuild
docker compose up -d --build

# Check services
docker compose ps

# View logs
docker compose logs

# Stop
docker compose down
```

PostgreSQL data is stored in a Docker named volume, so:

```bash
docker compose down
```

does **not** delete the database.

To completely remove the database volume:

```bash
docker compose down -v
```

> ⚠️ This permanently removes the PostgreSQL data stored in the Docker volume.

---

## 🔐 Environment & Secrets

Environment-specific configuration is kept outside Git.

```text
.env
```

is ignored by Git, while:

```text
.env.example
```

is committed as a template.

Frontend `VITE_*` variables are client-side configuration and **must never contain secrets**.

---

## 📚 Project Documentation

| Component     | Documentation                                          |
| ------------- | ------------------------------------------------------ |
| 🖥️ Backend   | [`notes-backend/README.md`](notes-backend/README.md)   |
| 🎨 Frontend   | [`notes-frontend/README.md`](notes-frontend/README.md) |
| 🐳 Full Stack | This README                                            |

---

## 🔮 What's Next

Some planned improvements:

* Note sharing and collaboration
* Viewer / editor permissions
* Refresh token authentication
* Automated tests
* CI/CD
* Cloud deployment
* HTTPS
* Monitoring and logging

---

## 👩‍💻 About the Project

This project is being developed as a hands-on exploration of full-stack application development, with an emphasis on understanding how the individual pieces fit together — from the database and API to the frontend and deployment environment.