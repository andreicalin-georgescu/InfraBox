variable "name_prefix" {
  type    = string
  default = "InfraBox"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "location" {
  type    = string
  default = "westeurope"
}

variable "dns_zone_name" {
  default = "infrabox-dev.com"
}

variable "tags" {
  type = map(string)
  default = {
    project     = "InfraBox"
    environment = "Dev"
  }
}
