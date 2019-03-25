import sys
import logging
import os
import importlib

sys.path.append("..")

class PocScan(object):

	def __init__(self, domain):
		self.data = []
		self.domain = "http://" + domain
		self.poc_list = []

	def get_poc(self):
		for poc in os.listdir("Poc"):
			file, ex = os.path.splitext(poc)
			if ex.lower()==".py" and poc.lower()!="__init__.py":
				file = file.replace(".","\\.")
				poc = "Poc." + file
				self.poc_list.append(poc)
			else:
				pass

	def run(self):
		self.get_poc()
		for poc in self.poc_list:
			info = "Testing " + poc
			logging.info(info)
			module = importlib.import_module(poc).Poc(self.domain)
			result = module.run()
			if result:
				info = "Valuable!!!"
				logging.info(info)
				self.data.append(result)
			else:
				info = "Unvaluable"
				logging.info(info)
		info = "Poc Scanner: Finished"
		logging.info(info)
		return self.data


if __name__ == "__main__":
	test = PocScan("http://127.0.0.1:8081/tp5131")
	data = test.run()
	print data