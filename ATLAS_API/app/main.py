from fastapi import FastAPI
from contextlib import asynccontextmanager
from ATLAS_API.app.utilities.utilities import check_battery
import asyncio

# @asynccontextmanager
# async def battery_status(app: FastAPI):
#     # creating task
#     task = asyncio.create_task(check_battery())
#     yield
#     task.cancel()


# app = FastAPI(lifespan=battery_status)
app = FastAPI()

@app.get("/")
def root():
    return {"message": "This is my personal AI assistant named 'ATLAS AI'."}


# including all the router
from ATLAS_API.app import telegram_api
app.include_router(telegram_api.router)