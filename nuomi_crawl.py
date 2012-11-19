# crawler by calling nuomi.com open API
# @author: Lixing Huang
# @time: 10/30/2012

import os
import urllib
import urllib2
import datetime
import tuan_http

class NuomiCrawler:
	def __init__(self):
		self.url_deal = "http://www.nuomi.com/api/dailydeal?version=v1&city="
		self.user_agent = "Chrome/22.0.1229.94"
		self.data_store = "nuomi"

	def fetch_deal_in(self, city):
		try:
			city = city.strip()
			print "nuomi_crawl.py fetch_deal_in", city
			content  = tuan_http.http_fetch(self.url_deal + city, self.user_agent)
			filepath = os.path.join(self.data_store, city)
			fhandler = open(filepath, "w")
			fhandler.write(content)
			fhandler.close()
		except Exception, e:
			print "Error: meituan_crawl.py fetch_deal_in", city, e
			raise
		return 1

	def get_fetch_deal_url(self, city):
		return self.url_deal + city

	def fetch_city_list(self):
		nuomi_city_list_str = "chaoyang, wenzhou, yingkou, yantai, xiangyang, yiyang, suqian, hulunbeier, nyingchi, haidong, qujing, wuxi, dongying, chenzhou, jian, huaihua, yangzhou, qiandongnanmiaodongautonomous, kaifeng, shanghai, xinxiang, hengyang, jinzhou, sanya, yinchuan, cixi, luzhou, heze, taiyuan, luoyang, rikaze, yingtan, beijing, jinchang, mudanjiang, kunming, daqing, shuangyashan, jiaxing, taian, tacheng, chengdu, changshu, nujianglisuzu, shaoyang, xianning, hefei, bazhong, beihai, suihua, liaocheng, liaoyang, weihai, liaoyuan, qitaihe, jiamusi, yanan, qingdao, dongguan, tongchuan, changdu, yichun1, hebi, benxi, huangshan, chaozhou, shuozhou, shanwei, hengshui, liupanshui, baotou, dali, yibin, binzhou, deyang, qinhuangdao, haibei, aomen, tianshui, tongling, guangzhou, yichun, zhangye, langfang, baoji, baiyin, bayannaoer, jilin, jinhua, qinzhou, quzhou, naqu, puyang, chaohu, hohhot, artux, qingyuan, guiyang, anshun, altay, daxinganling, honghe, tangshan, nanping, quanzhou, hetian, haikou, xuzhou, eerduosi, zhumadian, linyi, loudi, laibin, chifeng, shijiazhuang, wuzhong, ningbo, fuyang, fangchenggang, hegang, nanjing, boertalamongol, chuxiong, yancheng, yushu, zhangjiakou, sanming, shangluo, yulin1, chuzhou, shizuishan, zhangzhou, bengbu, haerbin, zhaoqing, emeishan, jiangmen, xinyang, jiyuan, qingyang, lincang, jingmen, xingtai, suzhou, weinan, xuchang, pingliang, anyang, guangyuan, pingdingshan, maoming, bijie, yueyang, ziyang, jixi, changde, dandong, nanyang, jining, chongqing, tianjin, xiaogan, baicheng, wulanchabu, shenyang, yangjiang, qianxinan, ganzhou, jiangyin, xishuangbanna, ankang, diqing, xiangxi, bayangolmongol, shannan, xining, tieling, fuzhou1, chizhou, yili, alashan, tonghua, huangshi, wulumuqi, putian, puer, kashgar, dazhou, laiwu, changzhi, handan, siping, anqing, qiqihar, tongren, xilinguole, shaoxing, kelamayi, fuxin, shantou, suzhou1, nantong, liangshan, jiaozuo, fuzhou, meishan, hezhou, yunfu, jincheng, ali, hanzhong, panzhihua, yangquan, yuncheng, akesu, huizhou, xianggang, haixi, zigong, xianyang, fushun, xiamen, hechi, jiuquan, aba, daidehongjingpo, jinzhong, tanggu, zhaotong, huaibei, baishan, changsha, jieyang, mianyang, tongliao, anshan, chongzuo, guoluo, baise, zhoushan, lishui, wujiang, dezhou, linfen, anqiu, xingan, huainan, huludao, qiannan, linxia, lasa, jinan, shaoguan, dalian, cangzhou, huangnan, lvliang, zhuhai, hangzhou, yulin, wenshan, zhongwei, huzhou, jindezhen, dingxi, jiayuguan, zhoukou, suizhou, shenzhen, xuancheng, shangrao, heihe, zunyi, tulufan, xinyu, wuhan, suining, yichang, baoshan, huaian, baoding, gannan, longyan, maanshan, nanchang, datong, zhangjiajie, taizhoux, wuhai, songyuan, longkou, liuan, guilin, qizhou, zhengzhou, zhuzhou, panjin, yaan, shiyan, wuhu, chengde, zhanjiang, yiwu, jiujiang, zibo, wuzhou, luohe, guigang, ganzizhou, changji, changchun, changzhou, wuwei, guyuan, weifang, yanbian, hami, zhenjiang, xiangtan, lanzhou, yongzhou, zaozhuang, pingxiang, longnan, yuxi, nanning, guangan, rizhao, zhongshan, neijiang, meizhou, shangqiu, taizhou, lijiang, xian, bozhou, kunshan, hainantibetan, lianyungang, nanchong, heyuan, liuzhou, foshan, sanmenxia, leshan, ningde"
		nuomi_city_list = nuomi_city_list_str.split(",")
		for i in xrange(0, len(nuomi_city_list)):
			nuomi_city_list[i] = nuomi_city_list[i].strip()
		return nuomi_city_list

if __name__ == "__main__":
	app = NuomiCrawler()
	city_list = app.fetch_city_list()
	for city in city_list:
		app.fetch_deal_in(city)
		break