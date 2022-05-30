#!/usr/bin/env python3

from src.argumentsHandling import *

# The main function: Running the parser to construct the needed objects and then run the requests in threads.
def main():
    requesters = parse_arguments()

    for requester in requesters:
        requester.start()

    for requester in requesters:
        requester.join()

if __name__ == "__main__":
    main()
