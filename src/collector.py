'''
		Collector.py is the local api endpoint for PP. It uses TAG_IDS to filter for markets. TOPICS will be handled in a seperate data filtering program.
		It is useful to have an understanding of the format of polymarket markets. Each Market{ has events{ }}. Each event{has trades}.  
'''


import requests
from http.client import RemoteDisconnected
from py_clob_client.client import ClobClient, OrderBookSummary
from py_clob_client.clob_types import BookParams
from typing import Dict, List
import time
import random
import os
import json


BASE_URL_GAMMA = "https://gamma-api.polymarket.com/"
BASE_URL_CLOB = "https://clob.polymarket.com/"
BASE_URL_DATA = "https://data-api.polymarket.com/"

#BASE_TOPICS_LIST = ["iran", "israel"]

BASE_PATH = 'C:/Users/holde/Documents/Engineering/Projects/Polymarket_Parasite'

TAG_IDS = {
	"politics": "2",
	"geopolitics": "100265"
}

class Gamma_API:
	'''
	Description: Upon initializing begins web session, returns queries through methods
	Methods: get_markets, fetch_by_slug, get_markets_by_pagination
	'''
	def __init__(self):
		self.session = requests.Session()

	def get_markets(self, tag_id: str, limit: int = 50, offset: int = 0) -> List[Dict]:
		'''
		Definition:
		Params: 
		'''
		resp = self.session.get(
			f"{BASE_URL_GAMMA}events?",
			params = {
				"tag_id" : tag_id,
				"limit": limit,
				"active": True,
				"closed": False,
			}
		)

		resp.raise_for_status()
		return resp.json()

	def fetch_by_slug(self, slug:str):
		resp = self.session.get(
			f"{BASE_URL_GAMMA}events/slug/{slug}"
			)
		resp.raise_for_status()
		return resp.json()

	def get_markets_by_pagination(self,tag_id: str, limit: int = 50, offset: int = 0) -> List[Dict]:
		listed_pages = []
		time.sleep(0.25) 		#Primitive rate limiting
		for i in range(offset):
			page = self.session.get(
				f"{BASE_URL_GAMMA}events?",
				params = {
					"tag_id" : tag_id,
					"limit" : limit,
					"closed": False,
					"active": True,
					"offset": i
				}
				)
			page.raise_for_status()
			listed_pages.append(page.json())

		return [conditionId for page in listed_pages for conditionId in page]

	def get_event_data(self, markets: List[Dict]) -> List[Dict]:
		ids_slugs_dicts = []
		for market in markets:
			for event in market["markets"]:
				if event["closed"]==True:
					break
				ids_slugs_dicts.append({"conditionId" : event["conditionId"], "slug": event["slug"], "endDate":event["endDate"]})
		return ids_slugs_dicts



	def end_session(self):
		self.session.close()

class Clob_API: #Prices, orderbooks, trading
	
	'''
	Class: Clob_API
	Description: Upon initializing begins web session, returns queries through methods
	Methods: event_data, tokens, retrieve_bids
	Note: not really relevent unless headless orders are to be made
	'''
	def __init__(self):
		self.client = ClobClient(
			host=BASE_URL_CLOB,
			chain_id=137
		)

	def event_data(self, conditionId: str):
		return self.client.get_market(conditionId)

	def tokens(self, eventData: Dict) -> List[Dict]:
		self.eventData = eventData 
		return self.eventData["tokens"] # ->
		

	def retrieve_bids(self, OrderBookSummary: OrderBookSummary) -> List[Dict]:
		bids = []
		for bid in OrderBookSummary.bids:
			bids.append({"price": bid.price, "size": bid.size})
		return bids


class Data_API: #Positions, activity, history  	
	'''
	Class: Data_API
	Description: Upon initializing begins web session, returns queries through methods
	Methods: get_trades, 
	'''
	def __init__(self):
		self.session = requests.Session()

	def get_trades(self, conditionId: str, takerOnly=True, limit = 100) -> List[Dict]: # market has to be list of conditionIds but list doesn't seem to work
		
		time.sleep(0.1) #trades limited to 200 req / 10s  - 20/1s [currently: 10/s]
		resp = self.session.get(														# passing single conditionIds does though
			f"{BASE_URL_DATA}trades?",
			params = {
				"market" : conditionId,
				"takerOnly" : takerOnly,
				"limit" : limit
				}
			)

		resp.raise_for_status()
		return resp.json()


	
def controller(file_name : str):
	Gamma = Gamma_API()
	Data = Data_API()

	from MHD_dump import freedom

	print(f"Polymarket parasitic collector:\n    {random.choice(freedom)}\n")

	markets = Gamma.get_markets_by_pagination(tag_id=TAG_IDS["politics"],limit=50, offset=10)
	
	condition_ids = []

	for market in markets:
		for event in market["markets"]:
			if event["closed"]==True:
				break
			else:
				condition_ids.append(event["conditionId"])


	print(f"Fetched {len(condition_ids)} events")

	trades = []
	fetch_counter = 0

	print("\nFetching trades...\n")

	for conditionId in condition_ids:
		try:
			trades.append(Data.get_trades(conditionId=conditionId, limit=1000))
			fetch_counter += 1
		except RemoteDisconnected as e:
			print(f"EXCEPTION: {e}\nCONDITION_ID:{conditionId}")
			continue
			
		if fetch_counter % 1000 == 0:
			print(f"Fetched trades for {fetch_counter} events")



	#trades = Data.get_trades(market= [event["conditionId"] for event in condition_ids])

	with open(f"{BASE_PATH}/data/{os.path.splitext(file_name)[0]}.json", "w") as f:
	    	json.dump(trades, f, indent = 4)

	print(f"Fetched {len(trades)}. \n")
	print(f"\n{random.choice(freedom)} \n")


