# -------- VPC --------
resource "google_compute_network" "vpc" {
  name                    = "${var.project_name}-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
  name          = "${var.project_name}-subnet"
  ip_cidr_range = "10.10.0.0/16"
  region        = var.gcp_region
  network       = google_compute_network.vpc.id
}

resource "google_compute_firewall" "allow_http" {
  name    = "allow-http"
  network = google_compute_network.vpc.name
  allow {
    protocol = "tcp"
    ports    = ["80", "443"]
  }
  source_ranges = ["0.0.0.0/0"]
}

# -------- GKE --------
resource "google_container_cluster" "gke" {
  name     = "${var.project_name}-gke"
  location = var.gcp_region
  initial_node_count = 1
}

# -------- Cloud SQL --------
resource "google_sql_database_instance" "postgres" {
  name             = "${var.project_name}-sql"
  database_version = "POSTGRES_14"
  region           = var.gcp_region
  settings {
    tier = "db-f1-micro"
  }
}