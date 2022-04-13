#!/usr/bin/env python3

import requests
import threading

class Requester(threading.Thread):
    # overriding constructor
    def __init__(self, url, method, data, headers, proxy, ssl, encode, iterator):
        # calling parent class constructor
        threading.Thread.__init__(self)
        # request related attribute
        self.session = requests.session()
        self.method = self.get_request_method(method)
        self.url = url
        self.data = data
        self.headers = headers
        self.proxy = proxy
        self.ssl = ssl
        self.encode = encode

        self.iterator = iterator

    def get_request_method(self, method):
        if method.upper() == 'GET':
            return self.session.get
        elif method.upper() == 'POST':
            return self.session.post
        else:
            print("Does not exist or not implemented yet")


    def execute_request(self, word, special, regex):
        url = self.url.replace("$FUZZ$", word)
        if special:
            url = url.replace("$SPECIAL$", special)
        if self.data:
            data = self.data.replace("$FUZZ$", word)
            if special:
                data = data.replace("$SPECIAL$", special)
            if self.encode:
                data = quote(data, safe='=&')
        if self.headers:
            headers = {}
            for header in self.headers:
                headers[header] = self.headers[header].replace("$FUZZ$", word)
                if (self.special):
                    headers[header] = headers[header].replace("$SPECIAL$", special)
        response = method(url=url, data=data, headers=headers, proxies=self.proxy, verify=self.ssl)
        print(f"{word} => status: {response.status_code} | size: {len(response.text)}", end='')
        if regex:
            regexp = re.compile(regex)
            if regexp.search(response.text):
                print(' | Pattern: Match')
            else:
                print(' | Pattern: Do not match')
        else:
            print()

    def run(self):
        for word in self.iterator.get_next_element():
            self.execute_request(word, None, None)

