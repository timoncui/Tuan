# parse the deal info from t.58.com open api
# @author: Lixing Huang
# @time: 11/2/2012

import os
import json
import datetime
import xml.etree.ElementTree as ET

class WubaParser:
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

				wuba_deal = dict()
				wuba_deal["deal_id"] = deal.find('id').text
				wuba_deal["deal_url"] = url.find('loc').text
				wuba_deal["deal_title"] = deal.find('title').text
				wuba_deal["deal_city"] = deal.find('city').text
				try:
					wuba_deal["deal_cate_id"] = int(deal.find('category').text)
				except Exception, e:
					print wuba_deal["deal_id"], "misses category"
					wuba_deal["deal_cate_id"] = None
				wuba_deal["deal_cate"] = deal.find('tag').text
				wuba_deal["deal_img"] = deal.find('image').text
				try:
					wuba_deal["start_time"] = long(deal.find('startTime').text)
					wuba_deal["end_time"] = long(deal.find('endTime').text)
				except Exception, e:
					print wuba_deal["deal_id"], "misses start and end time"
					wuba_deal["start_time"] = None
					wuba_deal["end_time"] = None
				try:
					wuba_deal["value"] = float(deal.find('value').text)
				except Exception, e:
					print wuba_deal["deal_id"], "misses value"
					wuba_deal["value"] = None
				try:
					wuba_deal["price"] = float(deal.find('price').text)
				except Exception, e:
					print wuba_deal["deal_id"], "misses price"
					wuba_deal["price"] = None
				try:
					wuba_deal["sales_num"] = int(deal.find('bought').text)
				except Exception, e:
					print wuba_deal["deal_id"], "misses bought"
					wuba_deal["sales_num"] = None
				wuba_deal["deal_sold_at"] = []
				wuba_shop = dict()
				wuba_shop["shop_addr"] = deal.find('address').text
				wuba_deal["deal_sold_at"].append(wuba_shop)

				self.deals.append(wuba_deal)
			print "deals number:", len(self.deals)
		except Exception, e:
			print "wuba_parse.py parse", e
			raise



if __name__ == "__main__":
	app = WubaParser()
	app.parse("/Users/Lixing/Documents/projects/Tuan/wuba/bj")
	for deal in app.deals:
		print deal["deal_id"]
		print deal["deal_url"]
		print deal["deal_title"]
		print deal["deal_cate_id"]
		print deal["deal_cate"]
		print deal["deal_img"]
		print deal["start_time"]
		print deal["end_time"]
		print deal["value"]
		print deal["price"]
		print deal["sales_num"]
		for shop in deal["deal_sold_at"]:
			print shop["shop_addr"]
		break



