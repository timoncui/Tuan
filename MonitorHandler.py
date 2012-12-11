#!/usr/bin/env python

import os
import re
import json
import tornado.httpserver
import tornado.web

class MonitorHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("monitor.html")

	def post(self):
		source = self.get_argument("src", None)
		date = self.get_argument("date", None)
		if not source: return

		folder = os.path.join("log", source)
		if not date:  # get the log file list in this folder
			entries = []
			for filename in os.listdir(folder):
				if filename == '.' or filename == '..':
					continue
				entries.append(filename)
			entries.reverse()
			self.write( json.dumps(entries) )

		else:   # get the log details for a date
			pattern  = re.compile('[0-9]+/[0-9]+/[0-9]+')  # try to match the date description
			filepath = os.path.join(folder, date)
			try:
				success_list = []
				failure_list = []
				total_event_num = 0
				fhandler = open(filepath, "r")
				lines = fhandler.readlines()
				for line in lines:
					tokens = line.strip().split(" ")
					if pattern.match(tokens[0]):
						if tokens[-1].strip() == "SUCCESS":
							success_list.append(" ".join( [tokens[0], tokens[1], tokens[2]] ))
						else:
							failure_list.append(line.strip())
						total_event_num = total_event_num + 1
				fhandler.close()
				res = {"total": total_event_num, "success": success_list, "failure": failure_list}
				self.write( json.dumps(res) )
			except Exception, e:
				print "Error: MonitorHandler.py post", str(e)
				self.write( "{\"error\": \"" + str(e) + "\"}" )


