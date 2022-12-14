import argparse
import scenarios


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-g", "--get_password", action="store_true", help="Get password"
    )
    parser.add_argument(
        "-a", "--add_password", action="store_true", help="Add password"
    )
    parser.add_argument(
        "-d", "--delete_password", action="store_true", help="Delete password"
    )

    args = parser.parse_args()

    if args.get_password:
        scenarios.get_password()

    if args.add_password:
        scenarios.add_password()

    if args.delete_password:
        scenarios.delete_password()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("^C")
