__package__ = "dobby"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import logging
from argparse import ArgumentParser, Namespace

from . import __version__, Dobby

log = logging.getLogger(__package__)


def run(args: Namespace):
    log.info(f"Dobby v{__version__}")
    dobby = Dobby.load(args.config_file)
    dobby.run()


def main():
    parser = ArgumentParser("dobby")
    subparsers = parser.add_subparsers(title="commands")

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("config_file", type=open)
    run_parser.set_defaults(func=run)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
