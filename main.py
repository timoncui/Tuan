# date collection and analysis pipeline
# 1. call API to get deals data
# 2. parse and extract useful information from deals

import pipeline
import async_pipeline
import miner
import find_deal_num
import datetime

start_time = datetime.datetime.now()

sources = ["dida", "dianping", "ftuan", "manzuo", "meituan", "nuomi", "wowo", "wuba"]

for source in sources:
	print "start crawling deals from", source
	async_pipeline.main(source, None, None)
	find_deal_num.main(source, True)
	miner.main(source, True)

print "start crawling deals from lashou"
pipeline.main("lashou", None, None)
find_deal_num.main("lashou", True)
miner.main("lashou", True)

end_time = datetime.datetime.now()
duration = end_time - start_time
print "====================="
print "The task takes", duration.seconds, "seconds to finish"
print "====================="

fhandler = open("finish_log.txt", "a")
fhandler.write(str(duration.seconds) + "\n")
fhandler.close()