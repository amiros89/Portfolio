locals{
    endpoint_parts = split(":",aws_db_instance.main.endpoint)
    hostname = element(local.endpoint_parts,0)
    port = element(local.endpoint_parts,1)
    test = local.endpoint_parts
    arn = aws_db_instance.main.arn
}

output "hostname" {
  value = local.hostname
}

output "port" {
  value = local.port
}

output "arn" {
  value = local.arn
}