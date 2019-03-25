import importlib
import urllib2
import json
import logging
import re
from Domain_Collect import DomainCollect
from outputer import Outputer
from Module import Finger, Port_Scan, Dir_Scan, Poc_Scan
from config import CONFIG
from common import my_request
from multiprocessing import Manager
import time

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(levelname)s - %(message)s')


class Scanner(object):
	
	def __init__(self):
		self.task= Manager().list()
		self.outputer = Outputer()

	def add_task(self, root_domain, domain, s_type):
		t = (root_domain, domain, s_type)
		self.task.append(t)
		print self.task
		return

	def check_network(self,domain):
		domain = "http://" + domain
		res, code, error = my_request(domain)
		if not error:
			return True
		else:
			warning = str(error)
			print warning
			return False

#	def get_ip(self, domain):
#		import socket
#		ip =  socket.getaddrinfo(domain, 'http')[0][4][0]
#		return str(ip)

	def _get_ip(self, domain):
		retry = 3
		ip = None
		num = 0
		api = "http://ip-api.com/json/%s?lang=en" %domain		
		while num != retry:
			try:
				res = urllib2.urlopen(api).read()
				ip = json.loads(res)["query"].encode('utf8') 
				if re.match("\d+\.\d+\.\d+\.\d+", ip):
					break
				else:
					num += 1
			except Exception, e:
				print e
				#print "[-] Get ip error : Network error"
				num += 1		
		return ip

	def dir_scan(self, domain):
		dir_scan = Dir_Scan.DirScan(domain)
		data = dir_scan.run()
		return data

	def port_scan(self, ip):
		port_scan = Port_Scan.PortScan(ip)
		data = port_scan.run()
		return data

	def finger(self, domain):
		finger = Finger.Finger(domain)
		data = finger.run()
		return data

	def poc_scan(self, domain):
		poc_scan = Poc_Scan.PocScan(domain)
		data = poc_scan.run()
		return data

	def run(self):
		while True:
			if self.task:
#				print self.task
				root_domain, domain, s_type = self.task.pop()
				data = dict()
				data["domain"] = domain

				if s_type == "domain_col":
					domain_col= DomainCollect(root_domain)
					domain_col.run()
				else:
					info = "Scanning %s"%domain
					logging.info(info)
					info = "Get IP : %s"%domain
					logging.info(info)
					if self.check_network(domain):
						ip = self._get_ip(domain)
						if ip:
							info = "IP : %s"%ip
							logging.info(info)
							data["ip"] = ip
						else:
							warning = "Get ip failed"
							logging.info(warning)

						if s_type == 'dir':
							info = "Dir Scanning: %s"%domain
							logging.info(info)
							result = self.dir_scan(domain)
							data["dir"] = result

						elif s_type == 'finger':
							info = "Finger testing : %s"%domain
							logging.info(info)
							result = self.finger(domain)
							data["finger"] = result

						elif s_type == 'poc':
							info = "Poc Testing : %s"%domain
							logging.info(info)
							result = self.poc_scan(domain)
							data['poc'] = result

						elif s_type == 'port' and ip:
							info = "Port Scanning : %s"%ip
							logging.info(info)
							result = self.port_scan(ip)
							data['port'] = result
						

						else:
							pass
						print data
						dic = {"dir":0,"port":1,"finger":2,"poc":3}
						self.outputer.change_scan_state(root_domain, domain, dic[s_type], "success")
						self.outputer.scan_update(data, root_domain)

					else:
						warning = "Can't connecting host: %s"%domain
						print warning
						pass
			else:
				pass

if __name__ =="__main__":
	test = Scanner()
#	data = test.scan("https://ww.baidu.com")
#	print test.data
	print test._get_ip("coin.jd.com")