#!/usr/bin/env python3

import re

import misc
import requests

class Special:
    def __init__(self, url, method, data, headers, proxy, ssl, regex, invert_regex, update_condition):
        # request related attribute
        self.session = requests.session()
        self.method = misc.get_request_method(self.session, method)
        self.url = url
        self.data = data
        self.headers = parse_headers(headers)
        self.proxy = proxy
        self.ssl = ssl

        self.regex = regex
        self.invert_regex = invert_regex
        self.update_condition = update_condition
        self.special_string = ""

    def update_special(self):
        if not self.regex or not update_condition:
            return
        if self.special_string != "" and not update_condition.update():
            return
        regexp = re.compile(self.regex)
        response = self.method(url=self.url, data=self.data, headers=self.headers, proxies=self.proxy, verify=self.ssl)
        text = response_to_string(response)
        try:
            res = regexp.search(text)[0]
        except TypeError:
            print("Special string not found in the server's response")
            exit()
        self.special_string = res.replace(self.invert_regex, '') if self.invert_regex else res

    def get_special(self):
        return self.special_string
