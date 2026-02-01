variable "cloud" { type = string }
variable "project_name" { type = string }
variable "db_username" { type = string }
variable "db_password" { type = string }
variable "vpc_id" { type = string }
variable "private_subnet_id" {
  type = list(string)
}
variable "region" { type = string }

