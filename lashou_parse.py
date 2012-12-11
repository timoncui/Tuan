# parse the deal info from lashou.com open api
# @author: Lixing Huang
# @time: 10/31/2012

import os
import json
import datetime
import xml.etree.ElementTree as ET

class LashouParser:
	def __init__(self):
		self.deals = []

	def parse(self, filepath):
		del self.deals[:]
		try:
			city_name = filepath.strip().split("/")[-1]
			tree = ET.parse(filepath)
			root = tree.getroot()
			for url in root.iter('url'):
				deal = url.find('data').find('display')

				lashou_deal = dict()
				lashou_deal["deal_city"] = city_name
				lashou_deal["deal_id"] = deal.find('gid').text
				lashou_deal["deal_cate"] = deal.find('cate').text
				lashou_deal["deal_url"] = url.find('loc').text
				lashou_deal["deal_title"] = deal.find('title').text
				lashou_deal["deal_img"] = deal.find('image').text
				try:
					lashou_deal["start_time"] = long(deal.find('startTime').text)
					lashou_deal["end_time"] = long(deal.find('endTime').text)
				except Exception, e:
					print lashou_deal["deal_id"], "misses start and end time"
					lashou_deal["start_time"] = None
					lashou_deal["end_time"] = None
				try:
					lashou_deal["value"] = float(deal.find("value").text)
				except Exception, e:
					print lashou_deal["deal_id"], "misses value"
					lashou_deal["value"] = None
				try:
					lashou_deal["price"] = float(deal.find("price").text)
				except Exception, e:
					print lashou_deal["deal_id"], "misses price"
					lashou_deal["price"] = None
				try:
					lashou_deal["sales_num"] = int(deal.find("bought").text)
				except Exception, e:
					print lashou_deal["deal_id"], "misses bought"
					lashou_deal["sales_num"] = None
				lashou_deal["deal_sold_at"] = []

				for shop in deal.iter('shop'):
					lashou_shop = dict()
					lashou_shop["shop_name"] = shop.find('name').text
					lashou_shop["shop_tel"] = shop.find('tel').text
					lashou_shop["shop_addr"] = shop.find('addr').text
					try:
						lashou_shop["geo"] = [float(shop.find('latitude').text), float(shop.find('longitude').text)]
					except Exception, e:
						print lashou_deal["deal_id"], lashou_shop["shop_name"], "misses geolocation"
						lashou_shop["geo"] = None
					lashou_deal["deal_sold_at"].append(lashou_shop)

				self.deals.append(lashou_deal)
		except Exception, e:
			print "Error: lashou_parse.py parse", e
			raise
		print "deals number: ", len(self.deals)


if __name__ == "__main__":
	app = LashouParser()
	app.parse("/Users/Lixing/Documents/projects/Tuan/lashou/2421_3")
	for deal in app.deals:
		print deal
		print deal["deal_title"]
		print datetime.datetime(1970, 1, 1, 0, 0, 0) + datetime.timedelta(seconds=deal["start_time"])
		break



