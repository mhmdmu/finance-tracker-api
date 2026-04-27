from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.database as db
from app.routers import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    app.state.pool = await db.connect()
    yield
    # On shutdown
    await db.disconnect(app.state.pool)


app = FastAPI(lifespan=lifespan)

routers_prefix = "/api/v1"
app.include_router(auth.router, prefix=routers_prefix)
