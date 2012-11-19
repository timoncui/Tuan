# crawler by calling manzuo.com open API
# @author: Lixing Huang
# @time: 11/2/2012

import os
import urllib
import urllib2
import datetime
import tuan_http
import xml.etree.ElementTree as ET

class ManzuoCrawler:
	def __init__(self):
		self.url_deal = "http://api.manzuo.com/common_"
		self.user_agent = "Chrome/22.0.1229.94"
		self.data_store = "manzuo"

	def fetch_city_list(self):
		return ["beijing", "shanghai", "dongguan", "linan", "linping", "yiwu", "yuhang", "foshan", "lanzhou", "nanjing", "nanning", "nanchang", "nantong", "xiamen", "hefei", "jilin", "wujiang", "haerbin", "dalian", "tianjin", "taiyuan", "ningbo", "yichang", "changzhou", "guangzhou", "zhangjiagang", "xuzhou", "cixi", "chengdu", "yangzhou", "wuxi", "kunshan", "kunming", "hangzhou", "wuhan", "jiangyin", "shenyang", "jstaizhou", "luoyang", "jinan", "zibo", "shenzhen", "wenzhou", "yantai", "yancheng", "shijiazhuang", "fuzhou", "shaoxing", "mianyang", "wuhu", "suzhou", "xiaoshanzj", "hengshui", "xian", "handan", "zhengzhou", "chongqing", "jinhua", "zhenjiang", "changchun", "changsha", "qingdao"]

	def get_fetch_deal_url(self, city):
		return self.url_deal + city + ".xml"

	def fetch_deal_in(self, city):
		try:
			print "manzuo_crawl.py fetch_deal_in", city
			content  = tuan_http.http_fetch(self.url_deal + city + ".xml", self.user_agent)
			filepath = os.path.join(self.data_store, city)
			fhandler = open(filepath, "w")
			fhandler.write(content)
			fhandler.close()
		except Exception, e:
			print "Error: manzuo_crawl.py fetch_deal_in", e
			raise
		return 1


if __name__ == "__main__":
	app = ManzuoCrawler()
	city_list = app.fetch_city_list()
	for city in city_list:
		app.fetch_deal_in(city)
		break