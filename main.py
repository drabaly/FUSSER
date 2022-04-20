#!/usr/bin/env python3

from src.argumentsHandling import *

def main():
    requesters = parse_arguments()

    for requester in requesters:
        requester.start()

    for requester in requesters:
        request.join()

if __name__ == "__main__":
    main()
