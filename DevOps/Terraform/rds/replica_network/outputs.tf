output "replica_a_subnet_id" {
    value = aws_subnet.replica_a.id
}

output "replica_b_subnet_id" {
    value = aws_subnet.replica_b.id
}

output "replica_c_subnet_id" {
    value = aws_subnet.replica_c.id
}

output "replica_vpc" {
    value = aws_vpc.replica.id
}
