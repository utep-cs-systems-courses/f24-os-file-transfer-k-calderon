#! /usr/bin/env python3

import socket, sys, params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
# use all available interfaces
listenAddr = ''

# what is going on here?
if paramMap['usage']:
    params.usage()

# socket.socket - create a new socket
# socket.AF_INET - use IPv4
# socket.SOCK_STREAM - TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# listen to all addresses, '', on port 50001
s.bind((listenAddr, listenPort))
# only 1 request
s.listen(1)

'''
accept returns a touple
conn - new socket created when accept establishes a connection
addr - address info of the client
'''
conn, addr = s.accept()
print('Connected to: ', addr)

# loop that echos out what the client sends
while 1:
    # save data client sends to data. max 1024 bytes at a time. loop ensures we get it all(?)
    data = conn.recv(1024).decode()
    # send is done. break the loop
    if len(data) == 0:
        print("Zero length read, nothing to send, terminating")
        break
    # print out what we got
    sendMsg = ("Echoing %s" % data).encode()
    print("Received '%s', sending '%s'" % (data, sendMsg.decode()))
    # loop to make sure to send the whole message
    while len(sendMsg):
        # conn.send returns the number of bytes sent
        bytesSent = conn.send(sendMsg)
        # send the next chunk of the message using slicing
        sendMsg = sendMsg[bytesSent:0]

# we're done, shut down the socket
conn.shutdown(socket.SHUT_WR)
#then close it
conn.close()
