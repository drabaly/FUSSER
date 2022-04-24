#!/usr/bin/env python3

import re
import time

class Updater:
    def update(self, response):
        raise NotImplementedError("A subclass of this one should be made, defining this method.")

class TimeUpdater(Updater):
    def __init__(self, delay):
        self.delay = delay
        self.last = time.time()

    def update(self, response):
        current_time = time.time()
        if self.last + self.delay <= current_time:
            self.last = current_time
            return True
        return False

class FlagUpdater(Updater):
    def __init__(self, pattern):
        self.regex = re.compile(pattern)

    def update(self, response):
        return self.regex.search(response) != None

def choose_updater(args):
    if args['special_delay'] and args['special_flag']:
        print("Please only select only one updater (-SD or -SF)")
        exit()
    if args['special_delay']:
        try:
            return TimeUpdater(int(args['special_delay']))
        except ValueError:
            print("The time-based update only takes nubers as argument for the \"special delay\"")
            exit()
    elif args['special_flag']:
        return FlagUpdater(args['special_flag'])
    else:
        return None

