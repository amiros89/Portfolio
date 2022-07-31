locals{
    endpoint_parts = split(":",aws_db_instance.replica.endpoint)
    hostname = element(local.endpoint_parts,0)
    port = element(local.endpoint_parts,1)
    test = local.endpoint_parts

}

output "hostname" {
  value = local.hostname
}

output "port" {
  value = local.port
}


output "test" {

  value = local.test
}