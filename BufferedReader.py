import os

class BufferedReader:
    def __init__(self):
        pass
    def __finish(self):
        os.close(self.fd)
        return self.bytesRead

    def read(self, fd, bufferSize = 1024, readSize = None):
        self.fd = fd
        self.bytesRead = b""
        buffer = b""
        
        # read bufferSize bytes at a time
        while True:
            if readSize and len(self.bytesRead) >= readSize:
                self.bytesRead = self.bytesRead[:readSize]
                return self.__finish()
            buffer = os.read(fd, bufferSize)
            print("buffer", buffer)
            if not buffer:
                return self.__finish()
            self.bytesRead += buffer
            print("bytes read", self.bytesRead)
            # get any remaining bytes
            # return bytes read