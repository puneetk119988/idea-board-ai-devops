output "rds_endpoint" {
  value = var.cloud == "aws" ? aws_db_instance.postgres[0].endpoint : ""
}