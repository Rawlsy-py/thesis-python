from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, Session, declarative_base
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# Load environment variables
import os
from dotenv import load_dotenv

load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    balances = relationship("Balance", back_populates="user")


class Balance(Base):
    __tablename__ = "balances"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="balances")


# Pydantic schemas
class BalanceCreate(BaseModel):
    id: int
    amount: float


class UserResponse(BaseModel):
    id: int
    name: str
    balances: list[BalanceCreate]


class UpdateBalanceRequest(BaseModel):
    id: int
    balance: float


class UpdateBalanceResponse(BaseModel):
    message: str
    data: BalanceCreate


# Initialize FastAPI app
app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware)
app.add_middleware(HTTPSRedirectMiddleware)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Routes
@app.get("/", response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).limit(10).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/update-balance", response_model=UpdateBalanceResponse)
async def update_balance(request: UpdateBalanceRequest, db: Session = Depends(get_db)):
    if not request.id or not request.balance:
        raise HTTPException(status_code=400, detail="id and balance are required")

    try:
        balance = db.query(Balance).filter(Balance.id == request.id).first()
        if not balance:
            raise HTTPException(status_code=404, detail="Balance not found")

        balance.amount = request.balance # type: ignore
        db.commit()
        db.refresh(balance)

        return {"message": "Balance updated successfully", "data": balance}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/health-check")
async def health_check():
    return {"health-check": "OK: top level api working"}


# Handle unknown endpoints
@app.middleware("http")
async def unknown_endpoint_middleware(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        return JSONResponse(status_code=404, content={"error": "route not found"})
    return response


# Create tables
Base.metadata.create_all(bind=engine)
