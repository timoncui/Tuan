import gzip

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

if __name__ == "__main__":
	app = Zipper()
#	app.encode_file("/Users/Lixing/Documents/projects/Tuan/meituan/beijing", "/Users/Lixing/Documents/projects/Tuan/beijing.gz")
	app.decode_file("/Users/Lixing/Documents/projects/Tuan/archive/meituan_beijing_2012_10_30_16_33.gz", "/Users/Lixing/Documents/projects/Tuan/archive/test")