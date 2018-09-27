import json
import requests
from prettytable import PrettyTable

class scb():
	'''
	Interacts with the api from the swedish naitonal statistics instsitute,
	Statistiska CentralByrån, SCB.
	'''
	# Base url for accessing database
	url 	= 'http://api.scb.se/OV0104/v1/doris/sv/ssd'
	# Header for calling the db, what data you get back?
	header 	= {'content-type': 'text/csv', 'accept': 'text/csv'}
	
	def __init__(self):
		self.current_level = ''
		self.current_categories = ''
	def print(self):
		r 		= requests.get(self.url+self.current_level)
		data 	= json.loads(r.text)
		print('Current url is: '+self.url+self.current_level)
		if type(data) != type(dict()):
			t = PrettyTable(['Table', 'Code'])
			for table in data:
				t.add_row([table['text'],table['id']])
			print(t)	
		else:
			print('  Title: ')
			print('	'+data['title'])
			print('Filters:')
			for filt in data['variables']:
				print('	'+filt['text'])

			print('You''ve reached a table, please use method get() to filter data.')
						



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
		Request data from current table and return dict with
		chosen filters and fetched values.
		'''
		# Get info about table:	
		r = requests.get(self.url + self.current_level)
		data = json.loads(r.text)

		print('Requesting data from table: '+data['title'])

		post_query = dict()
		post_query['query'] = []
		'''
		We want to print the content code filter first, makes more sense to select
		that first. So we want to find the index of the variable that has the code
		ContentsCode, and the delete it from the dict and move on to the rest 
		of the variables.
		'''
		contentcode_index = int([counter for counter,entry in enumerate(data['variables']) if entry['code'] == 'ContentsCode'][0])
		contentcode = data['variables'][contentcode_index]
		available_filters = contentcode['values']
		t = PrettyTable([contentcode['text'], 'Code'])
		available_filters = contentcode['values']					
		for variable in data['variables']:
			while True:
				t = PrettyTable([variable['text'], 'Code'])					
				available_filters = variable['values']
				for row in range(0,len(variable['values'])):
					t.add_row([variable['valueTexts'][row],variable['values'][row]])
				print(t)
				filter_chosen = input('Enter filters from above: (split entries with comma, or leave blank)\n')
				# Check if the enterd value is in the available values
				# If it's not, print the table again and let the user enter again.
				if filter_chosen != '':
					# User entered correct value(s), break while loop and go to next filter	
					post_query['query'].append(
						{'code': variable['code'], 'selection': {'filter': 'item', 'values': filter_chosen.split(',')}})
					break
				else:
					break
		# What type of data we want to return!						
		post_query['response'] = {'format': 'json'}

		# Finally, make a post request to the database at the current level with the specified filters
		print(post_query)
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
			# Check if value are only letters:
			if d.isalpha():
				output['values'].append(d)
			if d.isdigit():
				if '.' in d:			
					output['values'].append(float(d))
				else:
					output['values'].append(int(d))


		return output