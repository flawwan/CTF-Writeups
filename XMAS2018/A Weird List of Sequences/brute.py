from pwn import *
import hashlib

r = remote("199.247.6.180", 14003)
r.recvuntil("=")
captcha = r.recvuntil(".")[:-1]
i=0
while True:
	i+=1
	md5str=hashlib.md5(str(i)).hexdigest()[:5]
	if md5str == captcha:
		print "Found captcha %i" % i
		break

r.sendline(str(i))