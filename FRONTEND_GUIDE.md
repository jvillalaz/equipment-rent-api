# Frontend Integration Guide

This guide is aimed at frontend developers who consume this API. It covers how to get the environment running locally, how each piece fits together, how to authenticate, how requests and responses are structured, and what to do when things go wrong.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [What Each Container Does](#what-each-container-does)
- [Available Commands (Makefile)](#available-commands-makefile)
- [Authentication Flow](#authentication-flow)
- [Request & Response Conventions](#request--response-conventions)
- [Endpoint Reference](#endpoint-reference)
- [Error Reference](#error-reference)
- [What NOT To Do](#what-not-to-do)
- [Tips & Tricks](#tips--tricks)

---

## Prerequisites

Make sure you have the following installed before proceeding:

| Tool | Why it's needed |
|---|---|
| [Docker](https://docs.docker.com/get-docker/) | Runs all services in containers |
| [Docker Compose](https://docs.docker.com/compose/) | Orchestrates the multi-container setup |
| `make` | Shorthand commands (comes with most Linux/macOS; on Windows use WSL) |

Check your versions:

```bash
docker --version        # Docker version 24+
docker compose version  # Docker Compose v2+
make --version
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone <repo-url>
cd equipment-rent-api
```

### 2. Start the containers

```bash
make up
```

This command starts all three services in the background. The first run will **build the API image**, which takes a minute or two. Subsequent starts are instant.

### 3. Wait for everything to be healthy

The API container waits for PostgreSQL to pass its health check before starting. You can follow what's happening in real time:

```bash
make logs
```

Look for these two lines to confirm everything is ready:

```
Database connected!
[MQTT] Connected to rent-mosquitto:1883
```

### 4. Access the interactive docs

Once running, open your browser at:

```
http://localhost:8000/docs
```

This is a fully interactive interface where you can explore and test every endpoint without writing any code.

---

## What Each Container Does

The project runs three containers that work together. Understanding each one helps you diagnose problems faster.

### `equipment-rent` — The API

- Built from the local `Dockerfile` using Python 3.11
- Runs a **FastAPI** application on port `8000`
- Handles all business logic: users, reservations, equipment, commands
- Communicates with PostgreSQL for data persistence and with Mosquitto for sending commands to physical equipment
- Automatically reloads on code changes (hot-reload is enabled via `--reload`)

### `rent-postgres` — The Database

- Official **PostgreSQL 16** image
- Stores all persistent data: users, equipment, reservations, commands, statuses
- Data lives in a Docker volume (`rentdb-data`) so it survives container restarts
- Only accessible inside the Docker network — you cannot connect to it from outside unless you use a DB client pointed at `localhost:5432` with credentials `rentdb / rentdb`
- The API waits for this container to be healthy before it starts

### `rent-mqtt5` — The Message Broker (Mosquitto)

- **Eclipse Mosquitto** MQTT broker
- Used exclusively for sending real-time commands to physical equipment (e.g., start, stop, turn on)
- The frontend does **not** interact with this directly — it sends a command through the REST API and the API publishes the message to MQTT internally
- Exposed on ports `1883` (MQTT) and `9001` (WebSocket), but these are internal to the system

---

## Available Commands (Makefile)

All commands are run from the project root.

| Command | What it does |
|---|---|
| `make build` | Builds the Docker images without starting |
| `make up` | Starts all containers in the background |
| `make down` | Stops and removes all containers |
| `make restart` | Restarts all containers |
| `make restart-api` | Restarts only the API container (useful after dependency changes) |
| `make rebuild` | Full teardown + rebuild from scratch, no cache |
| `make logs` | Streams logs from all containers |
| `make logs-api` | Streams logs from the API only |
| `make logs-db` | Streams logs from PostgreSQL only |
| `make ps` | Shows the status of all containers |
| `make shell` | Opens a bash shell inside the API container |

> Use `make rebuild` when you change `requirements.txt` or `Dockerfile`. For code-only changes, hot-reload handles it automatically.

---

## Authentication Flow

Most endpoints require a valid JWT token. Here is the complete flow:

### Step 1 — Register a new user

```
POST /auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "password": "secret123"
}
```

Returns the created user (without the password).

### Step 2 — Login and get a token

> **Important:** the login endpoint uses `application/x-www-form-urlencoded`, not JSON. This is the OAuth2 standard used by FastAPI's built-in security scheme.

```
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=johndoe&password=secret123
```

Response:

```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "tokenType": "bearer"
}
```

### Step 3 — Include the token in every request

Add the `Authorization` header to all subsequent requests:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Step 4 — Check who is logged in

```
GET /auth/me
Authorization: Bearer <token>
```

Returns the current user's profile.

### Token expiry

Tokens expire after **30 minutes**. After expiry the API returns `401 Unauthorized`. Your frontend should handle this by redirecting the user to login again (or implementing a refresh mechanism if one is added later).

---

## Request & Response Conventions

### All field names are camelCase

The API uses camelCase for every field in both requests and responses, regardless of how they are stored internally.

| Internal name | Over the wire |
|---|---|
| `user_id` | `userId` |
| `equipment_id` | `equipmentId` |
| `current_status_id` | `currentStatusId` |
| `start_time` | `startTime` |
| `created_at` | `createdAt` |

If you send a field with snake_case it will be ignored and you will likely get a validation error.

### IDs are UUIDs

Every resource identifier is a UUID v4 string, for example:

```
"550e8400-e29b-41d4-a716-446655440000"
```

Never assume sequential integer IDs.

### Dates and times are ISO 8601 UTC

All timestamps are returned with a `Z` suffix indicating UTC:

```
"2024-07-15T10:30:00Z"
```

When sending datetime fields in requests (e.g., reservation start/end times), use the same format.

### Partial updates use PATCH

`PATCH` endpoints accept only the fields you want to change. You do not need to send the entire object — only include the fields you are updating.

---

## Endpoint Reference

The base URL is `http://localhost:8000`. All routes except `/auth/register` and `/auth/login` require the `Authorization: Bearer <token>` header.

### Auth

| Method | Path | Description |
|---|---|---|
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Login and receive a JWT token |
| `GET` | `/auth/me` | Get the currently authenticated user |

### Users

| Method | Path | Description |
|---|---|---|
| `GET` | `/users` | List all users |
| `GET` | `/users/{userId}` | Get a specific user by ID |
| `PATCH` | `/users/{userId}` | Update user information |
| `DELETE` | `/users/{userId}` | Delete a user |

### Equipments

| Method | Path | Description |
|---|---|---|
| `GET` | `/equipments` | List all equipments |
| `POST` | `/equipments` | Create a new equipment |
| `GET` | `/equipments/{equipmentId}` | Get a specific equipment |
| `PATCH` | `/equipments/{equipmentId}` | Update equipment data |
| `DELETE` | `/equipments/{equipmentId}` | Delete an equipment |
| `GET` | `/equipments/{equipmentId}/status` | Get current status of an equipment |

### Reservations

| Method | Path | Description |
|---|---|---|
| `GET` | `/reservations` | List all reservations |
| `POST` | `/reservations` | Create a new reservation |
| `GET` | `/reservations/{reservationId}` | Get a specific reservation |
| `PATCH` | `/reservations/{reservationId}` | Update reservation status |
| `DELETE` | `/reservations/{reservationId}` | Cancel a reservation |
| `GET` | `/reservations/status-reservation` | List all possible reservation statuses |

### Commands

| Method | Path | Description |
|---|---|---|
| `GET` | `/commands` | List all issued commands |
| `POST` | `/commands` | Send a command to equipment (triggers MQTT) |
| `GET` | `/commands/{commandId}` | Get a specific command |
| `GET` | `/commands/available-types` | List all available command types |

### Equipment Status & Logs

| Method | Path | Description |
|---|---|---|
| `GET` | `/equipment-status` | List all possible equipment statuses |
| `GET` | `/equipment-status-logs` | List all status change logs |
| `GET` | `/equipment-status-logs/{equipmentId}` | List status logs for a specific equipment |

---

## Error Reference

The API returns standard HTTP status codes with a JSON body in the format:

```json
{
  "detail": "Human-readable error message here"
}
```

| Status | Name | When it happens | What to do |
|---|---|---|---|
| `400` | Bad Request | Validation failed, duplicate entry, or invalid value | Check the `detail` field — it will name the exact problem |
| `401` | Unauthorized | Missing token, expired token, or wrong credentials | Re-authenticate; send the `Authorization` header |
| `403` | Forbidden | Authenticated but not allowed to perform this action | Check user permissions |
| `404` | Not Found | The requested resource does not exist | Verify the ID you are using is correct |
| `409` | Conflict | Trying to create something that already exists (e.g., duplicate username) | Change the conflicting value (username, equipment name, etc.) |
| `422` | Unprocessable Entity | The request body has the wrong shape or missing required fields | Check that field names are camelCase and all required fields are present |
| `500` | Internal Server Error | Something unexpected broke on the server side | Check `make logs-api` for the full stack trace |

### Common mistakes that cause `422`

- Sending snake_case field names instead of camelCase
- Sending a string where a UUID is expected
- Sending a date without the time component (e.g., `"2024-07-15"` instead of `"2024-07-15T10:00:00Z"`)
- Missing required fields

---

## What NOT To Do

**Do not connect directly to the database.**
PostgreSQL is an implementation detail. All data access must go through the API. Connecting directly bypasses authentication, validation, and business logic.

**Do not hardcode the JWT token.**
Tokens expire in 30 minutes. Store them in memory or `sessionStorage`, never in `localStorage` for long-lived sessions, and never commit them to source control.

**Do not run `make rebuild` while the containers are serving requests.**
This tears down and rebuilds everything. Use `make restart-api` for routine restarts, and reserve `make rebuild` for when you change dependencies or the Dockerfile.

**Do not run `docker compose down -v`.**
The `-v` flag deletes volumes, including `rentdb-data`. This permanently destroys all database data. The regular `make down` (without `-v`) keeps the data intact.

**Do not send the `Content-Type: application/json` header to `/auth/login`.**
That endpoint uses form encoding (`application/x-www-form-urlencoded`). Sending JSON will result in a `422` error.

**Do not cache status IDs in your frontend code.**
The IDs for equipment statuses (`Available`, `Occupied`, etc.) and reservation statuses (`Active`, `Completed`, etc.) are UUIDs generated at database seed time. They will be different across environments. Always fetch them at runtime from `/equipment-status` or `/reservations/status-reservation`.

---

## Tips & Tricks

**Use `/docs` while developing.**
`http://localhost:8000/docs` (Swagger UI) lets you explore and test every endpoint interactively. You can authorize with a token by clicking the lock icon at the top right. Use it to understand the exact shape of every request and response before writing any fetch calls.

**Use `/redoc` for reading.**
`http://localhost:8000/redoc` is a cleaner, read-only version of the docs. Better for understanding the data models without the noise of the interactive UI.

**Follow the logs when something is unexpectedly slow or broken.**

```bash
make logs-api
```

The API prints clear messages for MQTT connection, database connection, and seeding. Most startup errors are visible here.

**The database is pre-seeded on every start.**
Equipment statuses (`Available`, `Occupied`, `Offline`, `Maintenance`), reservation statuses (`Active`, `Completed`, `Canceled`), and command types (`Start`, `Stop`, `Turn On`, etc.) are inserted automatically on startup. You do not need to create them manually — but you need to fetch their IDs to use them in requests.

**If the API container crashes right after starting**, the most common cause is that PostgreSQL was not ready in time. Run `make logs-db` to check its status, then `make restart-api` to retry.

**If you get `401` on every request after login**, double-check that you are sending the header as `Authorization: Bearer <token>` — the word `Bearer` and the space are required.
