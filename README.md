# Personal Finance Tracker API

A backend API for tracking personal finances — built with FastAPI and PostgreSQL.

## What it does

The idea is straightforward: you have accounts (cash, bank, credit card), and you record transactions against them. You can categorize those transactions, filter through history, and pull monthly reports to see where your money is going.

Specifically, the API supports:

- Multiple accounts per user
- Income and expense tracking
- Custom categories (on top of the built-in defaults)
- Filtered, paginated transaction history
- Monthly cashflow and spending-by-category reports

## Tech stack

- **FastAPI** — async Python web framework
- **PostgreSQL** — relational database (accessed via asyncpg)
- **JWT** — for authentication (python-jose)

## Getting started

### Prerequisites

- Python 3.11+
- Docker (used to run Postgres locally)
- [just](https://github.com/casey/just) — a command runner (optional, but recommended)

### 1. Clone and install dependencies

```bash
git clone <repo-url>
cd personal-finance-api
pip install -r requirements.txt
```

### 2. Set up environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/finance_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
EXPIRE_MINUTES=30
```

- `DATABASE_URL` — async PostgreSQL connection string (required)
- `SECRET_KEY` — used to sign JWT tokens; do not hardcode this in production
- `EXPIRE_MINUTES` — how long issued tokens stay valid

### 3. Start the database

If you have `just` installed, this will spin up a Postgres container (or start an existing one):

```bash
just db
```

To wipe and re-initialize the database:

```bash
just db-reset
```

If you prefer to manage Postgres yourself, apply the schema from `migrations/init.sql` manually.

### 4. Run the server

```bash
just run
```

Or directly:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs are at `/docs`.

---

## API reference

All routes are prefixed with `/api/v1`. Protected routes require an `Authorization: Bearer <token>` header.

### Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create a new user account |
| POST | `/auth/login` | Authenticate and receive a bearer token |

Login response:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

### Accounts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/accounts` | List all accounts for the authenticated user |
| GET | `/accounts/{acc_id}` | Get a single account |
| POST | `/accounts` | Create a new account |
| PATCH | `/accounts/{acc_id}` | Update account name or type |
| DELETE | `/accounts/{acc_id}` | Delete an account |

### Transactions

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/accounts/{acc_id}/transactions` | List transactions (supports pagination and filters) |
| GET | `/accounts/{acc_id}/transactions/{trans_id}` | Get a single transaction |
| POST | `/accounts/{acc_id}/transactions` | Record a new transaction |
| DELETE | `/accounts/{acc_id}/transactions/{trans_id}` | Delete a transaction |

### Reports

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/accounts/{acc_id}/reports/cashflow` | Monthly income vs. expenses |
| GET | `/accounts/{acc_id}/reports/spendings` | Spending broken down by category |

Cashflow accepts `?month=MM&year=YYYY` query parameters.

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/categories` | List all categories (defaults + custom) |
| POST | `/categories` | Create a custom category |
| PATCH | `/categories/{cat_id}` | Rename a category |
| DELETE | `/categories/{cat_id}` | Delete a category |

---

## Notes

- Each user only sees their own accounts, transactions, and categories — ownership is enforced at the API level.
- Error responses use standard HTTP status codes: `401` for unauthorized, `404` for not found, `422` for validation errors.