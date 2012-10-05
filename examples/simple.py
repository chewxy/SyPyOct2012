#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
import sys, zmq

HOST = False
if '--host' in sys.argv:
	HOST = True

def hosting():
	context = zmq.Context()
	socket = context.socket(zmq.PULL)
	bound = 0
	for arg in sys.argv:
		try:
			socket.bind(arg)
			bound = 1
		except zmq.core.error.ZMQError:
			bound = 0
			continue
	if not bound:
		raise Exception('You suck. You need to provide an interface for the host to bind to')

	return socket
def connecting():
	context = zmq.Context()
	socket = context.socket(zmq.PUSH)
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
		while True:
			msg = socket.recv()
			print 'received: %s' % msg
	else:
		socket = connecting()
		while True:
			i = raw_input('send something > ')
			socket.send(i)

if __name__ == '__main__':
	main()
