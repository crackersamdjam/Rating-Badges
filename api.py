from bs4 import BeautifulSoup
import datetime
import json
import requests
import sys

cache = dict()
# I should probably use a database instead

def get_rating(site, user):
	# update each rating at most once each hour
	current_time = datetime.datetime.now()
	if (site, user) in cache and (current_time-cache[(site, user)][0]) < datetime.timedelta(hours=1, seconds=5):
		print('cached', site, user, file=sys.stderr)
		return cache[(site, user)][1]
	
	res = None
	if site == 'DMOJ':
		res = DMOJ(user)
	elif site == 'Codeforces':
		res = Codeforces(user)
	elif site == 'Atcoder':
		res = Atcoder(user)
	else:
		return None, None
		# maybe raise an error
	
	cache[(site, user)] = (current_time, res)
	return res

def DMOJ(user):
	response = requests.get(f'https://dmoj.ca/api/v2/user/{user}')
	json_data = json.loads(response.text)
	if 'data' not in json_data:
		return '0', 'black'
		
	data = json_data['data']['object']
	rating = data['rating']
	rating_color = 'black'
	if rating < 1000:
		rating_color = 'grey'
	elif rating < 1200:
		rating_color = 'green'
	elif rating < 1500:
		rating_color = 'blue'
	elif rating < 1800:
		rating_color = 'purple'
	elif rating < 2200:
		rating_color = 'yellow'
	else:
		rating_color = 'red'
	
	return str(rating), rating_color
	
def Codeforces(user):
	response = requests.get(f'https://codeforces.com/api/user.info?handles={user}')
	json_data = json.loads(response.text)
	#print('________________', json_data['result'], file=sys.stderr)
	if 'result' not in json_data:
		return '0', 'black'
		
	data = json_data['result'][0]
	rating = data['rating']
	rating_color = 'black'
	
	if rating < 1200:
		rating_color = 'grey'
	elif rating < 1400:
		rating_color = 'green'
	elif rating < 1600:
		rating_color = 'cyan'
	elif rating < 1900:
		rating_color = 'blue'
	elif rating < 2100:
		rating_color = 'purple'
	elif rating < 2300:
		rating_color = 'yellow'
	elif rating < 2400:
		rating_color = 'orange'
	else:
		rating_color = 'red'
	
	return str(rating), rating_color
	
def Atcoder(user):

	# need to scrape page since no atcoder api :monkey:
	page = requests.get(f'https://atcoder.jp/users/{user}')
	print(page.status_code, file=sys.stderr)
	if page.status_code != 200:
		return '0', 'black'
		
	soup = BeautifulSoup(page.content, "html.parser")
	results = soup.find(id='dl-table')
	table = soup.find_all('table', class_='dl-table')[1]
	th = table.find_all('span')[1]
	rating = int(th.getText())
	rating_color = 'black'
	
	if rating < 400:
		rating_color = 'grey'
	elif rating < 800:
		rating_color = 'brown'
	elif rating < 1200:
		rating_color = 'green'
	elif rating < 1600:
		rating_color = 'cyan'
	elif rating < 2000:
		rating_color = 'blue'
	elif rating < 2400:
		rating_color = 'yellow'
	elif rating < 2800:
		rating_color = 'orange'
	else:
		rating_color = 'red'
	
	return str(rating), rating_color

