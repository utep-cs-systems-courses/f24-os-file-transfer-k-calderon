import sys, os

def dataBuilder(fileName):
    fileData = b''
    fileNameEncoded = fileName.encode()
    # get the filename size
    # encode the filename size into 8 bits
    fileNameSize = len(fileNameEncoded).to_bytes(8, "big")
    # add the encoded filename size to the file data
    fileData += fileNameSize
    # add the encoded filename itself to the file data
    fileData += fileNameEncoded
    # get the file's data
    # add the file's data to fileData
    with open(fileName, "rb") as f:
        fileData += f.read()
    # escape all backslashes
    fileData.replace(b"\\", b"\\\\")
    # return the file data
    return fileData

def dataParser(fileData):
    # read 8 bytes from fileData to get filename size
    fileNameSize = int.from_bytes(fileData[:8], byteorder="big")
    # read the size in bytes to get the filename
    # store filename
    fileName = fileData[8:(8 + fileNameSize)].decode()
    # store fileData
    fileData = fileData[8 + fileNameSize:]
    # deframe the data
    fileData = fileData.replace(b"\\\\", b"\\")
    fileData = fileData.replace(b"\\e", b"")
    # return the filename and data
    return (fileName, fileData)