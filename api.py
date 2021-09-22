from bs4 import BeautifulSoup
import datetime
import json
from ratelimit import limits
import requests
import sys

cache = dict()
# I should probably use a database instead

def get_rating(site, user):
	# update each rating at most once each hour
	current_time = datetime.datetime.now()
	if (site, user) in cache and (current_time-cache[(site, user)][0]) < datetime.timedelta(hours=1, seconds=5):
		#print('cached', site, user, file=sys.stderr)
		return cache[(site, user)][1]
	
	if site == 'dmoj':
		res = DMOJ(user)
	elif site == 'codeforces':
		res = Codeforces(user)
	elif site == 'atcoder':
		res = Atcoder(user)
	else:
		raise ValueError('Site not found')

	cache[(site, user)] = (current_time, res)
	return res

# https://pypi.org/project/ratelimit/
@limits(calls=10, period=10)
def DMOJ(user):
	response = requests.get(f'https://dmoj.ca/api/v2/user/{user}')
	json_data = json.loads(response.text)
	if 'data' not in json_data:
		raise ValueError('User not found')
		
	rating = json_data['data']['object']['rating']

	if not rating:
		return 'unrated', 'grey'
	
	if rating < 1000:
		rating_color = 'grey'
	elif rating < 1300:
		rating_color = 'green'
	elif rating < 1600:
		rating_color = 'blue'
	elif rating < 1900:
		rating_color = 'purple'
	elif rating < 2400:
		rating_color = 'yellow'
	else:
		rating_color = 'red'
	
	return str(rating), rating_color

# https://codeforces.com/apiHelp
# API may be requested at most 5 times in one second. If you send more requests, you will receive a response with "FAILED" status and "Call limit exceeded" comment.
@limits(calls=4, period=1)
def Codeforces(user):
	response = requests.get(f'https://codeforces.com/api/user.info?handles={user}')
	json_data = json.loads(response.text)
	if 'result' not in json_data:
		raise ValueError('User not found')

	try:
		rating = json_data['result'][0]['rating']
	except:
		return 'unrated', 'grey'

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

# idk if I need rate limit
def Atcoder(user):
	# I need to scrape the page since there's no atcoder api
	page = requests.get(f'https://atcoder.jp/users/{user}')
	#print(page.status_code, file=sys.stderr)
	if page.status_code != 200:
		raise ValueError('User not found')
	
	try:
		soup = BeautifulSoup(page.content, "html.parser")
		results = soup.find(id='dl-table')
		table = soup.find_all('table', class_='dl-table')[1]
		th = table.find_all('span')[1]
		rating = int(th.getText())
	except:
		return 'unrated', 'grey'
	
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

