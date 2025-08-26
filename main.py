from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes import router
from db_config import create_db_and_tables


@asynccontextmanager
async def lifespan(_: FastAPI):
    print("📦 Creating tables...")
    create_db_and_tables()
    yield
    print("🔌 Shutdown application...")

app = FastAPI(
    title="My Awesome API",
    description="""
    This API provides endpoints for managing users, authentication, and other features.

    ### Features
    - ✅ RESTful endpoints
    - ✅ SQLite + SQLModel
    - ✅ Swagger
    """,
    version="1.0.0-rc1",
    contact={
        "name": "João Knoller",
        "url": "https://github.com/joaoknoller",
        "email": "joaofelipeknollermarques@gmail.com"
    },
    lifespan=lifespan
    )

app.include_router(router)
