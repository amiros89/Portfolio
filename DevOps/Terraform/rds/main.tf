module "rds" {
    source = "./rds/db_instances/master"
    name = local.name
    vpc_id = aws_vpc.main.id
    subnet_ids = [aws_subnet.a.id,aws_subnet.b.id]
    username = var.postgres_username
    password = var.postgres_password
    port = var.postgres_port
}

module "rds_replica" {
    providers = {
        aws = aws.frankfurt
    }
    source = "./rds/db_instances/replica"
    vpc_id = module.rds_replica_network.replica_vpc
    name = local.name
    subnet_ids = [module.rds_replica_network.replica_a_subnet_id,module.rds_replica_network.replica_b_subnet_id,module.rds_replica_network.replica_c_subnet_id]
    username = var.postgres_username
    password = var.postgres_password
    port = var.postgres_port
    replicate_source_db = module.rds.arn
}

module "rds_replica_network" {
    providers = {
        aws = aws.frankfurt
    }
    source = "./rds/replica_network"
    name = local.name
}