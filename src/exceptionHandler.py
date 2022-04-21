#!/usr/bin/env python3

class ExceptionHandler:
    def __init__(self):
        self.exception = None

    def set_exception(self, exception):
        self.exception = exception

    def exception_raised(self):
        return self.exception != None
