resource "aws_db_subnet_group" "replica_subnet_group" {
  name = local.resource_name
  subnet_ids = var.subnet_ids
  
  tags = {
    Name = local.resource_name
  }
}