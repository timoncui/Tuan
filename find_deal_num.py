# find the number of unique deals per source
# @author: Lixing Huang
# @time: 12/25/2012

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
import sys
import getopt
import datetime

class FindDealNum:
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

	# retrieve all deal files in the folder
	def get_deal_file_list(self, folder_path):
		deal_list = []
		for filename in os.listdir(folder_path):
			if filename == "city_list": continue
			else: deal_list.append(filename)
		return deal_list

	def find_deal_num(self, source):
		print "prcessing", source
		deal_set = set()
		deal_num_per_city = dict()

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

		filelist = self.get_deal_file_list(source)
		for filename in filelist:
			filepath = os.path.join(source, filename)
			parser.parse(filepath)

			# assume all deals in the same file belong to the same city
			city_name = None
			for deal in parser.deals:
				if deal["deal_city"] in self.cache:
					city_name = deal["deal_city"]
					break

			deal_subset = set()
			for deal in parser.deals:
				deal_id = deal["deal_id"]
				deal_set.add(deal_id)
				deal_subset.add(deal_id)
			deal_num_per_city[city_name] = len(deal_subset)
		return [len(deal_set), deal_num_per_city]

	def write_to_file(self, source, total_num, deal_num_per_city):
		LA_local_t = datetime.datetime.today()
		year  = str(LA_local_t.year)
		month = str(LA_local_t.month)
		day   = str(LA_local_t.day)
		hour  = str(LA_local_t.hour)
		filename = "_".join([source, year, month, day, hour])
		filepath = os.path.join("deal_number", filename)
		fhandler = open(filepath, "w")
		fhandler.write( str(total_num) + "\n" )
		for city in deal_num_per_city:
			fhandler.write( city.encode('utf-8') + "\t" + str(deal_num_per_city[city]) + "\n" )
		fhandler.close()

if __name__ == "__main__":
	source = None
	options, arg = getopt.getopt(sys.argv[1:], "s:", ["source="])
	for opt in options:
		if opt[0] == "-s": source = opt[1]

	if source:
		app = FindDealNum()
		total_num, deal_num_per_city = app.find_deal_num(source)
		app.write_to_file(source, total_num, deal_num_per_city)



