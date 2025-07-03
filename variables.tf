variable "environment" {
  default = "Dev"
}

variable "location" {
  default = "westeurope"
}

variable "admin_username" {
  default = "azureuser"
}

variable "ssh_public_key_path" {
  default = "~/.ssh/id_rsa_infrabox.pub"
}

variable "dns_zone_name" {
  default = "InfraBox-Dev.com"
}
