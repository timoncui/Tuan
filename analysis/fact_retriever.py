# wrapper of s3retriever.py
# retrieve deal facts from s3
# @author: Lixing Huang
# @time: 12/30/2012

from s3retriever import S3Retriever

class FactRetriever:
	def __init__(self):
		try:
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
				return data
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
				return data
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
				return data
			else:
				print fact_name, "is not valid right now"
				return None
		except Exception, e:
			print "Error: FactRetriever retrieve", str(e)

	def print_data(self, data, fact_name):
		if fact_name == "shop":
			for shop_key in data:
				print shop_key, data[shop_key][0], data[shop_key][1], data[shop_key][2], data[shop_key][3], data[shop_key][4]
		elif fact_name == "deal":
			for entry in data:
				for deal_key in entry:
					print deal_key, entry[deal_key][0], entry[deal_key][1]
		elif fact_name == "deal_number":
			for entry in data:
				for city_name in entry:
					print city_name, entry[city_name]

if __name__ == "__main__":
	fact_name = "deal"
	source = "meituan"
	year = "2012"
	month = "12"
	day = "30"
	fact_retriever = FactRetriever()
	data = fact_retriever.retrieve(source, fact_name, year, month, day)
	fact_retriever.print_data(data, fact_name)


