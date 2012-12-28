# mine useful information from deals
# @author: Lixing Huang
# @time: 12/27/2012

from meituan_parse import MeituanParser
from nuomi_parse import NuomiParser
from lashou_parse import LashouParser
from dida_parse import DidaParser
from wowo_parse import WowoParser
from dianping_parse import DianpingParser
from ftuan_parse import FtuanParser
from manzuo_parse import ManzuoParser
from wuba_parse import WubaParser
from compress import Zipper
from extract_shop_info import ShopExtractor

import os
import sys
import getopt
import datetime

class Miner:
	def __init__(self):
		self.shop_extractor = ShopExtractor()

	def construct_parser(self, source):
		parser = None
		if source == "dida": parser = DidaParser()
		elif source == "dianping": parser = DianpingParser()
		elif source == "ftuan": parser = FtuanParser()
		elif source == "lashou": parser = LashouParser()
		elif source == "manzuo": parser = ManzuoParser()
		elif source == "meituan": parser = MeituanParser()
		elif source == "nuomi": parser = NuomiParser()
		elif source == "wowo": parser = WowoParser()
		elif source == "wuba": parser = WubaParser()
		return parser

	def mine(self, source):
		price_not_match = 0
		parser = self.construct_parser(source)
		if not parser: return None

		deal_set = dict()
		shop_set = dict()

		filelist = self.shop_extractor.get_deal_file_list(source)
		for filename in filelist:
			filepath = os.path.join(source, filename)
			print "processing", source, filename
			parser.parse(filepath)

			# assume all deals in the same file belong to the same city
			city_name  = None
			city_index = None
			for deal in parser.deals:
				if deal["deal_city"] in self.shop_extractor.cache:
					city_name  = deal["deal_city"]
					city_index = self.shop_extractor.cache[city_name]
					break

			for deal in parser.deals:
				deal_id = str(city_index) + "_" + deal["deal_id"]  # add city information
				sales_num = deal["sales_num"]
				price = deal["price"]
				if deal_id not in deal_set:
					deal_set[deal_id] = [price, sales_num]
				else:
					if price != deal_set[deal_id][0] or sales_num != deal_set[deal_id][1]:
						print "price or sales_num does not match!"
						price_not_match = price_not_match + 1

				deal_sold_at = deal["deal_sold_at"]
				for shop in deal_sold_at:
					shop_entry = self.shop_extractor.make_shop_entry_name_as_key(shop)
					if len(shop_entry) > 0:
						shop_entry[0] = str(city_index) + "_" + shop_entry[0]
						if shop_entry[0] not in shop_set:
							shop_set[shop_entry[0]] = [deal_id, shop_entry[1], shop_entry[2], shop_entry[4], shop_entry[5]]  # tel, addr, lat, lng

		print "price or sales_num not match:", price_not_match
		return [deal_set, shop_set]

	def write_to_file(self, source, deal_set, shop_set):
		LA_local_t = datetime.datetime.today()
		year  = str(LA_local_t.year)
		month = str(LA_local_t.month)
		day   = str(LA_local_t.day)
		hour  = str(LA_local_t.hour)

		shop_filename = "_".join([source, year, month, day])
		shop_filepath = os.path.join("shop", shop_filename)
		if not os.path.exists(shop_filepath):
			fhandler = open(shop_filepath, "w")
			for shop_key in shop_set:
				shop_string = shop_key
				for ele in shop_set[shop_key]:
					if ele: shop_string = shop_string + "\t" + ele
					else: shop_string = shop_string + "\t-"
				fhandler.write(shop_string.encode('utf-8') + "\n")
			fhandler.close()

		deal_filename = "_".join([source, year, month, day, hour])
		deal_filepath = os.path.join("deal", deal_filename)
		fhandler = open(deal_filepath, "w")
		for deal_key in deal_set:
			deal_string = deal_key
			for ele in deal_set[deal_key]:
				if ele: deal_string = deal_string + "\t" + str(ele)
				else: deal_string = deal_string + "\t-"
			fhandler.write(deal_string.encode('utf-8') + "\n")
		fhandler.close()

if __name__ == "__main__":
	source = None
	options, arg = getopt.getopt(sys.argv[1:], "s:", ["source="])
	for opt in options:
		if opt[0] == "-s": source = opt[1]

	app = Miner()
	deal_set, shop_set = app.mine(source)
	app.write_to_file(source, deal_set, shop_set)


