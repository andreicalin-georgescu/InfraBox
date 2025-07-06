import os
from cli.utils import run_cmd, get_env_path, confirm

def create_environment(args):
    env_path = get_env_path(args.env)
    os.chdir(env_path)

    print(f"📁 Using environment: {args.env}")
    run_cmd("terraform init")

    targets = []
    if args.with_VM:
        targets.append("-target=module.vm")
    if args.with_Subnet:
        targets.append("-target=module.networking")

    plan_cmd = ["terraform", "plan"]
    if targets:
        plan_cmd += targets

    print("📜 Running Terraform plan...")
    run_cmd(plan_cmd)

    if args.dry_run:
        print("🛑 Dry-run: skipping terraform apply")
        return

    if confirm("⚠️ Apply changes?"):
        apply_cmd = ["terraform", "apply", "-auto-approve"]
        if targets:
            apply_cmd += targets
        run_cmd(apply_cmd)
    else:
        print("✅ Apply skipped.")


def destroy_environment(args):
    env_path = get_env_path(args.env)
    os.chdir(env_path)

    print(f"🗑️ Destroying environment: {args.env}")
    run_cmd("terraform init")

    if args.dry_run:
        print("📜 Running Terraform destroy plan...")
        run_cmd("terraform plan -destroy")
        print("🛑 Dry-run: skipping terraform destroy")
        return

    if confirm("⚠️ Confirm destruction of resources?"):
        run_cmd("terraform destroy -auto-approve")
    else:
        print("✅ Destroy skipped.")

