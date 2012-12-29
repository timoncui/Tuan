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
from s3archiver import S3Archiver

import os
import sys
import getopt
import datetime

class FindDealNum:
	def __init__(self):
		self.archiver = S3Archiver()
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
		deal_per_city = dict()

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
			try:
				parser.parse(filepath)
			except Exception, e:
				print "Error: find_deal_num.py", source, filename
				continue  # get rid of this error file

			# assume all deals in the same file belong to the same city
			city_name = None
			for deal in parser.deals:
				if deal["deal_city"] in self.cache:
					city_name = deal["deal_city"]
					if self.cache[deal["deal_city"]] == "283":  # if it is the whole country
						continue
					break

			for deal in parser.deals:
				current_city_name = None
				if deal["deal_city"] in self.cache:
					if self.cache[deal["deal_city"]] == "283":  # although the deal is country-wise, but it still belongs to the current city
						current_city_name = city_name
					else:
						current_city_name = deal["deal_city"]
				else:
					current_city_name = city_name

				deal_id = deal["deal_id"]
				deal_set.add(deal_id)
				if not current_city_name:
					continue
				if current_city_name in deal_per_city:
					deal_per_city[current_city_name].add(deal_id)
				else:
					deal_per_city[current_city_name] = set()
					deal_per_city[current_city_name].add(deal_id)

		for city in deal_per_city:
			deal_num_per_city[city] = len(deal_per_city[city])
		return [len(deal_set), deal_num_per_city]

	def write_to_file(self, source, total_num, deal_num_per_city, on_S3=False):
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
		if on_S3:
			try:
				self.archiver.archive(filepath, "deal_number_" + filename)
				os.remove(filepath)
			except Exception, e:
				raise

def main(source_, on_S3):
	source = source_
	if source:
		app = FindDealNum()
		try:
			total_num, deal_num_per_city = app.find_deal_num(source)
			app.write_to_file(source, total_num, deal_num_per_city, on_S3)   # whether to store on S3 or not
		except Exception, e:
			print "Error: find_deal_num.py", source, str(e)

if __name__ == "__main__":
	source = None
	options, arg = getopt.getopt(sys.argv[1:], "s:", ["source="])
	for opt in options:
		if opt[0] == "-s": source = opt[1]
	main(source, True)  # whether to store on S3 or not



