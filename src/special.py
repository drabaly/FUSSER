#!/usr/bin/env python3

import re
import requests
import threading

from src.misc import *
from src.listIterator import *
from src.updater import *

# Template class used to force the implementation of the *update_special* method in it's derivates and implement a simple *get_special*
class Special:
    # The method used to tell if the special needed to be updated and was updated
    def update_special(self, response):
        raise NotImplementedError("A subclass of this one should be made, defining this method.")

    # The method used to get the last updated special
    def get_special(self):
        return self.special_string

# A class used to get a special based on another request
class SpecialRequest(Special):
    # The __init__ of the class to set the needed data to perform the request
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

    # Perform the request to retrieve a new special if needed
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

# A class used to get a special based on a wordlist
class SpecialWordlist(Special):
    # A simple __init__ reusing the *Iterator* class that do what we need
    def __init__(self, filename, update_condition):
        self.special_string = ""
        self.update_condition = update_condition

        self.list = Iterator(filename)

    # Get the next element in the wordlist if needed
    def update_special(self, response):
        if self.update_condition and self.update_condition.update(response):
            self.special_string = self.list.get_next_element()
            return True
        else:
            return False

    def __del__(self):
        self.list.__del__()

class SpecialCode(Special):
    def __init__(self, code, update_condition):
        self.special_string = ""
        self.update_condition = update_condition

        self.code = code

    def update_special(self, response):
        if self.update_condition and self.update_condition.update(response):
            special = ""
            eval(self.code)
            special.special_string = special
            return True
        else:
            return False

# This function returns the correct special class depending on the arguments sent to the tool
def choose_special(args):
    if
        return None
    if not single_true([args['special_url'], args['special_wordlist'], args['special_code']):
        print("Please only select only one updater (-Su, -Sw or Sc)")
        exit()
    if args['special_url']:
        return SpecialRequest(args['special_url'], args['special_method'], args['special_data'], args['special_header'], proxy, ignore_ssl, args['special_pattern'], args['special_invert_pattern'], choose_updater(args))
    elif args['special_wordlist']:
        return SpecialWordlist(args['special_wordlist'], choose_updater(args))
    elif args['special_code']:
        return SpecialCode(args['special_code'], choose_updater(args))
    else:
        print("Oh no, I should have gone here")
        exit()
