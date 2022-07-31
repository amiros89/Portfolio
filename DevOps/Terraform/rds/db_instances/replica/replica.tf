resource "aws_db_instance" "replica" {
  allocated_storage    = 20
  max_allocated_storage = 100
  storage_type         = "gp2"
  instance_class       = "db.m5.large"
  identifier           = local.resource_name
  port                 = var.port
  db_subnet_group_name = aws_db_subnet_group.replica_subnet_group.id
  vpc_security_group_ids    = [aws_security_group.replica.id]
  skip_final_snapshot       = true
  final_snapshot_identifier = "Ignore"
  publicly_accessible = true
  delete_automated_backups = false
  deletion_protection = true
  backup_retention_period = 14
  backup_window                = "01:00-01:30"
  maintenance_window           = "SUN:01:31-SUN:02:01"
  allow_major_version_upgrade  = true
  apply_immediately            = true
  replicate_source_db = var.replicate_source_db
tags = {
    Name = var.name
  }
}

