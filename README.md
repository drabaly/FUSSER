# FUSSER
Fuzzer Short SEssion Reauth is a fuzzer aimed at authenticated fuzzing.

This tool has a simple purpose: easily perform fuzzing as an authenticated user by handling way to keep the session alive.

FUSSER can be splitted in 2 main parts:
* Standard: it can be used as a simple fuzzer like we all know, the keeword to FUZZ is '\\$FUZZ\\$' (Please ignore the '\\', GitHub is messing with me...)
* Special: That's were the fun begin... This is were you handle when and how you reauthenticate your session. It can be splitted in 2 parts (once again...):
  * The updater: how to detect if your session is dead
  * The special: how to updated your session

In theory, the tool should be easy to modify/add features if you want. But it's juste a theory (That I hope is real).

Guarantee: The ONLY guarantee so far is that I have missed a few bugs, if you can create an issue if you find one, that would be nice ;)


```
$ ./FUSSER.py --help

usage: Use the $FUZZ$ and $SPECIAL$ keywords in the normal requests to replace them by respectively the current word of the wordlist and the special string.
Options:

       [-h] [-t THREADS] [-p PROXY] -w WORDLIST [-is IGNORE_SSL] [-Ps PRINT_SIMPLE] [-Pc PRINT_COLORED] [-PC PRINT_CODE] -u URL [-m METHOD] [-d DATA] [-H HEADER] [-P PATTERN] [-ed ENCODE_DATA] [-to TIMEOUT]
       [-Su SPECIAL_URL] [-Sw SPECIAL_WORDLIST] [-Sc SPECIAL_CODE] [-SD SPECIAL_DELAY] [-SF SPECIAL_FLAG] [-Sm SPECIAL_METHOD] [-Sd SPECIAL_DATA] [-SH SPECIAL_HEADER] [-SP SPECIAL_PATTERN] [-SvP SPECIAL_INVERT_PATTERN]

options:
  -h, --help            show this help message and exit
  -t THREADS, --threads THREADS
                        The number of threads to use
  -p PROXY, --proxy PROXY
                        The proxy to use
  -w WORDLIST, --wordlist WORDLIST
                        The wordlist to use
  -is IGNORE_SSL, --ignore-ssl IGNORE_SSL
                        Ignore the certificate checks
  -Ps PRINT_SIMPLE, --print-simple PRINT_SIMPLE
                        Use the non-colored output of the tool
  -Pc PRINT_COLORED, --print-colored PRINT_COLORED
                        Use the colored output of the tool - The default behavior
  -PC PRINT_CODE, --print-code PRINT_CODE
                        Use the code-based output of the tool - The code have access to the current "word" of the wordlist, the "response" object and the "pattern" to look for
  -u URL, --url URL     The URL of the target
  -m METHOD, --method METHOD
                        The HTTP method to use
  -d DATA, --data DATA  The data in the body of the requests
  -H HEADER, --header HEADER
                        A header to add to the requests
  -P PATTERN, --pattern PATTERN
                        A regex to check against the body of the responses of the server
  -ed ENCODE_DATA, --encode_data ENCODE_DATA
                        URL encode POST data
  -to TIMEOUT, --timeout TIMEOUT
                        The timeout for all the requests
  -Su SPECIAL_URL, --special-url SPECIAL_URL
                        The URL of the special task - Incompatible with -Sw and Sc
  -Sw SPECIAL_WORDLIST, --special-wordlist SPECIAL_WORDLIST
                        The wordlist to use as the special - Incompatible with -Su and -Sc
  -Sc SPECIAL_CODE, --special-code SPECIAL_CODE
                        The code to use to update the special - The provided code have access to the response of the previous normal request with the "response" variable and to the previous special with the "special"
                        variable - Incompatible with -Su and -Sw
  -SD SPECIAL_DELAY, --special-delay SPECIAL_DELAY
                        The delay to wich the special task is to be performed (in seconds) - Incompatible with -SF
  -SF SPECIAL_FLAG, --special-flag SPECIAL_FLAG
                        The regular expression in the normal response to look for to know when the special task is to be performed - Incompatible with -SD
  -Sm SPECIAL_METHOD, --special-method SPECIAL_METHOD
                        The HTTP method to use for the special task
  -Sd SPECIAL_DATA, --special-data SPECIAL_DATA
                        The data in the body of the requests for the special task
  -SH SPECIAL_HEADER, --special-header SPECIAL_HEADER
                        A header to add to the requests for the special task
  -SP SPECIAL_PATTERN, --special-pattern SPECIAL_PATTERN
                        The regex for the element to get in the response
  -SvP SPECIAL_INVERT_PATTERN, --special-invert-pattern SPECIAL_INVERT_PATTERN
                        Element to be deleted from the matched special pattern (useful when searching for element after a specific keyword but the keyword is not part of the special string)
```
