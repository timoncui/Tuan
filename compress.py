import gzip
import os

from boto.s3.connection import S3Connection
from boto.s3.key import Key

try:
	# this is crap
	s3_conn = S3Connection('AKIAISVIMYXGTRTNY6AA', 'LRGG0ihbhZEZ5lopn+ndd7ZduxZWQ/85bX9GVPLo')
	tuan_bucket = s3_conn.lookup('lixing-tuan-usstandard')
except Exception, e:
	print "Error: compress.py ", e
	raise


class Zipper:
	def encode_file(self, filepath, output):
		f_in = open(filepath, "rb")
		f_out = gzip.open(output, "wb")
		f_out.writelines(f_in)
		f_out.close()
		f_in.close()

	def decode_file(self, filepath, output):
		f = gzip.open(filepath, "rb")
		content = f.read()
		f.close()
		f = open(output, "wb")
		f.write(content)
		f.close()

	def encode_and_save_to_s3(self, filepath, key):
		f_in = open(filepath, "rb")
		f_out = gzip.open(key + ".tmp.gz", "wb")
		f_out.writelines(f_in)
		f_out.close()
		f_in.close()
		try:
			k = Key(tuan_bucket)
			k.key = key
			k.set_contents_from_filename(key + ".tmp.gz")
			# remove the temp file
			os.remove(key + ".tmp.gz")
		except Exception, e:
			print "Error: compress.py encode_and_save_to_s3", e
			raise

if __name__ == "__main__":
	app = Zipper()
#	app.encode_file("/Users/Lixing/Documents/projects/Tuan/meituan/beijing", "/Users/Lixing/Documents/projects/Tuan/beijing.gz")
	app.decode_file("/Users/Lixing/Documents/projects/Tuan/archive/meituan_beijing_2012_10_30_16_33.gz", "/Users/Lixing/Documents/projects/Tuan/archive/test")
