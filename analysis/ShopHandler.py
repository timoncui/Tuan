import os
import json
import tornado.httpserver
import tornado.web
import redis
import calendar
import datetime

class ShopHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.redis_port = 6379
		self.redis_db = 0

	def get(self):
		self.render('shop.html');
	
	def post(self):
		type = self.get_argument("type", None)
		if type == "shoplist":
			try:
				city_name = self.get_argument("city", None)
				if not city_name:
					return
				# query redis
				r = redis.StrictRedis(host='localhost', port=self.redis_port, db=self.redis_db)
				redis_key = "shops_in_city:" + city_name
				shop_set  = r.smembers(redis_key)
				shop_list = []
				for shop_id in shop_set:
					shop_list.append(shop_id.decode('utf-8'))
				self.write( json.dumps(shop_list) )
			except Exception, e:
				print "shoplist", city_name, str(e)
		elif type == "num":
			try:
				city = self.get_argument("city", None)
				shop = self.get_argument("shop", None)
				beg  = self.get_argument("beg", None)
				end  = self.get_argument("end", None)
				if not city or not shop or not beg or not end:
					return

				beg_y, beg_m, beg_d = beg.strip().split("-")
				end_y, end_m, end_d = end.strip().split("-")
				beg_y = int(beg_y)
				beg_m = int(beg_m)
				beg_d = int(beg_d)
				end_y = int(end_y)
				end_m = int(end_m)
				end_d = int(end_d)

				result = dict()
				# query redis
				r = redis.StrictRedis(host='localhost', port=self.redis_port, db=self.redis_db)
				# use the shop id to retrieve sources
				redis_key = "source_of_shop:" + shop
				source_set = r.smembers(redis_key)

				# use the shop id to retrieve deal ids
				for source in source_set:
					redis_key = "deal_of_shop:" + source + ":" + shop
					deal_set  = r.smembers(redis_key)
					if len(deal_set) == 0:
						continue

					result[source] = [[], [], []]
					
					# use the deal id to retrieve sales information
					sales_info = []
					for deal_id in deal_set:
						redis_key = "deal:" + source + ":" + deal_id
						print redis_key
						sales = r.hgetall(redis_key)
						for date_key in sales.iterkeys():
							tokens = sales[date_key].strip().split(";")
							y, m, d, h = date_key.strip().split("_")

							date_time = datetime.datetime(int(y), int(m), int(d), int(h))
							price  = float(tokens[0])
							s_num  = int(tokens[1])
							sales_info.append([date_time, price, s_num])
					sales_info.sort(key=lambda ele: ele[0])

					# filter sales information based on the start time and end time
					beg_date = datetime.datetime(beg_y, beg_m, beg_d, 0)
					end_date = datetime.datetime(end_y, end_m, end_d, 23)
					for i in xrange(0,len(sales_info)):
						if beg_date<=sales_info[i][0] and sales_info[i][0]<=end_date:
							if i>0 and sales_info[i][0]==sales_info[i-1][0]:
								result[source][1][-1] = result[source][1][-1] + sales_info[i][1]
								result[source][2][-1] = result[source][2][-1] + sales_info[i][2]
							else:
								result[source][0].append( str(sales_info[i][0].year)+"_"+str(sales_info[i][0].month)+"_"+str(sales_info[i][0].day)+"_"+str(sales_info[i][0].hour) )
								result[source][1].append( sales_info[i][1] )
								result[source][2].append( sales_info[i][2] )
				print "------------------------"
				print result
				self.write( json.dumps(result) )
			except Exception, e:
				print "num", city, shop, str(e)





