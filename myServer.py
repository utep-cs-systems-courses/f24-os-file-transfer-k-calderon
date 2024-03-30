#! /usr/bin/env python3

import socket, sys, params, os

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

paramMap = params.parseParams(switchesVarDefaults)
listenPort = paramMap['listenPort']
# use all available interfaces
listenAddr = ''

if paramMap['usage']:
    # user has passed arg -? or --usage
    params.usage()

# socket.socket - create a new socket
# socket.AF_INET - use IPv4
# socket.SOCK_STREAM - TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#allow reusing of the socket address
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# listen to all addresses, '', on port 50001
s.bind((listenAddr, listenPort))
# allow up to 10 clients
s.listen(10)

# track child PIDs
childPIDs = []


# loop that echos out what the client sends
while 1:
    '''
    accept returns a touple
    conn - new socket created when accept establishes a connection
    addr - address info of the client
    '''
    conn, addr = s.accept()
    print('Connected to: ', addr)

    # new connection, do the fork
    pid = os.fork()

    if pid == 0:
        # we're the child and don't need the listener socket
        s.close()
        
        print(f"Child created pid:{os.getpid()}")

        # handle client connection
        while True:

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
            sys.exit(0)
    else:
        # we're the parent and don't need the client connection socket
        conn.close()
        
        print(f"Parent pid: {os.getpid()}")
        childPIDs.append(pid)

        # look for zombies and reap them
        while True:
            '''
            -1 means any child process that has terminated without reporting its exit status
            os.WNOHANG means waitpid returns immediately if there's no zombies to reap
            '''
            terminatedPID, status = os.waitpid(-1, os.WNOHANG)
            if terminatedPID == 0:
                break
            else:
                childPIDs.remove(terminatedPID)
                print(f"Child process pid: {terminatedPID} terminated with status: {status}")

        