output "vpc_id" {
  value = var.cloud == "aws" ? aws_vpc.vpc[0].id : ""
}

output "public_subnet_ids" {
  value = var.cloud == "aws" ? [aws_subnet.public_a[0].id, aws_subnet.public_b[0].id] : []
}

output "private_subnet_ids" {
  value = var.cloud == "aws" ? [aws_subnet.private_a[0].id, aws_subnet.private_b[0].id] : []
}