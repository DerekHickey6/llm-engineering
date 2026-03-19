# Kubernetes Deployment — FastAPI RAG

Deploys the Dockerized RAG API (FastAPI + ChromaDB + Ollama) to a local Kubernetes cluster using Minikube. Demonstrates pod orchestration, service discovery, scaling, and multi-container deployments in Kubernetes.

## What It Does

- Runs the FastAPI RAG backend as a Kubernetes Deployment with 2 replicas
- Runs Ollama as a separate pod, exposed internally via a Kubernetes Service
- FastAPI pods connect to Ollama using K8s service discovery (`http://ollama:11434`)
- Exposes the FastAPI API externally via a NodePort Service

## Tech Stack

- **Kubernetes** — container orchestration
- **Minikube** — local single-node K8s cluster for development
- **kubectl** — K8s CLI for managing deployments and pods
- **Docker** — container runtime (built inside Minikube's Docker daemon)
- **FastAPI** — REST API backend (from dockerized-rag project)
- **Ollama** — local LLM inference (`llama3.2`, `nomic-embed-text`)
- **ChromaDB** — vector database for RAG retrieval

## Project Structure

```
kubernetes/
├── k8s/
│   ├── deployment.yaml          # FastAPI app deployment (2 replicas)
│   ├── service.yaml             # Exposes FastAPI via NodePort
│   ├── ollama-deployment.yaml   # Ollama deployment (1 replica)
│   └── ollama-service.yaml      # Exposes Ollama internally on port 11434
├── .gitignore
└── README.md
```

## Setup

**1. Start Minikube**
```bash
minikube start
```

**2. Point shell at Minikube's Docker daemon**
```powershell
minikube docker-env | Invoke-Expression
```

**3. Build the Docker image inside Minikube**
```bash
docker build -t fastapi-rag:latest path/to/dockerized-rag/
```

**4. Apply all K8s configs**
```bash
kubectl apply -f k8s/
```

**5. Pull models into the Ollama pod**
```bash
kubectl exec -it <ollama-pod-name> -- ollama pull llama3.2
kubectl exec -it <ollama-pod-name> -- ollama pull nomic-embed-text
```

**6. Copy PDF and run ingest**
```bash
kubectl exec <fastapi-pod-name> -- mkdir -p /app/data
kubectl cp Intro_to_Data_Mining.pdf <fastapi-pod-name>:/app/data/Intro_to_Data_Mining.pdf
kubectl exec -it <fastapi-pod-name> -- python ingest.py
```

**7. Get the service URL**
```bash
minikube service fastapi-rag-service --url
```

## Usage

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:<port>/ask" -Method POST -ContentType "application/json" -Body '{"question": "What is data mining?"}'
```

## Key Concepts

- **Pod** — smallest deployable unit in K8s, wraps one or more containers
- **Deployment** — manages a set of identical pods, handles scaling and restarts
- **Service** — exposes pods to network traffic; NodePort for external access, ClusterIP for internal
- **Service Discovery** — pods find each other by service name (e.g. `http://ollama:11434`)
- **`imagePullPolicy: Never`** — tells K8s to use the locally built image instead of pulling from a registry
- **`kubectl exec`** — runs commands inside a running pod (equivalent to `docker exec`)
- **`kubectl cp`** — copies files between local machine and a pod

## Notes

- ChromaDB data is stored inside the pod and lost on restart — a persistent volume would be needed in production
- Ollama runs on CPU inside the cluster — inference is slow without a GPU node
- In production, this cluster would run on cloud-managed K8s (EKS, GKE, AKS) across multiple worker nodes
