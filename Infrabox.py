from cli.parser import parse_arguments
from cli.commands import create, destroy

def main():
    args = parse_arguments()

    if args.command == "create":
        create.run(args)
    elif args.command == "destroy":
        destroy.run(args)
    else:
        print("Unsupported command.")

if __name__ == "__main__":
    main()
