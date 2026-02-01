# ================= AWS ROOT STACK =================

module "network" {
  source       = "../modules/network"
  cloud        = "aws"
  project_name = var.project_name
  aws_region   = var.aws_region
  gcp_region   = ""
}

module "database" {
  source            = "../modules/database"
  cloud             = "aws"
  project_name      = var.project_name
  db_username       = var.db_username
  db_password       = var.db_password
  vpc_id            = module.network.vpc_id
  private_subnet_id = module.network.private_subnet_ids
  region            = var.aws_region
}

module "kubernetes" {
  source       = "../modules/kubernetes"
  cloud        = "aws"
  project_name = var.project_name
  region       = var.aws_region

  subnet_ids = concat(
    module.network.public_subnet_ids,
    module.network.private_subnet_ids
  )

  eks_instance_type = var.eks_instance_type
  desired_size      = var.eks_desired_capacity
  min_size          = var.eks_min_size
  max_size          = var.eks_max_size
}