#!/usr/bin/env python
# @author Lixing Huang
# @date 1/15/2013
# word frequency of category

import os
import sys
import getopt
from parser_factory import ParserFactory
from data_retriever import DataRetriever
from compress import Zipper

class CategoryCount:
	def __init__(self):
		self.parser_factory = ParserFactory()
		self.category_count = dict()  # mapping from category to count
		self.local_category_count = dict()
		self.history = []  # each entry is beijing,2013,1,1

	def _incr_val_of_key(self, dictionary, key):
		if key in dictionary:
			dictionary[key] = dictionary[key]+1
		else:
			dictionary[key] = 1

	def _load_local(self, source, city):
		# load the history data
		filepath = os.path.join("category", source+"_"+city)
		if os.path.exists(filepath):
			fhandler = open(filepath, "r")
			lines = fhandler.readlines()
			fhandler.close()
			for line in lines:
				category, count = line.strip().split("\t")
				self.local_category_count[category.strip()] = int(count.strip())

	def _load(self, source):
		# load what has been recorded
		filepath = os.path.join("category", source+"_history")
		if os.path.exists(filepath):
			fhandler = open(filepath, "r")
			lines = fhandler.readlines()
			fhandler.close()
			for line in lines:  # each line is beijing,2013,1,1
				self.history.append(line.strip())

		# load the history data
		filepath = os.path.join("category", source)
		if os.path.exists(filepath):
			fhandler = open(filepath, "r")
			lines = fhandler.readlines()
			fhandler.close()
			for line in lines:
				category, count = line.strip().split("\t")
				self.category_count[category.strip()] = int(count.strip())

	def _parse(self, source, filepath):
		try:
			# decode the zipped file first
			zipper = Zipper()
			zipper.decode_file(filepath, filepath)
			# parse
			parser = self.parser_factory.get_parser(source)
			parser.parse(filepath)
			for deal in parser.deals:
				if ("deal_cate" in deal) and deal["deal_cate"]:
					category = deal["deal_cate"].strip().encode('utf-8')
					self._incr_val_of_key(self.category_count, category)
				#	self._incr_val_of_key(self.local_category_count, category)
		except Exception, e:
			print "category_analysis _parse", source, filepath, str(e)

	def _check_exist(self, city, year, month, day):
		history_entry = ",".join([city, str(year), str(month), str(day)])
		if history_entry in self.history:
			return True
		else:
			return False

	def _save(self, source, city, year, month, day):
		try:
			# save the history
			history_entry = ",".join([city, str(year), str(month), str(day)])
			if history_entry not in self.history:
				self.history.append(history_entry)

			filepath = os.path.join("category", source+"_history")
			fhandler = open(filepath, "w")
			for entry in self.history:
				fhandler.write(entry+"\n")
			fhandler.close()

			# save the category count
			result = []
			for category in self.category_count:
				result.append([category, self.category_count[category]])
			result.sort(key = lambda ele: ele[0])

			filepath = os.path.join("category", source)
			fhandler = open(filepath, "w")
			for entry in result:
				string = entry[0].strip() + "\t" + str(entry[1]) + "\n"
				fhandler.write(string)
			fhandler.close()

			# save the local category count
		#	local_result = []
		#	for category in self.local_category_count:
		#		local_result.append([category, self.local_category_count[category]])
		#	local_result.sort(key = lambda ele: ele[0])

		#	filepath = os.path.join("category", source+"_"+city)
		#	fhandler = open(filepath, "w")
		#	for entry in local_result:
		#		string = entry[0].strip() + "\t" + str(entry[1]) + "\n"
		#		fhandler.write(string)
		#	fhandler.close()
		except Exception, e:
			print "category_analysis _save", str(e)

	def retrieve_and_parse(self, retriever, source, city, year, month, day):
		print "loading..."
		self._load(source)
	#	self._load_local(source, city)
		if self._check_exist(city, year, month, day):
			print city, str(year), str(month), str(day), "has already existed"
			return
		print "retrieving..."
		cache_filelist = retriever.retrieve(source, city, year, month, day)
		print "parsing..."
		for filepath in cache_filelist:
			print "parsing", filepath
			self._parse(source, filepath)
		print "saving..."
		self._save(source, city, year, month, day)


if __name__ == "__main__":
	y = None  # year
	m = None  # month
	d = None  # day
	s = None  # source
	c = None  # city

	options, arg = getopt.getopt(sys.argv[1:], "y:m:d:s:c:", ["year=", "month=", "day=", "source=", "city="])
	for opt in options:
		if   opt[0] == "-y": y = opt[1]
		elif opt[0] == "-m": m = opt[1]
		elif opt[0] == "-d": d = opt[1]
		elif opt[0] == "-s": s = opt[1]
		elif opt[0] == "-c": c = opt[1]

	if not (y==None or m==None or d==None or s==None or c==None):
		cc = CategoryCount()
		cc.retrieve_and_parse(s, c, int(y), int(m), int(d))
	else:
		sources = ["dianping", "dida", "ftuan", "lashou", "manzuo", "meituan", "nuomi", "wowo", "wuba"]
		retriever = DataRetriever('lixing-tuan-usstandard')
		for source in sources:
			#if source != "wowo":
			#	continue
			for cityname in os.listdir(source):
				if cityname == "." or cityname == ".." or cityname == "city_list":
					continue
				print source, cityname
				cc = CategoryCount()
				cc.retrieve_and_parse(retriever, source, cityname, int(y), int(m), int(d))




