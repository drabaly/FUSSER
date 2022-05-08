# FUSSER
Fuzzer Short SEssion Reauth is a fuzzer aimed at authenticated fuzzing.

This tool has a simple purpose: easily perform fuzzing as an authenticated user by handling way to keep the session alive.

FUSSER can be splitted in 2 main parts:
* Standard: it can be used as a simple fuzzer like we all know, the keeword to FUZZ is '$FUZZ$'
* Special: That's were the fun begin... This is were you handle when and how you reauthenticate your session. It can be splitted in 2 parts (once again...):
** The updater: how to detect if your session is dead
** The special: how to updated your session

In theory, the tool should be easy to modify/add features if you want. But it's juste a theory (That I hope is real).

Guarantee: The ONLY guarantee so far is that I have missed a few bugs, if you can create an issue if you find one, that would be nice ;)
