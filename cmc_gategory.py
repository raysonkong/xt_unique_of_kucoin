from requests import Request, Session
import json
import pprint
import datetime
import time
import os
from config_cmc import *

SLEEP_TIME = 0.2

## ==================================##
## setup config_cmc.py in the same folder
## ==================================##

## ================ ##
## Notes on Config ## 
## ================ ##
  ## each cmc page has 100 coins
  ## each txt file represents one CMC Page
  ## and each symbol produces n * 2 outputs(BTC and USDT pairs)
  ## Hence each page produces n * 2 * 100 outputs
  ##(n=num of exchanges, 2 represents BTC and USDT pairs
  ## e.g 4 exchanges, each cmc page produces 4 * 2 * 100 = 800 outputs(trading pairs) in each txt file

 ## each additional exchange is 
    ## an extra 2 outputs for each pair
    ## Hence an extra 200 output for each page/txt file
 ## so max 5 exchange is allowed to keep each list < 1000

## ==============##
## Config Code  ## 
## ==============## 

## HOW_MANY_COINS Determine how many coins you are getting from CMC
## EXCHANGES determines exhanges you want

# HOW_MANY_COINS = 4000
# EXCHANGES=["BINANCE", "KUCOIN", 'BITTREX', 'HUOBI']


## Do not alter below easily

## Tradingview Lists limited by 1000 output per file
## GROUP_SIZE determines output number per text file

# GROUP_SIZE = len(EXCHANGES) * 200
## CURRENCIES determine the trading pairs
# CURRENCIES = ['BTC', 'USDT']
# API_KEY = 'Your Api Key'
# URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

## end of Config file



#===== Setup Date and Time #======== 
# Date
generation_date = datetime.datetime.now()
generation_date = generation_date.strftime("%d_%m_%Y")


# Time now
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
#print(current_time)


#generation_time = now.strftime("%H:%M:%S")


## Getting the Category ID ### 



# Tell CMC I want json response
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY' :API_KEY
}

session = Session()
session.headers.update(headers)

parameters = {
    'limit': HOW_MANY_CATEGORY
}


# Get Gategory ID
response = session.get(URLCATEGORIES, params=parameters)
#pprint.pprint(json.loads(response.text)['data'])
parsed_response = response.json()['data']

categoryId = ''

for item in parsed_response:
    if item['title'] == CATEGORY:
        categoryId = item['id']

## success!
#print(categoryId)

## Calling the particular gategory

parameters2 = {
    'limit': HOW_MANY_COINS,
    'id': categoryId
}

#print(parameters2)

response2 = session.get(URLCATEGORY, params=parameters2)
#pprint.pprint(json.loads(response2.text))
parsed_response2 = response2.json()['data']['coins']

#print(parsed_response2)


#================================================ # 
# Step 1 #
# Turn Json response to a list of symbols
# output: [ 'BTC', "ETH", ...] 

symbols = []
def json_to_tickers(data):
    for item in data:
        symbols.append(item["symbol"])

json_to_tickers(parsed_response2)
#print(symbols)

# now symbols hold all our ..well.. symbols

#================================================ # 
# Step 2 # 
# Helper Function
# Convert one symbol to tradingview format with exchange currency pair, in a list

exchanges = EXCHANGES
currencies = CURRENCIES

def symbol_to_tradingview(symbol):
    one_symbol_watchlist = []
    for exchange in exchanges:
        for currency in currencies:
            current_pair = ""
            one_symbol_watchlist.append(f"{exchange}:{symbol}{currency}")
    return one_symbol_watchlist

#symbol_to_tradingview('ADA')

#================================================
# Step 3 #
# Convert Step output, which is symbols, 
#  to a list of trading view pair
# using helper from Step 2

def flatten(t):
    return [item for sublist in t for item in sublist]

nested_tradingview_pairs=[]

for symbol in symbols:
    nested_tradingview_pairs.append(symbol_to_tradingview(symbol))

tradingview_pairs = flatten(nested_tradingview_pairs)
#print(tradingview_pairs)

#================================================
# Step 4 #
# Group output from step 3
# to a list containing lists of n 

# Group size, in production n=400
n=GROUP_SIZE

def group_into_n(data_list, n):
    return [data_list[i:i+n] for i in range(0, len(data_list), n)]

#test = [1,2,3,4,5,6,7,8]
#print(group_into_n(test, n))

grouped_pairs = group_into_n(tradingview_pairs, n)

#print(grouped_pairs)


#================================================
# Step 5 #

# write a function to output each of the group in step 4 
# to a separate file


#def output_to_text_file(nested_grouped_pairs):
#    for idx, group in enumerate(nested_grouped_pairs):
#        with open(f'{idx+1}CMC p.{idx+1} {generation_date}.txt ', 'w') as f:
#            for pair in group:
#                f.write("%s,\n" % pair)


# /Users/raysonkong/code/python/webscrapping/scripts_v2/cmc_api_to_tradingview/outputs
def output_to_text_file(nested_grouped_pairs):
    for idx, group in enumerate(nested_grouped_pairs):
            filename=f"{os.getcwd()}/CMC_{CATEGORY}_{generation_date}total{HOW_MANY_COINS}/{idx+1}.CMC p.{idx+1} ({generation_date}).txt"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as f:
                for pair in group:
                  f.write("%s,\n" % pair)

#output_to_text_file(grouped_pairs)


def run_srapper():
    os.system('clear')
    output_to_text_file(grouped_pairs)


    print("== CMC Scrapping Completed ==")
    print('\n')
    #print("======================================================")
if __name__ =='__main__':
    run_srapper()

