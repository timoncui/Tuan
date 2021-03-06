#!/usr/bin/env python

import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from MonitorHandler import MonitorHandler

define("port", default=8483, type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MonitorHandler),
		]

		settings = dict(
			title = "Monitor Crawlers",
			base_url = "http://localhost:8483/",
			static_path = os.path.join(os.path.dirname(__file__), "static"),
			template_path = os.path.join(os.path.dirname(__file__), "templates"),
		)

		tornado.web.Application.__init__(self, handlers, **settings)

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
	main()