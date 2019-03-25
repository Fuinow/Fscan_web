import urllib2
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser
import time
import logging
import sys

sys.path.append("..")
from config import CONFIG

class PortScan(object):

	def __init__(self, ip):
		self.data = []
		self.ip = ip
		self.timeout = 300
		self.retry = 2

	def run(self):
		run_time = 0
		try:
			options = "--open -p %s"%str(CONFIG.PORT_LIST)[1:-1].replace(" ","")
			nmap_proc = NmapProcess(targets=self.ip, options=options)
		
			nmap_proc.run_background()
			while nmap_proc.is_running():
				if run_time <= self.timeout:
					time.sleep(5)
					run_time += 5
					print nmap_proc.progress
				else:
					print "Timeout"
					return []
			if nmap_proc.is_successful():
				report = NmapParser.parse(nmap_proc.stdout)
				for host in report.hosts:
					for service in host.services:
						add = dict()
						data =  service.get_dict()
						add["service"] = data["service"]
						add["port"] = data["port"]
						self.data.append(add)
		except Exception, e:
			print e
			return []

		info = "Port Scanner : Finished"
		logging.info(info)
		return self.data

if __name__  == "__main__":
	test = PortScan(ip="119.75.217.26")
	a = test.run()
	print a 