#!/usr/bin/env python3

import misc
import requests
import threading

class Requester(threading.Thread):
    # overriding constructor
    def __init__(self, url, method, data, headers, proxy, ssl, encode, iterator, special):
        # calling parent class constructor
        threading.Thread.__init__(self)
        # request related attribute
        self.session = requests.session()
        self.method = misc.get_request_method(self.session, method)
        self.url = url
        self.data = data
        self.headers = headers
        self.proxy = proxy
        self.ssl = ssl
        self.encode = encode

        self.iterator = iterator
        self.special = special

    def print_response(self, word, response, regex): 
        print(f"{word} => status: {response.status_code} | size: {len(response.text)}", end='')
        if regex:
            regexp = re.compile(regex)
            if regexp.search(response.text):
                print(' | Pattern: Match')
            else:
                print(' | Pattern: Do not match')
        else:
            print()

    def execute_request(self, word):
        url = self.url.replace("$FUZZ$", word)
        if self.special:
            self.special.update_special()
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
        return self.method(url=url, data=data, headers=headers, proxies=self.proxy, verify=self.ssl)

    def run(self):
        word = self.iterator.get_next_element()
        while word:
            response = self.execute_request(word)
            self.print_response(word, response, None)
            word = self.iterator.get_next_element()

