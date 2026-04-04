from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()
from contextlib import asynccontextmanager
from ATLAS_API.app.utilities.utilities import check_battery
import asyncio

@asynccontextmanager
async def on_startup(app: FastAPI):
    task = asyncio.create_task(check_battery())
    yield
    task.cancel()

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:8080",
    "http://localhost:5173/"
]
app = FastAPI(lifespan=on_startup)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "This is my personal AI assistant named 'ATLAS AI'."}


# including all the router
from ATLAS_API.app.telegram import telegram_api
from ATLAS_API.app.frontend_endpoint import auth
from ATLAS_API.app.micro_controller import hardware_api
app.include_router(telegram_api.router)
app.include_router(auth.router)
app.include_router(hardware_api.router)