import ipaddress
import os
import re
import subprocess  # nosec B404
import sys
from pathlib import Path

VALID_ENVIRONMENTS = {"dev", "stage"}
INFRA_ROOT = Path(__file__).resolve().parent.parent
ENVIRONMENTS_DIR = INFRA_ROOT / "environments"
DEFAULT_VNET = "10.0.0.0/16"
DEFAULT_SUBNET = "10.0.1.0/24"


def sanitize_input(value: str) -> str:
    """Sanitize CLI input to avoid injection or path traversal."""
    return re.sub(r"[^\w\-]", "", value.strip())


def sanitize_env_name(name):
    """Return a safe environment name (alphanumeric, dashes, underscores)."""
    return "".join(c for c in name if c.isalnum() or c in ("-", "_")).lower()


def validate_environment(env, allow_new=False):
    if not allow_new and env not in VALID_ENVIRONMENTS:
        raise ValueError(f"Invalid environment: {env}")


def get_env_path(env):
    """Get the path to the specified environment directory. Abort if it doesn't exist."""
    validate_environment(env)
    env_path = os.path.join(ENVIRONMENTS_DIR, env)

    if not os.path.exists(env_path):
        print(f"INFRABOX: ❌ Environment directory '{env}' does not exist.")
        print(
            f"INFRABOX: 💡 You may need to run: `infrabox.py initialize {env}` first."
        )
        sys.exit(1)

    return env_path


def validate_cidr(cidr: str) -> str:
    """Ensure the given CIDR is valid."""
    try:
        return str(ipaddress.IPv4Network(cidr, strict=True))
    except Exception as e:
        raise ValueError(f"Invalid CIDR '{cidr}': {e}") from e


def check_cidr_overlap(new_cidr: str, current_env: str, environments_dir: Path) -> None:
    """Check that the new CIDR doesn't overlap with existing ones in other environments."""
    new_network = ipaddress.IPv4Network(new_cidr, strict=True)

    for env_dir in environments_dir.iterdir():
        if not env_dir.is_dir() or env_dir.name == current_env:
            continue

        variables_file = env_dir / "variables.tf"
        if not variables_file.exists():
            continue

        content = variables_file.read_text()
        matches = re.findall(r'["\'](\d+\.\d+\.\d+\.\d+/\d+)["\']', content)

        for match in matches:
            try:
                existing_net = ipaddress.IPv4Network(match, strict=True)
                if new_network.overlaps(existing_net):
                    raise ValueError(
                        f"CIDR {new_network} overlaps with {existing_net} in environment '{env_dir.name}'"
                    )
            except Exception:
                raise ValueError(
                    f"Invalid CIDR '{match}' in environment '{env_dir.name}'"
                ) from None


def run_cmd(cmd, cwd, dry_run=False, capture_output=True):
    """Run a command in a specified directory."""
    print(f"\nINFRABOX: 📦 Running command: {' '.join(cmd)} in {cwd}")
    if dry_run:
        print("INFRABOX: 🔍 Dry-run mode: command not executed.")
        return

    # subprocess call is safe — shell=False and cmd is a validated list

    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=capture_output,
        text=True,
        shell=False,
        check=False,
    )  # nosec: B603
    if capture_output:
        print(result.stdout)
    return result


def prompt_input(prompt, default=""):
    """Ask user for input with a default fallback."""
    response = input(f"{prompt} [{default}]: ").strip()
    return response or default


def prompt_with_default(prompt_text: str, default: str) -> str:
    """Prompt user for input, return sanitized string or default."""
    user_input = input(f"{prompt_text} [default: {default}]: ").strip()
    return sanitize_input(user_input) if user_input else default


def prompt_user_confirmation(message="INFRABOX: Proceed?", default=False):
    """Prompt the user for confirmation with a default option."""
    suffix = "[Y/n]" if default else "[y/N]"
    answer = input(f"{message} {suffix}: ").strip().lower()
    if not answer:
        return default
    return answer in ("y", "yes")


def create_provider_symlink(env_path: Path, dry_run=False):
    """Create a symlink from Shared/provider.tf to the environment directory."""
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
