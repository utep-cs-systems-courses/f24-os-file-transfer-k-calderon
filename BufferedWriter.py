import os

class BufferedWriter:
    def __init__(self, fd):
        self.fd = fd
    def write(self, byteArr, bufferSize = 1024):
        # initialize and cleanup after previous write calls
        buffer = b""
        # buffered writing here
        for chunk in [byteArr[i:i + bufferSize] for i in range(0, len(byteArr), bufferSize)]:
            if len(buffer) + len (chunk) > bufferSize:
                # time to write
                os.write(self.fd, buffer)
                buffer = b""
            buffer += chunk
        # check if there's anything left to write after buffered writing is done
        if buffer:
            os.write(self.fd, buffer)