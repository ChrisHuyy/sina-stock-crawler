# coding=utf-8
import pymysql
from pymysql.converters import escape_item
from pymysql import escape_string

def get_conn():
	db = pymysql.connect(
				host='127.0.0.1',
				user='root',
				password='root',
				db='sina_stock',
				charset='utf8mb4',
				cursorclass=pymysql.cursors.DictCursor)
	return db

def q(s):
	if isinstance(s,str):
		return escape_string(s)
	elif isinstance(s,unicode):
		return escape_string(s).encode('utf-8')
	elif isinstance(s,float):
		return ('%.15g' % s)
	elif isinstance(s,int):
		return str(s)
	else:
		return escape_item(s,charset='utf-8')


def query(sql):
	db = get_conn()
	cursor = db.cursor()
	try:
		cursor.execute(sql)
		print sql
		ret = cursor.fetchall()
	except:
		ret = None
		print "Error: unable to fecth data"
	finally:
		db.close()
	return ret

def execute(sql):
	db = get_conn()
	cursor = db.cursor()
	try:
		cursor.execute(sql)
		print sql
		db.commit()
		return True
	except:
		# Rollback in case there is any error
		print 'Insert FAIL!'
		db.rollback()
		return False
	finally:
		db.close()




if __name__ == '__main__':
# 	json_str = """
# {"amount":42890185,"buy":"40.510","changepercent":"2.633","code":"603788","high":"40.620","low":"39.250","mktcap":666287.057946,"name":"\u5b81\u6ce2\u9ad8\u53d1","nmc":568982.954,"open":"39.450","pb":3.454,"per":25.497,"pricechange":"1.040","sell":"40.550","settlement":"39.500","symbol":"sh603788","ticktime":"15:00:00","trade":"40.540","turnoverratio":0.76738,"volume":1077026}
# 	"""
# 	import demjson
# 	insObj = demjson.decode(json_str)
# 	print insObj
# 	print check_redandunt(insObj)
# 	update(insObj,pk='symbol')

	# k_list = []
	# v_list = []
	# for k in insObj.keys():
	# 	k_list.append(k)
	# 	v_list.append(q(insObj[k]))
	# insert_sql = "INSERT INTO `stocks_info`(`{}`)VALUES('{}')".format("`,`".join(k_list),"','".join(v_list).encode('utf-8'))
	# execute(insert_sql)
	pass