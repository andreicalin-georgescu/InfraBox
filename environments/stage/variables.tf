variable "name_prefix" {
  type    = string
  default = "Infrabox"
}

variable "environment" {
  type    = string
  default = "stage"
}

variable "location" {
  type    = string
  default = "westeurope"
}

variable "vnet_address_space" {
  type    = list(string)
  default = ["10.0.0.0/16"]
}

variable "subnet_address_space" {
  type    = list(string)
  default = ["10.0.1.0/24"]
}

variable "dns_zone_name" {
  type    = string
  default = "Infrabox-stage.com"
}

variable "admin_username" {
  type    = string
  default = "azureuser"
}

variable "ssh_public_key_path" {
  type    = string
  default = "~/.ssh/id_rsa_infrabox.pub"
}

variable "tags" {
  type = map(string)
  default = {
    project     = "InfraBox"
    environment = "stage"
  }
}