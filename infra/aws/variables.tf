variable "project_name" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "db_username" {
  type = string
}

variable "db_password" {
  type = string
  sensitive = true
}

variable "eks_instance_type" {
  type = string
  default = "t3.small"
}

variable "eks_desired_capacity" {
  type = number
  default = 2
}

variable "eks_min_size" {
  type = number
  default = 1
}

variable "eks_max_size" {
  type = number
  default = 3
}
