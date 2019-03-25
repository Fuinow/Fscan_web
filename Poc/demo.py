#coding=utf8
#poc filename don't suppose "."

import urllib2


class Poc(object):

	def __init__(self, domain):
		self.domain = domain
		self.data = {
					"file_name" : __name__,
					"name" : "ThinkPHP V5.0.X < 5.0.23,V5.1.X <= 5.1.31 远程代码执行漏洞",
					"referer" : "https://bbs.ichunqiu.com/thread-48687-1-1.html",
		}

	def _poc(self):
		# return True or False
		pass
		
	def run(self):
		check = self._poc()
		if check:
			return self.data
		else:
			return False




if __name__ == "__main__":
	test = Poc("http://127.0.0.1:8081/tp5131")
	data = test.run()
	print data