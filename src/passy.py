import argparse
import scenarios

parser = argparse.ArgumentParser()
parser.add_argument("-g", "--get_password", action="store_true", help="Get password")
parser.add_argument("-a", "--add_password", action="store_true", help="Add password")

args = parser.parse_args()

if args.get_password:
    scenarios.get_password()

if args.add_password:
    scenarios.add_password()
