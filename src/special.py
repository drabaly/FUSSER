#!/usr/bin/env python3

import re
import requests
import threading

from src.misc import *
from src.listIterator import *
from src.updater import *

class Special:
    def update_special(self, response):
        raise NotImplementedError("A subclass of this one should be made, defining this method.")

    def get_special(self):
        return self.special_string

class SpecialRequest(Special):
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

    def update_special(self, response):
        if not self.regex or not self.update_condition:
            return False
        self.lock.acquire()
        if self.special_string != "" and not self.update_condition.update(response):
            self.lock.release()
            return False
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
        return True

class SpecialWordlist(Special):
    def __init__(self, filename, update_condition):
        self.special_string = ""
        self.update_condition = update_condition

        self.list = Iterator(filename)

    def update_special(self, response):
        if self.update_condition and self.update_condition.update(response):
            self.special_string = self.list.get_next_element()
            return True
        else:
            return False

    def __del__(self):
        self.list.__del__()

def choose_special(args):
    if args['special_url'] and args['special_wordlist']:
        print("Please only select only one updater (-Su or -Sw)")
        exit()
    if args['special_url']:
        return SpecialRequest(args['special_url'], args['special_method'], args['special_data'], args['special_header'], proxy, ignore_ssl, args['special_pattern'], args['special_invert_pattern'], choose_updater(args))
    elif args['special_wordlist']:
        return SpecialWordlist(args['special_wordlist'], choose_updater(args))
    else:
        return None
