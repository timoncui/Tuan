# @author Lixing Huang
# @date 1/15/2013

import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.s3.bucketlistresultset import BucketListResultSet

class DataRetriever:
	def __init__(self, bucket_name):
		try:
			self.data_cache_folder = 'cache'
			self.s3_conn = S3Connection('AKIAISVIMYXGTRTNY6AA', 'LRGG0ihbhZEZ5lopn+ndd7ZduxZWQ/85bX9GVPLo')
			self.bucket = self.s3_conn.lookup(bucket_name)
		except Exception, e:
			print "Error: data_retriever.py", str(e)
			raise

	def retrieve(self, source, city, year, month, day):
		try:
			index = 1
			filelist = []
			prefix = "_".join([source, city, str(year), str(month), str(day)])
			prefix = prefix + "_"

			result_set = self.bucket.list(prefix)
			for item in result_set:
				key = self.bucket.get_key(item.name)
				if key:
					cache_filepath = os.path.join(self.data_cache_folder, source + "_" + city + "_" + str(index))
					print "fetching", item.name
					key.get_contents_to_filename(cache_filepath)
					filelist.append(cache_filepath)
					index = index + 1
			return filelist
		except Exception, e:
			print "Error: data_retriever.py", str(e)
			return None

if __name__ == "__main__":
	app = DataRetriever('lixing-tuan-usstandard')
	filelist = app.retrieve('wowo', 'beijing', 2013, 1, 8)
	print filelist