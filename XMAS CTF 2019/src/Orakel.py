from pwn import *
r = remote('challs.xmas.htsp.ro', 13000)
context.log_level = "DEBUG"
num = [30000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,30000]
#            65                                                 97

def smallguess(i,mystr):#a when i=26
	r.sendlineafter('Tell me your guess:',mystr+chr(71+i))
	r.recvuntil(':')
	dist = r.recvline()	
	num[1+i] = dist[1:]

def bigguess(i,mystr):
	r.sendlineafter('Tell me your guess:',mystr+chr(65+i))
	r.recvuntil(':')
	dist = r.recvline()	
	num[1+i] = dist[1:]

def slt(number):
	return bool((num[number]<num[number-1]) and (num[number]<num[number+1]))


def guess(mystr):
	smallguess(26,mystr)
	bigguess(25,mystr)
	if(num[27] < num[26]):
		smallguess(38,mystr)
		smallguess(39,mystr)
		if(num[40] < num[39]):
			smallguess(45,mystr)
			smallguess(46,mystr)
			if(num[47] < num[46]):
				smallguess(49,mystr)
				smallguess(50,mystr)
				if(num[51] < num[50]):
					smallguess(51,mystr)
					if(slt(52)):
						return mystr+chr(71+51)
					else:
						return mystr+chr(71+50)
				else:				
					smallguess(47,mystr)
					smallguess(48,mystr)
					if(slt(50)):
						return mystr+chr(71+49)
					elif(slt(49)):
						return mystr+chr(71+48)
					elif(slt(48)):
						return mystr+chr(71+47)
					else:
						return mystr+chr(71+46)
			else:
				smallguess(42,mystr)
				smallguess(43,mystr)
				if(num[44] < num[43]):
					smallguess(44,mystr)
					if(slt(46)):
						return mystr+chr(71+45)
					if(slt(45)):
						return mystr+chr(71+44)
					else:
						return mystr+chr(71+43)
				else:				
					smallguess(40,mystr)
					smallguess(41,mystr)
					if(slt(43)):
						return mystr+chr(71+42)
					elif(slt(42)):
						return mystr+chr(71+41)
					elif(slt(41)):
						return mystr+chr(71+40)
					else:
						return mystr+chr(71+39)

		else:
			smallguess(31,mystr)
			smallguess(32,mystr)
			if(num[33] < num[32]):
				smallguess(35,mystr)
				smallguess(36,mystr)
				if(num[37] < num[36]):
					smallguess(37,mystr)
					if(slt(39)):
						return mystr+chr(71+38)
					elif(slt(38)):
						return mystr+chr(71+37)
					else:
						return mystr+chr(71+36)
				else:				
					smallguess(33,mystr)
					smallguess(34,mystr)
					if(slt(36)):
						return mystr+chr(71+35)
					elif(slt(35)):
						return mystr+chr(71+34)
					elif(slt(34)):
						return mystr+chr(71+33)
					else:
						return mystr+chr(71+32)
			else:
				smallguess(28,mystr)
				smallguess(29,mystr)
				if(num[30] < num[29]):
					smallguess(30,mystr)
					if(slt(32)):
						return mystr+chr(71+31)
					elif(slt(31)):
						return mystr+chr(71+30)
					else:
						return mystr+chr(71+29)
				else:				
					smallguess(27,mystr)
					if(slt(29)):
						return mystr+chr(71+28)
					elif(slt(28)):
						return mystr+chr(71+27)
					else:
						return mystr+chr(71+26)
	else:
		bigguess(12,mystr)
		bigguess(13,mystr)
		if(num[14] < num[13]):
			bigguess(19,mystr)
			bigguess(20,mystr)
			if(num[21] < num[20]):
				bigguess(22,mystr)
				bigguess(23,mystr)
				if(num[24] < num[23]):
					bigguess(24,mystr)
					if(slt(26)):
						return mystr+chr(65+25)
					elif(slt(25)):
						return mystr+chr(65+24)
					else:
						return mystr+chr(65+23)
				else:				
					bigguess(21,mystr)
					if(slt(23)):
						return mystr+chr(65+22)
					elif(slt(22)):
						return mystr+chr(65+21)
					else:
						return mystr+chr(65+20)
			else:
				bigguess(16,mystr)
				bigguess(17,mystr)
				if(num[18] < num[17]):
					bigguess(18,mystr)
					if(slt(20)):
						return mystr+chr(65+19)
					elif(slt(19)):
						return mystr+chr(65+18)
					else:
						return mystr+chr(65+17)
				else:				
					bigguess(14,mystr)
					bigguess(15,mystr)
					if(slt(17)):
						return mystr+chr(65+16)
					elif(slt(16)):
						return mystr+chr(65+15)
					elif(slt(15)):
						return mystr+chr(65+14)
					else:
						return mystr+chr(65+13)
		else:
			bigguess(5,mystr)
			bigguess(6,mystr)
			if(num[7] < num[6]):
				bigguess(9,mystr)
				bigguess(10,mystr)
				if(num[11] < num[10]):
					bigguess(11,mystr)
					if(slt(13)):
						return mystr+chr(65+12)
					elif(slt(12)):
						return mystr+chr(65+11)
					else:
						return mystr+chr(65+10)
				else:				
					bigguess(7,mystr)
					bigguess(8,mystr)
					if(slt(10)):
						return mystr+chr(65+9)
					elif(slt(9)):
						return mystr+chr(65+8)
					elif(slt(8)):
						return mystr+chr(65+7)
					else:
						return mystr+chr(65+6)
			else:
				bigguess(2,mystr)
				bigguess(3,mystr)
				if(num[4] < num[3]):
					bigguess(4,mystr)
					if(slt(6)):
						return mystr+chr(65+5)
					elif(slt(5)):
						return mystr+chr(65+4)
					else:
						return mystr+chr(65+3)
				else:				
					bigguess(0,mystr)
					bigguess(1,mystr)
					if(slt(3)):
						return mystr+chr(65+2)
					elif(slt(2)):
						return mystr+chr(65+1)
					else:
						return mystr+chr(65+0)

		





a = ''
for i in range(96):
	a = guess(a)
	num = [30000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,30000]

	print a
r.interactive()
