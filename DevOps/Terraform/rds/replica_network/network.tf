resource "aws_vpc" "replica" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support = true

  tags = {
    Name = local.resource_name
  }
}

resource "aws_subnet" "replica_a" {
  vpc_id     = aws_vpc.replica.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "eu-central-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = local.resource_name
  }
}

resource "aws_subnet" "replica_b" {
  vpc_id     = aws_vpc.replica.id
  cidr_block = "10.0.2.0/24"
  availability_zone = "eu-central-1b"
    map_public_ip_on_launch = true

    tags = {
    Name = local.resource_name
  }
}

resource "aws_subnet" "replica_c" {
  vpc_id     = aws_vpc.replica.id
  cidr_block = "10.0.3.0/24"
  availability_zone = "eu-central-1c"
    map_public_ip_on_launch = true

    tags = {
    Name = local.resource_name
  }
}

resource "aws_internet_gateway" "replica_gw" {
  vpc_id = aws_vpc.replica.id

  tags = {
    Name = local.resource_name
  }
}
resource "aws_route_table" "replica_all" {
  vpc_id = aws_vpc.replica.id

  route {
      cidr_block = "0.0.0.0/0"
      gateway_id = aws_internet_gateway.replica_gw.id
    }
}

resource "aws_route_table_association" "replica_a" {
  subnet_id      = aws_subnet.replica_a.id
  route_table_id = aws_route_table.replica_all.id
}

resource "aws_route_table_association" "replica_b" {
  subnet_id      = aws_subnet.replica_b.id
  route_table_id = aws_route_table.replica_all.id
}

resource "aws_route_table_association" "replica_c" {
  subnet_id      = aws_subnet.replica_c.id
  route_table_id = aws_route_table.replica_all.id
}