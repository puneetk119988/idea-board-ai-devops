# Idea Board — AI-First, Cloud-Agnostic DevOps Platform

This repository is a complete reference solution for the case study **“Building an AI‑First, Cloud‑Agnostic DevOps Platform”** (Idea Board app + Docker + Kubernetes + Terraform multi-cloud + AI-assisted CI/CD).

## Architecture (high level)

- **Frontend**: React (served via Nginx)  
- **Backend**: FastAPI (REST API)  
- **DB**: PostgreSQL  
- **Local dev**: Docker Compose  
- **Cloud runtime**: Kubernetes (EKS / GKE)  
- **Managed DB**: RDS (AWS) / Cloud SQL (GCP) *(infra skeleton provided)*  
- **CI/CD**: GitHub Actions with AI-assisted deployment planning + optional AI log analysis

---

## 1) Run locally with Docker Compose

### Prereqs
- Docker + Docker Compose

### Start
```bash
docker compose up --build
```

Open:
- Frontend: http://localhost:3000
- Backend health: http://localhost:8000/health
- Backend API: http://localhost:8000/api/ideas

### Stop
```bash
docker compose down -v
```

---

## 2) Container images

Build locally:
```bash
docker build -t idea-board-backend:local ./backend
docker build -t idea-board-frontend:local ./frontend
```

---

## 3) Kubernetes deploy (any K8s)

### Prereqs
- kubectl configured to your cluster
- A container registry (ECR/GAR/DockerHub) and pushed images
- A PostgreSQL endpoint (managed DB or in-cluster)

### Apply manifests
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/
```

> Update `k8s/backend-deployment.yaml` with your `DATABASE_URL` secret and image names.

---

## 4) Cloud-agnostic IaC (Terraform)

The `infra/` folder provides a **multi-cloud structure** and reusable modules.

- `infra/aws` → EKS + networking + RDS placeholders
- `infra/gcp` → GKE + networking + Cloud SQL placeholders
- `infra/modules` → shared module interface

### Example
```bash
cd infra/aws
terraform init
terraform apply -var="project_name=idea-board" -var="region=us-east-1"
```

```bash
cd infra/gcp
terraform init
terraform apply -var="project_name=idea-board" -var="region=us-central1"
```

> The modules are intentionally written so adding a 3rd cloud means adding a new provider folder with minimal changes.

---

## 5) AI integration in CI/CD

Workflow: `.github/workflows/ai-cicd.yaml`

### What it can do
- Generate a deployment plan using an LLM (e.g., OpenAI) based on:
  - branch name (`feature/*` → preview namespace)
  - PR comment commands (`/deploy-preview`, `/promote-prod`)
- Run post-deploy health checks
- (Optional) Fetch logs and ask AI to summarize + decide rollback

### Setup secrets in GitHub
- `OPENAI_API_KEY` (or set `LLM_API_KEY` and change script)
- `KUBECONFIG_B64` (base64 of kubeconfig) **or** use OIDC + cloud auth

---

## 6) Deliverables checklist
- ✅ App code: frontend + backend + postgres schema
- ✅ Dockerfiles + Compose
- ✅ K8s manifests (namespace, deployments, services, ingress template)
- ✅ Terraform multi-cloud skeleton + modules
- ✅ AI-powered CI/CD workflow + scripts
- ✅ Comprehensive README

---

## Notes
This repo is designed to be:
- easy to run locally
- portable to any Kubernetes
- cloud-agnostic at the “platform interface” level (variables + modules)

