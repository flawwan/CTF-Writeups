python
from pwn import *
import hashlib
import requests
from pyquery import PyQuery as pq

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

for i in range(25):
	r.readuntil("[")
	numbers_sequence = r.readuntil("]")[:-1]
	plog = log.progress("Debug")
	plog.success("Sequence %d of %d" % (i,25))

	plog = log.progress('Server')
	plog.success("Recieved sequence from server:\n%s" % numbers_sequence) 	
	response = ""
	plog = log.progress("Oesis")
	plog.status("Searching on oesis")
	try:
		rr = requests.get("https://oeis.org/search?q=%s" % numbers_sequence)
		p = pq(rr.text)
		response = rr.text
		found_sequence = pq(p("table td tr tt > b")[0]).parent().text()
		plog.status("Found sequence:\n %s" % found_sequence)
		next_number = int(found_sequence.replace(numbers_sequence,"")[2:].split(",")[0])
		plog.success("Predicting new number to be %d" % next_number)
	except Exception:
		plog.error("Failed to parse numbers from oeis")
		print response
		exit()
	print "Predicting next number is {%d}" % next_number
	r.sendline(str(next_number))
r.interactive()