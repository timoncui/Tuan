# crawler by calling dianping.com open API
# @author: Lixing Huang
# @time: 11/1/2012

import os
import urllib
import urllib2
import datetime
import tuan_http
import xml.etree.ElementTree as ET

class DianpingCrawler:
	def __init__(self):
		self.mapping = dict()
		self.url_deal = "http://api.t.dianping.com/n/api.xml?cityId="
		self.url_city_list = "http://api.t.dianping.com/n/base/cities.xml"
		self.user_agent = "Chrome/22.0.1229.94"
		self.data_store = "dianping"

	def fetch_city_list(self):
		try:
			print "dianping_crawl.py fetch_city_list"
			content  = tuan_http.http_fetch(self.url_city_list, self.user_agent)
			filepath = os.path.join(self.data_store, "city_list")
			fhandler = open(filepath, "w")
			fhandler.write(content)
			fhandler.close()

			try:
				city_list = []
				root = ET.fromstring(content)
				for city in root.iter('city'):
					self.mapping[city.find('enname').text] = city.find('id').text
					city_list.append(city.find('enname').text)
				return city_list
			except Exception, e:
				print "Error: dianping_crawl.py fetch_city_list", e
				raise
		except Exception, e:
			print "Error: dianping_crawl.py fetch_city_list", e
			raise

	def get_fetch_deal_url(self, city):
		start_page_num = 1
		count_per_page = 10000
		return self.url_deal + self.mapping[city] + "&page=" + str(start_page_num) + "&count=" + str(count_per_page)

	def fetch_deal_in(self, city):
		try:
			start_page_num = 1
			count_per_page = 10000
			print "dianping_crawl.py fetch_deal_in", city
			content  = tuan_http.http_fetch(self.url_deal + self.mapping[city] + "&page=" + str(start_page_num) + "&count=" + str(count_per_page), self.user_agent)
			filepath = os.path.join(self.data_store, city)
			fhandler = open(filepath, "w")
			fhandler.write(content)
			fhandler.close()
		except Exception, e:
			print "Error: dianping_crawl.py fetch_deal_in", city, e
			raise
		return 1


if __name__ == "__main__":
	app = DianpingCrawler()
	city_list = app.fetch_city_list()
	for city in city_list:
		app.fetch_deal_in(city)
		break





