#!/usr/bin/env python3

# A simple class used to handle exceptions in threads
class ExceptionHandler:
    # Basic __init__
    def __init__(self):
        self.exception = None

    # Call this method when an exception has occured
    def set_exception(self, exception):
        self.exception = exception

    # Returns a boolean telling if an exception has already been raised
    def exception_raised(self):
        return self.exception != None
