output "eks_cluster_name" {
  value = var.cloud == "aws" ? aws_eks_cluster.eks[0].name : ""
}