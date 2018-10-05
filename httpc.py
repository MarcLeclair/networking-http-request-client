#!/usr/bin/env python
import sys
import argparse
from get import getUrl
from post import postUrl


def checkContentType(js):
    for pair in js:
        key, value = pair.split(':')
        if key == "Content-Type":
            if value.find("text") or value.find("multipart") or value.find("message") or value.find("image") or value.find("audio") or value.find("video") or value.find("application"):
                return True
    return False

parser = argparse.ArgumentParser(prog='httpc', add_help=False,  description = 'cURL like functionality to do GET and POST requests in python', 
                                    usage="httpc (get|post) [-v] (-h \"k:v\")* [-d inline-data] [-f file] URL")

parser.add_argument("request" ,default = 'get',
                    nargs='?',
                    choices={'get', 'post'},
                    help="http request chosen to use")
parser.add_argument("-v", "--verbosity", action="store_true",
                    help="increase output verbosity")
parser.add_argument('-h',"--headers", nargs='*')
parser.add_argument('-d', '--data', nargs ='*', help = "the data to pass as the post request")
parser.add_argument('--help', action='help', help='show this help message and exit')
parser.add_argument('url',help='url to do request upon')

args = parser.parse_args()

rawUrl = args.url
requestType = args.request
verbose = False
parsed_headers = {}
parsed_data = {}

if args.verbosity:
            verbose = True

if args.headers:
    headerSeparator = '='
    if requestType == 'post':
        if not checkContentType(args.headers):
            print("Headers for a post request can only be of type text / multipart / message / image/ audio/video/application")
            exit()
        headerSeparator = ':'
    for pair in args.headers:
        key, value = pair.split(headerSeparator)
        parsed_headers[key] = value

if args.data:
    if args.request == 'get':
        print("Cannot use get with data. Please try this again with a post")
        quit()
    for pair in args.data:
        key, value = pair.split(':')
        parsed_data[key] = value 

if rawUrl.startswith("http://www."):
    rawUrl = rawUrl[11:]
if rawUrl.startswith("www."):
    rawUrl = rawUrl[4:]

if requestType == 'get':
    getUrl(verbose,rawUrl,parsed_headers)
elif requestType == 'post':
    postUrl(verbose, rawUrl, parsed_headers, parsed_data)


