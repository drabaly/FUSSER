#!/usr/bin/env python3

import src/argumentsHandling

def main():
    requesters = parse_arguments()

    for requester in requesters:
        requester.start()

    for requester in requesters:
        request.join()

if __name__ == "__main__":
    main()
