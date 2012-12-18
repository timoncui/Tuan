# parse the deal info from didatuan.com open api
# @author: Lixing Huang
# @time: 11/1/2012

import os
import json
import datetime
import xml.etree.ElementTree as ET

class DidaParser:
	def __init__(self):
		self.deals = []

	def parse(self, filepath):
		del self.deals[:]
		try:
		#	city_name = filepath.strip().split("/")[-1]
			tree = ET.parse(filepath)
			root = tree.getroot()
			for url in root.iter('url'):
				dida_deal = dict()

				dida_deal["deal_id"] = url.find('loc').text.strip().split("=")[1]
				dida_deal["deal_url"] = url.find('loc').text

				url = url.find('data').find('display')
				dida_deal["deal_city"] = url.find('city').text
				dida_deal["deal_title"] = url.find('title').text
				dida_deal["deal_img"] = url.find('image').text
				try:
					dida_deal["deal_cate_id"] = int(url.find('category').text)
				except Exception, e:
					print dida_deal["deal_id"], "misses category"
					dida_deal["deal_cate_id"] = None
				dida_deal["deal_subcate"] = url.find('subcategory').text
				dida_deal["deal_name"] = url.find('name').text
				dida_deal["deal_seller"] = url.find('seller').text
				try:
					dida_deal["start_time"] = long(url.find('startTime').text)
					dida_deal["end_time"] = long(url.find('endTime').text)
				except Exception, e:
					print dida_deal["deal_id"], "misses start and end time"
					dida_deal["start_time"] = None
					dida_deal["end_time"] = None
				try:
					dida_deal["value"] = float(url.find('value').text)
				except Exception, e:
					dida_deal["value"] = None
					print dida_deal["deal_id"], "misses value"
				try:
					dida_deal["price"] = float(url.find('price').text)
				except Exception, e:
					dida_deal["price"] = None
					print dida_deal["deal_id"], "misses price"
				try:
					dida_deal["sales_num"] = int(url.find('bought').text)
				except Exception, e:
					dida_deal["sales_num"] = None
					print dida_deal["deal_id"], "misses bought"
				dida_deal["deal_sold_at"] = []

				dida_shop = dict()
				dida_shop["shop_addr"] = url.find('address').text
				dida_shop["shop_tel"]  = url.find('phone').text
				dida_shop["shop_name"] = url.find('name').text
				dida_deal["deal_sold_at"].append(dida_shop)

				self.deals.append(dida_deal)
		except Exception, e:
			print "Error: dida_parse.py parse", e
			raise
		print "deals number: ", len(self.deals)


if __name__ == "__main__":
	app = DidaParser()
	app.parse("/Users/Lixing/Documents/projects/Tuan/dida/beijing")
	for deal in app.deals:
		print deal["deal_city"]
		print deal["deal_id"]
		print deal["deal_url"]
		print deal["deal_title"]
		print deal["deal_img"]
		print deal["deal_cate_id"]
		print deal["deal_subcate"]
		print deal["deal_name"]
		print deal["deal_seller"]
		print deal["start_time"]
		print deal["end_time"]
		print deal["value"]
		print deal["price"]
		print deal["sales_num"]
		print deal["deal_sold_at"][0]["shop_addr"]
		print deal["deal_sold_at"][0]["shop_tel"]
		print deal["deal_sold_at"][0]["shop_name"]
		break





