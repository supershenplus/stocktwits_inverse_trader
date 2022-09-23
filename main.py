import os
import time
import datetime
import alpaca_trade_api as tradeapi
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re

ser = Service("C:\\chromedriver\\chromedriver.exe")
op = webdriver.ChromeOptions()
# op.add_argument('--headless')
op.add_argument('--log-level=3')
page = webdriver.Chrome(service=ser, options=op)

API_KEY = "PKA9ABGKEN9A7F76RB9R"
API_SECRET = "ZhveESrsoDAgvvRrVtGZfvXXkkNebU25zuuSoS49"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"

alpaca = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, api_version='v2')

page.get('https://raybb.github.io/random-stock-picker/')
gen_stonk = page.find_element(By.ID, 'refresh')
gen_stonk.click()
current_stonk = page.find_element(By.ID, 'ticker')
page.get('https://stocktwits.com/symbol/' + current_stonk.text)


full_body = page.find_element(By.XPATH, "/html/body").text
time.sleep(1)
'''
stock_real = re.search('Uh-oh, we (.*)an', full_body)

while stock_real.group(1) == 'c':
    page.get('https://raybb.github.io/random-stock-picker/')
    gen_stonk = page.find_element(By.ID, 'refresh')
    gen_stonk.click()
    current_stonk = page.find_element(By.ID, 'ticker')
    page.get('https://stocktwits.com/symbol/' + current_stonk.text)
else:
    print('Stock found.')
'''

for _ in range(50):
    webdriver.ActionChains(page).key_down(Keys.PAGE_DOWN).perform()
    time.sleep(.6)

bear = 'Bearish'
bull = 'Bullish'

get_bear = len(re.findall(bear, full_body))
get_bull = len(re.findall(bull, full_body))

print(current_stonk.text + ' analysis complete.')
print('Bearish count: ', get_bear)
print('Bullish count: ', get_bull)

'''
if get_bear > get_bull:
    alpaca.submit_order(all_stonks[0], 1, 'buy', 'market', 'day')
    print('Inversing StockTwits sentiment....')
    print('Order for ' + all_stonks[0] + ' placed.')
elif get_bear < get_bull and alpaca.get_asset(all_stonks[0]).shortable == 'True':
    alpaca.submit_order(all_stonks[0], 1, 'sell', 'market', 'day')
    print('Inversing StockTwits sentiment....')
    print('Short order for ' + all_stonks[0] + ' placed.')
elif get_bear < get_bull and alpaca.get_asset(all_stonks[0]).shortable == 'False':
    print('Cannot short this stock on Alpaca. Please choose another stock.')
elif get_bear and get_bull == 0:
    print('Not enough sentiment data to place order.'
          '\n Please try again')

'''
get_bears = re.split(r'\W', full_body)
get_bears.count('Bearish')
get_bulls = re.split(r'\W', full_body)
get_bulls.count('Bullish')

print(get_bears.count)
print(get_bulls.count)
