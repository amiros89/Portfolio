resource "aws_security_group" "replica" {
  name        = local.resource_name
  description = "Allow just Postgres inbound"
  vpc_id      = var.vpc_id
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "TCP"
    cidr_blocks = ["0.0.0.0/0"]
  }

 tags = {
    Name = local.resource_name
  }
}

