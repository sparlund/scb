import json
import requests

class scb():
	'''
	Interacts with the api from the swedish naitonal statistics instsitute,
	Statistiska CentralByrån, SCB.
	'''
	# Base url for accessing database
	url 	= 'http://api.scb.se/OV0104/v1/doris/sv/ssd/'
	# Header for calling the db, what data you get back?
	header 	= {'content-type': 'text/csv', 'accept': 'text/csv'}
	
	def __init__(self):
		self.current_level = ''
		self.current_categories = ''
	def print(self):
		r 		= requests.get(self.url+self.current_level)
		data 	= json.loads(r.text)
		# If data is a dict, we are at a table, otherwise we're not
		if type(data) == type(list()):
			print('Title: '+data['title'])
			for variable in data['variables']:
				print('	'+variable['code'])
		else:
			print('Categories for current level:')
			for var in data['variables']:
				print(type(val))
				print('	'+var['code'],var['valueTexts'])
	def enter(self,id):
		# Get current available categories
		r = requests.get(self.url+self.current_level)
		data = json.loads(r.text)
		self.current_categories = dict()
		for cat in data:
			self.current_categories[cat['id']] = cat['type']
		if id in self.current_categories.keys():
			#if self.current_categories[id] == 'l':
			self.current_level = self.current_level+'/'+id	
			#else:
			#	print(id+' is a table and can''t be entered, use method get() to access data in table')
		else:
			print(id+' not found in current level, use method print() to see available categories')	

	def up(self):
		if self.current_level is not '':
			if '/' in self.current_level:
				self.current_level = self.current_level[:self.current_level.rindex('/')]
			else:
				self.current_level = ''
		else:
			print('At base level, can not go up')	

	def get(self):
		'''
		Request data from current table and return.... hm 
		'''
		# Get info about table:
		r = requests.get(self.url + self.current_level)
		data = json.loads(r.text)
		print(data)

		post_query = dict()
		# What type of data to return!
		post_query['response'] = {'format': 'csv'}
		post_query['query'] = []

		# Finally, make a post request to the database at the current level with the specified filters
		r = requests.post(self.url + self.current_level,data=json.dumps(post_query),headers=self.header)


s = scb()
s.enter('BE')
s.enter('BE0101')
s.enter('BE0101A')
s.enter('BefolkningNy')
s.print()
#s.get()
#s.print()
# j={()
#   "post_query": [
#     {
#       "code": "Tilltalsnamn",
#       "selection": {
#         "filter": "vs:Pojkar10",
#         "values": [
#           "10Adam"
#         ]
#       }
#     },
#     {
#       "code": "ContentsCode",
#       "selection": {
#         "filter": "item",
#         "values": [
#           "BE0001AJ"
#         ]
#       }
#     },
#     {
#       "code": "Tid",
#       "selection": {
#         "filter": "item",
#         "values": [
#           "2017"
#         ]
#       }
#     }
#   ],
#   "response": {
#     "format": "json"
#   }
# }
#r = requests.post(url,data=json.dumps(j),headers=header)
#jd = json.loads(r.content)
#print(jd['data'][0]['values'][0])



