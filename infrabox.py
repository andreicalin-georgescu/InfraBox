# CLI entry point for InfraBox

from cli.commands import create, destroy
from cli.parser import parse_arguments


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
