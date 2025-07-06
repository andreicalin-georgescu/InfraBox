from cli.utils import run_cmd, get_env_path, prompt_user_confirmation, has_changes

def run(args):
    env_path = get_env_path(args.environment)

    run_cmd(["terraform", "init", "-input=false"], cwd=env_path, dry_run=args.dry_run)
    run_cmd(["terraform", "validate"], cwd=env_path, dry_run=args.dry_run)

    if has_changes(env_path, destroy=True, dry_run=args.dry_run) and prompt_user_confirmation():
        run_cmd(["terraform", "destroy", "-auto-approve"], cwd=env_path, capture_output=False)
