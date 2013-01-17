#!/usr/bin/env python

import os
import json
import tornado.httpserver
import tornado.web
import redis
import calendar

class CategoryHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("category.html")
	
	def post(self):
		source = self.get_argument('source', None)
		if not source:
			return
		try:
			result = dict()
			fhandler = open("../category/"+source, "r")
			lines = fhandler.readlines()
			fhandler.close()
			for line in lines:
				categories, amount = line.strip().split("\t")
				categories = categories.strip().split(",")
				amount = int(amount)
				for category in categories:
					if category.strip() == "":
						continue
					if category in result:
						result[category] = result[category] + amount
					else:
						result[category] = amount
			self.write(json.dumps(result));
		except Exception, e:
			print "load category", source, str(e)