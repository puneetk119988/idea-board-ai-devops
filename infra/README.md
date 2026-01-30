# Terraform (Multi-Cloud Skeleton)

This folder provides a multi-cloud layout:

- `aws/` — AWS provider: VPC + EKS skeleton + RDS placeholders
- `gcp/` — GCP provider: VPC + GKE skeleton + Cloud SQL placeholders
- `modules/` — shared interface modules

This is intentionally **minimal but correct** so you can extend quickly in an interview:
- add node groups
- add managed DB resources
- wire secrets to K8s via External Secrets / CSI driver

