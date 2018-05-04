# coding=utf-8
from __future__ import division
from dao import query,execute,q
import pandas as pd

# load 出所有数据
query_sql = "SELECT * FROM `stocks_info`"
all_info = query(query_sql)
stocks_info = pd.DataFrame(all_info)

# 转化函数
wan_to_yi = lambda x : x/10000
yi_to_wan = lambda x : x*10000

# print stocks_info.head(5)
print stocks_info.info()
print stocks_info.shape
print "\n"

# # 沪市A股总市值
print"沪市A股总市值: %d万万亿".decode('utf-8')% wan_to_yi(wan_to_yi(stocks_info['mktcap'].sum()))
print "\n"

# 市值最高股票
print "沪市A股市值最高股票(万亿)".decode('utf-8')
stocks_info.mktcap = stocks_info.mktcap.apply(wan_to_yi)
print stocks_info.sort_values(['mktcap'], ascending=False)[['name','mktcap']].head(1)
print "\n"

# 市值前五股票
print "沪市A股市值前五股票(万亿)".decode('utf-8')
print stocks_info.sort_values(['mktcap'], ascending=False)[['name','mktcap']].head(5)
print "\n"

# 备用【市值】属性转化为原数据
# stocks_info.mktcap = stocks_info.mktcap.apply(yi_to_wan)

# 停牌股票总数
stocks_closed = stocks_info[stocks_info.amount == 0]
print "停牌股票总数%d支".decode('utf-8')%stocks_closed.shape[0]
print "\n"

# 停牌股票中市值最高
print "停牌股票中市值最高(万亿)".decode('utf-8')
print stocks_closed.sort_values(['mktcap'], ascending=False)[['name','mktcap','symbol','per']].head(1)
print "\n"

# 沪市A股平均市盈率
print "沪市A股平均市盈率%f".decode('utf-8')%stocks_info['per'].mean()
# 沪市A股中位市盈率
print "沪市A股中位市盈率%f".decode('utf-8')%stocks_info['per'].median()
print "\n"