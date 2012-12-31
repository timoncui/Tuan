# retrieve files from s3
# @author: Lixing Huang
# @time: 12/30/2012

import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key

class S3Retriever:
	def __init__(self):
		try:
			self.data_cache_folder = 'temp'
			self.s3_conn = S3Connection('AKIAISVIMYXGTRTNY6AA', 'LRGG0ihbhZEZ5lopn+ndd7ZduxZWQ/85bX9GVPLo')
			self.fact_bucket = self.s3_conn.lookup('lixing-tuan-facts')
		except Exception, e:
			print "Error: s3retriever.py", str(e)
			raise

	def retrieve_files(self, file_key_prefix):
		filenames = []
		try:
			print "listing", file_key_prefix
			for key in self.fact_bucket.list(file_key_prefix):
				cache_filename = os.path.join(self.data_cache_folder, key.name)
				if os.path.exists(cache_filename):
					filenames.append(cache_filename)
					continue
				else:
					key = self.fact_bucket.get_key(key.name)
					if key:
						try:
							print "retrieve", key.name, "from s3"
							key.get_contents_to_filename(cache_filename)
							filenames.append(cache_filename)
							print key.name, "downloaded"
						except Exception, e:
							print "Error: s3retriever.py retrieve_files", str(e)
							continue
			return filenames
		except Exception, e:
			print "Error: s3retriever.py retrieve_files", str(e)
		return None

	def retrieve_file(self, file_key):
		try:
			# check whether the key has already been cached or not
			cache_filename = os.path.join(self.data_cache_folder, file_key)
			if os.path.exists(cache_filename):
				return cache_filename
			key = self.fact_bucket.get_key(file_key)
			if key:
				print "retrieve", file_key, "from s3"
				key.get_contents_to_filename(cache_filename)
				print file_key, "downloaded"
				return cache_filename
		except Exception, e:
			print "Error: s3retriever.py retrieve_file", str(e)
		return None


