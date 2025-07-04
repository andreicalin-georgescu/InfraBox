locals {
  prefix   = "InfraBox-${var.environment}"
  location = var.location
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
