variable "name_prefix" {
  description = "The prefix used in naming resources"
  type        = string
}

variable "environment" {
  description = "The environment name (e.g., dev, test, prod)"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "tags" {
  description = "Tags to apply to the resource group"
  type        = map(string)
  default     = {}
}
