#coding=utf-8
import os

class Config(object):

	def __init__(self):

		self.MONGO_IP = "127.0.0.1"
		self.MONGO_USER = "root"
		self.MONGO_PWD = "1051231987"
		self.MONGO_DB = "Fscan"

		self.DIR_DICT = "Dict/dir.txt"
		self.DIR_THREAD = 10
		self.DIR_RATIO = 0.5

		self.FINGER_DICT = "Dict/finger.json"
		self.FINGER_THREAD = 10

		self.PORT_LIST = [21,22,23,80,81,82,83,84,85,86,87,88,89,90,161,389,443,445,873,1099,1433,1521,
												1900,2082,2083,2222,2601,2604,3128,3306,3311,3312,3389,
												4440,4848,5432,5560,5900,5901,5902,6082,6379,7001,7002,7003,7004,7005,7006,7007,7008,7009,7010,
												7778,8080,8081,8082,8083,8084,8085,8086,8087,8088,8089,8090,8649,8888,9000,9200,10000,11211,27017,
												28017,50000,50030,50060]

		self.HTTP_DEBUG = False
		self.HTTP_PROXY = False
		self.PROXY_INFO = { 'host' : '127.0.0.1',
               										 'port' : 8080
            									 }
		self.TIMEOUT = 3
		self.HEADERS = {
							"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0",
							"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
							"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
							"Accept-Encoding": "deflate",
							"Connection": "close",
							"Upgrade-Insecure-Requests": 1
		}

CONFIG = Config()