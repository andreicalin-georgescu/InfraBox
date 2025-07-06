import subprocess
import os
import sys
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

    result = subprocess.run(cmd, cwd=cwd, capture_output=capture_output, text=True, shell=False)
    if capture_output:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, cmd)

def has_changes(env_path, destroy=False, dry_run=False):
    if destroy:
        cmd = ["terraform", "plan", "-destroy", "-detailed-exitcode"]
    else:
        cmd = ["terraform", "plan", "-detailed-exitcode"]
    print(f"\nINFRABOX: 📦 Running command: {' '.join(cmd)} in {env_path}")

    if dry_run:
        print("INFRABOX: 🔍 Dry-run mode: changes not checked.")
        return False
    
    result = subprocess.run(cmd, cwd=env_path, capture_output=False, text=True, shell=False)
    if result.returncode == 0:
        print("INFRABOX: ✅ No changes detected.")
        return False
    elif result.returncode == 2:
        print("INFRABOX: ⚠️ Changes detected.")
        return True
    else:
        print("INFRABOX: ❌ Error occurred while checking for changes.")
        return False

def prompt_user_confirmation():
    confirm = input("INFRABOX: ⚠️  Proceed with 'terraform apply'? (y/N): ").strip().lower()
    if confirm == "y":
        print("INFRABOX: ✅ Proceeding with apply.")
        return True
    else:
        print("INFRABOX: ❌ Operation cancelled.")
        return False
