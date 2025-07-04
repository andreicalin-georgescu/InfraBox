module "resource_group" {
  source      = "../../modules/resource_group"
  name_prefix = var.name_prefix
  environment = var.environment
  location    = var.location
  tags        = var.tags
}

module "networking" {
  source                  = "../../modules/networking"
  prefix                  = var.name_prefix
  location                = var.location
  resource_group_name     = module.resource_group.resource_group_name
  dns_zone_name           = var.dns_zone_name
  vnet_address_space      = ["10.0.0.0/16"]
  subnet_address_prefixes = ["10.0.1.0/24"]
}
