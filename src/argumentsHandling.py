#!/usr/bin/env python3

import argparse
from urllib3.exceptions import InsecureRequestWarning

from src.listIterator import *
from src.requester import *
from src.special import *
from src.updater import *

def generate_parser():
    parser = argparse.ArgumentParser()

    # Global
    parser.add_argument('-t', '--threads', help='The number of threads to use', required=False, default='20')
    parser.add_argument('-p', '--proxy', help='The proxy to use', required=False, default='None')
    parser.add_argument('-w', '--wordlist', help='The wordlist to use', required=True)
    parser.add_argument('-is', '--ignore-ssl', help='Ignore the certificate checks', required=False, default='False')

    # Standard fuzzing
    parser.add_argument('-u', '--url', help='The URL of the target', required=True)
    parser.add_argument('-m', '--method', help='The HTTP method to use', required=False, default='GET')
    parser.add_argument('-d', '--data', help='The data in the body of the requests', required=False, default=None)
    parser.add_argument('-H', '--header', help='A header to add to the requests', required=False, action='append')
    parser.add_argument('-P', '--pattern', help='A regex to check against the body of the responses of the server', required=False, default=None)
    parser.add_argument('-ed', '--encode_data', help='URL encode POST data', required=False, default='False')

    # Special task
    parser.add_argument('-Su', '--special-url', help='The URL of the special task', required=False, default=None)
    parser.add_argument('-SD', '--special-delay', help='The delay to wich the special task is to be performed (in seconds)', required=False, default=None)
    parser.add_argument('-Sm', '--special-method', help='The HTTP method to use for the special task', required=False, default="GET")
    parser.add_argument('-Sd', '--special-data', help='The data in the body of the requests for the special task', required=False, default=None)
    parser.add_argument('-SH', '--special-header', help='A header to add to the requests for the special task', required=False, action='append', default=None)
    parser.add_argument('-SP', '--special-pattern', help='The regex for the element to get in the response', required=False, default=None)
    parser.add_argument('-SvP', '--special-invert-pattern', help='Element to be deleted from the matched special pattern (useful when searching for element after a specific keyword but the keyword is not part of the special string)', required=False, default=None)

    return parser

def parse_arguments():
    parser = generate_parser()

    # Arguments treatment
    args = vars(parser.parse_args())
    proxy = None
    if args['proxy'] != 'None':
        proxy = {
                    "http": f'http://{args["proxy"]}',
                    "https": f'http://{args["proxy"]}'
                }
    ignore_ssl = not args['ignore_ssl'].lower() == 'true' # The variable name is bad, it should be something like 'perform_ssl_checks'
    encode = not args['encode_data'].lower() == 'true' # The variable name is bad, it should be something like 'perform_encoding'
    if not ignore_ssl:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    iterator = listIterator(args['wordlist'])
    special = special.Special(args['special_url'], args['special_method'], args['special_data'], args['special_header'], proxy, ignore_ssl, args['special_pattern'], args['special_invert_pattern'], choose_updater(args))
    requesters = []
    for i in range(int(args['threads'])):
        requesters.append(requester.Requester(args['url'], args['method'], args['data'], args['header'], proxy, ignore_ssl, encode, iterator, special))

    return requesters
