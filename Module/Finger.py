import logging
import sys
import Queue
import json
import urllib2
import urllib
import threading
import hashlib

sys.path.append("..")
from config import CONFIG
from common import my_request

class Finger(object):

	def __init__(self, domain):
		self.data = []
		self.domain = "http://" + domain
		self.Q = Queue.Queue()

	def get_md5(self,html):
		m2 = hashlib.md5()
		m2.update(html)
		return m2.hexdigest()

	def load_finger(self):
		with open(CONFIG.FINGER_DICT) as f:
			fingers = json.load(f)

		for finger in fingers:
			if finger:
				self.Q.put(json.dumps(finger))

	def check(self):
		while not self.Q.empty():
			ret = True
			finger = json.loads(self.Q.get())
			data = urllib.urlencode(finger["request"]["data"])
			name = finger["name"]
			url = finger["request"]["url"]
			headers = finger["request"]["headers"]
			method = finger["request"]["method"]
			res_headers = finger["response"]["headers"]
			res_code = finger["response"]["code"]
			md5 = finger["response"]["md5"]
			html = finger["response"]["html"].encode("utf-8") 
			
			url = self.domain + url
			if (name not in self.data):
#				print url
				if method == "POST":
					res, code, error = my_request(url=url, data=data, headers=headers)
				else:
					res, code, error = my_request(url=url, headers=headers)
				if error:
					logging.warning(error)
					continue
				if res:
					buf = res.read()
				else:
					buf = ''

				if res_code:
					ret &= (res_code==code)

				if html:
					ret &= (html in buf)

				if res_headers:
					ret &= (res_headers in str(res.headers))

				if md5:
					ret &= (md5==self.get_md5(buf))

				if ret:
					info = "Find finger %s"%name
					logging.info(info)
					self.data.append(name)
			else:
				continue

	def run(self):
		self.load_finger()
		t_list = []
		for i in range(CONFIG.FINGER_THREAD):
			t = threading.Thread(target=self.check)
			t.start()
			t_list.append(t)

		for t in t_list:
			t.join()

		info = "Finger : Finished"
		logging.info(info)
		return list(set(self.data))

if __name__ == "__main__":
	CONFIG.FINGER_DICT = "../" + CONFIG.FINGER_DICT 
	test = Finger("http://119.23.207.202")
	res = test.run()
	print res
