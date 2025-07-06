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

def run_cmd(cmd, cwd, dry_run=False):
    print(f"\n📦 Running command: {' '.join(cmd)} in {cwd}")
    if dry_run:
        print("🔍 Dry-run mode: command not executed.")
        return

    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, cmd)

def prompt_user_confirmation():
    confirm = input("⚠️  Proceed with 'terraform apply'? (y/N): ").strip().lower()
    return confirm == "y"
