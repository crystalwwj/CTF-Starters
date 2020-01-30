# Python bytecode 3.7 (3394)
# Embedded file name: H0W.py
# Size of source mod 2**32: 387 bytes
# Decompiled by https://python-decompiler.com
import sys, struct
import random
import time
from terrynini import *

def rotl(n, rotations):
    """Return a given number of bitwise left rotations of an integer n,
       for a given bit field width.
    """
    rotations %= 32
    if rotations < 1:
        return n
    n &= 2**32-1
    return ((n << rotations) & (2**32-1)) | (n >> (32 - rotations))

def rotr(n, rotations):
    """Return a given number of bitwise left rotations of an integer n,
       for a given bit field width.
    """
    rotations %= 32
    if rotations < 1:
        return n
    n &= 2**32-1
    return (n >> rotations) | ((n << (32 - rotations)) & (2**32-1))
#time.gmtime(1564809914)
random.seed(1568179514) #2019/09/03 05:25:14
f = open('answer.txt', 'rb').read()
s = open('seed.txt', 'r')
out = open('output.png', 'wb')
if len(f) % 4 != 0:
    f += (4 - len(f) % 4) * '\x00'

for i in range(0, len(f), 4):
	#fun = random.randrange(4)
	fun = int(s.readline())
	print(fun)
	string = struct.unpack('<I', f[i:i + 4])[0]
	print(i)
	#print(fun)
	if fun==0:
		#print(0)
		string = string ^ 0xfaceb00c
		if string > 2**31:
			string = string - 2**32
		out.write(struct.pack('<i',string))
	elif fun==1:
		#print(1)
		string = string - 74628
		#print(string)
		if string > 2**31:
			string = string - 2**32
		out.write(struct.pack('<i',string))
		#out.write(string-74628)
	elif fun==2:
		#print(2)
		string = rotr((string & 0xAAAAAAAA),2) | rotl((string & 0x55555555),4)
		if string > 2**31:
			string = string - 2**32
		out.write(struct.pack('<i', string))
	elif fun==3:
		#print(3)
		string = rotr((string & 0xAAAAAAAA),2) | rotl((string & 0x55555555),4)
		string = (string - 74628) ^ 0xfaceb00c
		if string > 2**31:
			string = string - 2**32
		if string < -2**31:
			string = string + 2**32
		out.write(struct.pack('<i',string))
	else:
		print('something went wrong!')

print('Complete')
