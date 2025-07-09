from pathlib import Path
from cli.utils import INFRA_ROOT, ENVIRONMENTS_DIR
from cli.terraform_utils import terraform_init, terraform_validate
from jinja2 import Environment, FileSystemLoader
import re

TEMPLATE_DIR = INFRA_ROOT / "templates"

jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=True,
    trim_blocks=True,
    lstrip_blocks=True,
)


def sanitize_input(value: str) -> str:
    """Sanitize CLI input to avoid injection or path traversal."""
    return re.sub(r"[^\w\-]", "", value.strip())


def prompt_with_default(prompt_text: str, default: str) -> str:
    user_input = input(f"{prompt_text} [default: {default}]: ").strip()
    return sanitize_input(user_input) if user_input else default


def render_template_to_file(
    template_name: str, destination: Path, context: dict, dry_run: bool = False
):
    template = jinja_env.get_template(template_name)
    rendered_content = template.render(context)

    if dry_run:
        print(f"INFRABOX: 🔍 Dry-run mode: {destination.name} not written to disk.")
        print(rendered_content)
    else:
        destination.write_text(rendered_content)
        print(f"INFRABOX: 📝 Generated {destination.name}")


def create_provider_symlink(env_path: Path, dry_run=False):
    shared_provider_path = ENVIRONMENTS_DIR.parent / "Shared" / "provider.tf"
    target_symlink_path = env_path / "provider.tf"

    if not shared_provider_path.exists():
        raise FileNotFoundError(
            f"Shared provider.tf not found at {shared_provider_path}"
        )

    if dry_run:
        print(
            f"INFRABOX: 🔍 Dry-run mode: would create symlink: {target_symlink_path} → {shared_provider_path}"
        )
        return

    try:
        target_symlink_path.symlink_to(shared_provider_path)
        print(
            f"INFRABOX: 🔗 Created symlink: {target_symlink_path} → {shared_provider_path}"
        )
    except FileExistsError:
        print(f"INFRABOX: ⚠️ Symlink already exists: {target_symlink_path}")
    except Exception as e:
        print(f"INFRABOX: ❌ Failed to create symlink: {e}")


def run(args):
    environment = sanitize_input(args.environment.lower())
    env_path = ENVIRONMENTS_DIR / environment

    if env_path.exists():
        print(f"INFRABOX: ⚠️ Environment '{environment}' already exists. Aborting.")
        return

    if not args.dry_run:
        env_path.mkdir(parents=True)
        print(f"INFRABOX: 📁 Created environment directory at {env_path}")
        create_provider_symlink(env_path, dry_run=args.dry_run)

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

    # Used for dynamic template rendering
    render_template_to_file(
        "variables.tf.j2", env_path / "variables.tf", variables, dry_run=args.dry_run
    )
    render_template_to_file(
        "main.tf.j2", env_path / "main.tf", variables, dry_run=args.dry_run
    )
    render_template_to_file(
        "outputs.tf.j2", env_path / "outputs.tf", variables, dry_run=args.dry_run
    )

    terraform_init(env_path, dry_run=args.dry_run)
    terraform_validate(env_path, dry_run=args.dry_run)

    if not args.dry_run:
        print(
            f"INFRABOX: ✅ Initialization and validation complete for environment: {environment}"
            f"\nINFRABOX: 📂 Environment files created at {env_path}."
        )
