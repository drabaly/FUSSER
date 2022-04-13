#!/usr/bin/env python3

class Iterator:
    def __init__(self, filename):
        self.wordlist = open(filename, 'r')

    def get_next_element(self):
        result = self.wordlist.readline()
        result = result[:-1] if result and result[-1] == '\n' else result
        return result

    def __del__(self):
        self.wordlist.close()
