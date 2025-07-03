# Define the cloud provider. In this case, we use Azure
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }

  required_version = ">=1.4"
}

provider "azurerm" {
  features {}
}