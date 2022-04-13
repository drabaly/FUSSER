#!/usr/bin/env python3

def get_request_method(session, method):
    if method.upper() == 'GET':
        return session.get
    elif method.upper() == 'POST':
        return session.post
    else:
        print("Does not exist or not implemented yet")

