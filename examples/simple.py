#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
import sys, zmq

HOST = False  # sane defaults are sane
if '--host' in sys.argv:
	HOST = True

def hosting():
	context = zmq.Context()	 # we start by defining a zeroMQ context
	# then we decide what kind of socket we want
	# By convention, the host/listener is also the receiver
	# You can actually swap it around and it will still work	
	# But for the context of this example, we'll stick with tradition just because
	socket = context.socket(zmq.PULL)
	bound = 0  # this is for sanity checks: if it's not bound, then an error should be raised

	# the loop below tries to bind the socket to an address
	for arg in sys.argv:
		try:
			socket.bind(arg)
			bound = 1
		except zmq.core.error.ZMQError:
			bound = 0
			continue
	if not bound:
		raise Exception('You suck. You need to provide an interface for the host to bind to')
	
	#once bound, the socket is returned
	return socket

def connecting():
	# this function is exactly the same as above, except it's used for connecting
	context = zmq.Context()
	socket = context.socket(zmq.PUSH)  # again, tradition
	connected = 0
	for arg in sys.argv:
		try:
			socket.connect(arg)
			connected = 1
		except zmq.core.error.ZMQError:
			connected = 0
			continue
	if not connected:
		raise Exception('You need to provide an interface for the client to connect to')
	
	return socket

def main():
	if HOST:
		socket = hosting()
		while True: # INFINITE LOOP FTW! Who cares about proper daemonizing!
			# if it's hosting, then the socket should be receiving
			msg = socket.recv()
			print ('received: %s' % msg)
	else:
		socket = connecting()
		while True: # another infinite loop. Just cause I can.
			# if it's connecting, you should be sending something. But what? Why not user input?
			i = raw_input('send something > ')  # why not zoidberg?
			socket.send(i)

if __name__ == '__main__':
	main()
