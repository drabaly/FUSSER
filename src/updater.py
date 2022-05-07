#!/usr/bin/env python3

import re
import time

# Template class used to force the implementation of the *update* method in it's derivates
class Updater:
    # The method that every Updater needs to implement
    def update(self, response):
        raise NotImplementedError("A subclass of this one should be made, defining this method.")

# A time based upadted
class TimeUpdater(Updater):
    # A simple __init__ used to set the needed delay
    def __init__(self, delay):
        self.delay = delay
        self.last = 0

    # Checks if an update with the special request is needed
    def update(self, response):
        current_time = time.time()
        if self.last == 0:
            self.last = current_time
            return True
        if self.last + self.delay <= current_time:
            self.last = current_time
            return True
        return False

# A patter based updater: if the pattern is found in the response => the session is dead and you need performing the special request is needed
class FlagUpdater(Updater):
    # A simple __init__ used to set the pattern
    def __init__(self, pattern):
        self.regex = re.compile(pattern)

    # Checks if an update with the special request is needed
    def update(self, response):
        return self.regex.search(response) != None

# This function returns the correct updater depending on the arguments sent to the tool
def choose_updater(args):
    if args['special_delay'] and args['special_flag']:
        print("Please only select only one updater (-SD or -SF)")
        exit()
    if args['special_delay']:
        try:
            return TimeUpdater(float(args['special_delay']))
        except ValueError:
            print("The time-based update only takes nubers as argument for the \"special delay\"")
            exit()
    elif args['special_flag']:
        return FlagUpdater(args['special_flag'])
    else:
        print("If a special is defined, a method to update it must be selected")
        exit()

