#!/usr/bin/env python3

# This file containes the functions that don't really have their place in other files

# Convert a string to a python3 requests method
# Methods are missing and will be implemented later
def get_request_method(session, method):
    if method.upper() == 'GET':
        return session.get
    elif method.upper() == 'POST':
        return session.post
    else:
        print("Does not exist or not implemented yet")

# Convert a list of headers to a dictionnary one
def parse_headers(headers):
    if not headers:
        return None
    res = {}
    for header in headers:
        key, value = header.split(':')
        key = key.strip()
        value = value.strip()
        res[key] = value
    return res

# Convert a python3 requests' response to a string to work with only one variable
def response_to_string(response):
    res = ''
    for elt in response.headers:
        res += f"{elt}:{response.headers[elt]}\n"
    res += response.text
    return res
