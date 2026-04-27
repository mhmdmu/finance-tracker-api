from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.database as db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    app.state.pool = await db.connect()
    yield
    # On shutdown
    await db.disconnect(app.state.pool)


app = FastAPI(lifespan=lifespan)
