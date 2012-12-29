# archive stuff onto s3

import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key

class S3Archiver:
	def __init__(self):
		try:
			self.s3_conn = S3Connection('AKIAISVIMYXGTRTNY6AA', 'LRGG0ihbhZEZ5lopn+ndd7ZduxZWQ/85bX9GVPLo')
			self.fact_bucket = self.s3_conn.lookup('lixing-tuan-facts')
		except Exception, e:
			print "Error: s3archiver.py", str(e)
			raise

	# filepath: which file I want to archive to S3
	# key: the key value of the file stored on S3
	def archive(self, filepath, key):
		try:
			k = Key(self.fact_bucket)
			k.key = key
			k.set_contents_from_filename(filepath)
		except Exception, e:
			print "Error: s3archiver.py archive", str(e)
			raise

if __name__ == "__main__":
	archiver = S3Archiver()
	archiver.archive("/Users/Lixing/Documents/projects/Tuan/deal_number/dida_2012_12_27_17", "deal_number_dida_2012_12_27_17")