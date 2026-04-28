from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import app.database as db
from app.exceptions import AuthenticationFailed, DuplicateUsername
from app.routers import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    app.state.pool = await db.connect()
    yield
    # On shutdown
    await db.disconnect(app.state.pool)


app = FastAPI(lifespan=lifespan)

# Routers
routers_prefix = "/api/v1"
app.include_router(auth.router, prefix=routers_prefix)


# Exception handling
@app.exception_handler(AuthenticationFailed)
async def auth_failed_handler(_: Request, e: AuthenticationFailed):
    return JSONResponse(status_code=401, content={"detail": str(e)})


@app.exception_handler(DuplicateUsername)
async def duplicate_username_handler(_: Request, e: DuplicateUsername):
    return JSONResponse(status_code=409, content={"detail": str(e)})
