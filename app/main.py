"""FastAPI CRUD Benchmarking App."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()


class User(BaseModel):
    name: str
    country_code: str = Field(..., min_length=2, max_length=2)
    points_balance: int


# In-memory "database"
db: List[User] = []


@app.post("/users/", response_model=User)
def create_user(user: User):
    db.append(user)
    return user


@app.get("/users/", response_model=List[User])
def read_users():
    return db


@app.get("/users/{user_name}", response_model=User)
def read_user(user_name: str):
    for user in db:
        if user.name == user_name:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.put("/users/{user_name}", response_model=User)
def update_user(user_name: str, user_update: User):
    for index, user in enumerate(db):
        if user.name == user_name:
            db[index] = user_update
            return user_update
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_name}", response_model=User)
def delete_user(user_name: str):
    for index, user in enumerate(db):
        if user.name == user_name:
            return db.pop(index)
    raise HTTPException(status_code=404, detail="User not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
