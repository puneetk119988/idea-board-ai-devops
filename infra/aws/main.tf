# Minimal AWS skeleton (extend as needed):
# - VPC
# - EKS
# - RDS Postgres
#
# In interviews, explain you keep cloud-specific resources here,
# while exposing a common interface (cluster endpoint, kubeconfig, db endpoint).

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = { Name = "${var.project_name}-vpc" }
}

output "aws_vpc_id" {
  value = aws_vpc.main.id
}
