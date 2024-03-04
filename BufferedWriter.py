import os

class BufferedWriter:
    def __init__(self):
        pass
    def write(self, destPath, byteArr, bufferSize = 1024):
        fd = os.open(destPath, os.O_WRONLY | os.O_CREAT)
        if not fd:
            print("no fd")
            return
        # initialize and cleanup after previous write calls
        buffer = b""
        # buffered writing here
        for chunk in [byteArr[i:i + bufferSize] for i in range(0, len(byteArr), bufferSize)]:
            if len(buffer) + len (chunk) > bufferSize:
                # time to write
                os.write(fd, buffer)
                buffer = b""
            buffer += chunk
        # check if there's anything left to write after buffered writing is done
        if buffer:
            os.write(fd, buffer)
        # open the file, write the file, close the file
        os.close(fd)