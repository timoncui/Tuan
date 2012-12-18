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
	cities = app.load("/Users/Lixing/Documents/projects/Tuan/lashou/city_list")
	app.save_to_db("city", cities)




