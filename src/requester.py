#!/usr/bin/env python3

import re
import requests
import threading
from urllib.parse import quote

from src.misc import *

class Requester(threading.Thread):
    # overriding constructor
    def __init__(self, url, method, data, headers, pattern, proxy, ssl, encode, iterator, special, exception_handler):
        # calling parent class constructor
        threading.Thread.__init__(self)

        # request related attribute
        self.session = requests.session()
        self.method = get_request_method(self.session, method)
        self.url = url
        self.data = data
        self.headers = parse_headers(headers)
        self.pattern = pattern
        self.proxy = proxy
        self.ssl = ssl
        self.encode = encode

        self.iterator = iterator
        self.special = special
        self.exception_handler = exception_handler

    def print_response(self, word, response):
        print(f"{word} => status: {response.status_code} | size: {len(response.text)}", end='')
        if self.pattern:
            regexp = re.compile(self.pattern)
            if regexp.search(response.text):
                print(' | Pattern: Match')
            else:
                print(' | Pattern: Do not match')
        else:
            print()

    def execute_request(self, word):
        url = self.url.replace("$FUZZ$", word)
        if self.special:
            url = url.replace("$SPECIAL$", self.special.get_special())
        data = self.data
        if data:
            data = data.replace("$FUZZ$", word)
            if self.special:
                data = data.replace("$SPECIAL$", self.special.get_special())
            if self.encode:
                data = quote(data, safe='=&')
        headers = self.headers
        if headers:
            headers = {}
            for header in headers:
                headers[header] = headers[header].replace("$FUZZ$", word)
                if (self.special):
                    headers[header] = headers[header].replace("$SPECIAL$", special)
        response = self.method(url=url, data=data, headers=headers, proxies=self.proxy, verify=self.ssl)
        response_text = response_to_string(response)
        if self.special.update_special(response_text):
            return self.execute_request(word)
        return response

    def run(self):
        word = self.iterator.get_next_element()
        while word:
            if self.exception_handler.exception_raised():
                return
            try:
                response = self.execute_request(word)
            except Exception as e:
                self.exception_handler.set_exception(e)
                print(f"Exception occured: {e}")
                return
            self.print_response(word, response)
            word = self.iterator.get_next_element()
