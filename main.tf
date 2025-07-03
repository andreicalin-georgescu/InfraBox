locals {
  prefix   = "InfraBox-${var.environment}"
  location = var.location
}

resource "azurerm_resource_group" "main" {
  name     = "${local.prefix}-RG"
  location = local.location
}

resource "azurerm_virtual_network" "main" {
  name                = "${local.prefix}-VNet"
  address_space       = ["10.0.0.0/16"]
  location            = local.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_subnet" "main" {
  name                 = "${local.prefix}-Subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_public_ip" "main" {
  name                = local.prefix
  resource_group_name = azurerm_resource_group.main.name
  location            = local.location
  allocation_method   = "Static"
  sku                 = "Basic"
}

resource "azurerm_network_interface" "main" {
  name                = "${local.prefix}-NIC"
  location            = local.location
  resource_group_name = azurerm_resource_group.main.name
  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.main.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.main.id
  }
}

resource "azurerm_linux_virtual_machine" "main" {
  name                  = "${local.prefix}-VM"
  resource_group_name   = azurerm_resource_group.main.name
  location              = local.location
  size                  = "Standard_B1s"
  admin_username        = var.admin_username
  network_interface_ids = [azurerm_network_interface.main.id]
  admin_ssh_key {
    username   = var.admin_username
    public_key = file(var.ssh_public_key_path)
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-focal"
    sku       = "20_04-lts"
    version   = "latest"
  }
}

resource "azurerm_storage_account" "main" {
  name                     = lower(replace("${local.prefix}SA01", "-", ""))
  resource_group_name      = azurerm_resource_group.main.name
  location                 = local.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_dns_zone" "main" {
  name                = var.dns_zone_name
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_dns_a_record" "main" {
  name                = "www"
  zone_name           = azurerm_dns_zone.main.name
  resource_group_name = azurerm_resource_group.main.name
  ttl                 = 300
  records             = [azurerm_public_ip.main.ip_address]
}