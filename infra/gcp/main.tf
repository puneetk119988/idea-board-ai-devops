# Minimal GCP skeleton (extend as needed):
# - VPC
# - GKE
# - Cloud SQL Postgres
#
# In interviews, explain you keep cloud-specific resources here,
# while exposing a common interface (cluster endpoint, kubeconfig, db endpoint).

resource "google_compute_network" "main" {
  name                    = "${var.project_name}-vpc"
  auto_create_subnetworks = true
}

output "gcp_network_name" {
  value = google_compute_network.main.name
}
