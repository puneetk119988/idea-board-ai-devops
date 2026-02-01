variable "cloud" { type = string }
variable "project_name" { type = string }
variable "region" { type = string }
variable "subnet_ids" { type = list(string) }
variable "eks_instance_type" { type = string }
variable "desired_size" { type = number }
variable "min_size" { type = number }
variable "max_size" { type = number }