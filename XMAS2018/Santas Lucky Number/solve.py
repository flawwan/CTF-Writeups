import requests
import re
from pyquery import PyQuery as pq
import base64
import time

data = ""
for i in range(0,2000):
	r = requests.get("http://95.179.163.167:12005/?page=" + str(i))
	d = pq(r.text)
	unknown_line = d("p:nth-child(3)").text()
	print "%d - %s" % (i, unknown_line)