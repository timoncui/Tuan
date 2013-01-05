#!/usr/bin/env python

import os
import json
import tornado.httpserver
import tornado.web
import redis
import calendar

class DealnumHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.redis_port = 6379
		self.redis_db = 0

	def get(self):
		self.render("deal_num.html")

	def _load_city_list(self):
		try:
			city_list = []
			print "loading city list..."
			fhandler = open("../city_list", "r")
			lines = fhandler.readlines()
			fhandler.close()
			print "city list loaded!"
			for line in lines:
				city_name = line.strip().split("\t")[1]
				city_list.append(city_name.strip())
			return city_list
		except Exception, e:
			print "DealnumHandler _load_city_list", str(e)
			return []

	def _incr_date(self, y, m, d):
		day = []
		if calendar.isleap(y):
			days = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		else:
			days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		if d+1 <= days[m]:
			return [y, m, d+1]
		elif m <= 11:
			return [y, m+1, 1]
		else:
			return [y+1, 1, 1]

	def post(self):
		type = self.get_argument("type", None)
		if type == "citylist":
			city_list = self._load_city_list()
			self.write(json.dumps(city_list))
		elif type == "num":
			city = self.get_argument("city",None)
			srcs = self.get_argument("src", None)
			beg  = self.get_argument("beg", None)
			end  = self.get_argument("end", None)
			if not city or not srcs or not beg or not end:
				return
			srcs = srcs.strip().split(",")
			beg_y, beg_m, beg_d = beg.strip().split("-")
			end_y, end_m, end_d = end.strip().split("-")
			beg_y = int(beg_y)
			beg_m = int(beg_m)
			beg_d = int(beg_d)
			end_y = int(end_y)
			end_m = int(end_m)
			end_d = int(end_d)

			# query redis
			r = redis.StrictRedis(host='localhost', port=self.redis_port, db=self.redis_db)
			
			key_list = []
			for src in srcs:
				if src == "": continue
				_beg_y = beg_y  # keep the original date
				_beg_m = beg_m
				_beg_d = beg_d
				while True:
					for h in xrange(0,24):
						date = "_".join([str(_beg_y), str(_beg_m), str(_beg_d), str(h)])
						redis_key = "deal_number:" + src + ":" + city + ":" + date
						key_list.append(redis_key)
					_beg_y, _beg_m, _beg_d = self._incr_date(_beg_y, _beg_m, _beg_d)
					if (_beg_y>end_y) or (_beg_y==end_y and _beg_m>end_m) or (_beg_y==end_y and _beg_m==end_m and _beg_d>end_d):
						break
			val_list = r.mget(key_list)
			# key: source(e.g. meituan); val: array whose element is an array having
			# 2 entries, first entry contains time, second one contains deal number
			# for example: meituan -> [ [2012_12_30, 2012_12_31], [100, 200] ]
			result = dict()
			for i in xrange(0, len(key_list)):
				if val_list[i]:
					print key_list[i], val_list[i]
					tokens = key_list[i].strip().split(":")
					source = tokens[1]
					date = tokens[3]
					if source in result:
						result[source][0].append(date)
						result[source][1].append(val_list[i])
					else:
						result[source] = [ [date], [val_list[i]] ]
			self.write(json.dumps(result))


