from fastapi import FastAPI, HTTPException
from asyncpg import create_pool, Connection
from typing import List, Dict
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import os

app = FastAPI()


# Load environment variables from .env file
load_dotenv()

# PostgreSQL connection string from .env file
DATABASE_URL = os.getenv("CONNECTION_STRING")


# Create a connection pool
async def get_db_pool():
    pool = await create_pool(DATABASE_URL)
    return pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_pool = await get_db_pool()
    await app.state.db_pool.close()


@app.get("/", response_model=List[Dict])
async def get_users():
    try:
        async with app.state.db_pool.acquire() as connection:
            records = await connection.fetch("SELECT * FROM users")
            return [dict(record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
