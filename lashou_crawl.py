# crawler by calling lashou.com open API
# @author: Lixing Huang
# @time: 10/31/2012

import os
import tuan_http
import xml.etree.ElementTree as ET

class LashouCrawler:
	def __init__(self):
		self.url_deal = "http://open.client.lashou.com/api/detail/city/"
		self.url_city_list = "http://open.client.lashou.com/api/cities"
		self.user_agent = "Chrome/22.0.1229.94"
		self.data_store = "lashou"
		self.mapping = dict()

	def fetch_city_list(self):
		try:
			print "lashou_crawl.py fetch_city_list"
			content  = tuan_http.http_fetch(self.url_city_list, self.user_agent)
			filepath = os.path.join(self.data_store, "city_list")
			fhandler = open(filepath, "w")
			fhandler.write(content)
			fhandler.close()

			try:
				city_list = []
				root = ET.fromstring(content)
				for city in root.iter("city"):
					city_list.append(city.find('id').text)
					self.mapping[city.find('id').text] = city.find('name').text
				return city_list
			except Exception, e:
				raise
		except Exception, e:
			print "Error: lashou_crawl.py fetch_city_list", e
			raise

	# because lashou.com only allows us to retrieve at most 500 items by each HTTP get call,
	# we need calculate how many pages beforehand.
	# this function will return the total number of pages for the city.
	def fetch_deal_in(self, city_id):
		try:
			total_page_num = -1
			total_deal_num = -1
			start_page_num = 1
			print "lashou_crawl.py fetch_deal_in", self.mapping[city_id]
			while True:
				content  = tuan_http.http_fetch(self.url_deal + city_id + "/p/" + str(start_page_num) + "/r/500", self.user_agent)
				filepath = None
				if  start_page_num == 1:
					filepath = os.path.join(self.data_store, city_id)
				else:
					filepath = os.path.join(self.data_store, city_id + "_" + str(start_page_num))
				fhandler = open(filepath, "w")
				fhandler.write(content)
				fhandler.close()

				if  total_deal_num == -1:
					root = ET.fromstring(content)
					total_deal_num = int(root.attrib["count"])
					total_page_num = total_deal_num / 500 + 1
				if  start_page_num == total_page_num:
					break
				else:
					start_page_num = start_page_num + 1
		except Exception, e:
			print "Error: lashou_crawl.py fetch_deal_in", self.mapping[city_id], e
			raise
		return total_page_num


if __name__ == "__main__":
	app = LashouCrawler()
	city_list = app.fetch_city_list()
	for city in city_list:
		app.fetch_deal_in(city)
		break


