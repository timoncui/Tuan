import urllib
import urllib2
import datetime
import socket

import tornado.httpclient
import tornado.ioloop

def __http_fetch(url, user_agent, timeout=300):
	socket.setdefaulttimeout(timeout)  # set a global timeout for all sockets

	headers = {'User-Agent': user_agent}
	request = urllib2.Request(url, None, headers)  # url, data, and headers

	start_time = datetime.datetime.now()

	print "start opening ", url
	try:
		response= urllib2.urlopen(request, timeout=timeout)
		content = response.read()
	except socket.timeout:
		print "Timeout: open url:", url
		raise

	print "finish loading ", url
	end_time = datetime.datetime.now()
	duration = end_time - start_time
	print "it takes", duration.seconds, "seconds"
	return content

# tornado based http client is much better!
def http_fetch(url, user_agent, timeout=600):
	try:
		headers = {'User-Agent': user_agent}
		request = tornado.httpclient.HTTPRequest(url=url, method="GET", headers=headers, connect_timeout=20.0, request_timeout=timeout)
		http_client = tornado.httpclient.HTTPClient()

		start_time = datetime.datetime.now()
		print "start loading  ", url

		response = http_client.fetch(request)

		print "finish loading ", url
		end_time = datetime.datetime.now()
		duration = end_time - start_time
		print "it takes", duration.seconds, "seconds"
		return response.body
	except Exception, e:
		print "tuan_http.py http_fetch", url, e
		raise

def tornado_http_fetch(url, user_agent, handle_request):
	try:
		headers = {'User-Agent': user_agent}
		request = tornado.httpclient.HTTPRequest(url=url, method="GET", headers=headers, connect_timeout=20.0, request_timeout=3.0)
		http_client = tornado.httpclient.AsyncHTTPClient()
		http_client.fetch(request, handle_request)
		tornado.ioloop.IOLoop.instance().start()
	except Exception, e:
		print "tuan_http.py tornado_http_fetch", e

if __name__ == "__main__":
	def handle_request(response):
		print "callback - handle_request"
		if  response.error:
			print response.error
		else:
			print "success"
		tornado.ioloop.IOLoop.instance().stop()

	tornado_http_fetch("http://www.nuomi.com/api/dailydeal?version=v1&city=chaoyang", "Chrome/22.0.1229.94", handle_request)




