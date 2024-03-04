import os

class BufferedReader:
    def __init__(self, fd):
        self.fd = fd
    def read(self, readSize, bufferSize = 1024):
        buffer = b""
        while len(buffer) < readSize:
            print("self.fd", self.fd)
            dataRead = os.read(self.fd, bufferSize)
            if not dataRead:
                break
            buffer += dataRead
        bufferedBytes = buffer[:bufferSize]
        buffer = buffer[bufferSize:]
        if buffer:
            print("buffer remaining", buffer)
        else:
            print ("Null buffer")
        print("bufferedBytes returned", bufferedBytes)
        return bufferedBytes