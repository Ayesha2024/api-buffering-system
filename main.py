
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient

app = FastAPI()

# In-memory buffer
buffer = []

# MongoDB connection using environment variable
mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017/")
client = MongoClient(mongo_url)

db = client["people_db"]
collection = db["people"]

# Person schema


class Person(BaseModel):
    first_name: str
    last_name: str

# POST /submit


@app.post("/submit")
async def submit(data: List[Person]):
    global buffer
    for person in data:
        buffer.append({"first_name": person.first_name,
                      "last_name": person.last_name})

    # Flush only in 100-record batches
    while len(buffer) >= 100:
        batch = buffer[:100]
        collection.insert_many(batch)
        print(
            f"🔁 Flushing 100 records to MongoDB (buffer size before flush: {len(buffer)})")
        del buffer[:100]

    return {"message": f"Received {len(data)} records."}

# Serve the index.html at root "/"


@app.get("/", response_class=HTMLResponse)
async def serve_form():
    return FileResponse("static/index.html")
