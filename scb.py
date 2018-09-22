import json
import requests
from prettytable import PrettyTable

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
		print('Current url is: '+self.url+self.current_level)
		print(data)
		if type(data) == type(list()):
			print('Title: '+data['title'])
			for variable in data['variables']:
				print('	'+variable['code'])
		else:
			print('Categories for current level:')
			for var in data['variables']:
				print('	'+var['text'])

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

		print('Requesting data from table: '+data['title'])

		post_query = dict()
		# What type of data to return!
		post_query['query'] = []
		for variable in data['variables']:
			t = PrettyTable([variable['text'], 'Code'])
			for row in range(0,len(variable['values'])):
				t.add_row([variable['valueTexts'][row],variable['values'][row]])
			print(t)
			filter_chosen = input('Enter filters from above: ')
			if filter_chosen != '-':
				# Make filter_chosen separata items i en lista, inte som saker på rad!!!
				post_query['query'].append(
					{'code': variable['code'], 'selection': {'filter': 'item', 'values': filter_chosen.split(',')}})
				post_query['response'] = {'format': 'json'}
		# Finally, make a post request to the database at the current level with the specified filters
		r = requests.post(self.url + self.current_level,data=json.dumps(post_query),headers=self.header)
		jd = json.loads(r.content)
		# Create output dict
		output = dict()
		output['filters'] = list()
		output['values'] = list()
		print('--- PRINTING REQEUSTED DATA ---')
		print('Filters:')
		for j,filters in enumerate(jd['columns']):
			if filters['type'] != 'c':
				values = list()
				for entry in range(0,len(jd['data'])):
					values.append(jd['data'][entry]['key'][j])
				valuestring = str(values).replace('[','').replace(']','').replace('\'','')
				print('	'+filters['text']+'='+str(valuestring))
				output['filters'].append({filters['text']: values})
				del values					
			else:
				print('	'+filters['text'])	
		print('Values:')
		for d in jd['data']:
			# Clean values:
			d = str(d['values']).replace('[','').replace(']','').replace('\'','')
			print(d)
			# Check if value are only letters:
			if d.isalpha():
				output['values'].append(d)
			if d.isdigit():
				if '.' in d:			
					output['values'].append(float(d))
				else:
					output['values'].append(int(d))

		return output				



#s = scb()
#s.enter('BE')
#s.enter('BE0101')
#s.enter('BE0101A')
#s.enter('BefolkningNy')
#o=s.get()
#print(o)
