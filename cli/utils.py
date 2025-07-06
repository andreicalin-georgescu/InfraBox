import subprocess
import os
import sys
import re

def run_cmd(cmd, capture_output=False):
    try:
        result = subprocess.run(
            cmd,
            shell=isinstance(cmd, str),
            check=True,
            stdout=subprocess.PIPE if capture_output else None,
            stderr=subprocess.PIPE if capture_output else None,
            text=True
        )
        if capture_output:
            return result.stdout
    except subprocess.CalledProcessError as e:
        print("❌ Command failed.")
        if capture_output:
            print(e.stderr)
        sys.exit(e.returncode)

def get_env_path(env):
    # Prevent path traversal or injection
    if not re.match(r"^[a-zA-Z0-9_-]+$", env):
        print(f"❌ Invalid environment name: '{env}'")
        sys.exit(1)

    root = os.path.dirname(os.path.dirname(__file__))
    env_path = os.path.join(root, "environments", env)
    if not os.path.isdir(env_path):
        print(f"❌ Environment '{env}' not found.")
        sys.exit(1)
    return env_path

def confirm(prompt):
    try:
        user_input = input(f"{prompt} (y/N): ").strip().lower()
        return user_input == 'y'
    except KeyboardInterrupt:
        print("\nCancelled by user.")
        sys.exit(1)
