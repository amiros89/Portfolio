variable "username" {
    type = string
  }
  
variable "password" {
  type = string
}

variable "port" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}

variable "name" {
  type = string
  
}

variable "vpc_id" {
  type=string
}

variable "replicate_source_db" {
  type = string
}

locals {
  resource_name = "${var.name}-rds-replica"
}
