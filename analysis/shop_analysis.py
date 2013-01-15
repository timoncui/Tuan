# meituan:shop_id -> [deal_id, ...]
# analyze shop information offline
# @author Lixing Huang
# @date 1/6/2013

import os
import sys
import getopt
import redis

class ShopAnalyzer:
	def __init__(self):
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

	def snapshot_redis(self):
		try:
			r = redis.StrictRedis(host='localhost', port=self.redis_port, db=self.redis_db)
			print "save db to disk..."
			r.save()
			print "saved!"
		except Exception, e:
			print "ShopAnalyzer snapshot_redis", str(e)

	# meituan:shop_id -> [deal_id, ...]
	def parse_and_save_to_redis(self, source, filepath):
		try:
			r = redis.StrictRedis(host='localhost', port=self.redis_port, db=self.redis_db)
			fhandler = open(filepath, "r")
			lines = fhandler.readlines()
			fhandler.close()
			for line in lines:
				if line.strip() == "": continue
				tokens = line.strip().split("\t")
				if len(tokens) < 6: continue  # not valid
				shop_id = tokens[0].strip()
				deal_id = tokens[1].strip()
				redis_key = "deal_of_shop:" + source + ":" + shop_id
				redis_val = deal_id
				r.sadd(redis_key, redis_val)  # no duplicated deal id
			#	print redis_key, redis_val
		except Exception, e:
			print "ShopAnalyzer parse_and_save_to_redis", filename, str(e)

	def process_shop_files_of_date(self, folder, year, month, day):
		for filename in os.listdir(folder):
			if filename == "." or filename == "..":
				continue
			tokens = filename.strip().split("_")
			if tokens[0] == "shop":
				if int(tokens[2]) == year and int(tokens[3]) == month and int(tokens[4]) == day:
					source = tokens[1]
					print "processing", filename
					self.parse_and_save_to_redis(source, os.path.join(folder, filename))

	# save two types of data to redis
	# 1. shops_in_city:beijing -> [shop_id, shop_id, ...]
	# 2. source_of_shop:shop_id -> [meituan, nuomi, ...]
	def shop_to_source(self, folder, year, month, day):
		shop_set = dict()
		shop_with_more_than_one_source = []
		max_src_num = 0
		min_src_num = 9
		histogram   = [0,0,0,0,0,0]  # the number of shops that appear in 1, 2,...6 sources

		for filename in os.listdir(folder):
			if filename == "." or filename == "..":
				continue
			tokens = filename.strip().split("_")
			if tokens[0] == "shop":
				if int(tokens[2]) == year and int(tokens[3]) == month and int(tokens[4]) == day:
					source = tokens[1]
					fhandler = open(os.path.join(folder, filename), "r")
					lines = fhandler.readlines()
					fhandler.close()
					print filename, "roughly has", len(lines), "shops"
					for line in lines:
						if line.strip() == "": continue
						tokens = line.strip().split("\t")
						if len(tokens) < 6: continue  # not valid
						shop_name = tokens[0].strip()
						if shop_name not in shop_set:
							shop_set[shop_name] = [source]
						else:
							shop_set[shop_name].append(source)

		city_count = dict()
		for shop_id in shop_set.iterkeys():
			src_num = len(shop_set[shop_id])
			histogram[src_num-1] = histogram[src_num-1] + 1
			if src_num > 1:
				if src_num == 6:
					print shop_id, shop_set[shop_id]
				if src_num > max_src_num:
					max_src_num = src_num
				if src_num < min_src_num:
					min_src_num = src_num
				shop_with_more_than_one_source.append(shop_id)
				city_name = self.city_index[ shop_id.strip().split("_")[0] ]
				if city_name not in city_count: city_count[city_name] = 1
				else: city_count[city_name] = city_count[city_name] + 1

		try:
			r = redis.StrictRedis(host='localhost', port=self.redis_port, db=self.redis_db)
			for shop_id in shop_with_more_than_one_source:
				city_number = shop_id.strip().split("_")[0]
				if city_number in self.city_index:
					city_name = self.city_index[city_number]

					redis_key = "shops_in_city:" + city_name.decode('utf-8')
					redis_val = shop_id
					r.sadd(redis_key, redis_val)

					srcs = shop_set[shop_id]
					for src in srcs:
						redis_key = "source_of_shop:" + shop_id
						redis_val = src
						r.sadd(redis_key, redis_val)
		except Exception, e:
			print "ShopAnalyzer shop_to_source", str(e)

		print len(shop_set)
		print len(shop_with_more_than_one_source)
		print histogram
	#	for c in city_count:
	#		print c, "\t", city_count[c]


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
		app = ShopAnalyzer()
		app.shop_to_source('temp', int(year), int(month), int(day))
		app.process_shop_files_of_date('temp', int(year), int(month), int(day))
		app.snapshot_redis()


