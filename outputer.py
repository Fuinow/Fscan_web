import json
from pymongo import MongoClient
from config import CONFIG

class Outputer(object):

	def __init__(self):
		self.url = "mongodb://" + CONFIG.MONGO_USER + ":" + CONFIG.MONGO_PWD + "@" + CONFIG.MONGO_IP
		self.conn = MongoClient(self.url, connect=False)
		self.db = self.conn[CONFIG.MONGO_DB]

	def change_scan_state(self, root_domain, domain, pos, state):
		col = self.db[root_domain]
		query = {"domain":domain}
		res = col.find_one(query)
		if res:
			res["state"][pos] = state
			col.update(query, res)
		else:
			print "No data"
		return
		self.conn.close()

	def get_collection_name(self):
		return self.db.collection_names()
		self.conn.close()
	
	def get_domain_list(self, root_domain):
		return self.db[root_domain].find()
		self.conn.close()

	def get_info(self, root_domain, domain):
		info_set = self.db[root_domain]
		return info_set.find_one({"domain":domain})

	def scan_update(self, data, root_domain):
		set_name = root_domain.replace(".","_")
		if data:
			scan_set = self.db[set_name]
			query = {"domain":data["domain"]}
			query_data = scan_set.find_one(query)
			if query_data:
					data = {"$set":data}
					scan_set.update(query, data)
			else:
				scan_set.insert(data)
		else:
			print "Data is none"

		self.conn.close()
		return

	def domain_update(self, datas, col):
		col = col.replace(".","_")
		if datas:
			domain_set = self.db[col]
			for data in datas:
				query = {"domain":data["domain"]}
				if domain_set.find_one(query):
					data = {"$set":data}
					domain_set.update(query, data)
				else:
					domain_set.insert(data)
		else:
			print "Data is none"
			
		self.conn.close()
		return


if __name__ == "__main__":
#	data = {"domain":"aa.aaa.com","port":[20]}
	test = Outputer()
#	test.scan_update(data, "aaa.com")
	print 	test.get_collection_name()
