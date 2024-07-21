import argparse
import scenarios


def main():
    parser = argparse.ArgumentParser(
        prog="passy", description="Sussy CLI password manager"
    )
    parser.add_argument("-g", "--get_pass", action="store_true", help="get password")
    parser.add_argument("-a", "--add_pass", action="store_true", help="add password")
    parser.add_argument("-d", "--del_pass", action="store_true", help="remove password")

    args = parser.parse_args()

    if args.get_pass:
        scenarios.get_password()
    elif args.add_pass:
        scenarios.add_password()
    elif args.del_pass:
        scenarios.delete_password()
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
