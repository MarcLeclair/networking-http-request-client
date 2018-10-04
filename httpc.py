#!/usr/bin/env python
import sys
import argparse

parser = argparse.ArgumentParser(prog='httpc', add_help=False,                                  description = 'cURL like functionality to do                            GET and POST requests in python', usage="httpc (get|post) [-v] (-h \"k:v\")* [-d inline-data] [-f file] URL")

parser.add_argument("request" ,default = 'get',
                    nargs='?',
                    choices={'get', 'post'},
                    help="http request chosen to use")
parser.add_argument("-v", "--verbosity", action="store_true",
                    help="increase output verbosity")
parser.add_argument('-(h \"k:v\")*',"--headers", nargs='*')
parser.add_argument('--help', action='help', help='show this help message and exit')

args = parser.parse_args()
verbose = False
requestType = 'get'
parsed_conf = {}
if args.request:
            requestType = args.request
if args.verbosity:
            verbose = True

for pair in args.headers:
    key, value = pair.split('=')
    parsed_conf[key] = value

