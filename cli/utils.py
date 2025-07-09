import os
import sys
import subprocess  # nosec B404
from pathlib import Path

VALID_ENVIRONMENTS = {"dev", "stage"}
INFRA_ROOT = Path(__file__).resolve().parent.parent
ENVIRONMENTS_DIR = INFRA_ROOT / "environments"


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


def prompt_user_confirmation(message="INFRABOX: Proceed?", default=False):
    """Prompt the user for confirmation with a default option."""
    suffix = "[Y/n]" if default else "[y/N]"
    answer = input(f"{message} {suffix}: ").strip().lower()
    if not answer:
        return default
    return answer in ("y", "yes")


def prompt_input(prompt, default=""):
    """Ask user for input with a default fallback."""
    response = input(f"{prompt} [{default}]: ").strip()
    return response or default


def sanitize_env_name(name):
    """Return a safe environment name (alphanumeric, dashes, underscores)."""
    return "".join(c for c in name if c.isalnum() or c in ("-", "_")).lower()
