#!/usr/bin/env python

__package__ = "dobby"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import logging
from argparse import ArgumentParser, Namespace

from . import __version__, Dobby
from .errors import DobbyError

log = logging.getLogger(__package__)


def run(args: Namespace):
    log.info(f"Dobby v{__version__}")
    try:
        dobby = Dobby.load(args.config_file)
    except DobbyError as e:
        text = "Couldn't start Dobby"
        if e.hint:
            text += ": " + e.hint
        log.exception(text)
    else:
        dobby.run()


def test(args: Namespace):
    log.info(f"Dobby v{__version__} TEST")
    dobby = Dobby.load(args.config_file)
    dobby.test()


def main(*args):
    args = args or None

    parser = ArgumentParser("dobby")
    subparsers = parser.add_subparsers(title="commands")

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("config_file", type=Path)
    run_parser.set_defaults(func=run)

    run_parser = subparsers.add_parser("test")
    run_parser.add_argument("config_file", type=Path)
    run_parser.set_defaults(func=test)

    args = parser.parse_args(args)
    args.func(args)


if __name__ == "__main__":
    main()
