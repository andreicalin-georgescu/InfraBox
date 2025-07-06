import argparse
from cli.core import create_environment, destroy_environment

def build_parser():
    parser = argparse.ArgumentParser(description="InfraBox CLI: Provision reusable infrastructure safely.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Common argument sets
    def add_common_args(subparser):
        subparser.add_argument("env", help="Environment name (e.g., dev)")
        subparser.add_argument("--dry-run", action="store_true", help="Only run terraform plan, do not apply/destroy")

    # Create command
    parser_create = subparsers.add_parser("create", help="Create an environment")
    add_common_args(parser_create)
    parser_create.add_argument("--with-VM", action="store_true", help="Include VM module")
    parser_create.add_argument("--with-Subnet", action="store_true", help="Include Networking module")
    parser_create.set_defaults(func=create_environment)

    # Destroy command
    parser_destroy = subparsers.add_parser("destroy", help="Destroy an environment")
    add_common_args(parser_destroy)
    parser_destroy.set_defaults(func=destroy_environment)

    return parser
