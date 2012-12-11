# parse the deal info from nuomi open api
# @author: Lixing Huang
# @time: 10/30/2012

import os
import json
import datetime
import xml.etree.ElementTree as ET

class NuomiParser:
	def __init__(self):
		self.deals = []

	def parse(self, filepath):
		del self.deals[:]
		try:
			feed_quality = 0
			city_name = filepath.split('/')[-1]
			tree = ET.parse(filepath)
			root = tree.getroot()
			for data in root.iter('url'):
				deal_url = data.find('loc').text
				tokens = deal_url.split("/")

				deal = data.find('data')
				deal = deal.find('display')

				nuomi_deal = dict()
				nuomi_deal["deal_city"] = city_name
				nuomi_deal["deal_id"] = city_name + "_" + tokens[-1].split(".")[0]  # deal id = city_name + the last part of URL
				nuomi_deal["deal_title"] = deal.find('title').text
				nuomi_deal["deal_url"] = deal_url
				nuomi_deal["deal_img"] = deal.find('image').text
				try:
					nuomi_deal["deal_cate_id"] = int(deal.find('category').text)
				except Exception, e:
					print nuomi_deal["deal_id"], "misses category id"
					nuomi_deal["deal_cate_id"] = None
					feed_quality = feed_quality + 1
				try:
					nuomi_deal["value"] = float(deal.find('value').text)
				except Exception, e:
					print nuomi_deal["deal_id"], "misses value"
					feed_quality = feed_quality + 1
					nuomi_deal["value"] = None
				try:
					nuomi_deal["price"] = float(deal.find('price').text)
				except Exception, e:
					print nuomi_deal["deal_id"], "misses price"
					feed_quality = feed_quality + 1
					nuomi_deal["price"] = None
				try:
					nuomi_deal["sales_num"] = int(deal.find('bought').text)
				except Exception, e:
					print nuomi_deal["deal_id"], "misses bought"
					feed_quality = feed_quality + 1
					nuomi_deal["sales_num"] = None
				try:
					nuomi_deal["start_time"] = long(deal.find('startTime').text)
					nuomi_deal["end_time"] = long(deal.find('endTime').text)
				except Exception, e:
					print nuomi_deal["deal_id"], "misses start and end time"
					feed_quality = feed_quality + 1
					nuomi_deal["start_time"] = None
					nuomi_deal["end_time"] = None
				nuomi_deal["deal_sold_at"] = []

				for shop in deal.iter('shop'):
					nuomi_shop = dict()
					nuomi_shop["shop_name"] = shop.find('name').text
					nuomi_shop["shop_tel"]  = shop.find('tel').text
					nuomi_shop["shop_addr"] = shop.find('addr').text
					nuomi_shop["shop_area"] = shop.find('area').text
					try:
						nuomi_shop["geo"] = [float(shop.find('latitude').text), float(shop.find('longitude').text)]
					except Exception, e:
						print nuomi_deal["deal_id"], nuomi_shop["shop_name"], "misses geolocation"
						feed_quality = feed_quality + 1
						nuomi_shop["geo"] = None
					nuomi_shop["shop_trafficinfo"] = shop.find('direction').text
					nuomi_deal["deal_sold_at"].append(nuomi_shop)

				self.deals.append(nuomi_deal)
		except Exception, e:
			print "Error: nuomi_parse.py parse", e
			raise
		print "deals number: ", len(self.deals)
		print "feed quality: ", feed_quality


if __name__ == "__main__":
	app = NuomiParser()
	app.parse("/Users/Lixing/Documents/projects/Tuan/nuomi/chaoyang")
	for deal in app.deals:
		print str(deal)
		break





