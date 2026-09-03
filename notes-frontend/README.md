# 🎨 Notes Frontend

The frontend for the Notes App, built with **React, TypeScript, and Vite**.

> A lightweight React application that communicates with the FastAPI backend through REST APIs.

---

## 🧩 What it does

|    | Feature                                                            |
| -- | ------------------------------------------------------------------ |
| 🔐 | **Authentication** — Login and session handling                    |
| 📝 | **Notes** — Create, view, edit, and delete notes                   |
| 👤 | **User-specific data** — Displays notes for the authenticated user |
| 🔌 | **API Integration** — Communicates with the FastAPI backend        |
| 🎨 | **UI** — React-based application interface                         |
| ⚡  | **Development** — Fast development workflow with Vite              |
| 🌐 | **Production** — Static React build served through Nginx           |

---

## 🏗️ Architecture

```text id="f5qj3d"
                    ┌─────────────────┐
                    │     Browser     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │      React      │
                    │   TypeScript    │
                    └────────┬────────┘
                             │
                       REST / JSON
                             │
                             ▼
                    ┌─────────────────┐
                    │  FastAPI API    │
                    │ localhost:10000  │
                    └─────────────────┘
```

For production, the React application is built into static files and served by Nginx.

---

## 🛠️ Built With

`React` · `TypeScript` · `Vite` · `Nginx` · `Docker`

---

## 📁 Project Structure

```text id="j1c7oe"
notes-frontend/
│
├── src/
│   ├── api/                 # API clients
│   ├── components/         # Reusable React components
│   ├── App.tsx             # Main application
│   ├── Login.tsx           # Login page
│   └── ...
│
├── public/                 # Static assets
├── Dockerfile              # Production container
├── nginx.conf              # Nginx configuration
├── package.json            # Node dependencies & scripts
├── tsconfig.json           # TypeScript configuration
└── vite.config.ts          # Vite configuration
```

---

## 🚀 Running Locally

### Prerequisites

* Node.js
* npm
* Git

### 1. Install dependencies

From `notes-frontend`:

```bash id="v4o1fj"
npm install
```

### 2. Configure the API

Create:

```text id="4r1v9x"
.env.development
```

with:

```env id="d5u6kx"
VITE_API_BASE_URL=http://localhost:10000
```

### 3. Start the development server

```bash id="8j3w1q"
npm run dev
```

The frontend will normally be available at:

```text id="x0w7qn"
http://localhost:5173
```

---

## 🔌 API Configuration

The frontend uses:

```env id="z3n6kf"
VITE_API_BASE_URL=http://localhost:10000
```

to determine where API requests should be sent.

For example:

```text id="h2r5cb"
React
  │
  │ POST /auth/login
  ▼
http://localhost:10000
  │
  ▼
FastAPI
```

For a deployed application, `VITE_API_BASE_URL` should point to the deployed backend.

> ⚠️ `VITE_*` variables are included in the client-side application. Never store passwords, API keys, JWT secrets, or other sensitive values in them.

---

## 📦 Production Build

Create a production build:

```bash id="b8j2qp"
npm run build
```

This generates:

```text id="2r5n6w"
dist/
```

The `dist/` directory contains the static files that can be served by a web server.

You can preview the production build locally with:

```bash id="s6c8yt"
npm run preview
```

---

## 🌐 Nginx

The production Docker image uses Nginx to serve the React build.

The process is:

```text id="p7f4vz"
React + TypeScript
        ↓
    npm run build
        ↓
       dist/
        ↓
      Nginx
        ↓
     Browser
```

Nginx also handles the fallback to `index.html` required by client-side routing.

---

## 🐳 Docker

The frontend uses a multi-stage Docker build.

### Build stage

Node.js is used to:

```text id="q3h7ws"
install dependencies
        ↓
build React application
        ↓
generate dist/
```

### Runtime stage

Nginx serves the generated files.

This means Node.js is not required in the final runtime container.

Start the complete application from the project root:

```bash id="j8m2kc"
docker compose up -d --build
```

The frontend will be available at:

```text id="6r0xpg"
http://localhost:5173
```

---

## ⚙️ Environment Variables

| Variable            | Purpose                    |
| ------------------- | -------------------------- |
| `VITE_API_BASE_URL` | URL of the FastAPI backend |

Example:

```env id="e4n8st"
VITE_API_BASE_URL=http://localhost:10000
```

Because Vite embeds these values during the build, changing the API URL requires rebuilding the frontend.

---

## 🔮 Future Improvements

* Improved responsive design
* Better loading and error states
* Client-side routing improvements
* Note search
* Note filtering
* Rich text editing
* Automated frontend tests
* Production deployment
