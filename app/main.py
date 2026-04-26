from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.database as db


@asynccontextmanager
async def lifespan(_: FastAPI):
    # On startup
    await db.connect()
    yield
    # On shutdown
    await db.disconnect()


app = FastAPI(lifespan=lifespan)
