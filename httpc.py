#!/usr/bin/env python
import sys
import argparse

parser = argparse.ArgumentParser(prog='httpc', add_help=False)

parser.add_argument("(get|post)",
                    help="display a square of a given number")
parser.add_argument("-v", "--verbosity", action="store_true",
                    help="increase output verbosity")
parser.add_argument("-((h 'k:v'))*", "--headers", action="store_true",
                    help="headers")
parser.add_argument('--help', action='help', help='show this help message and exit')

args = parser.parse_args()
answer = args.square**2

