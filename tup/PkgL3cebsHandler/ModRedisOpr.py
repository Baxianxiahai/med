# -*- coding: utf-8 -*-
# @Author: qwang011
# @Date:   2019-04-19 16:18:36
# @Last Modified 2019-04-19
# @Last Modified time: 2019-04-19 16:27:26
TUP_REDIS_HOST ="redis"
TUP_REDIS_PORT = 6379
TUP_REDIS_DB = 0
TUP_REDIS_PASSWD = ''
import redis
class tupRedisOpr():
	def __init__(self,host=TUP_REDIS_HOST,port=TUP_REDIS_PORT,db=TUP_REDIS_DB,password=TUP_REDIS_PASSWD):
		self.host=host
		self.port=port
		self.password=password
		self.db=db

	def fun_redis_get_connect(self):
		pool=redis.ConnectionPool(host=self.host, port=self.port, password=self.password, db=self.db)
		coon = redis.Redis(connection_pool=pool)
		return coon
