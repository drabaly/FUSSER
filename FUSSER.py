#!/usr/bin/env python3

import argparse
import re
import requests
import time

from urllib3.exceptions import InsecureRequestWarning

# TODO: implement multi threading
# import concurrent.future

def get_request_method(method):
    if method == 'GET':
        return requests.get
    elif method == 'POST':
        return requests.post
    else:
        print("Does not exist or not implemented yet")

def response_to_string(response):
    res = ''
    for elt in response.headers:
        res += f"{elt}:{response.headers[elt]}\n"
    res += response.text
    return res

def parse_headers(headers):
    res = {}
    for header in headers:
        key, value = header.split(':')
        key = key.strip()
        value = value.strip()
        res[key] = value
    return res

def execute_request(word, special, url, method, data, headers, proxy, ssl, regex):
    url = url.replace("$FUZZ$", word)
    if (special):
        url = url.replace("$SPECIAL$", special)
    if data:
        data = data.replace("$FUZZ$", word)
        if (special):
            data = data.replace("$SPECIAL$", special)
    if headers:
        for header in headers:
            headers[header] = headers[header].replace("$FUZZ$", word)
            if (special):
                headers[header] = headers[header].replace("$SPECIAL$", special)
    response = method(url=url, data=data, headers=headers, proxies=proxy, verify=ssl)
    print(f"{word} => status: {response.status_code} | size: {len(response.text)}", end='')
    if regex:
        regexp = re.compile(regex)
        if regexp.search(response.text):
            print(' Pattern: Match')
        else:
            print(' Pattern: Do not match')
    else:
        print()

def execute_special_request(url, method, data, headers, proxy, ssl, regex):
    regexp = re.compile(regex)
    response = method(url=URL, data=data, headers=headers, proxies=proxy, verify=ssl)
    text = response_to_string(response)
    try:
        res = regexp.search(test)[0]
    except IndexError:
        print("Special string not found")
        exit()
    return res

parser = argparse.ArgumentParser()

# Global
#parser.add_argument('-t', '--threads', help='The number of threads to use', required=False, default='20')
parser.add_argument('-p', '--proxy', help='The proxy to use', required=False, default='None')
parser.add_argument('-w', '--wordlist', help='The wordlist to use', required=True)
parser.add_argument('-is', '--ignore-ssl', help='Ignore the certificate checks', required=False, default='True')

# Standard fuzzing
parser.add_argument('-u', '--url', help='The URL of the target', required=True)
parser.add_argument('-m', '--method', help='The HTTP method to use', required=False, default='GET')
parser.add_argument('-d', '--data', help='The data in the body of the requests', required=False)
parser.add_argument('-H', '--header', help='A header to add to the requests', required=False, action='append')
parser.add_argument('-P', '--pattern', help='A regex to check against the body of the responses of the server', required=False, default=None)

# Regular task
parser.add_argument('-SD', '--special-delay', help='The delay to wich the special task is to be performed', required=False, default=-1)
parser.add_argument('-Su', '--special-url', help='The URL of the special task', required=False, default=None)
parser.add_argument('-Sm', '--special-method', help='The HTTP method to use for the special task', required=False, default="GET")
parser.add_argument('-Sd', '--special-data', help='The data in the body of the requests for the special task', required=False, default=None)
parser.add_argument('-SH', '--special-header', help='A header to add to the requests for the special task', required=False, action='append', default=None)
parser.add_argument('-SP', '--special-pattern', help='The regex for the element to get in the response', required=False, default=None)

# Arguments treatment
args = vars(parser.parse_args())
#threads = int(args['threads'])
proxy = None
if args['proxy'] != 'None':
    proxy = {
                "http": f'http://{args["proxy"]}',
                "https": f'http://{args["proxy"]}'
            }
method = get_request_method(args['method'])
special_method = get_request_method(args['special_method'])
special_delay = int(args['special_delay'])
ignore_ssl = not args['ignore_ssl'].lower() == 'true' # The variable name is bad, it should be something like 'perform_ssl_checks'
if not ignore_ssl:
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
headers = parse_headers(args['header'])

# Fuzzing
with open(args['wordlist'], 'r') as wordlist:
#   with concurrent.future.ThreadPoolExecutor(max_workers = threads) as executor:
    if args['special_url']:
        special = execute_special_request(args['special_url'], special_method, args['special_data'], args['special_header'], proxy, ignore_ssl, args['special_pattern'])
        last_special = time.time()
    else:
        special = None
    word = wordlist.readline()
    while word:
        if word[-1] == '\n':
            word = word[:-1]
        if special and time.time() - last_special < special_delay:
            special = execute_special_equest(args['special_url'], special_method, args['special_data'], args['special_header'], proxy, ignore_ssl, args['special_pattern'])
            last_special = time.time()
        execute_request(word, special, args['url'], method, args['data'], headers, proxy, ignore_ssl, args['pattern'])
        word = wordlist.readline()
