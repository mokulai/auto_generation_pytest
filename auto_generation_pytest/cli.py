import argparse
import enum
import os
import sys
import pytest

from auto_generation_pytest.create import Create
from shutil import copyfile
from utlis import add_file, init_py, load_josn

#from auto_generation_pytest import __description__

__description__ = 'test'
__version__ = "0.0.1"


def make_init():
    path = os.path.dirname(os.path.realpath(__file__))+'/demo/'
    demo_folder = os.path.join(os.getcwd())
    copyfile(os.path.join(path, 'demo_grpc.json'),os.path.join(demo_folder, 'demo_grpc.json'))
    copyfile(os.path.join(path, 'demo_http.json'),os.path.join(demo_folder, 'demo_http.json'))

def make_pytest_file(args):
    if '::' not in args[0]:
        Create(args[0]).make_pytest().save_case()
    return 0

def run(args):
    Create(args[0]).make_pytest().run()
    return 0

def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        "-V", "--version", dest="version", action="store_true", help="show version"
    )
    subparsers = parser.add_subparsers(help="sub-command help")
    parser_init = subparsers.add_parser('init', help="Make init file")
    parser_run = subparsers.add_parser('run', help="Running testcase with JSON")
    parser_create = subparsers.add_parser('create', help="Make pytest file")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
        
    elif len(sys.argv) == 2 and sys.argv[1] != 'init':
        if sys.argv[1] in ["-V", "--version"]:
            print(f"{__version__}")
        elif sys.argv[1] == "run":
            parser_run.print_help()
        elif sys.argv[1] == "create":
            parser_create.print_help()
        sys.exit(0)

    extra_args = []
    if len(sys.argv) >= 2 and sys.argv[1] in ["run", "create"]:
        args, extra_args = parser.parse_known_args()
    else:
        args = parser.parse_args()

    if sys.argv[1] == "run":
        sys.exit(run(extra_args))
    elif sys.argv[1] == "init":
        sys.exit(make_init())
    elif sys.argv[1] == "create":
        sys.exit(make_pytest_file(extra_args))



if __name__ == "__main__":
   main()

