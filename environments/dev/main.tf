module "resource_group" {
  source      = "../../modules/resource_group"
  name_prefix = var.name_prefix
  environment = var.environment
  location    = var.location
  tags        = var.tags
}
