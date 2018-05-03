# coding=utf-8
import requests
import demjson

stock_url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData"\
			"?page={page}&num={num}&sort=symbol&asc=1&node={node}&symbol=&_s_r_a=init"
# 沪市A股
sh_a_mkt = {'page':1,'num' :40,'node':"sh_a"}
# 沪市B股
sh_b_mkt = {'page':1,'num' :40,'node':"sh_b"}
# 深市A股
sz_a_mkt = {'page':1,'num' :40,'node':"sz_a"}
# 深市B股
sz_a_mkt = {'page':1,'num' :40,'node':"sz_b"}

def req(url):
	try:
		r = requests.get(url,timeout=10)
	except:
		r = None
		raise "requests error"
	if r is not None:
		print r.url
		return r.content
	else:
		return

def get_stocks_package(stock_url,mkt,stocks):
	package = req(stock_url.format(**mkt))
	if package is not None:
		if package == "null":
			print "nullpage Ending Crawing; Total: %d" % len(stocks)
			return stocks
		else:
			stocks_package = demjson.decode(package.decode('gb18030').encode('utf-8'))
			stocks.extend(stocks_package)
			print len(stocks)
			mkt['page']+=1
			return get_stocks_package(stock_url,mkt,stocks)


if __name__ == '__main__':
	stocks_sh_a = get_stocks_package(stock_url,sh_a_mkt,stocks=[])
	print stocks_sh_a