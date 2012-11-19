# parse the deal info from meituan open api
# @author: Lixing Huang
# @time: 10/22/2012

import os
import json
import msgpack
import datetime
import xml.etree.ElementTree as ET
from carrier import Carrier

def convert_to_date(t):
	return datetime.datetime(1970, 1, 1, 0, 0, 0) + datetime.timedelta(seconds=t)

class MeituanParser:
	def __init__(self):
		self.deals = []

	def parse(self, filepath):
		del self.deals[:]
		try:
			feed_quality = 0
			tree = ET.parse(filepath)
			root = tree.getroot()
			for data in root.iter('data'):
				deal = data.findall('deal')
				if len(deal) > 1:
					raise Exception('more than one deal contained in one data item')
				else:
					deal = deal[0]

					meituan_deal = dict()
					meituan_deal["deal_city"] = filepath.strip().split("/")[1]
					meituan_deal["deal_id"] = deal.find('deal_id').text
					meituan_deal["deal_title"] = deal.find('deal_title').text
					meituan_deal["deal_url"] = deal.find('deal_url').text
					meituan_deal["deal_wap_url"] = deal.find('deal_wap_url').text
					meituan_deal["deal_img"] = deal.find('deal_img').text
					try:
						meituan_deal["deal_cate_id"] = int(deal.find('deal_cate_id').text)
					except Exception, e:
						print meituan_deal["deal_id"], "misses cate id"
						feed_quality = feed_quality + 1
						meituan_deal["deal_cate_id"] = None
					meituan_deal["deal_cate"] = deal.find('deal_cate').text
					try:
						meituan_deal["deal_subcate_id"] = int(deal.find('deal_subcate_id').text)
					except Exception, e:
						print meituan_deal["deal_id"], "misses subcate id"
						feed_quality = feed_quality + 1
						meituan_deal["deal_subcate_id"] = None
					meituan_deal["deal_subcate"] = deal.find('deal_subcate').text
					meituan_deal["deal_desc"] = deal.find('deal_desc').text
					try:
						meituan_deal["value"] = float(deal.find('value').text)
					except Exception, e:
						print meituan_deal["deal_id"], "misses value"
						feed_quality = feed_quality + 1
						meituan_deal["value"] = None
					try:
						meituan_deal["price"] = float(deal.find('price').text)
					except Exception, e:
						print meituan_deal["deal_id"], "misses price"
						feed_quality = feed_quality + 1
						meituan_deal["price"] = None
					try:
						meituan_deal["sales_min"] = int(deal.find('sales_min').text)
					except Exception, e:
						print meituan_deal["deal_id"], "misses sales_min"
						feed_quality = feed_quality + 1
						meituan_deal["sales_min"] = None
					try:
						meituan_deal["sales_num"] = int(deal.find('sales_num').text)
					except Exception, e:
						print meituan_deal["deal_id"], "misses sales_num"
						feed_quality = feed_quality + 1
						meituan_deal["sales_num"] = None
					meituan_deal["sold_out"] = deal.find('sold_out').text
					meituan_deal["is_post"]  = deal.find('is_post').text
					try:
						meituan_deal["start_time"] = long(deal.find('start_time').text)
						meituan_deal["end_time"] = long(deal.find('end_time').text)
					except Exception, e:
						print meituan_deal["deal_id"], "misses start and end time"
						feed_quality = feed_quality + 1
						meituan_deal["start_time"] = None
						meituan_deal["end_time"] = None
					try:
						meituan_deal["coupon_start_time"] = long(deal.find('coupon_start_time').text)
						meituan_deal["coupon_end_time"] = long(deal.find('coupon_end_time').text)
					except Exception, e:
						print meituan_deal["deal_id"], "misses coupon start and end time"
						feed_quality = feed_quality + 1
						meituan_deal["coupon_start_time"] = None
						meituan_deal["coupon_end_time"] = None
					meituan_deal["deal_tips"]   = deal.find('deal_tips').text
					meituan_deal["deal_name"]   = deal.find('deal_name').text
					meituan_deal["deal_seller"] = deal.find('deal_seller').text
					meituan_deal["deal_sold_at"]= []

					for shop in data.iter('shop'):
						meituan_shop = dict()
						meituan_shop["shop_name"] = shop.find('shop_name').text
						meituan_shop["shop_tel"]  = shop.find('shop_tel').text
						meituan_shop["shop_addr"] = shop.find('shop_addr').text
						meituan_shop["shop_area"] = shop.find('shop_area').text
						try:
							meituan_shop["geo"] = [float(shop.find('shop_lat').text), float(shop.find('shop_long').text)]
						except Exception, e:
							print meituan_deal["deal_id"], meituan_shop["shop_name"], "misses geolocation"
							feed_quality = feed_quality + 1
							meituan_shop["geo"] = None
						meituan_shop["shop_trafficinfo"] = shop.find('shop_trafficinfo').text
						meituan_deal["deal_sold_at"].append(meituan_shop)

					self.deals.append(meituan_deal)
		except Exception, e:
			print "Error: meituan_parse.py parse", e
			raise
		print "deals number: ", len(self.deals)
		print "feed quality: ", feed_quality

if __name__ == "__main__":
	# test meituan parser
	meituan = MeituanParser()
	meituan.parse("/Users/Lixing/Documents/projects/Tuan/meituan/beijing")
	for deal in meituan.deals:
		print str(deal)
		break



