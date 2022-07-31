variable "vpc_id" {  
  type = string
}

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

locals {
  resource_name = "${var.name}-rds"
}