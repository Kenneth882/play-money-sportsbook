from fastapi import FastAPI

from app.api import health

app = FastAPI(title="HoopsExchange")
app.include_router(health.router)
