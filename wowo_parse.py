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
			city_name = filepath.strip().split("/")[-1]
			tree = ET.parse(filepath)
			root = tree.getroot()
			for deal in root.iter('deal'):
				wowo_deal = dict()
				wowo_deal["deal_id"] = deal.find('id').text
			#	wowo_deal["deal_city"] = city_name
				wowo_deal["deal_city"] = deal.find('division_name').text
				wowo_deal["deal_title"] = deal.find('title').text
				wowo_deal["deal_url"] = deal.find('deal_url').text
				wowo_deal["deal_img"] = deal.find('large_image_url').text
				try:
					wowo_deal["start_time"] = long(deal.find('start_date').text)
					wowo_deal["end_time"] = long(deal.find('end_date').text)
				except Exception, e:
					print wowo_deal["deal_id"], "misses start and end time"
					wowo_deal["start_time"] = None
					wowo_deal["end_time"] = None
				try:
					wowo_deal["sales_num"] = int(deal.find('quantity_sold').text)
				except Exception, e:
					print wowo_deal["deal_id"], "misses quantity_sold"
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

				for shop in deal.iter('vendor'):
					wowo_shop = dict()
					wowo_shop["shop_name"] = shop.find('name').text
					wowo_shop["shop_tel"]  = shop.find('phone').text
					wowo_shop["shop_addr"] = shop.find('address').text
					wowo_shop["shop_area"] = shop.find('area').text
					try:
						wowo_shop["geo"] = [float(shop.find('lat').text), float(shop.find('lng').text)]
					except Exception, e:
					#	print wowo_deal["deal_id"], wowo_shop["shop_name"], "misses geolocation"
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






