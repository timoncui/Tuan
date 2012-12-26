# check all city names, print the ones that are not in the current database

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
import tornado.database
import os

class CheckCityNames:
	def __init__(self, password="", user="root", db_name="tuan", host="127.0.0.1:3306"):
		self.found_city_set = set()
		self.notfound_city_set = set()
		self.cache = dict()
		self.mysql_host = host
		self.mysql_database = db_name
		self.mysql_user = user
		self.mysql_password = password

		fhandler = open("city_list", "r")
		lines = fhandler.readlines()
		fhandler.close()
		for line in lines:
			index, city_name_zh, city_name_py = line.strip().split("\t")
			index = index.strip()
			city_name_zh = city_name_zh.strip()
			city_name_zh = unicode( city_name_zh, "utf-8" )
			self.cache[city_name_zh] = index

		try:
			self.connection = tornado.database.Connection(self.mysql_host, self.mysql_database, self.mysql_user, self.mysql_password)
		except Exception, e:
			print "Fails to connect to mysql database", e
			raise

	# get city name information by its Chinese version.
	def get_city_info(self, city_name_zh):
		try:
			if city_name_zh in self.cache:
				return [ { "city_id": self.cache[city_name_zh] } ]
			else:
				city_name = self.connection.query("SELECT * FROM city WHERE city_name_zh = %s", city_name_zh)
				if len(city_name) > 0:
					self.cache[city_name_zh] = city_name[0]["city_id"]
				return city_name  # dictionary, {"city_id": ..., "city_name_zh": ..., "city_name_py": ...}
		except Exception, e:
			print "Error: parse_basic_numeric_info.py get_city_info", str(e)
			return None

	# retrieve all deal files in the folder
	def get_deal_file_list(self, folder_path):
		deal_list = []
		for filename in os.listdir(folder_path):
			if filename == "city_list": continue
			else: deal_list.append(filename)
		return deal_list

	# check the city names in a specified source, e.g. meituan
	def check_source(self, source):
		city_set = set()

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
			# run the corresponding parser
			parser.parse(filepath)
			# go through all deals
			for deal in parser.deals:
				deal_cities = deal["deal_city"].split(",")
				for deal_city in deal_cities:
				#	deal_city = unicode(deal_city.strip(), "utf-8")
					deal_city = deal_city.strip()
					current_city_id = self.get_city_info(deal_city)
					if len(current_city_id) == 0: self.notfound_city_set.add(deal_city)
					else: self.found_city_set.add(deal_city)

	def report(self):
		print "==== Found city list===="
		for city in self.found_city_set: print city
		print "==== Not Found city list===="
		for city in self.notfound_city_set: print city

if __name__ == "__main__":
	app = CheckCityNames()
	app.check_source("dianping")
	app.check_source("dida")
	app.check_source("ftuan")
	app.check_source("lashou")
	app.check_source("manzuo")
	app.check_source("meituan")
	app.check_source("nuomi")
	app.check_source("wowo")
	app.check_source("wuba")
	app.report()


