# parse the deal info from ftuan.com open api
# @author: Lixing Huang
# @time: 11/2/2012

import os
import json
import msgpack
import datetime
import xml.etree.ElementTree as ET

class FtuanParser:
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

				ftuan_deal = dict()
				ftuan_deal["deal_city"] = city_name
				ftuan_deal["deal_url"] = url.find('loc').text
				deal_info = ftuan_deal["deal_url"].strip().split("/")[-1]
				deal_info = deal_info.split(".")[0]
				deal_info = deal_info.split("_")
				ftuan_deal["deal_cate"] = deal_info[0]
				ftuan_deal["deal_id"] = deal_info[-1]
				ftuan_deal["deal_title"] = deal.find('title').text
				ftuan_deal["deal_img"] = deal.find('image').text
				try:
					ftuan_deal["start_time"] = long(deal.find('startTime').text)
					ftuan_deal["end_time"] = long(deal.find('endTime').text)
				except Exception, e:
					print ftuan_deal["deal_id"], "misses start and end time"
					ftuan_deal["start_time"] = None
					ftuan_deal["end_time"] = None
				try:
					ftuan_deal["value"] = float(deal.find('value').text)
				except Exception, e:
					print ftuan_deal["deal_id"], "misses value"
					ftuan_deal["value"] = None
				try:
					ftuan_deal["price"] = float(deal.find('price').text)
				except Exception, e:
					print ftuan_deal["deal_id"], "misses price"
					ftuan_deal["price"] = None
				try:
					ftuan_deal["sales_num"] = int(deal.find('bought').text)
				except Exception, e:
					print ftuan_deal["deal_id"], "misses bought"
					ftuan_deal["sales_num"] = None

				self.deals.append(ftuan_deal)
			print "deals number:", len(self.deals)
		except Exception, e:
			print "Error: ftuan_parse.py parse", e
			raise


if __name__ == "__main__":
	app = FtuanParser()
	app.parse("/Users/Lixing/Documents/projects/Tuan/ftuan/beijing")
	for deal in app.deals:
		print deal["deal_id"]
		print deal["deal_city"]
		print deal["deal_url"]
		print deal["deal_cate"]
		print deal["deal_title"]
		print deal["deal_img"]
		print deal["start_time"]
		print deal["end_time"]
		print deal["value"]
		print deal["price"]
		print deal["sales_num"]
		break








