from pwn import *
import numpy

#context.log_level = "DEBUG"
p = remote('challs.xmas.htsp.ro', 13005)
ans = numpy.zeros((32,32))
p.recvline()
p.recvline()
for i in range(961):
	cor = p.recvuntil('=')
	print i
	print cor
	p.sendline('0')
	val = p.recvline()
	#print val
	c1,c2 = cor.split('(')[1].split(')')[0].split(',')
	ans[int(c1)][int(c2)] = 0 if val == 'Good!\n' else 1
	#s += '0' if val == 'Good!\n' else '1'
print ans
numpy.savetxt('func.out',ans,delimiter=' ', fmt='%d')
p.interactive()
