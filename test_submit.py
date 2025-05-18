import requests
import random
import string
import os
from pymongo import MongoClient


def generate_name():
    first = ''.join(random.choices(string.ascii_letters, k=5)).capitalize()
    last = ''.join(random.choices(string.ascii_letters, k=7)).capitalize()
    return {"first_name": first, "last_name": last}


# Step 1: Send 100 names to FastAPI
url = "http://localhost:8000/submit"
headers = {"Content-Type": "application/json"}
data = [generate_name() for _ in range(100)]

response = requests.post(url, json=data, headers=headers)
# print("POST Status:", response.status_code)
print("POST Response:", response.json())

# Step 2: Use strict environment-based MongoDB connection
mongo_url = os.getenv("MONGO_URL")
if not mongo_url:
    print("❌ ERROR: MONGO_URL environment variable is not set.")
    print("💡 Tip: Run `export MONGO_URL=\"mongodb://localhost:27017/\"` or use start_project.sh")
    exit(1)

print(f"🧩 Connecting to MongoDB at: {mongo_url}")
client = MongoClient(mongo_url)
db = client.people_db
collection = db.people

# Step 3: Count and display how many records are stored
count = collection.count_documents({})
print(f"✅ MongoDB now contains {count} people records.")
