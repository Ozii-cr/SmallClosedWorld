output "scw_server_public_ip" {
  description = "Public IP address of the instance "
  value       = module.scw_server.public_ip
}

output "scw_server_private_ip" {
  description = "private IP address of the instance "
  value       = module.scw_server.private_ip
}