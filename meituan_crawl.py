# crawler by calling meituan.com open API
# @author: Lixing Huang
# @time: 10/22/2012

import os
import urllib
import urllib2
import datetime
import tuan_http
import xml.etree.ElementTree as ET


class MeituanCrawler:
	def __init__(self):
		self.url_city_list = "http://www.meituan.com/api/v1/divisions"
		self.url_deal = "http://www.meituan.com/api/v2/"
		self.user_agent = "Chrome/22.0.1229.94"
		self.data_store = "meituan"

	def _fetch(self, url):
		return tuan_http.http_fetch(url, self.user_agent)
	#	headers = {'User-Agent': self.user_agent}
	#	request = urllib2.Request(url, None, headers)

	#	start_time = datetime.datetime.now()
	#	print "start opening ", url
	#	response= urllib2.urlopen(request)
	#	print response.geturl()
	#	print response.info()
	#	content = response.read()
	#	print "finish loading ", url
	#	end_time = datetime.datetime.now()
	#	duration = end_time - start_time
	#	print "it takes", duration.seconds, "seconds"
	#	return content

	def fetch_city_list(self):
		try:
			print "meituan_crawl.py fetch_city_list"
			content  = self._fetch(self.url_city_list)
		#	filepath = os.path.join(self.data_store, "city_list")
		#	fhandler = open(filepath, "w")
		#	fhandler.write(content)
		#	fhandler.close()
			return self.parse_city_list(content)
		except Exception, e:
			print "Error: meituan_crawl.py fetch_city_list", e
			raise
		return None

	def parse_city_list_file(self, filepath=None):
		if not filepath:
			filepath = os.path.join(self.data_store, "city_list")
		fhandler = open(filepath, "r")
		content = fhandler.read()
		fhandler.close()
		return self.parse_city_list(content)

	def parse_city_list(self, content):
		try:
			division_list = []
			root = ET.fromstring(content)
			for division in root.iter("division"):
				division_list.append(division.find("id").text)
			return division_list
		except Exception, e:
			print "meituan_crawl.py extract_city_list", e
			raise

	def get_fetch_deal_url(self, city):
		return self.url_deal + city + "/deals"

	def fetch_deal_in(self, city):
		try:
			print "meituan_crawl.py fetch_deal_in", city
			content  = self._fetch(self.url_deal + city + "/deals")
			filepath = os.path.join(self.data_store, city)
			fhandler = open(filepath, "w")
			fhandler.write(content)
			fhandler.close()
		except Exception, e:
			print "Error: meituan_crawl.py fetch_deal_in", city, e
			raise
		return 1

if __name__ == "__main__":
	meituan = MeituanCrawler()
	city_list = meituan.fetch_city_list()
	for city in city_list:
		meituan.fetch_deal_in(city)
		break

