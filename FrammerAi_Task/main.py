from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pymysql
from db import get_db_connection
import os

app = FastAPI()

# CORS middleware setup
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:8000",
    "file://",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specify the allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Serve static files (index.html and others)
app.mount("/static", StaticFiles(directory="."), name="static")

# Pydantic model for user data
class User(BaseModel):
    name: str
    email: str
    phone: str

@app.get("/")
async def read_root():
    with open("index.html", "r") as f:
        content = f.read()
    return Response(content=content, media_type="text/html")

@app.post("/api/users")
async def add_user(user: User):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, phone) VALUES (%s, %s, %s)", 
                   (user.name, user.email, user.phone))
    conn.commit()
    conn.close()
    return {"message": "User added successfully"}

@app.get("/api/users")
async def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return [{"id": user[0], "name": user[1], "email": user[2], "phone": user[3]} for user in users]

@app.put("/api/users/{user_id}")
async def update_user(user_id: int, user: User):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET name = %s, email = %s, phone = %s WHERE id = %s", 
        (user.name, user.email, user.phone, user_id)
    )
    conn.commit()
    conn.close()
    return {"message": "User updated successfully"}

@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    conn.close()
    return {"message": "User deleted successfully"}
