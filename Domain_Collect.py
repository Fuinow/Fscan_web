import urllib2
import json
import sys
import logging
import re
from outputer import Outputer
from common import my_request

reload(sys)  
sys.setdefaultencoding('gb2312')

class DomainCollect(object):

	def __init__(self, domain):
		self.domain = domain
		self.domains = set()
		self.outputer = Outputer()
		
	def get_title(self,domain):
		url = "http://" + domain
		res,code,error = my_request(url)
		if res:
			try:
				title = re.search(r'<title>(.*)</title>',res.read()).group(1).encode("utf8")
			except:
				title = "None"
		elif error:
			title = str(error)
		else:
			title = str(code)
		print "[get_title]: " + title
		return title

	def from_virustotal(self):
		domain = "www." + self.domain
		apikey = '5708918004f2700156dcd65e0d15c96935d7eb662112b2de5802ef790b4ab271'
		api_url = 'https://www.virustotal.com/vtapi/v2/domain/report?apikey=%s&domain=%s'%(apikey,domain)
		try:
			res = urllib2.urlopen(api_url,timeout=5).read()
		except Exception, e:
			logging.warning(str(e))
			return
		dict = json.loads(res)
		if dict["response_code"] == 1:
			for domain in dict['domain_siblings']:
				self.domains.add(domain.strip())
		return


	def run(self):
		info = "Collect domains : %s"%self.domain
		logging.info(info)
		self.from_virustotal()
		print self.domains
		data = []
		for domain in list(self.domains):
			title = self.get_title(domain)
			data.append({"domain":domain,"title":title,"state":["default","default","default","default"]})
		self.outputer.domain_update(data, self.domain)
		return self.domains

if __name__ == "__main__":
	test = DomainCollect("www.baidu.com")
	print test.get_title("m.jd.com")
