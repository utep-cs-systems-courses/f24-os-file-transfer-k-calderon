#! /usr/bin/env python3

import os
from TestClass import TestClass
import testModule
from BufferedWriter import BufferedWriter
from BufferedReader import BufferedReader

def main ():
    testClass = TestClass()
    testClass.hi()
    testModule.hello()
    fd = os.open("test.txt", os.O_WRONLY | os.O_CREAT)
    byteArr = b"0123456789" * 500
    byteArr += b'END'
    bWriter = BufferedWriter(fd)
    bWriter.write(byteArr)
    fd2 = os.open("test.txt", os.O_RDONLY)
    bReader = BufferedReader(fd2)
    byteArrRead = bReader.read(50000, 1024)
    print("byteArrRead", byteArrRead)
if __name__ == "__main__":
    main()