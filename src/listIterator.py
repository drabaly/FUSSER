#!/usr/bin/env python3

import threading

class Iterator:
    def __init__(self, filename):
        self.wordlist = open(filename, 'r')

        self.lock = threading.Lock()

    def get_next_element(self):
        self.lock.acquire()
        result = self.wordlist.readline()
        self.lock.release()
        result = result[:-1] if result and result[-1] == '\n' else result
        return result

    def __del__(self):
        self.wordlist.close()
