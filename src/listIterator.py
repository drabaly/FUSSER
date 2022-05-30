#!/usr/bin/env python3

import threading

# The object giving one element of the wordlist to each thread each time it's needed
class Iterator:
    # A simple __init__ opening the wordlist file
    def __init__(self, filename):
        try:
            self.wordlist = open(filename, 'r')
        except FileNotFoundError:
            print(f"The file {filename} was not found")
            exit()

        self.lock = threading.Lock()

    # The method called by the threads to get a new element
    def get_next_element(self):
        self.lock.acquire()
        result = self.wordlist.readline()
        self.lock.release()
        result = result[:-1] if result and result[-1] == '\n' else result
        return result

    # Used to close the file at the end of running the script
    def __del__(self):
        self.wordlist.close()
