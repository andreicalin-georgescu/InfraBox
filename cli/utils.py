import os
import subprocess  # nosec B404
from pathlib import Path

VALID_ENVIRONMENTS = {"dev"}
INFRA_ROOT = Path(__file__).resolve().parent.parent
ENVIRONMENTS_DIR = INFRA_ROOT / "environments"


def validate_environment(env):
    if env not in VALID_ENVIRONMENTS:
        raise ValueError(f"Invalid environment: {env}")


def get_env_path(env):
    validate_environment(env)
    return os.path.join(ENVIRONMENTS_DIR, env)


def run_cmd(cmd, cwd, dry_run=False, capture_output=True):
    print(f"\nINFRABOX: 📦 Running command: {' '.join(cmd)} in {cwd}")
    if dry_run:
        print("INFRABOX: 🔍 Dry-run mode: command not executed.")
        return

    # subprocess call is safe — shell=False and cmd is a validated list

    # nosec: B603
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=capture_output,
        text=True,
        shell=False,
        check=False,  # nosec B603
    )
    if capture_output:
        print(result.stdout)
    return result


def prompt_user_confirmation():
    confirm = (
        input("INFRABOX: ⚠️  Proceed with 'terraform apply'? (y/N): ").strip().lower()
    )
    if confirm == "y":
        print("INFRABOX: ✅ Proceeding with apply.")
        return True
    else:
        print("INFRABOX: ❌ Operation cancelled.")
        return False
