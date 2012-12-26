# find the number of unique deals per source
# @author: Lixing Huang
# @time: 12/25/2012

from meituan_parse import MeituanParser
from nuomi_parse import NuomiParser
from lashou_parse import LashouParser
from dida_parse import DidaParser
from wowo_parse import WowoParser
from dianping_parse import DianpingParser
from ftuan_parse import FtuanParser
from manzuo_parse import ManzuoParser
from wuba_parse import WubaParser
from compress import Zipper
import os

class FindDealNum:
	def __init__(self):
		pass

	# retrieve all deal files in the folder
	def get_deal_file_list(self, folder_path):
		deal_list = []
		for filename in os.listdir(folder_path):
			if filename == "city_list": continue
			else: deal_list.append(filename)
		return deal_list

	def find_deal_num(self, source):
		deal_set = set()

		parser = None
		if source == "dida": parser = DidaParser()
		elif source == "dianping": parser = DianpingParser()
		elif source == "ftuan": parser = FtuanParser()
		elif source == "lashou": parser = LashouParser()
		elif source == "manzuo": parser = ManzuoParser()
		elif source == "meituan": parser = MeituanParser()
		elif source == "nuomi": parser = NuomiParser()
		elif source == "wowo": parser = WowoParser()
		elif source == "wuba": parser = WubaParser()

		filelist = self.get_deal_file_list(source)
		for filename in filelist:
			filepath = os.path.join(source, filename)
			parser.parse(filepath)
			for deal in parser.deals:
				deal_id = deal["deal_id"]
				deal_set.add(deal_id)
		print source, len(deal_set)
		return len(deal_set)

if __name__ == "__main__":
	app = FindDealNum()
	dp = app.find_deal_num("dianping")
	dida = app.find_deal_num("dida")
	ftuan = app.find_deal_num("ftuan")
	lashou = app.find_deal_num("lashou")
	manzuo = app.find_deal_num("manzuo")
	meituan = app.find_deal_num("meituan")
	nuomi = app.find_deal_num("nuomi")
	wowo = app.find_deal_num("wowo")
	wuba = app.find_deal_num("wuba")
	print "dianping", dp
	print "dida", dida
	print "ftuan", ftuan
	print "lashou", lashou
	print "manzuo", manzuo
	print "meituan", meituan
	print "nuomi", nuomi
	print "wowo", wowo
	print "wuba", wuba


