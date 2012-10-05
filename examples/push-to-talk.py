#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
import sys, zmq, socket, re

HOSTING = False
if '--host' in sys.argv:
	HOSTING = True

IP = None
IPPattern = '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
PORT = None
for arg in sys.argv:
	try:
		PORT = int(arg)
	except:
		pass

for arg in sys.argv:
	try:
		IP = re.match(IPPattern, arg).group()
	except:
		pass

if not HOSTING and not IP:
	raise Exception('IP Address needed')
	sys.exit()
if not PORT:
	raise Exception('PORT NEEDED')
	sys.exit()

context = zmq.Context()
pushSocket = context.socket(zmq.PUSH)
pullSocket = context.socket(zmq.PULL)

if HOSTING:
	pushSocket.bind('tcp://*:%s' % PORT)
	pullSocket.bind('tcp://*:%s' % (PORT + 1))
	print ('Now Listening on: %s') % (socket.gethostbyname(socket.gethostname()) + ':' + str(PORT))
else:
	pullSocket.connect('tcp://%s:%s' % (IP,PORT))
	pushSocket.connect('tcp://%s:%s' % (IP, (PORT + 1)))

poller = zmq.Poller()
poller.register(pullSocket, zmq.POLLIN)

def main():
	while True:
		try:
			socks = dict(poller.poll(1000))
			msg = pullSocket.recv()
			print ('Received: %s' % msg)
			continue
		except KeyboardInterrupt:
			print ('\b\b')
			i = raw_input('Sent: ')
			pushSocket.send(i)

if __name__ == '__main__':
	main()
