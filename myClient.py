#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os
import params
import FileHandler as FH

# defines defaults for when params.parseParams is invoked
switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    (('-f', '--file'), 'file', "README.md"), # file to send
    )

# this library parses the command line args. default values are used if no args are present
paramMap = params.parseParams(switchesVarDefaults)

# store args in descriptive vars
server, usage, fileName  = paramMap["server"], paramMap["usage"], paramMap["file"]

if usage:
    # user invoked a help arg
    params.usage()
if not fileName:
    print("Please provide a file to send using -f or --file")
    sys.exit(1)

try:
    #further break down the server address to more specific vars
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
'''https://docs.python.org/3/library/socket.html#socket.getaddrinfo
# socket.AF_UNSPEC - use either IPv4 or IPv6
# socket.SOCK_STREAM - use TCP
# getaddrinfo - returns 5 touples for use in creating socket
'''
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    '''
    af- address family. tells socket.socket is creating a compatible socket with the server
    socktype - TCP (from socket.SOCK_STREAM)
    proto - a number that represents the protocol. usually 0 indicating to use the default 
            type for the address family and socket type
    canonname - name of the host or empty string if none
    sa - socket address 
    '''
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        # create the socket with the info above
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        # loop around and try again
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        # establish the connection
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        # loop around try again
        continue
    break

# None indicates getaddrinfo failed entirely
if s is None:
    print('could not open socket')
    sys.exit(1)

# s.fileno() returns the file descriptor of the socket. write to that file descriptor to send the data to the server
socketFD = s.fileno()
fileData = FH.dataBuilder(fileName)
while fileData:
    # send a chunk
    bytesSent = s.send(fileData)
    print(f"Sent {bytesSent} bytes")
    # get ready for the next chunk
    fileData = fileData[bytesSent:]



print("Waiting for server response")
# print out server response
serverResponse = os.read(s.fileno(), 1024).decode()
print("Received '%s'" % serverResponse)


'''
shutdown followed by close is best practice
shutdown signals the server of intent to close the connection.
close releases the resources on the client.
should do both in most cases
'''
s.shutdown(socket.SHUT_WR)
s.close()