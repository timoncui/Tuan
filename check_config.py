# while the crawler is running repeatedly, I want it to check a config file every round
# so that I can stop the crawler or the period by changing the values in config file.
# the format of this file:
#   source=meituan (this must be the first line)
#   period=4
#   stop=0

import os

class CheckConfig:
	def check(self, filepath):
		conf = dict()
		try:
			fhandler = open(filepath, "r")
			lines = fhandler.readlines()
			fhandler.close()
			current_source = ""
			for line in lines:
				if len(line.strip()) == 0: continue
				key, value = line.strip().split("=")
				if key == "source":
					current_source = value
					conf[current_source] = {}
				elif key == "period" or key == "stop":
					conf[current_source][key] = int(value)
			return conf
		except Exception, e:
			return {}

if __name__ == "__main__":
	check_config = CheckConfig()
	config = check_config.check("crawl_config")
	if "meituan" in config:
		print config["meituan"]
		period = config["meituan"]["period"]
		stop_crawl = config["meituan"]["stop"]
		print period
		print stop_crawl