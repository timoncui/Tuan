# compress and store the raw data into database
# @author: Lixing Huang
# @time: 10/30/2012

import database
import datetime
from compress import Zipper
import os
import sys
import getopt

class Archiver:
	def __init__(self):
		self.archive_root = "archive"

	# archive the data
	# filename: source_city_time
	# for example: meituan_beijing_2012_10_29_17_50
	# folder: where the to-be-archived files are
	# source: a string indicates the data source, for example, meituan, nuomi, etc.
	def archive(self, folder, source, on_S3=False):
		zipper = Zipper()
		LA_local_t = datetime.datetime.today()

		if not on_S3:
			folder_name = None
			try:
				folder_name = [str(LA_local_t.year), str(LA_local_t.month), str(LA_local_t.day)]
				folder_name = "_".join(folder_name)
				folder_path = self.archive_root + "/" + source + "/" + folder_name
				if not os.path.exists(folder_path):
					print "creating folder", folder_path
					os.mkdir(folder_path)
			except Exception, e:
				print "Error: archiver.py archive", e
				raise

		for filename in os.listdir(folder):
			if filename == "." or filename == "..":
				continue
			else:
				print "archiving", filename
				key = [source, filename, str(LA_local_t.year), str(LA_local_t.month), str(LA_local_t.day), str(LA_local_t.hour), str(LA_local_t.minute)]
				key = "_".join(key)
				if not on_S3:
					zipper.encode_file( folder + "/" + filename, self.archive_root + "/" + source + "/" + folder_name + "/" + key + ".gz" )
				else:
					zipper.encode_and_save_to_s3( folder + "/" + filename, key )

# Usage: python archiver.py -s "meituan,dida"
if __name__ == "__main__":
	options, arg = getopt.getopt(sys.argv[1:], "s:", ["source="])
	source = None
	for opt in options:
		if opt[0] == "-s": source = opt[1]
	source = source.strip().split(",")

	for src in source:
		app = Archiver()
		app.archive(src, src)



