#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
import sys, zmq, socket, re

HOSTING = False  # sane defaults are sane
if '--host' in sys.argv:
	HOSTING = True

IP = None  # sane defaults that act as an error check
IPPattern = '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'  # yes this is a ridiculous IP regular expression. And it's not a very good one
PORT = None  # sane defaults that act as an error check

# the two loops below attempts to set a IP and port
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

# sanity checks. If they fail, raise exceptions and run!
if not HOSTING and not IP:
	raise Exception('IP Address needed')
	sys.exit()
if not PORT:
	raise Exception('PORT NEEDED')
	sys.exit()

# now that we've passed all the sanity checks,
# let's commence with the connecting
# In this example, we only assume two machines are talking to each other 
# like a walkie talkie
# So every machine will have a pull (receive)
# and a push (send) mechanism
context = zmq.Context()  # define a context
pushSocket = context.socket(zmq.PUSH)
pullSocket = context.socket(zmq.PULL)

if HOSTING:  # anyone can host
	pushSocket.bind('tcp://*:%s' % PORT)
	pullSocket.bind('tcp://*:%s' % (PORT + 1))
	print ('Now Listening on: %s' % (socket.gethostbyname(socket.gethostname()) + ':' + str(PORT)))
else: # if you are not hosting you are connecting
	pullSocket.connect('tcp://%s:%s' % (IP,PORT))
	pushSocket.connect('tcp://%s:%s' % (IP, (PORT + 1)))

def main():
	while True:
		# the rule is exactly the same as walkie talkies:
		# You keep receiving unless you wanna talk. Then you push a button and you stop receiving
		# In this case we're abusing KeyboardInterrupt for Fun and Profit
		# It will always wait for new messages until you press Ctrl+C
		try:
			msg = pullSocket.recv()
			print ('Received: %s' % msg)
		except KeyboardInterrupt:
			print ('\b\b')
			i = raw_input('Sent: ')
			pushSocket.send(i)

if __name__ == '__main__':
	main()
