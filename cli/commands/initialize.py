from pathlib import Path
from cli.utils import ENVIRONMENTS_DIR
from cli.terraform_utils import terraform_init, terraform_validate
import re


def sanitize_input(value: str) -> str:
    """Sanitize CLI input to avoid injection or path traversal."""
    return re.sub(r"[^\w\-]", "", value.strip())


def prompt_with_default(prompt_text: str, default: str) -> str:
    user_input = input(f"{prompt_text} [default: {default}]: ").strip()
    return sanitize_input(user_input) if user_input else default


def generate_variables_tf(env_path: Path, variables: dict, dry_run=False):
    content = f"""\
    variable "name_prefix" {{
    type    = string
    default = "{variables['name_prefix']}"
    }}

    variable "environment" {{
    type    = string
    default = "{variables['environment']}"
    }}

    variable "location" {{
    type    = string
    default = "{variables['location']}"
    }}

    variable "dns_zone_name" {{
    type = string
    default = "{variables['dns_zone_name']}"
    }}

    variable "admin_username" {{
    type = string
    default = "{variables['admin_username']}"
    }}

    variable "ssh_public_key_path" {{
    type = string
    default = "{variables['ssh_public_key_path']}"
    }}

    variable "tags" {{
    type = map(string)
    default = {{
        "project" = "InfraBox"
        "environment" = "{variables['environment']}"
    }}
    }}
    """
    if dry_run:
        print("INFRABOX: 🔍 Dry-run mode: variables.tf not written to disk.")
        print(content)
        return
    (env_path / "variables.tf").write_text(content)
    print("INFRABOX: 📝 Generated variables.tf")


def generate_main_tf(env_path: Path, dry_run=False):
    content = """\
    module "resource_group" {
    source   = "../../modules/resource_group"
    name     = "${var.name_prefix}-${var.environment}-RG"
    location = var.location
    tags     = var.tags
    }

    module "networking" {
    source                  = "../../modules/networking"
    name                    = "${var.name_prefix}-${var.environment}"
    location                = var.location
    resource_group_name     = module.resource_group.resource_group_name
    dns_zone_name           = var.dns_zone_name
    vnet_address_space      = ["10.0.0.0/16"]
    subnet_address_prefixes = ["10.0.1.0/24"]
    tags                    = var.tags
    }

    module "virtual_machine" {
    source               = "../../modules/virtual_machine"
    name                 = "${var.name_prefix}-VM"
    resource_group_name  = module.resource_group.resource_group_name
    location             = var.location
    vm_size              = "Standard_B1s"
    admin_username       = "${var.admin_username}-${var.environment}"
    ssh_public_key_path  = var.ssh_public_key_path
    network_interface_id = module.networking.network_interface_id
    tags                 = var.tags
    }

    module "storage_account" {
    source                   = "../../modules/storage_account"
    name                     = lower(replace("${var.name_prefix}-${var.environment}-SA01", "-", ""))
    resource_group_name      = module.resource_group.resource_group_name
    location                 = var.location
    account_tier             = "Standard"
    account_replication_type = "LRS"
    tags                     = var.tags
    }
    """
    if dry_run:
        print("INFRABOX: 🔍 Dry-run mode: main.tf not written to disk.")
        print(content)
        return
    (env_path / "main.tf").write_text(content)
    print("INFRABOX: 📝 Generated main.tf")


def generate_outputs_tf(env_path: Path, dry_run=False):
    content = """\
    output "resource_group_name" {
    value = module.resource_group.resource_group_name
    }

    output "vm_name" {
    value = module.virtual_machine.name
    }

    output "storage_account_name" {
    value = module.storage_account.name
    }
    """
    if dry_run:
        print("INFRABOX: 🔍 Dry-run mode: outputs.tf not written to disk.")
        print(content)
        return
    (env_path / "outputs.tf").write_text(content)
    print("INFRABOX: 📝 Generated outputs.tf")


def run(args):
    environment = sanitize_input(args.environment.lower())
    env_path = ENVIRONMENTS_DIR / environment

    if env_path.exists():
        print(f"INFRABOX: ⚠️ Environment '{environment}' already exists. Aborting.")
        return

    if not args.dry_run:
        env_path.mkdir(parents=True)
        print(f"INFRABOX: 📁 Created environment directory at {env_path}")

    # Prompts for interactive UX with secure defaults
    name_prefix = prompt_with_default("Name prefix", "InfraBox")
    location = prompt_with_default("Azure region", "westeurope")
    dns_zone_name = prompt_with_default(
        "DNS zone name", "infrabox-" + environment + ".com"
    )
    admin_username = prompt_with_default("Admin username", "azureuser")
    ssh_public_key_path = prompt_with_default(
        "SSH public key path", "~/.ssh/id_rsa_infrabox.pub"
    )

    variables = {
        "name_prefix": name_prefix,
        "environment": environment,
        "location": location,
        "dns_zone_name": dns_zone_name,
        "admin_username": admin_username,
        "ssh_public_key_path": ssh_public_key_path,
    }

    generate_variables_tf(env_path, variables, dry_run=args.dry_run)
    generate_main_tf(env_path, dry_run=args.dry_run)
    generate_outputs_tf(env_path, dry_run=args.dry_run)

    terraform_init(env_path, dry_run=args.dry_run)
    print(
        ""
        if args.dry_run
        else f"INFRABOX: ✅ Initialization complete for environment: {environment}"
    )
    terraform_validate(env_path, dry_run=args.dry_run)
    print(
        ""
        if args.dry_run
        else f"INFRABOX: ✅ Validation complete for environment: {environment}"
    )
