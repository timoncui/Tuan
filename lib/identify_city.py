# mapping from a unique city id to city name
# @author: Lixing Huang
# @date: 12/11/2012

import tornado.database
import xml.etree.ElementTree as ET
from xpinyin import Pinyin

class CityIdentifier:
	def __init__(self):
		self.connection = None

	def connect_to_db(self, table_name, password="", user="root", db_name="tuan", host="127.0.0.1:3306"):
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

	# construct a full city list, combining lashou.com city list and cities not found in lashou, but appear in other sources
	def construct_city_set(self, lashou_city_list, unlisted):
		result = []
		p = Pinyin()
		tree = ET.parse(lashou_city_list)
		root = tree.getroot()
		for city in root.iter('city'):
			city_name = city.find('name').text
			result.append( [city_name, p.get_pinyin(city_name)] )

		fhandler = open(unlisted, "r")
		lines = fhandler.readlines()
		fhandler.close()
		for line in lines:
			city_name = line.strip()
			city_name = unicode( city_name, "utf-8" )
			result.append( [city_name, p.get_pinyin(city_name)] )

		city_index = 1
		for city in result:
			print city_index, "\t", city[0], "\t", city[1]
			city_index = city_index + 1

	# lashou.com has a comprehensive city list
	def load(self, lashou_city_list):
		result = []
		p = Pinyin()
		tree = ET.parse(lashou_city_list)
		root = tree.getroot()
		for city in root.iter('city'):
			city_id = city.find('id').text
			city_name = city.find('name').text
			result.append( [city_id, city_name, p.get_pinyin(city_name)] )
		return result

	# @cities is the result from load()
	def save_to_db(self, table_name, cities):
		self.connect_to_db(table_name)
		for city in cities:
			print city
			self.connection.execute("INSERT INTO " + table_name + " (city_id, city_name_zh, city_name_py) VALUES (%s,%s,%s)", city[0], city[1], city[2])


if __name__ == "__main__":
	app = CityIdentifier()
#	cities = app.load("/Users/Lixing/Documents/projects/Tuan/lashou/city_list")
#	app.save_to_db("city", cities)
	app.construct_city_set("/Users/Lixing/Documents/projects/Tuan/lashou/city_list", "unlisted.txt")




