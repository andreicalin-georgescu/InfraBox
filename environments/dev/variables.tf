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

variable "tags" {
  type = map(string)
  default = {
    project     = "InfraBox"
    environment = "Dev"
  }
}
