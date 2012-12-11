# data generation pipeline
# @author: Lixing Huang
# @time: 10/30/2012

from meituan_crawl import MeituanCrawler
from meituan_parse import MeituanParser
from nuomi_crawl import NuomiCrawler
from nuomi_parse import NuomiParser
from lashou_crawl import LashouCrawler
from lashou_parse import LashouParser
from dida_crawl import DidaCrawler
from dida_parse import DidaParser
from wowo_crawl import WowoCrawler
from wowo_parse import WowoParser
from dianping_crawl import DianpingCrawler
from dianping_parse import DianpingParser
from ftuan_crawl import FtuanCrawler
from ftuan_parse import FtuanParser
from manzuo_crawl import ManzuoCrawler
from manzuo_parse import ManzuoParser
from wuba_crawl import WubaCrawler
from wuba_parse import WubaParser

from carrier import Carrier
from archiver import Archiver
from check_config import CheckConfig

import os
import sys
import time
import getopt
import random
import logging
import datetime

class Pipeline:
	def __init__(self, crawler, parser, carrier, source):
		self.crawler = crawler
		self.parser  = parser
		self.carrier = carrier
		self.source  = source

	# try to log which cities the crawler fails to fetch
	# error_cities is an array consists of city names
	# error_messages is an array consists of error information
	def log_result(self, error_cities, error_messages):
		log_folder_name = os.path.join("log", self.source)
		LA_local_t = datetime.datetime.today()
		filename = [str(LA_local_t.year), str(LA_local_t.month), str(LA_local_t.day)]
		filename = "_".join(filename)
		filepath = os.path.join(log_folder_name, filename)

		logging.basicConfig(filename=filepath, level=logging.INFO, filemode="a", format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
		if len(error_cities) > 0:
			for i in xrange(0, len(error_cities)):
				log_string = "Error:\t" + error_cities[i]
				log_string = log_string + "\t" + str(error_messages[i])
				logging.info(log_string)
		else:
			logging.info("SUCCESS")

	# sometimes because of low network connection, the feed from open APIs is not complete, which causes the xml parser fails.
	# this function wants to retry those files.
	# sleep_interval is used to generate a random waiting time.
	def rescue(self, error_list, sleep_interval):
		error_files = []
		error_msg = []

		for city in error_list:
			try:
				print "[start ] fetching deals in", city
				page_num = self.crawler.fetch_deal_in(city)
				print "[finish] fetching deals in", city

				if  page_num == 1 or page_num == None:
					self.parser.parse( os.path.join(self.source, city) )
				else:
					for i in xrange(1, page_num+1):
						if  i == 1:
							self.parser.parse( os.path.join(self.source, city) )
						else:
							self.parser.parse( os.path.join(self.source, city + "_" + str(i)) )

				wait_time = random.randint(sleep_interval[0], sleep_interval[1])
				print "wait", wait_time, "seconds"
				time.sleep( wait_time )

			except Exception, e:
				error_files.append(city)
				error_msg.append(str(e))
				print "Error in parsing data in", city
				print e
	#	print "Fail to parse", error_files
	#	print "Error message", error_msg
		self.log_result(error_files, error_msg)

	def start(self, sleep_interval):
		error_files = []
		error_msg = []

		start_time = datetime.datetime.now()

		city_list = None
		try:
			city_list = self.crawler.fetch_city_list()
		except Exception, e:
			print e
			return

		for city in city_list:
			try:
				print "[start ] fetching deals in", city
				page_num = self.crawler.fetch_deal_in(city)
				print "[finish] fetching deals in", city

				if  page_num == 1 or page_num == None:
					self.parser.parse( os.path.join(self.source, city) )
				else:
					for i in xrange(1, page_num+1):
						if  i == 1:
							self.parser.parse( os.path.join(self.source, city) )
						else:
							self.parser.parse( os.path.join(self.source, city + "_" + str(i)) )

				wait_time = random.randint(sleep_interval[0], sleep_interval[1])
				print "wait", wait_time, "seconds"
				time.sleep( wait_time )
			#	print "[start ] sending deal in", city, "to database"
			#	self.carrier.carry(self.source, self.parser.deals)
			#	print "[finish] sending deal in", city, "to database"
			except Exception, e:
				error_files.append(city)
				error_msg.append(str(e))
				print "Error in parsing data in", city
				print e

		end_time = datetime.datetime.now()
		duration = end_time - start_time
		print self.source, "takes", duration.seconds, "seconds"
	#	print "Fail to parse", error_files
	#	print "Error message", error_msg
		self.log_result(error_files, error_msg)

		return error_files


# Usage: python pipeline.py -s "meituan,dida,wowo"
# Usage: python pipeline.py -s "meituan" -c "beijing,shanghai"
# Usage: python pipeline.py -s "meituan" -r "4"  run it every 4 hours
if __name__ == "__main__":
	options, arg = getopt.getopt(sys.argv[1:], "s:c:r:", ["source=", "citylist=", "repeat="])
	source   = None
	citylist = None
	period   = None
	for opt in options:
		if opt[0] == "-s": source = opt[1]
		elif opt[0] == "-c": citylist = opt[1]
		elif opt[0] == "-r": period = opt[1]

	if  source:
		source = source.split(",")
		print "source: ", source
	if  citylist:
		citylist = citylist.split(",")
		print "city list: ", citylist

	while True:
		if not source: break
		sleep_interval = (0,30)
		if "meituan" in source:
			meituan_app = Pipeline(MeituanCrawler(), MeituanParser(), None, "meituan")
			if not citylist:
				error = meituan_app.start(sleep_interval)
				if len(error) > 0:
					meituan_app.rescue(error, sleep_interval)
			else:
				meituan_app.rescue(citylist, sleep_interval)
		if "nuomi" in source:
			nuomi_app = Pipeline(NuomiCrawler(), NuomiParser(), None, "nuomi")
			if not citylist:
				error = nuomi_app.start(sleep_interval)
				if len(error) > 0:
					nuomi_app.rescue(error, sleep_interval)
			else:
				nuomi_app.rescue(citylist, sleep_interval)
		if "lashou" in source:
			lashou_app = Pipeline(LashouCrawler(), LashouParser(), None, "lashou")
			if not citylist:
				error = lashou_app.start(sleep_interval)
				if len(error) > 0:
					lashou_app.rescue(error, sleep_interval)
			else:
				lashou_app.rescue(citylist, sleep_interval)
		if "wowo" in source:
			wowo_app = Pipeline(WowoCrawler(), WowoParser(), None, "wowo")
			if not citylist:
				error = wowo_app.start(sleep_interval)
				if len(error) > 0:
					wowo_app.rescue(error, sleep_interval)
			else:
				wowo_app.rescue(citylist, sleep_interval)
		if "dida" in source:
			dida_app = Pipeline(DidaCrawler(), DidaParser(), None, "dida")
			if not citylist:
				error = dida_app.start(sleep_interval)
				if len(error) > 0:
					dida_app.rescue(error, sleep_interval)
			else:
				dida_app.rescue(citylist, sleep_interval)
		if "dianping" in source:
			dianping_app = Pipeline(DianpingCrawler(), DianpingParser(), None, "dianping")
			if not citylist:
				error = dianping_app.start(sleep_interval)
				if len(error) > 0:
					dianping_app.rescue(error, sleep_interval)
			else:
				dianping_app.rescue(citylist, sleep_interval)
		if "manzuo" in source:
			manzuo_app = Pipeline(ManzuoCrawler(), ManzuoParser(), None, "manzuo")
			if not citylist:
				error = manzuo_app.start(sleep_interval)
				if len(error) > 0:
					manzuo_app.rescue(error, sleep_interval)
			else:
				manzuo_app.rescue(citylist, sleep_interval)
		if "ftuan" in source:
			ftuan_app = Pipeline(FtuanCrawler(), FtuanParser(), None, "ftuan")
			if not citylist:
				error = ftuan_app.start(sleep_interval)
				if len(error) > 0:
					ftuan_app.rescue(error, sleep_interval)
			else:
				ftuan_app.rescue(citylist, sleep_interval)
		if "wuba" in source:
			wuba_app = Pipeline(WubaCrawler(), WubaParser(), None, "wuba")
			if not citylist:
				error = wuba_app.start(sleep_interval)
				if len(error) > 0:
					wuba_app.rescue(error, sleep_interval)
			else:
				wuba_app.rescue(citylist, sleep_interval)

		# archive first
		archiver = Archiver()
		for src in source:
			archiver.archive(src, src, True)  # False achive locally, True achive to S3

		# repeat
		if not period: break
		time.sleep( int(period) * 3600 )

		# check config file
		stop_crawl = 0
		check_config = CheckConfig()
		config = check_config.check('crawl_config')
		for src in source:
			if src in config:
				if "period" in config[src]:
					period = config[src]["period"]
				if "stop" in config[src]:
					stop_crawl = config[src]["stop"]
				break
		if stop_crawl == 1:
			break



