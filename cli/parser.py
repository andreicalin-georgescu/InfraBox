import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="InfraBox CLI",
        description="A command-line interface for managing InfraBox environments. Supports creating and destroying environments with Terraform.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create
    create_parser = subparsers.add_parser("create", help="Create an environment")
    create_parser.add_argument(
        "environment", choices=["dev"], help="Target environment"
    )
    create_parser.add_argument("--dry-run", action="store_true", help="Dry run only")

    # Destroy
    destroy_parser = subparsers.add_parser("destroy", help="Destroy an environment")
    destroy_parser.add_argument(
        "environment", choices=["dev"], help="Target environment"
    )
    destroy_parser.add_argument("--dry-run", action="store_true", help="Dry run only")

    return parser.parse_args()
