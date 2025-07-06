from cli.parser import build_parser
from cli.core import create_environment, destroy_environment

def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == 'create':
        create_environment(args)
    elif args.command == 'destroy':
        destroy_environment(args)
    else:
        print("Unsupported command")

if __name__ == "__main__":
    main()