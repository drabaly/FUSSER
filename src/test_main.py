#!/usr/bin/env python3

import sys

import listIterator
import requester 
import special

iterator = listIterator.Iterator(sys.argv[2])
special = special.Special(sys.argv[4], 'GET', None, None, None, None, None, None, None) 
threads = []
for i in range(int(sys.argv[3])):
    threads.append(requester.Requester(sys.argv[1], 'GET', None, None, None, None, None, iterator, special))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
