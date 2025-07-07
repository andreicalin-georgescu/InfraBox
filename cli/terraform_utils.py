from cli.utils import run_cmd


def terraform_init(env_path, dry_run=False):
    """
    Initialize the Terraform environment.
    """
    return run_cmd(
        ["terraform", "init", "-input=false"],
        cwd=env_path,
        dry_run=dry_run,
        capture_output=True,
    )


def terraform_validate(env_path, dry_run=False):
    """
    Validate the Terraform configuration.
    """
    return run_cmd(
        ["terraform", "validate"], cwd=env_path, dry_run=dry_run, capture_output=True
    )


def terraform_plan(env_path, destroy=False, dry_run=False):
    """
    Generate and show an execution plan.
    """
    cmd = ["terraform", "plan", "-detailed-exitcode"]
    if destroy:
        cmd.append("-destroy")
    return run_cmd(cmd, cwd=env_path, dry_run=dry_run, capture_output=False)


def terraform_state_has_changes(env_path, destroy=False, dry_run=False):
    """
    Check if there are changes in the Terraform state.
    """
    result = terraform_plan(env_path, destroy=destroy, dry_run=dry_run)

    if dry_run:
        print("\nINFRABOX: 🔍 Dry-run mode: Terraform state changes not checked.")
        cmd = ["terraform", "apply", "-auto-approve"]
        if destroy:
            cmd.append("-destroy")
        run_cmd(cmd, cwd=env_path, dry_run=True, capture_output=False)
        return False
    if result.returncode == 0:
        print("INFRABOX: ✅ No changes detected.")
        return False
    elif result.returncode == 2:
        print("INFRABOX: ⚠️ Changes detected.")
        return True
    else:
        print("INFRABOX: ❌ Error occurred while checking for changes.")
        return False


def terraform_apply(env_path, destroy=False, dry_run=False):
    """
    Apply the changes required to reach the desired state of the configuration.
    """
    cmd = ["terraform", "apply", "-auto-approve"]

    if destroy:
        cmd.append("-destroy")

    return run_cmd(cmd, cwd=env_path, dry_run=dry_run, capture_output=False)
