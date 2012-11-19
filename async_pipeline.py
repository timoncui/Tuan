# async data generation pipeline
# @author: Lixing Huang
# @time: 11/4/2012

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

import tornado.ioloop
import tornado.httpclient

import os
import sys
import time
import getopt
import random
import logging
import datetime
import functools
import threading

meituan_crawler = MeituanCrawler()
meituan_parser = MeituanParser()
nuomi_crawler = NuomiCrawler()
nuomi_parser = NuomiParser()
#lashou_crawler = LashouCrawler()
#lashou_parser = LashouParser()
dida_crawler = DidaCrawler()
dida_parser = DidaParser()
wowo_crawler = WowoCrawler()
wowo_parser = WowoParser()
dianping_crawler = DianpingCrawler()
dianping_parser = DianpingParser()
ftuan_crawler = FtuanCrawler()
ftuan_parser = FtuanParser()
manzuo_crawler = ManzuoCrawler()
manzuo_parser = ManzuoParser()
wuba_crawler = WubaCrawler()
wuba_parser = WubaParser()

error_cities = {}
error_messages = {}

pipeline_sources = []

# try to log which cities the crawler fails to fetch
# source: where the deal comes from, e.g. meituan, nuomi, etc.
def log_result(source):
	log_folder_name = os.path.join("log", source)
	LA_local_t = datetime.datetime.today()
	filename = [str(LA_local_t.year), str(LA_local_t.month), str(LA_local_t.day)]
	filename = "_".join(filename)
	filepath = os.path.join(log_folder_name, filename)

	logging.basicConfig(filename=filepath, level=logging.DEBUG, filemode="a", format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
	if source in error_cities:
		for i in xrange(0, len(error_cities[source])):
			log_string = "Error:\t" + error_cities[source][i]
			log_string = log_string + "\t" + error_messages[source][i]
			logging.info(log_string)
	else:
		logging.info("SUCCESS")

def report_errors():
	print "================================================="
	print "==================REPORT ERRORS=================="
	print "================================================="
	print pipeline_sources
	for source in pipeline_sources:
		print source
		if source in error_cities:
			print "======== CITY LIST ========"
			print error_cities[source]
		log_result(source)

def _handle_response(data, response):
	source = data["source"]
	city = data["city"]
	if response.error:
	#	if "Timeout" in str(response.error):  # only retry the timeout sites
		if source in error_cities:
			error_cities[source].append(city)
		else:
			error_cities[source] = [city]
		if source in error_messages:
			error_messages[source].append(response.error)
		else:
			error_messages[source] = [response.error]
	else:
		filepath = os.path.join(source, city)
		fhandler = open(filepath, "w")
		fhandler.write(response.body)
		fhandler.close()

		try:
			if source == "meituan": meituan_parser.parse(filepath)
			elif source == "nuomi": nuomi_parser.parse(filepath)
			elif source == "dida": dida_parser.parse(filepath)
			elif source == "wowo": wowo_parser.parse(filepath)
			elif source == "dianping": dianping_parser.parse(filepath)
			elif source == "ftuan": ftuan_parser.parse(filepath)
			elif source == "manzuo": manzuo_parser.parse(filepath)
			elif source == "wuba": wuba_parser.parse(filepath)
		except Exception, e:
			if source in error_cities:
				error_cities[source].append(city)
			else:
				error_cities[source] = [city]
			if source in error_messages:
				error_messages[source].append(str(e))
			else:
				error_messages[source] = [str(e)]

	tornado.ioloop.IOLoop.instance().stop()


class AsyncPipeline:
	def __init__(self):
		self.user_agent = "Chrome/22.0.1229.94"

	def start(self, source_names, city_list=None):
		del pipeline_sources[:]  # since this function will be called multiple times
		for source in source_names:
			pipeline_sources.append(source)
		time1 = datetime.datetime.now()

		crawlers = []
		for source in source_names:
			if source == "meituan": crawlers.append(meituan_crawler)
			elif source == "nuomi": crawlers.append(nuomi_crawler)
			elif source == "dida": crawlers.append(dida_crawler)
			elif source == "wowo": crawlers.append(wowo_crawler)
			elif source == "dianping": crawlers.append(dianping_crawler)
			elif source == "ftuan": crawlers.append(ftuan_crawler)
			elif source == "manzuo": crawlers.append(manzuo_crawler)
			elif source == "wuba": crawlers.append(wuba_crawler)
			if city_list: break

		headers = {'User-Agent': self.user_agent}
		for crawler in crawlers:
			source = crawler.data_store
			print "start crawling data from", source
			if not city_list:
				city_list = crawler.fetch_city_list()
			for city in city_list:
				start_time = datetime.datetime.now()

				url = crawler.get_fetch_deal_url(city)
				print str(start_time), "start  loading", url

				request = tornado.httpclient.HTTPRequest(url=url, method="GET", headers=headers, connect_timeout=20.0, request_timeout=600.0)
				handle_response = functools.partial(_handle_response, {"city": city, "source": source})
				http_client = tornado.httpclient.AsyncHTTPClient()
				http_client.fetch(request, callback=handle_response)

				tornado.ioloop.IOLoop.instance().start()

				end_time = datetime.datetime.now()
				duration = end_time - start_time
				print str(end_time), "finish loading", url
				print "it takes", duration.seconds, "seconds"

				# try to be friendly to website
				wait_time = random.randint(0, 30)
				print "[wait]", wait_time, "seconds"
				time.sleep( wait_time )

		time2 = datetime.datetime.now()

		duration = time2 - time1
		print str(source_names), "takes", duration.seconds, "seconds"

		report_errors()

# Usage: python async_pipeline.py -s "meituan"
if __name__ == "__main__":
	options, arg = getopt.getopt(sys.argv[1:], "s:c:", ["source=", "citylist="])
	source = None
	citylist = None

	for opt in options:
		if opt[0] == "-s": source = opt[1]
		elif opt[0] == "-c": citylist = opt[1]

	if source:
		source = source.split(",")
		print "source: ", source
	if citylist:
		citylist = citylist.split(",")
		print "city list: ", citylist

	if source:
		app = AsyncPipeline()
		app.start(source, citylist)

	# rescue
	if  len(error_cities) > 0:
		for source in error_cities.iterkeys():
			print "Try to rescue", source
			remain_cities = error_cities[source]
			error_cities[source] = []
			error_messages[source] = []
			app = AsyncPipeline()
			app.start([source], remain_cities)






