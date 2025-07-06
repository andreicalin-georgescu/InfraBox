from cli.utils import run_cmd, get_env_path, prompt_user_confirmation

def run(args):
    env_path = get_env_path(args.environment)

    run_cmd(["terraform", "init", "-input=false"], cwd=env_path, dry_run=args.dry_run)
    run_cmd(["terraform", "plan", "-destroy"], cwd=env_path, dry_run=args.dry_run)

    if not args.dry_run and prompt_user_confirmation():
        run_cmd(["terraform", "destroy", "-auto-approve"], cwd=env_path)
