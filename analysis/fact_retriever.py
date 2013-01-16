# wrapper of s3retriever.py
# retrieve deal facts from s3 and save data to redis db
# @author: Lixing Huang
# @time: 12/30/2012

from s3retriever import S3Retriever
import os
import sys
import getopt
import redis

class FactRetriever:
	def __init__(self):
		try:
			self.redis_port = 6379
			self.redis_db = 0
			self.s3 = S3Retriever()
		except Exception, e:
			pass

	# if the fact_name is shop,
	# 	return a dictionary, the key is shop name, and the value is [city_index_deal_id, phone, address, lat, lng]
	#	if the entry is "-", it means the value is empty
	
	# if the fact_name is deal or deal_number, return an array, because it is possible that we can sample multiple times within one day
	# each element in this array is a dictionary
	#	when fact_name is deal:
	#		key is city_index_deal_id -> price, sales_num
	#	when fact_name is deal_number:
	#		key is city_name_zh -> deal number
	def retrieve(self, source, fact_name, year, month, day):
		try:
			if fact_name == "shop":
				data = dict()
				file_key = "_".join([fact_name, source, year, month, day])
				filename = self.s3.retrieve_file(file_key)
				if not filename:
					print file_key, "not available"
					return None
				fhandler = open(filename, "r")
				lines = fhandler.readlines()
				fhandler.close()
				for line in lines:
					try:
						tokens = line.strip().split("\t")
						data[tokens[0].strip()] = [tokens[1].strip(), tokens[2].strip(), tokens[3].strip(), tokens[4].strip(), tokens[5].strip()]
					except Exception, e:
						continue
				return [data, filename]
			elif fact_name == "deal":
				data = []
				file_key_prefix = "_".join([fact_name, source, year, month, day])
				filenames = self.s3.retrieve_files(file_key_prefix)
				if not filenames:
					print file_key_prefix, "not available"
					return None
				for filename in filenames:
					deal_data = dict()
					fhandler = open(filename, "r")
					lines = fhandler.readlines()
					fhandler.close()
					for line in lines:
						try:
							tokens = line.strip().split("\t")
							deal_data[tokens[0].strip()] = [tokens[1].strip(), tokens[2].strip()]
						except Exception, e:
							continue
					data.append(deal_data)
				return [data, filenames]
			elif fact_name == "deal_number":
				data = []
				file_key_prefix = "_".join([fact_name, source, year, month, day])
				filenames = self.s3.retrieve_files(file_key_prefix)
				if not filenames:
					print file_key_prefix, "not available"
					return None
				for filename in filenames:
					deal_num_data = dict()
					fhandler = open(filename, "r")
					lines = fhandler.readlines()
					fhandler.close()
					line_index = 1
					for line in lines:
						try:
							tokens = line.strip().split("\t")
							if line_index == 1:
								deal_num_data["total"] = tokens[0].strip()
							else:
								deal_num_data[tokens[0].strip()] = tokens[1].strip()
							line_index = line_index + 1
						except Exception, e:
							continue
					data.append(deal_num_data)
				return [data, filenames]
			else:
				print fact_name, "is not valid right now"
				return None
		except Exception, e:
			print "Error: FactRetriever retrieve", str(e)

	def save_to_redis(self, data, fact_name, filenames):
		r = redis.StrictRedis(host='localhost', port=self.redis_port, db=self.redis_db)
		if fact_name == "deal_number":
			# key scheme:  deal_number:meituan:city_name_zh:2012_12_31_9
			for i in range(0, len(filenames)):
				fileinfo = filenames[i].strip().split("/")[-1]
				tokens = fileinfo.split("_")
				source = tokens[2]
				date = "_".join(tokens[3:])
				for city in data[i]:
					redis_key = "deal_number:" + source + ":" + city.decode('utf8') + ":" + date
					if not r.exists(redis_key):
						redis_val = data[i][city]
						r.set(redis_key, redis_val)
					else:
						print redis_key, r.get(redis_key)

	def snapshot_redis(self):
		r = redis.StrictRedis(host='localhost', port=6379, db=0)
		print "save db to disk..."
		r.save()
		print "saved!"

# python fact_retriever.py -y 2012 -m 12 -d 30
if __name__ == "__main__":
	year  = None
	month = None
	day   = None

	options, arg = getopt.getopt(sys.argv[1:], "y:m:d:", ["year=", "month=", "day="])
	for opt in options:
		if opt[0] == "-y": year = opt[1]
		elif opt[0] == "-m": month = opt[1]
		elif opt[0] == "-d": day = opt[1]

	fact_names = ["deal_number", "deal", "shop"]
	sources = ["dida", "dianping", "lashou", "ftuan", "meituan", "manzuo", "nuomi", "wowo", "wuba"]
	print year, month, day

	if year and month and day:
		fact_retriever = FactRetriever()
		for fact_name in fact_names:
			for source in sources:
				result = fact_retriever.retrieve(source, fact_name, year, month, day)
				if not result:
					continue
				data, filenames = result
				fact_retriever.save_to_redis(data, fact_name, filenames)
		fact_retriever.snapshot_redis()

