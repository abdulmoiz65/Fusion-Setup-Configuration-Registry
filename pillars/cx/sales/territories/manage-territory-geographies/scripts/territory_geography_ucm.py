#!/usr/bin/env python3
"""Retired task-local Fusion execution route; use core Data Loader."""
import argparse
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_known_args(argv)
    print("This task-local route is retired. Use core/data-loader/SKILL.md for native CX preflight, Task Hook approval, upload and initiation, or explicitly requested status. Existing uncertain staged files require supported reconciliation; do not reupload them.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
