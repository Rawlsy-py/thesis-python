from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from typing import List
import models
from database import engine, get_db
from models import MyTable

app = FastAPI()

# Index Route
@app.get("/")
async def index():
    return {"message":"Server Active"}


