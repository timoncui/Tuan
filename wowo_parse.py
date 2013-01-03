# parse the deal info from 55tuan.com open api
# @author: Lixing Huang
# @time: 10/31/2012

import os
import json
import datetime
import xml.etree.ElementTree as ET

class WowoParser:
	def __init__(self):
		self.deals = []

	def parse(self, filepath):
		del self.deals[:]
		try:
			tree = ET.parse(filepath)
			root = tree.getroot()
			for url in root.iter('url'):
				wowo_deal = dict()
				wowo_deal["deal_url"] = url.find('loc').text
				deal_id = wowo_deal["deal_url"].strip().split("/")[-1]
				deal_id = deal_id.strip().split(".")[0]
				wowo_deal["deal_id"] = deal_id

				deal = url.find('data').find('display')
				wowo_deal["deal_city"] = deal.find('city').text
				wowo_deal["deal_title"] = deal.find('title').text
				wowo_deal["deal_img"] = deal.find('image').text
				try:
					wowo_deal["start_time"] = deal.find('startTime').text  # standard Linux timestamp
					wowo_deal["end_time"] = deal.find('endTime').text
				except Exception, e:
					print wowo_deal["deal_id"], "misses start and end time"
					wowo_deal["start_time"] = None
					wowo_deal["end_time"] = None
				try:
					wowo_deal["deal_cate"] = deal.find('catName').text
				except Exception, e:
					wowo_deal["deal_cate"] = None
				try:
					wowo_deal["sales_num"] = int(deal.find('bought').text)
				except Exception, e:
					print wowo_deal["deal_id"], "misses bought"
					wowo_deal["sales_num"] = None
				try:
					wowo_deal["value"] = float(deal.find('value').text)
				except Exception, e:
					print wowo_deal["deal_id"], "misses value"
					wowo_deal["value"] = None
				try:
					wowo_deal["price"] = float(deal.find('price').text)
				except Exception, e:
					print wowo_deal["deal_id"], "misses price"
					wowo_deal["price"] = None
				wowo_deal["deal_sold_at"] = []

				shops = url.find('data').find('shops')
				for shop in shops.iter('shop'):
					wowo_shop = dict()
					wowo_shop["shop_name"] = shop.find('name').text
					wowo_shop["shop_tel"]  = shop.find('tel').text
					wowo_shop["shop_addr"] = shop.find('addr').text
					wowo_shop["shop_area"] = shop.find('area').text
					try:
						wowo_shop["geo"] = [float(shop.find('latitude').text), float(shop.find('longitude').text)]
					except Exception, e:
						wowo_shop["geo"] = None
					wowo_deal["deal_sold_at"].append(wowo_shop)

				self.deals.append(wowo_deal)
		except Exception, e:
			print "Error: wowo_parse.py parse", e
			raise
		print "deals number: ", len(self.deals)


if __name__ == "__main__":
	app = WowoParser()
	app.parse("/Users/Lixing/Documents/projects/Tuan/wowo/beijing")
	for deal in app.deals:
		print deal
		print deal["deal_title"]
		break






