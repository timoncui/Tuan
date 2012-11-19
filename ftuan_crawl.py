# crawler by calling ftuan.com open API
# @author: Lixing Huang
# @time: 11/2/2012

import os
import urllib
import urllib2
import datetime
import tuan_http
import xml.etree.ElementTree as ET

class FtuanCrawler:
	def __init__(self):
		self.url_city_list = "http://newapi.ftuan.com/api/City.aspx"
		self.url_deal = "http://newapi.ftuan.com/api/v2.aspx?city="
		self.user_agent = "Chrome/22.0.1229.94"
		self.data_store = "ftuan"

	def fetch_city_list(self):
		try:
			content = tuan_http.http_fetch(self.url_city_list, self.user_agent)
			try:
				city_list = []
				root = ET.fromstring(content)
				for city in root.iter('city'):
					city_list.append(city.find('enname').text)
				return city_list
			except Exception, e:
				print "Error: ftuan_crawl.py fetch_city_list", e
				raise
		except Exception, e:
			print "Error: ftuan_crawl.py fetch_city_list", e
			raise

	def get_fetch_deal_url(self, city):
		return self.url_deal + city

	def fetch_deal_in(self, city):
		try:
			print "ftuan_crawl.py fetch_deal_in", city
			content  = tuan_http.http_fetch(self.url_deal + city, self.user_agent)
			filepath = os.path.join(self.data_store, city)
			fhandler = open(filepath, "w")
			fhandler.write(content)
			fhandler.close()
		except Exception, e:
			print "Error: ftuan_crawl.py fetch_deal_in", city, e
			raise
		return 1


if __name__ == "__main__":
	app = FtuanCrawler()
	city_list = app.fetch_city_list()
	for city in city_list:
		app.fetch_deal_in(city)
		break




