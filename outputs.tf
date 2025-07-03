output "public_ip" {
  description = "Public IP of the virtual machine"
  value       = azurerm_public_ip.main.ip_address
}

output "vm_name" {
  description = "Name of the virtual machine"
  value       = azurerm_linux_virtual_machine.main.name
}

output "resource_group" {
  description = "Resource group name"
  value       = azurerm_resource_group.main.name
}
