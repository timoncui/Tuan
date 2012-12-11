# parse the deal info from dianping.com open api
# @author: Lixing Huang
# @time: 11/1/2012

import os
import json
import datetime
import xml.etree.ElementTree as ET

class DianpingParser:
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
				dianping_deal = dict()
				dianping_deal["deal_id"] = deal.find('identifier').text
				dianping_deal["deal_url"] = url.find('loc').text
				dianping_deal["deal_title"] = deal.find('title').text
				dianping_deal["deal_cate"] = deal.find('category').text
				dianping_deal["deal_subcate"] = deal.find('subcategory').text
				dianping_deal["deal_img"] = deal.find('image').text
				try:
					dianping_deal["start_time"] = long(deal.find('startTime').text)
					dianping_deal["end_time"] = long(deal.find('endTime').text)
				except Exception, e:
					print dianping_deal["deal_id"], "misses start and end time"
					dianping_deal["start_time"] = None
					dianping_deal["end_time"] = None
				try:
					dianping_deal["value"] = float(deal.find('value').text)
				except Exception, e:
					print dianping_deal["deal_id"], "misses value"
					dianping_deal["value"] = None
				try:
					dianping_deal["price"] = float(deal.find('price').text)
				except Exception, e:
					print dianping_deal["deal_id"], "misses price"
					dianping_deal["price"] = None
				dianping_deal["deal_desc"] = deal.find('description').text
				try:
					dianping_deal["sales_num"] = int(deal.find('bought').text)
				except Exception, e:
					print dianping_deal["deal_id"], "misses bought"
					dianping_deal["sales_num"] = None
				self.deals.append(dianping_deal)
			print "deals number:", len(self.deals)
		except Exception, e:
			print "Error: dianping_parse.py parse", e
			raise


if __name__ == "__main__":
	app = DianpingParser()
	app.parse("/Users/Lixing/Documents/projects/Tuan/dianping/shanghai")
	for deal in app.deals:
		print deal["deal_id"]
		print deal["deal_url"]
		print deal["deal_title"]
		print deal["deal_cate"]
		print deal["deal_subcate"]
		print deal["deal_img"]
		print deal["start_time"]
		print deal["end_time"]
		print deal["value"]
		print deal["price"]
		print deal["deal_desc"]
		print deal["sales_num"]
		break







