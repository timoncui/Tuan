# extract shop information
# @author: Lixing Huang
# @time: 12/26/2012

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
import os

class ShopExtractor:
	def __init__(self):
		self.cache = dict()
		fhandler = open("city_list", "r")
		lines = fhandler.readlines()
		fhandler.close()
		for line in lines:
			index, city_name_zh, city_name_py = line.strip().split("\t")
			index = index.strip()
			city_name_zh = city_name_zh.strip()
			city_name_zh = unicode( city_name_zh, "utf-8" )
			self.cache[city_name_zh] = index

	def get_deal_file_list(self, folder_path):
		deal_list = []
		for filename in os.listdir(folder_path):
			if filename == "city_list": continue
			else: deal_list.append(filename)
		return deal_list

	def get_value(self, table, key):
		if key in table:
			return table[key]
		else:
			return None

	def is_phone_number(self, string):
		for c in string:
			if c.isalpha():
				return False
		return True

	# return an array representing a shop, shop_tel is the first element, and acts as the key
	def make_shop_entry_tel_as_key(self, shop):
		entry = []
		shop_tel = self.get_value(shop, "shop_tel")
		if shop_tel and self.is_phone_number(shop_tel):
			entry.append(shop_tel)
			keys = ["shop_name", "shop_addr", "shop_area"]
			for key in keys:
				val = self.get_value(shop, key)
				if val:
					val = val.strip()
				entry.append(val)
			geo = self.get_value(shop, "geo")
			if geo:
				entry.append(str(geo[0]))
				entry.append(str(geo[1]))
			else:
				entry.append(None)
				entry.append(None)
		return entry

	# return an array representing a shop, shop_name is the first element, and acts as the key
	def make_shop_entry_name_as_key(self, shop):
		entry = []
		shop_name = self.get_value(shop, "shop_name")
		if shop_name:
			entry.append(shop_name)
			keys = ["shop_tel", "shop_addr", "shop_area"]
			for key in keys:
				val = self.get_value(shop, key)
				if val:
					val = val.strip()
				entry.append(val)
			geo = self.get_value(shop, "geo")
			if geo:
				entry.append(str(geo[0]))
				entry.append(str(geo[1]))
			else:
				entry.append(None)
				entry.append(None)
		return entry

	# shop information is separated by tab, shop_index, deal_id, city, shop_name, shop_tel, shop_addr, shop_area, lat, lng
	def extract(self, source, output_file):
		parser = None
		if source == "dida": parser = DidaParser()
		elif source == "dianping": parser = DianpingParser()
		elif source == "lashou": parser = LashouParser()
		elif source == "meituan": parser = MeituanParser()
		elif source == "nuomi": parser = NuomiParser()
		elif source == "wowo": parser = WowoParser()
		elif source == "wuba": parser = WubaParser()
		else:
			print source, "does not have shop information"
			return

		shop_set = dict()
		filelist = self.get_deal_file_list(source)
		for filename in filelist:
			filepath = os.path.join(source, filename)
			print "processing", source, filename
			parser.parse(filepath)

			# assume all deals in the same file belong to the same city
			city_name = None
			for deal in parser.deals:
				if deal["deal_city"] in self.cache:
					city_name = deal["deal_city"]
					break

			for deal in parser.deals:
				deal_id = deal["deal_id"]
				deal_sold_at = deal["deal_sold_at"]
				for shop in deal_sold_at:
				#	shop_entry = self.make_shop_entry_tel_as_key(shop)
					shop_entry = self.make_shop_entry_name_as_key(shop)
					if len(shop_entry) > 0:
						shop_entry[0] = self.cache[city_name] + "_" + shop_entry[0]
						if shop_entry[0] not in shop_set:
							shop_set[shop_entry[0]] = [deal_id, city_name, shop_entry[1], shop_entry[2], shop_entry[3], shop_entry[4], shop_entry[5]]

		# save the shop list
		fhandler = open(output_file, "w")
		for key in shop_set:
			shop_string = key
			for ele in shop_set[key]:
				if ele: shop_string = shop_string + "\t" + ele
				else: shop_string = shop_string + "\t-"
			fhandler.write(shop_string.encode('utf-8') + "\n")
		fhandler.close()

if __name__ == "__main__":
	app = ShopExtractor()
#	app.extract("dianping", "shop/dianping_1")
	app.extract("meituan", "shop/meituan_1")




