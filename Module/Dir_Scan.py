#encoding=utf-8
import time
import Queue
import urllib2
import threading
import os
import sys
from difflib import SequenceMatcher
import logging

sys.path.append("..")
from common import my_request
from config import CONFIG

class DirScan(object):
	
	def __init__(self, domain):
		self.Q = Queue.Queue()
		self.lock = threading.Lock()
		self.domain = "http://" + domain
		self._404_page = None
		self.data = []
		self.percent = 0

	def load_dict(self, file):
		with open(file) as f:
			for line in f.xreadlines():
				url = str(line.strip())
				if url:
					self.Q.put(url)
				else:
					pass

	def get_404_page(self):
		url1 = self.domain + "/s4dsad"
		url2 = self.domain + "/asdas/1.txt"
		retry = 1
		while True:
			if retry == 3:
				return
			res1, code1, error1 = my_request(url1)
			res2, code2, error2 = my_request(url2)
			if error1 or error2:
				warning = str(error1) + ": retry %d"%retry
				logging.warning(warning)
				retry = retry +1 
			else:
				break
		if code1==404 and code2==404:
			self._404_page = {
					"code" : code1,
					"page" : None,
						} 
			return
		elif code1==200 and code2==200:
			page1 = res1.read()
			page2 = res2.read()
			ratio = self.page_ratio(page1, page2)
			if ratio > 0.7:
				self._404_page = {
						"code" : 200,
						"page" : page1,
				}
				return
		else:
			self._404_page = None
			return

	def page_ratio(self, page1, page2):
		if page2 and page1:
			seqm  =SequenceMatcher()
			seqm.set_seq1(page1)
			seqm.set_seq2(page2)
			return seqm.ratio()
		else:
			return None

	def cmp_page(self, url):
		res, code, error = my_request(url=url)
		if self._404_page["page"]:			
			if code == 200:
				if self.page_ratio(res.read(), self._404_page["page"]) < CONFIG.DIR_RATIO:
					return True
				else: 
					return False
			else:
				return False

		elif self._404_page["code"] == 404:
			if code==200:
				return True
			else: 
				return False
		else:
			return False

	def brute(self):
		self.lock.acquire()
		while not self.Q.empty():
			num = self.Q.qsize()
			self.percent = num
			url = self.domain + self.Q.get()
			self.lock.release()
			if self.cmp_page(url):
				info = " **********Found:%s"% url
				logging.info(info)
				self.data.append(url)
			else:
				logging.info(url)
				pass 
			self.lock.acquire()
		self.lock.release()

	def run(self):
		t_list = []
		self.load_dict(CONFIG.DIR_DICT)
		self.get_404_page()
		if self._404_page:
			for i in range(CONFIG.DIR_THREAD):
				t = threading.Thread(target=self.brute)
				t.start()
				t_list.append(t)
			for t in t_list:
				t.join()
			info = "Dir Scanner: Finished"
			logging.info(info)
			return self.data
		else:
			info = "Dir Scanner: Failed"
			logging.info(info)
			return self.data

if __name__ == "__main__":
	

#	proxy_info = { 'host' : '127.0.0.1',
#	               'port' : 8080
#	             }
#	proxy_support = urllib2.ProxyHandler({"http" : "http://%(host)s:%(port)d" % proxy_info})
#	opener = urllib2.build_opener(proxy_support)
#	urllib2.install_opener(opener)

#	httpHandler = urllib2.HTTPHandler(debuglevel=1)
#	httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
#	opener = urllib2.build_opener(httpHandler, httpsHandler)
# 	urllib2.install_opener(opener)	
# http://ke.yuanfudao.com
	test = DirScan("http://ke.yuanfudao.com")
	CONFIG.DIR_DICT = "../" + CONFIG.DIR_DICT
	data = test.run()
	print test._404_page
	print data
	
