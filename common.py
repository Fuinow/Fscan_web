import urllib2
from config import CONFIG

def my_request(url, data=None, headers={}):
	if CONFIG.HTTP_DEBUG:
		httpHandler = urllib2.HTTPHandler(debuglevel=1)
		opener = urllib2.build_opener(httpHandler)
		urllib2.install_opener(opener)
	if CONFIG.HTTP_PROXY:
		proxy_support = urllib2.ProxyHandler({"http" : "http://%(host)s:%(port)d" % CONFIG.PROXY_INFO})
		opener = urllib2.build_opener(proxy_support)
		urllib2.install_opener(opener)

	raw_headers = CONFIG.HEADERS
	res = None
	error = None
	code = 0

	if headers:
		for k,v in headers.items():
			raw_headers[k] = v
	if data:
		req = urllib2.Request(url, data=data, headers=raw_headers)
	else:
		req = urllib2.Request(url, headers=raw_headers)

	try:
		res = urllib2.urlopen(req, timeout=CONFIG.TIMEOUT)
		code = res.getcode()
	except urllib2.HTTPError, e:
			code = e.code
	except Exception, e:
		error = e
	return res, code, error

if __name__ == "__main__":
	res, code, error = my_request(url="http://www.baidu.com")
	print code
	print error
#	print res.read()
