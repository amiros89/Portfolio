variable "name" {
  type = string
}
locals {
  resource_name = "${var.name}-rds-replica"
}

