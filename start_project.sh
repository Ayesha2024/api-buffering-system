#!/bin/bash

echo "🚀 Starting API Buffering System (FastAPI + MongoDB via Kubernetes)"

# Step 1: Kill existing port-forward processes (if any)
echo "🛑 Killing any previous port-forwarding on ports 8000 and 27017..."
lsof -ti:8000 | xargs -r kill -9
lsof -ti:27017 | xargs -r kill -9

# Step 2: Start MongoDB port-forward in background
echo "📡 Starting MongoDB port-forward (localhost:27017)..."
kubectl port-forward svc/mongo 27017:27017 > /dev/null 2>&1 &
echo $! > .mongo_pf_pid

# Step 3: Start FastAPI port-forward in background
echo "📡 Starting FastAPI port-forward (localhost:8000)..."
kubectl port-forward svc/api-buffering-service 8000:8000 > /dev/null 2>&1 &
echo $! > .fastapi_pf_pid

# Step 4: Export environment variable
export MONGO_URL="mongodb://localhost:27017/"
echo "✅ MONGO_URL exported as $MONGO_URL"

echo "🎯 Project is now ready. Visit: http://localhost:8000/"

