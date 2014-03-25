import json, requests, oauth2

from requests_oauthlib import OAuth1Session
from pprint import pprint

READ = 'rb'
SEARCH_API_URL = 'http://api.yelp.com/v2/search'
tokens = json.load(open('tokens.json',READ))

#-- Unpack tokens

class Yelp(object):

	def __init__(self,query):
		self.query = query
		self.parameters={'term':'bars', 'location':'NYC'}

		self._session = OAuth1Session(tokens['Consumer Key'], tokens['Consumer Secret'], 
											tokens['Token'], tokens['Token Secret'])

		print self.search_query()

	class YelpError(Exception):
			def __init__(self,exception):
				pprint(exception)

	class YelpAPIError(Exception):
		def __init__(self,field,error):
			print '%s-%s'%(field,error)

	def search_query(self):
		response = self._session.get(SEARCH_API_URL, params=self.parameters)

		try:
			response_json = response.json()
		except ValueError as e:
			raise self.YelpError(e)

		if 'error' in response_json:
			if 'field' in response_json['error']:
				raise self.YelpAPIError(response_json['error']['id'], 
					'%s [field=%s]' % (response_json['error']['text'], response_json['error']['field']))
			else:
				raise self.YelpAPIError(response_json['error']['id'], response_json['error']['text'])

		return response_json

	def __repr__(self):
		return 'Yelp Query for %s'%self.query