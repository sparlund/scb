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
		Request data from current table and return.... hm 
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
		ContentsCode, and what index it has in the recieved json data.
		'''
		contentcode_index = int([counter for counter,entry in enumerate(data['variables']) if entry['code'] == 'ContentsCode'][0])
		for j,variable in enumerate(data['variables']):
			while True:
				# Print ContentCode variable filter first!
				if j == 0:
					contentcode = data['variables'][contentcode_index]
					t = PrettyTable([contentcode['text'], 'Code'])
					available_filters = contentcode['values']					
					for row in range(0,len(contentcode['values'])):
						t.add_row([contentcode['valueTexts'][row],contentcode['values'][row]])
				else:		
					t = PrettyTable([variable['text'], 'Code'])					
					available_filters = variable['values']
					for row in range(0,len(variable['values'])):
						t.add_row([variable['valueTexts'][row],variable['values'][row]])
				print(t)
				filter_chosen = input('Enter filters from above: ')
				# Check if the enterd value is in the available values
				# If it's not, print the table again and let the user enter again.
				if filter_chosen not in available_filters and filter_chosen != '':
					print('You entered code:'+str(filter_chosen)+', and it''s not available.')
				else:
					# User entered correct value(s), break while loop and go to next filter	
					if filter_chosen != '':
						# Make filter_chosen separata items i en lista, inte som saker på rad!!!
						if j == 0:
							code = data['variables'][contentcode_index]['code'] 
							del data['variables'][contentcode_index]
							print(data['variables'])
						else:
							code = variable['code'] 	
						post_query['query'].append(
							{'code': code, 'selection': {'filter': 'item', 'values': filter_chosen.split(',')}})
						post_query['response'] = {'format': 'json'}
					break	

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



s = scb()
s.enter('OE')
s.enter('OE0108')
s.enter('OffEkoMott')
s.print()
o=s.get()
#s.enter('BE0101')
#s.enter('BE0101A')
#s.enter('BefolkningNy')
#o=s.get()
#print(o)
