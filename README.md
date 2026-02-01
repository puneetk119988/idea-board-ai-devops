Idea Board – AI-First, Cloud-Agnostic DevOps Platform

Repository:
https://github.com/puneetk119988/idea-board-ai-devops

This project demonstrates the design and implementation of a modern, AI-enhanced, cloud-agnostic DevOps platform using a simple full-stack application called Idea Board.
The focus is not just application code, but production-grade deployment, automation, and intelligent CI/CD workflows.

1️) High-Level Architecture

Application Flow
User Browser
     |
     v
Cloud Load Balancer (AWS ELB)
     |
     v
Frontend (React + Nginx)
     |
     |  /api proxy
     v
Backend (FastAPI on Kubernetes)
     |
     v
Managed PostgreSQL Database (RDS)

Components

Frontend: React application served via Nginx

Backend: FastAPI (Python) REST API

Database: PostgreSQL

Orchestration: Kubernetes

Infrastructure as Code: Terraform

CI/CD: GitHub Actions

AI Integration: AI-assisted deployment planning, configuration, and health analysis

2️) Local Development (Docker Compose)

Prerequisites

Docker

Docker Compose

Run the Application Locally
git clone https://github.com/puneetk119988/idea-board-ai-devops.git
cd idea-board-ai-devops
docker compose up --build

Access Locally

Frontend: http://localhost:8080
API: http://localhost:8080/api/ideas

Verify Persistence
docker exec -it idea_board_db psql -U postgres -d idea_board
SELECT * FROM ideas;


This confirms data is stored in PostgreSQL.

3️) Cloud Deployment (Production)

AWS Deployment (Implemented)
Infrastructure Provisioning (Terraform)
cd infra/aws
terraform init
terraform apply -auto-approve


Terraform provisions:

VPC and networking

EKS cluster

Amazon RDS PostgreSQL

Configure kubectl
aws eks update-kubeconfig --name idea-board-eks --region us-east-1
kubectl get nodes

Deploy Application to Kubernetes
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml


Verify:

kubectl -n idea-board get pods
kubectl -n idea-board get svc frontend-svc

4️) AI-Powered CI/CD Pipeline

Pipeline Overview

The CI/CD pipeline is implemented using GitHub Actions and enhanced with AI-assisted automation.

Triggers

Push to main

Manual workflow dispatch

Natural language commands (example):

/deploy prod goal=ha

Required GitHub Secrets
Secret Name Purpose
AWS_ACCESS_KEY_ID AWS authentication
AWS_SECRET_ACCESS_KEY AWS authentication
AWS_REGION  AWS region
KUBECONFIG_B64  Base64-encoded kubeconfig
OPENAI_API_KEY  (Optional) Enables AI reasoning
Generate KUBECONFIG_B64
python - << 'EOF'
import base64, os
path = os.path.expanduser("~/.kube/config")
print(base64.b64encode(open(path,"rb").read()).decode())
EOF

5️) AI Integration (Design & Value)
What AI Does

AI is used to assist, not replace, deterministic automation.

1. AI-Assisted Deployment Planning

AI generates a safe, idempotent kubectl deployment plan

Guardrails prevent destructive commands (no delete/destroy)

2. Dynamic Environment Configuration

AI suggests replica counts based on intent:

cost → minimal replicas

balanced → standard

ha → high availability

Automatically applied before deployment

3. Intelligent Health Checks & Rollback

AI analyzes:

Pod status

Backend logs

Produces human-readable health summaries

Can automatically rollback on anomalies

Safety & Guardrails

Deterministic fallback if AI is unavailable

AI never directly modifies Terraform

Explicit validation against unsafe commands

Result:
AI improves speed, reliability, and clarity without compromising control.


6) Public URLs (Production)
Cloud Provider 1 – AWS (LIVE)
http://a03cb27cd80ba46d594a1f78c654122d-2044313400.us-east-1.elb.amazonaws.com


7) Frequently Used Commands (Interview-Friendly)
Docker
docker compose up --build
docker compose down -v
docker compose logs -f

Kubernetes
kubectl get pods -n idea-board
kubectl logs deploy/backend -n idea-board
kubectl rollout restart deploy/backend -n idea-board
kubectl exec -it deploy/backend -n idea-board -- sh

Terraform
terraform init
terraform plan
terraform apply
terraform destroy

8) Final Notes

-The application is fully functional locally and in production.
-Data persistence is verified via direct database queries.
-CI/CD pipeline demonstrates real-world AI DevOps use cases.