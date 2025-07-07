# CLI entry point for InfraBox
# This script serves as the main entry point for the InfraBox CLI, handling command-line arguments and dispatching to the appropriate command handlers

from cli.parser import parse_arguments
from cli.commands import create, destroy

def main():
    args = parse_arguments()

    if args.command == "create":
        create.run(args)
    elif args.command == "destroy":
        destroy.run(args)
    else:
        print("INFRABOX: ❌ Unsupported command.")

if __name__ == "__main__":
    main()
