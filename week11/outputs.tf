# Outputs are printed after apply and by `terraform output`

# The ID AWS assigned to the instance
output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.app_server.id
}

# Public IP used to SSH into or browse to the server
output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.app_server.public_ip
}