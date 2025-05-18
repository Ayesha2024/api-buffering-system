# 🛠️ DevOps Assessment Project: API Buffering System

> **FastAPI + MongoDB + Docker + Kubernetes (Minikube)**

A fully containerized and Kubernetes-ready REST API system that buffers JSON payloads in-memory, flushes to MongoDB every 100 records, and provides automation scripts for seamless local testing and deployment.

---

## 🔧 Technologies Used

| Tool         | Purpose                        |
| ------------ | ------------------------------ |
| **FastAPI**  | High-performance API server    |
| **MongoDB**  | NoSQL database for persistence |
| **Docker**   | Containerization               |
| **Minikube** | Local Kubernetes cluster       |
| **kubectl**  | Kubernetes CLI                 |
| **Uvicorn**  | ASGI server for FastAPI        |

---

## 💻 System Requirements & Installation

### ✅ Prerequisites

Before running the project, install the following tools:

#### 🐍 Install Python & pip

```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

#### 📦 Install venv (Virtual Environment Tool)

```bash
sudo apt install python3-venv -y
```

#### 🐳 Install Docker

Follow official instructions based on your OS:
[https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

Then check installation:

```bash
docker --version
```

#### ☸️ Install Minikube & kubectl

* Minikube: [https://minikube.sigs.k8s.io/docs/start/](https://minikube.sigs.k8s.io/docs/start/)
* kubectl: [https://kubernetes.io/docs/tasks/tools/](https://kubernetes.io/docs/tasks/tools/)

#### 🟢 Install MongoDB Client (mongosh)

```bash
curl -fsSL https://pgp.mongodb.com/server-6.0.asc | \
  gpg --dearmor -o /usr/share/keyrings/mongodb-server-6.0.gpg

echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | \
  sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

sudo apt update
sudo apt install -y mongodb-mongosh
```

---

## 📦 Setup & Run Instructions (From Scratch)

### 1. **Clone the Repo**

```bash
git clone https://github.com/Ayesha2024/api-buffering-system.git
cd api-buffering-system
```

### 2. **Create Virtual Environment & Install Python Dependencies**

```bash
python3 -m venv venv
source venv/bin/activate
```

Then install required packages:

```bash
pip install fastapi uvicorn pymongo
```

Or install them from:

```bash
pip install -r requirements.txt
```

> 📄 **What is `requirements.txt`?**
> This file lists all required Python libraries. It lets others install the same dependencies using one command: `pip install -r requirements.txt`

---

## 🧪 Project Phases & Execution Flow

### ✅ PHASE 1: Run the App Locally (Without Docker)

1. Make sure MongoDB is installed and running locally:

```bash
sudo systemctl start mongod
```

2. Start FastAPI manually:

```bash
uvicorn main:app --reload
```

3. Access the frontend form page:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

4. Fill in the form and submit — the data is collected and buffered in memory.

5. Once 100 records are buffered, they're flushed to MongoDB.

> 🧠 **Frontend Note:**
> A simple HTML form was created inside `static/index.html` to interact with the FastAPI backend.
> The form uses JavaScript `fetch()` to send JSON data to the `/submit` endpoint.

---

### ✅ PHASE 2: Dockerize the App

While Kubernetes is the final execution environment for this project, Docker was used to demonstrate containerization.

> 🐳 **Note:** You don't need to run this phase manually. The Dockerization process is already reflected in the `Dockerfile` and the pushed image. You may review the following steps for understanding only:

1. Build the Docker image:

```bash
docker build -t api-buffering-app .
```

2. Tag the image for Docker Hub:

```bash
docker tag api-buffering-app callmeash/api-buffering-app:latest  # Public Docker Hub image
```

3. Push the image to Docker Hub:

```bash
docker push callmeash/api-buffering-app:latest
```

4. (Optional) Run locally using Docker Compose:

```bash
docker compose up
```

> This will run the FastAPI app and MongoDB services using the configuration defined in `docker-compose.yml`.

---

### ✅ PHASE 3: Kubernetes Deployment (Minikube)

1. Start Minikube:

```bash
minikube start
```

2. Apply Kubernetes Manifests:

```bash
kubectl apply -f k8s/mongo-deployment.yaml
kubectl apply -f k8s/mongo-service.yaml
kubectl apply -f k8s/app-deployment.yaml
kubectl apply -f k8s/app-service.yaml
```

3. Start port-forwarding + set environment:

```bash
source start_project.sh
```

4. Run test submit script:

```bash
source venv/bin/activate
python test_submit.py
```

5. Confirm entries in MongoDB using:

```bash
mongosh
use people_db
db.people.countDocuments()
```

---

## 📁 Folder Structure

```bash
api-buffering-system/
├── Dockerfile
├── main.py
├── index.html
├── static/
│   └── index.html
├── test_submit.py
├── requirements.txt
├── k8s/
│   ├── app-deployment.yaml
│   ├── app-service.yaml
│   ├── mongo-deployment.yaml
│   └── mongo-service.yaml
├── start_project.sh
```

---

## 🧪 API Behavior Overview

### `/submit` Endpoint

* Accepts a list of person records:

```json
[
  {"first_name": "John", "last_name": "Doe"},
  {"first_name": "Jane", "last_name": "Smith"}
]
```

* Stores records temporarily in memory
* Flushes them to MongoDB when 100 records are reached

---

## 📜 Notes for Reviewers

* ✅ All tools used are open-source and free
* ✅ Docker image is pushed to Docker Hub: `callmeash/api-buffering-app:latest`
* ✅ To confirm DB writes: use `mongosh`, switch to `people_db`, run `db.people.countDocuments()`
* ✅ The `start_project.sh` automates port-forward and env setup cleanly

> 💡 **Important:** Always run the script using `source start_project.sh` (not `./start_project.sh`) to ensure environment variables like `MONGO_URL` persist in your session.

---

## 🧹 Optional Kubernetes Clean-up

```bash
kubectl delete -f k8s/mongo-deployment.yaml
kubectl delete -f k8s/mongo-service.yaml
kubectl delete -f k8s/app-deployment.yaml
kubectl delete -f k8s/app-service.yaml
```

---

## ✅ Final Thoughts

This project demonstrates:

* FastAPI application design
* Docker image creation
* Kubernetes deployment with service integration
* Use of automation scripts for smoother DevOps workflows
* Beginner-friendly setup with clean documentation
