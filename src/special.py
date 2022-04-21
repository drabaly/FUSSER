#!/usr/bin/env python3

import re
import requests
import threading

from src.misc import *

class Special:
    def __init__(self, url, method, data, headers, proxy, ssl, regex, invert_regex, update_condition):
        # request related attribute
        self.session = requests.session()
        self.method = get_request_method(self.session, method)
        self.url = url
        self.data = data
        self.headers = parse_headers(headers)
        self.proxy = proxy
        self.ssl = ssl

        self.regex = regex
        self.invert_regex = invert_regex
        self.update_condition = update_condition
        self.special_string = ""

        self.lock = threading.Lock()

    def update_special(self):
        if not self.regex or not self.update_condition:
            return
        self.lock.acquire()
        if self.special_string != "" and not self.update_condition.update():
            self.lock.release()
            return
        regexp = re.compile(self.regex)
        try:
            response = self.method(url=self.url, data=self.data, headers=self.headers, proxies=self.proxy, verify=self.ssl)
        except Exception as e:
            self.lock.release()
            raise e
        text = response_to_string(response)
        try:
            res = regexp.search(text)[0]
        except TypeError:
            self.lock.release()
            raise TypeError("Special string not found in the server's response")
        self.special_string = res.replace(self.invert_regex, '') if self.invert_regex else res
        self.lock.release()

    def get_special(self):
        return self.special_string
