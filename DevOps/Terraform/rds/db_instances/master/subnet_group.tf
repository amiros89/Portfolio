resource "aws_db_subnet_group" "rds" {
  name = local.resource_name
  subnet_ids = var.subnet_ids
  
  tags = {
    Name = local.resource_name
  }
}