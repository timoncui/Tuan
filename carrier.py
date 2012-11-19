# carry the data from all sources into database
# @author: Lixing Huang
# @time: 10/30/2012

import database
import uuid
import datetime
import msgpack

class Carrier:
	def __init__(self, table_name, password="", user="root", db_name="tuan", host="127.0.0.1:3306"):
		self.mysql_host = host
		self.mysql_database = db_name
		self.mysql_user = user
		self.mysql_password = password
		self.mysql_table_name = table_name
		try:
			self.connection = database.Connection(self.mysql_host, self.mysql_database, self.mysql_user, self.mysql_password)
		except Exception, e:
			print "Fails to connect to mysql database", e
			raise

	# source: a string indicates the data source, for example, meituan, nuomi, etc.
	# deals: it is the member variable of parser
	def carry(self, source, deals):
		# get current local time
		LA_local_t = datetime.datetime.today()
		# calibrate the time to Beijing time
		interval   = datetime.timedelta(hours = 15)  # change it to 15 after Nov. 4th, 2012
		BJ_local_t = LA_local_t + interval

		for deal in deals:
			try:
				mysql_uuid = str(uuid.uuid4())
				serialized = msgpack.packb(deal)
				self.connection.execute("INSERT INTO " + self.mysql_table_name + " (uuid, deal_id, deal_time, source, content) VALUES (%s,%s,%s,%s,%s)", mysql_uuid, deal["deal_id"], BJ_local_t, source, serialized)
			except Exception, e:
				print "Error: carrier.py carry", source, str(deal), e
				continue

	@property
	def db(self):
		return self.connection

if __name__ == "__main__":
	# test database
	app = Carrier("deals")
	try:
		deal_id = 'Nexus4'
		deals = app.db.query("SELECT content from deals WHERE deal_id = %s", deal_id)
		deserialized = msgpack.unpackb(deals[0]["content"])
		print deserialized["deal_desc"]
	except Exception, e:
		print e
