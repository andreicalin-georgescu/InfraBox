from cli.utils import (
    ENVIRONMENTS_DIR,
    sanitize_input,
    prompt_with_default,
    create_provider_symlink,
)
from cli.terraform_utils import terraform_init, terraform_validate
from cli.infrastructure_templates import (
    generate_main_tf,
    generate_variables_tf,
    generate_outputs_tf,
)


def run(args):
    environment = sanitize_input(args.environment.lower())
    env_path = ENVIRONMENTS_DIR / environment

    if env_path.exists():
        print(
            f"INFRABOX: ⚠️ Environment files for environment '{environment}' already exist. Aborting."
        )
        return

    if not args.dry_run:
        env_path.mkdir(parents=True)
        print(f"INFRABOX: 📁 Created environment directory at {env_path}")
        create_provider_symlink(env_path, dry_run=args.dry_run)

    # Prompt user for core environment values
    variables = {
        "name_prefix": prompt_with_default("Enter name prefix", "Infrabox"),
        "environment": environment,
        "location": prompt_with_default("Enter Azure location", "westeurope"),
        "dns_zone_name": prompt_with_default(
            "Enter DNS zone name", f"Infrabox-{environment}.com"
        ),
        "admin_username": prompt_with_default("Enter admin username", "azureuser"),
        "ssh_public_key_path": prompt_with_default(
            "Enter path to SSH public key", "~/.ssh/id_rsa_infrabox.pub"
        ),
    }

    # Render all Terraform files using jinja2 templates
    generate_variables_tf(env_path, context=variables, dry_run=args.dry_run)
    generate_main_tf(env_path, context=variables, dry_run=args.dry_run)
    generate_outputs_tf(env_path, context=variables, dry_run=args.dry_run)

    # Run Terraform initialization & validation
    terraform_init(env_path, dry_run=args.dry_run)
    terraform_validate(env_path, dry_run=args.dry_run)

    if not args.dry_run:
        print(
            f"INFRABOX: ✅ Initialization and validation complete for environment: {environment}"
            f"\nINFRABOX: 📂 Environment files created at {env_path}."
        )
