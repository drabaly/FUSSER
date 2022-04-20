#!/usr/bin/env python3

import time

class Updater:
    def update(self):
        raise NotImplementedError("A subclass of this one should be made, defining this method.")

class TimeUpdater(Updater):
    def __init__(self, delay):
        self.delay = delay
        self.last = time.time()

    def update(self):
        current_time = time.time()
        if self.last + self.delay <= current_time:
            self.last = current_time
            return True
        return False

def choose_updater(args):
    if args['special_delay']:
        try:
            return TimeUpdater(int(args['special_delay']))
        except ValueError:
            print("The time-based update only takes nubers as argument for the \"special delay\"")
            exit()
    else:
        return None

