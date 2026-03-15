from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "This is my personal AI assistant named 'ATLAS AI'."}

# including all the router
from ATLAS_API.app import telegram_api
app.include_router(telegram_api.router)