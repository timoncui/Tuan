# parse the deal info from manzuo.com open api
# @author: Lixing Huang
# @time: 11/2/2012

import os
import json
import datetime
import xml.etree.ElementTree as ET

class ManzuoParser:
	def __init__(self):
		self.deals = []

	def parse(self, filepath):
		try:
			city_name = filepath.strip().split("/")[-1]
			tree = ET.parse(filepath)
			root = tree.getroot()
			for url in root.iter('url'):
				deal = url.find('data').find('display')

				manzuo_deal = dict()
				manzuo_deal["deal_url"] = url.find('loc').text
				deal_info = manzuo_deal["deal_url"].strip().split("?")[0]
				manzuo_deal["deal_id"] = deal_info.strip().split("/")[-1]
				manzuo_deal["deal_title"] = deal.find('title').text
				manzuo_deal["deal_img"] = deal.find('image').text
				manzuo_deal["deal_desc"] = deal.find('description').text
				try:
					manzuo_deal["start_time"] = long(deal.find('startTime').text)
					manzuo_deal["end_time"] = long(deal.find('endTime').text)
				except Exception, e:
					print manzuo_deal["deal_id"], "misses start and end time"
					manzuo_deal["start_time"] = None
					manzuo_deal["end_time"] = None
				try:
					manzuo_deal["value"] = float(deal.find('value').text)
				except Exception, e:
					print manzuo_deal["deal_id"], "misses value"
					manzuo_deal["value"] = None
				try:
					manzuo_deal["price"] = float(deal.find('price').text)
				except Exception, e:
					print manzuo_deal["deal_id"], "misses price"
					manzuo_deal["price"] = None
				try:
					manzuo_deal["sales_num"] = int(deal.find('bought').text)
				except Exception, e:
					print manzuo_deal["deal_id"], "misses bought"
					manzuo_deal["sales_num"] = None

				self.deals.append(manzuo_deal)
			print "deals number:", len(self.deals)
		except Exception, e:
			print "Error: manzuo_parse.py parse", e
			raise


if __name__ == "__main__":
	app = ManzuoParser()
	app.parse("/Users/Lixing/Documents/projects/Tuan/manzuo/beijing")
	for deal in app.deals:
		print deal["deal_id"]
		print deal["deal_url"]
		print deal["deal_title"]
		print deal["deal_img"]
		print deal["deal_desc"]
		print deal["start_time"]
		print deal["end_time"]
		print deal["value"]
		print deal["price"]
		print deal["sales_num"]
		break








