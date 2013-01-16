#!/usr/bin/env python
# @author Lixing Huang
# @date 1/15/2013

from dida_parse import DidaParser
from dianping_parse import DianpingParser
from ftuan_parse import FtuanParser
from lashou_parse import LashouParser
from manzuo_parse import ManzuoParser
from meituan_parse import MeituanParser
from nuomi_parse import NuomiParser
from wowo_parse import WowoParser
from wuba_parse import WubaParser

class ParserFactory:
	def __init__(self):
		self.dida_parser = DidaParser()
		self.dianping_parser = DianpingParser()
		self.ftuan_parser = FtuanParser()
		self.lashou_parser = LashouParser()
		self.manzuo_parser = ManzuoParser()
		self.meituan_parser = MeituanParser()
		self.nuomi_parser = NuomiParser()
		self.wowo_parser = WowoParser()
		self.wuba_parser = WubaParser()

	def get_parser(self, name):
		if name == "dida":
			return self.dida_parser
		elif name == "dianping":
			return self.dianping_parser
		elif name == "ftuan":
			return self.ftuan_parser
		elif name == "lashou":
			return self.lashou_parser
		elif name == "manzuo":
			return self.manzuo_parser
		elif name == "meituan":
			return self.meituan_parser
		elif name == "nuomi":
			return self.nuomi_parser
		elif name == "wowo":
			return self.wowo_parser
		elif name == "wuba":
			return self.wuba_parser
		else:
			print "has not implemented", name
			return None