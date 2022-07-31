variable "environment" {
  type = string
}
locals {
  name = "${var.environment}-rds"
}

variable "postgres_username" {
  type = string
}

variable "postgres_password" {
    type = string
    sensitive = true
}

variable "postgres_port" {
}
