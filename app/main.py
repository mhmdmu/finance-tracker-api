from contextlib import asynccontextmanager

import database as db
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_: FastAPI):
    # On startup
    await db.connect()
    yield
    # On shutdown
    await db.disconnect()


app = FastAPI(lifespan=lifespan)
