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
    byteArr = b"0123456789" * 500
    byteArr += b'END'
    bWriter = BufferedWriter()
    bWriter.write("test.txt", byteArr)
    
    
    fd2 = os.open("test.txt", os.O_RDONLY)
    bReader = BufferedReader()
    byteArrRead = bReader.read(fd2, 16, 20)
    print("byteArrRead", byteArrRead)
if __name__ == "__main__":
    main()