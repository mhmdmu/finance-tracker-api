# Personal Finance Tracker API

A simple backend service for tracking personal finances across multiple accounts.

## Overview

This project allows users to:

- Manage multiple financial accounts (cash, bank, credit)
- Record income and expenses
- Categorize transactions
- View transaction history with filters
- Get basic monthly summaries

## Features

* User authentication (register & login)
* Multiple accounts per user
* Transaction tracking (income & expense)
* Categories (default + custom)
* Monthly reports:
  * Total income vs expense
  * Spending by category
* Pagination on list endpoints

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL

---

## Base URL

```
/api/v1
```

---

## Auth

### `POST /auth/register`

Create a new user.

### `POST /auth/login`

Returns a bearer token.

```
{
  "access_token": "...",
  "token_type": "bearer"
}
```

---

## Accounts

### `GET /accounts`

List all user accounts.

### `GET /accounts/{acc_id}`

Get a single account.

### `POST /accounts`

Create account.

### `PATCH /accounts/{acc_id}`

Update account (name/type).

### `DELETE /accounts/{acc_id}`

Delete account.

---

## Transactions

### `GET /accounts/{acc_id}/transactions`

List transactions (supports pagination and filters via query params).

### `GET /accounts/{acc_id}/transactions/{trans_id}`

Get a specific transaction.

### `POST /accounts/{acc_id}/transactions`

Create a transaction.

### `DELETE /accounts/{acc_id}/transactions/{trans_id}`

Delete transaction.

---

## Reports

### `GET /accounts/{acc_id}/reports/cashflow`

Monthly income vs expenses.

Query:

```
?month=MM&year=YYYY
```

### `GET /accounts/{acc_id}/reports/spendings`

Spending grouped by category.

---

## Categories

### `GET /categories`

List user categories.

### `POST /categories`

Create category.

```
{ "name": "Food" }
```

### `PATCH /categories/{cat_id}`

Rename category.

### `DELETE /categories/{cat_id}`

Delete category.

---

## Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/finance_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Notes

* `DATABASE_URL` → Async PostgreSQL connection (required)
* `SECRET_KEY` → used to sign JWT tokens (don’t hardcode this in production)
* `ACCESS_TOKEN_EXPIRE_MINUTES` → token lifetime

---
## Running the Project

### Install dependencies

```
pip install -r requirements.txt
```

### Setup database

Run:

```
migrations/init.sql
```

### Start server

```
uvicorn app.main:app --reload
```

---

## Notes

* All protected routes require `Authorization: Bearer <token>`
* Ownership is enforced (accounts, transactions, categories)
* Errors return meaningful HTTP status codes (401, 404, 422, etc.)
