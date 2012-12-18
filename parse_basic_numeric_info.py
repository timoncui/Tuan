# parse the xml deal file to get: source, city, deal_id, sales_num, price, type, time
# @author: Lixing Huang
# @time: 12/11/2012

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
import datetime

class BasicNumericParser:
	def __init__(self, table_name, password="", user="root", db_name="tuan", host="127.0.0.1:3306"):
		self.mysql_host = host
		self.mysql_database = db_name
		self.mysql_user = user
		self.mysql_password = password
		self.mysql_table_name = table_name
		try:
			self.connection = tornado.database.Connection(self.mysql_host, self.mysql_database, self.mysql_user, self.mysql_password)
		except Exception, e:
			print "Fails to connect to mysql database", e
			raise

	# get city name information by its Chinese version.
	def get_city_info(self, city_name_zh):
		try:
			city_name = self.connection.query("SELECT * FROM city WHERE city_name_zh = %s", city_name_zh)
			return city_name  # dictionary, {"city_id": ..., "city_name_zh": ..., "city_name_py": ...}
		except Exception, e:
			print "Error: parse_basic_numeric_info.py get_city_info", str(e)
			return None

	def parse(self, source, created_time, filepath):
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

		# run the corresponding parser
		parser.parse(filepath)

		# go through the deals until we find the city_id.
		# assumption: the city_id should be consistent for all deals in the current file
		city_id = None
		for deal in parser.deals:
			if not city_id:
				city_id = self.get_city_info(deal["deal_city"])  # query the city table
				if len(city_id) != 0:
					city_id = city_id[0]["city_id"]
					break

		for deal in parser.deals:
			deal_id      = deal["deal_id"]
			sales_num    = deal["sales_num"]
			price        = deal["price"]
			start_time   = deal["start_time"]
			end_time     = deal["end_time"]
			deal_cate    = deal["deal_cate"]
			deal_subcate = deal["deal_subcate"]
			current_city_id = self.get_city_info(deal["deal_city"])
			if len(current_city_id) == 0:   # if cannot find city id, use the global one.
				current_city_id = city_id
			else:
				current_city_id = current_city_id[0]["city_id"]
			print deal_id, current_city_id, sales_num, price, start_time, end_time, deal_cate, deal_subcate

	# decode the deal xml file and parse it.
	def decode_and_parse(self, source, created_time, filepath):
		zipper = Zipper()
		zipper.decode_file(filepath, filepath + ".raw")
		self.parse(source, created_time, filepath + ".raw")
		os.remove(filepath + ".raw")


if __name__ == "__main__":
	app = BasicNumericParser("tuan")
	app.decode_and_parse("meituan", "2012-11-19", "/Users/Lixing/Documents/projects/Tuan/archive/meituan/2012_11_19/meituan_beijing_2012_11_19_16_21.gz")

