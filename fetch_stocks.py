# coding=utf-8
import requests
import demjson
import datetime
import os
import time
from dao import query,execute,q


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


def store_as_file(infoObj):
	file_name = os.path.dirname(os.path.realpath(__file__)) + "\save\s_%s.log" % datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
	with open(file_name,'w') as f:
		f.write(demjson.encode(infoObj))
	print "Data has been store at %s" % file_name


def store_in_db(infoObj):
	for info in infoObj:
		info['ctime'] = int(time.time())
		info['last_update_time'] = int(time.time())
		if check_redandunt(info):
			update(info,pk='symbol')
		else:
			insert(info)

def check_redandunt(info):
	if info.has_key('symbol'):
		query_sql = "SELECT * FROM `stocks_info` WHERE `symbol` = '{}'".format(info['symbol'])
		ret = query(query_sql)
		if ret is not None and len(ret) > 0:
			return True
		else:
			return False

def update(info,pk):
	update_list = []
	for k in info.keys():
		update_part = "`{}`='{}'".format(k,q(info[k]))
		update_list.append(update_part)
	update_sql = "UPDATE `stocks_info` SET {} WHERE `{}` = '{}'".format(",".join(update_list),pk,info[pk])
	execute(update_sql)


def insert(info):
	k_list = []
	v_list = []
	for k in info.keys():
		k_list.append(k)
		v_list.append(q(info[k]))
	insert_sql = "INSERT INTO `stocks_info`(`{}`)VALUES('{}')".format("`,`".join(k_list),"','".join(v_list))
	execute(insert_sql)


def main():
	stocks_sh_a = get_stocks_package(stock_url,sh_a_mkt,stocks=[])
	store_in_db(stocks_sh_a)
	store_as_file(stocks_sh_a)	

if __name__ == '__main__':
	main()