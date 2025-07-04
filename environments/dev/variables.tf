variable "name_prefix" {
  type    = string
  default = "InfraBox"
}

variable "environment" {
  type    = string
  default = "Dev"
}

variable "location" {
  type    = string
  default = "westeurope"
}

variable "dns_zone_name" {
  default = "infrabox-dev.com"
}

variable "admin_username" {
  default = "azureuser"
}

variable "ssh_public_key_path" {
  default = "~/.ssh/id_rsa_infrabox.pub"
}

variable "tags" {
  type = map(string)
  default = {
    project     = "InfraBox"
    environment = "Dev"
  }
}
