#encoding=utf-8
import time
import Queue
import urllib2
import gevent
from gevent import monkey
monkey.patch_all()
import os
import sys
from difflib import SequenceMatcher
import threading

sys.path.append("..")
from Config import CONFIG

class DirScan(object):
	
	def __init__(self, domain):
		self.Q = Queue.Queue()
		self.lock = threading.Lock()
		self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
           }
		self.domain = domain
		self._404_page = None
		self.data = []
		self.percent = 0

	def load_dict(self, file):
		with open(file) as f:
			for line in f.xreadlines():
				url = line.strip()
				if url:
					self.Q.put(url)
				else:
					pass

	def get_404_page(self):
		url1 = self.domain + "/s4dsad"
		url2 = self.domain + "/asdas/1.txt"
		req1 = urllib2.Request(url1, headers=self.headers)
		req2 = urllib2.Request(url2, headers=self.headers)
		try:
			res1 = urllib2.urlopen(req1)
			page1 = res1.read()
			code1 = res1.getcode()
		except urllib2.HTTPError, e:
			page1 = None
			code1 = e.code
		try:	
			res2 = urllib2.urlopen(req2)
			page2 = res2.read()
			code2 = res2.getcode()
		except urllib2.HTTPError, e:
			page2 = None
			code2 = e.code
		if code1==404 and code2==404:
			self._404_page = {
					"code" : code1,
					"page" : None,
						} 
			return
#		print self.page_ratio(page1, page2)
		if page1 and page2 and self.page_ratio(page1, page2) > 0.7:
			self._404_page = {
					"code" : code1,
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
		req = urllib2.Request(url, headers=self.headers)
		try:
			res = urllib2.urlopen(req)
			page = res.read()
			code = res.getcode()
		except urllib2.HTTPError, e:
			code = e.code
			page = None

		if self._404_page["page"]:			
			if code == 200:
				if self.page_ratio(page, self._404_page["page"]) < CONFIG.DIR_RATIO:
					return True
				else: 
					return False
			else:
				return False

		else:
			if code==200:
				return True
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
				print "[%d] %s                                      ------Found-------"%(num, url)
				self.data.append(url)
			else:
				print "[%d] %s"%(num, url)
				pass 
			self.lock.acquire()
		self.lock.release()

	def run(self):
		g_list = []
		self.load_dict(CONFIG.DIR_DICT)
		self.get_404_page()
		if self._404_page:
			for i in range(CONFIG.DIR_THREAD):
				g = gevent.spawn(self.brute)
				g_list.append(g)
			gevent.joinall(g_list)
			return self.data
		else:
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

	test = DirScan("https://www.baidu.com")
	CONFIG.DIR_DICT = "../" + CONFIG.DIR_DICT
	data = test.run()
	print data
	
