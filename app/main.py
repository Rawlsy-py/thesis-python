# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
SQLALCHEMY_DATABASE_URL = "postgresql://username:password@postgres:5432/database"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Model
class MyModel(Base):
    __tablename__ = "my_table"
    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(String, index=True)
    balance = Column(Float)


# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI setup
app = FastAPI()


# Pydantic model for request body
class UpdateBalance(BaseModel):
    id: int
    balance: float


# Routes
@app.get("/")
async def get_data():
    db = SessionLocal()
    data = db.query(MyModel).limit(10).all()
    db.close()
    return data


@app.post("/update-balance")
async def update_balance(balance_info: UpdateBalance):
    db = SessionLocal()
    row = db.query(MyModel).filter(MyModel.id == balance_info.id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Row not found")
    row.balance = balance_info.balance
    db.commit()
    db.close()
    return {"message": "Balance updated successfully"}
