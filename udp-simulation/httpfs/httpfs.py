import sys
import argparse
import os
import serverConnection

sys.dont_write_bytecode = True

#no server logs
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

#allow server logs
def enablePrint():
    sys.stdout = sys.__stdout__

parser = argparse.ArgumentParser(prog='httpfs', add_help=False,  description = 'cURL like functionality to do GET and POST requests in python', 
                                    usage="httpc (get|post) [-v] (-h \"k:v\")* [-d inline-data] [-f file] URL")


parser.add_argument("-v", "--debug", action="store_true",
                    help="Prints debugging messages")
parser.add_argument('-p',"--Port", default=8007, type=int , help="Port on which the server will run. Please make sure the designated port is NOT in use.")
parser.add_argument('-d', '--Directory', default=os.path.dirname(__file__), type=str, help = "the data to pass as the post request")
parser.add_argument('--help', action='help', help='show this help message and exit')


args = parser.parse_args()

blockPrint()
if args.debug:
    enablePrint()

serverConnection.startServer('', args.Port, args.Directory)