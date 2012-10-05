SyPyOct2012
===========

Examples for SyPy October 2012

I have provided two examples: `simple.py` and `push-to-talk.py`

## simple.py ##

To use simple.py is simple:

* If you want to connect: `./simple.py <address>`
* If you want to host: `./simple.py --host <address>`
* `<address>` is in this format: `PROTOCOL://ADDRESS:PORT`
* Try these for fun and profit:
  * ipc://interprocess.socket
  * tcp://*:1234

The nature of zmq is that it doesn't matter the order of connecting and hosting. It just works ^_^

## push-to-talk.py ##

Push to talk is a walkie talkie simulator I built because I was working on an older test machine and I didn't want to login to my email to send myself a link.

To use: 

* If you want to connect: `./push-to-talk.py <IP> <PORT>`
* If you want to host: `./push-to-talk.py <PORT>`
* Press Ctrl+C if you want to send something to the other machine.
* This is most fun if you do it on multiple physical machines on multiple different OSes
* Or if you are boring you can just fire up two terminals and talk to yourself as if you're FOREVER APHONE.
