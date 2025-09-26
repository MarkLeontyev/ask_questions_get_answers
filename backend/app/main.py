from fastapi import FastAPI
from .core.config import settings
from .db.base import Base
from .db.session import engine
from .api.router import api_router
from . import models  # noqa: F401

# Создать таблицы при старте (для простоты без миграций)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Answer Question API", version="1.0.0")

app.include_router(api_router)


@app.get("/health")
def health_check():
    return {"status": "ok", "db": True}
