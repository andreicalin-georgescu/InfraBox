import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="InfraBox CLI")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create
    create_parser = subparsers.add_parser("create", help="Create environment")
    create_parser.add_argument("environment", choices=["dev"], help="Target environment")
    create_parser.add_argument("--dry-run", action="store_true", help="Dry run only")

    # Destroy
    destroy_parser = subparsers.add_parser("destroy", help="Destroy environment")
    destroy_parser.add_argument("environment", choices=["dev"], help="Target environment")
    destroy_parser.add_argument("--dry-run", action="store_true", help="Dry run only")

    return parser.parse_args()
