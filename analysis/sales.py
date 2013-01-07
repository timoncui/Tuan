# extract the sales data
# @author Lixing Huang
# @date 1/6/2013

import os
import sys
import getopt
import calendar
import redis

class Sales:
	def __init__(self):
		try:
			self.redis_port = 6379
			self.redis_db = 0
			self.city_index = dict()

			fhandler = open("../city_list", "r")
			lines = fhandler.readlines()
			fhandler.close()

			for line in lines:
				idx, city_name_zh, city_name_py = line.strip().split("\t")
				idx = idx.strip()
				city_name_zh = city_name_zh.strip()
				self.city_index[idx] = city_name_zh
		except Exception, e:
			print "sales.py __init__", str(e)

	def _parse(self, filename):
		try:
			deal_data = dict()

			fhandler = open(filename, "r")
			lines = fhandler.readlines()
			fhandler.close()

			for line in lines:
				deal_id, price_str, sold_num_str = line.strip().split("\t")
				deal_id = deal_id.strip()
				price = 0
				sold_num = 0
				try:
					price = float(price_str.strip())
					sold_num = int(sold_num_str.strip())
				except Exception, e:  # sold_num or price is invalid
					pass
				if deal_id not in deal_data:
					deal_data[deal_id] = [price, sold_num]
				else:
					print "duplicate deal", filename, deal_id
			return deal_data
		except Exception, e:
			print "sales.py _parse", filename, str(e)
			return None

	def _calc(self, curr_filename, prev_filename):
		try:
			global_deal_set = set()
			sales_data = dict()
			sales_data["total"] = 0

			curr = self._parse(curr_filename)
			prev = self._parse(prev_filename)
			if (not curr) or (not prev):
				return None

			for deal_id in curr:
				amount = 0
				if deal_id in prev:
					if curr[deal_id][1] >= prev[deal_id][1]:
						if curr[deal_id][0] > 0:
							amount = curr[deal_id][0] * (curr[deal_id][1] - prev[deal_id][1])
						elif prev[deal_id][0] > 0:
							amount = prev[deal_id][0] * (curr[deal_id][1] - prev[deal_id][1])
				else:
					amount = curr[deal_id][0] * curr[deal_id][1]

				# when calculate the total sales, should get rid of city index in order to avoid
				# duplication. because different city may share the same deal.
				if deal_id.split("_")[1] not in global_deal_set:
					global_deal_set.add(deal_id.split("_")[1])
					sales_data["total"] = sales_data["total"] + amount

				city_idx  = deal_id.split("_")[0]
				if city_idx in self.city_index:
					city_name = self.city_index[city_idx]
					if city_name not in sales_data:
						sales_data[city_name] = amount
					else:
						sales_data[city_name] = sales_data[city_name] + amount
				else:
					print deal_id, "has an invalid city index"
			return sales_data
		except Exception, e:
			print "sales.py _calc", str(e)
			return None

	def decr_date(self, y, m, d):
		days_of_month = []
		if calendar.isleap(y):
			days_of_month = [0,31,29,31,30,31,30,31,31,30,31,30,31]
		else:
			days_of_month = [0,31,28,31,30,31,30,31,31,30,31,30,31]

		if d-1 > 0:
			return [y, m, d-1]
		elif m-1 > 0:
			return [y, m-1, days_of_month[m-1]]
		else:
			return [y-1, 12, 31]

	def calc(self, source, year, month, day):
		try:
			curr_filename = None
			prev_filename = None
			# find the deal filename within the specified date
			curr_hour = 23
			while curr_hour >= 0:
				deal_filename = "_".join(['deal', source, str(year), str(month), str(day), str(curr_hour)])
				deal_filename = os.path.join('temp', deal_filename)
				if os.path.exists(deal_filename):
					curr_filename = deal_filename
					break
				curr_hour = curr_hour - 1
			if not curr_filename:
				print "cannot find deal on", str(year), str(month), str(day)
				return
			# find the previous deal filename
			curr_hour = curr_hour - 1
			while True:
				while curr_hour >= 0:
					deal_filename = "_".join(['deal', source, str(year), str(month), str(day), str(curr_hour)])
					deal_filename = os.path.join('temp', deal_filename)
					if os.path.exists(deal_filename):
						prev_filename = deal_filename
						break
					curr_hour = curr_hour - 1
				if prev_filename:
					break
				year, month, day = self.decr_date(year, month, day)
				curr_hour = 23
				if year == 2012 and month == 12 and day == 29:
					break
			if not prev_filename:
				print "cannot find prev deal"
				return
			# calculate the sales number
			print "calculate between", curr_filename, prev_filename
			sales_data = self._calc(curr_filename, prev_filename)
			if sales_data:
				self.save_to_redis(source, curr_filename, sales_data)
			#	self.update_redis(source, curr_filename, sales_data)
		except Exception, e:
			print "sales.py calc", str(e)

	def save_to_redis(self, source, curr_filename, sales_data):
		r = redis.StrictRedis(host='localhost', port=self.redis_port, db=self.redis_db)
		# key scheme:  sales:meituan:city_name_zh:2012_12_31_9
		date = "_".join(curr_filename.split("_")[2:])
		for city in sales_data:
			redis_key = "sales:" + source + ":" + city.decode('utf8') + ":" + date
			if not r.exists(redis_key):
				print "inserting", redis_key
				redis_val = sales_data[city]
				r.set(redis_key, redis_val)
			else:
				print redis_key, r.get(redis_key)

	# update the existing key
	def update_redis(self, source, curr_filename, sales_data):
		r = redis.StrictRedis(host='localhost', port=self.redis_port, db=self.redis_db)
		# key scheme: sales:meituan:city_name_zh:2012_12_31_9
		date = "_".join(curr_filename.split("_")[2:])
		for city in sales_data:
			redis_key = "sales:" + source + ":" + city.decode('utf8') + ":" + date
			redis_val = sales_data[city]
			r.set(redis_key, redis_val)
			print "updating", redis_key, redis_val

	def snapshot_redis(self):
		r = redis.StrictRedis(host='localhost', port=self.redis_port, db=self.redis_db)
		print "save db to disk..."
		r.save()
		print "saved!"


# usage: python sales.py -y 2012 -m 12 -d 31
# assumption: the date frequency is one day. If we crawl data several times per day, need change the code in calc!
if __name__ == "__main__":
	year = None
	month = None
	day = None

	options, arg = getopt.getopt(sys.argv[1:], "y:m:d:", ["year=", "month=", "day="])
	for opt in options:
		if opt[0] == "-y": year = opt[1]
		elif opt[0] == "-m": month = opt[1]
		elif opt[0] == "-d": day = opt[1]

	if year and month and day:
		try:
			year = int(year)
			month = int(month)
			day = int(day)
			app = Sales()
			sources = ["dida", "dianping", "lashou", "ftuan", "meituan", "manzuo", "nuomi", "wowo", "wuba"]
			for source in sources:
				app.calc(source, year, month, day)
			app.snapshot_redis()
		except Exception, e:
			print "sales.py", str(e)

