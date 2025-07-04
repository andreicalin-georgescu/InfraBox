variable "name" {
    description = "Name of the storage account"
    type        = string
}
variable "resource_group_name" {
    description = "Resource group in which to create the storage account"
    type        = string
}
variable "location" {
    description = "Azure region for the storage account"
    type        = string
}
variable "account_tier" {
  description = "Performance tier for the storage account"
  type        = string
  default     = "Standard"
}
variable "account_replication_type" {
  description = "Replication type for the storage account"
  type        = string
  default     = "LRS"
}
