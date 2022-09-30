from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from top_secret import API_KEY, API_SECRET
import chromedriver_autoinstaller
import re
import time

# selenium and alpaca config
# selenium is the web automation tool we use to navigate through and find the data we need on webpages
chromedriver_autoinstaller.install()
op = webdriver.ChromeOptions()
op.add_argument("--headless")
op.add_argument("--log-level=3")
page = webdriver.Chrome(options=op)
# alpaca markets API is used to place orders linked to our paper trading account
trading_client = TradingClient(API_KEY, API_SECRET, paper=True)


random_stonk = 'undefined'


# grab a random stock and stores it in random_stonk
def randomize_stonk():
    page.get("https://raybb.github.io/random-stock-picker/")
    gen_stonk = page.find_element(By.ID, "refresh")
    gen_stonk.click()
    find_stonk = page.find_element(By.ID, "ticker")
    global random_stonk
    random_stonk = find_stonk.text
    print("Stock found: ", random_stonk)
    page.get("https://stocktwits.com/symbol/" + random_stonk)
    time.sleep(1)

    # checking to see if stocktwits returns an "Uh-oh, we can't find this stock" page
    # there is probably a cleaner way to check if the ticker is not available on stocktwits
    stock_real = re.search(
        "Uh-oh, we (.*)an", page.find_element(By.XPATH, "/html/body").text
    )
    if stock_real is None:
        print("Analyzing StockTwits sentiment...")
    else:
        print("Ticker not found on StockTwits, finding another ticker...")
        randomize_stonk()


randomize_stonk()

# scrolls down through the stocktwits feed to collect data, includes a time delay to help buffer the action without
# causing issues
for _ in range(50):
    webdriver.ActionChains(page).key_down(Keys.PAGE_DOWN).perform()
    time.sleep(0.6)
# aggregating bearish and bullish tags affixed to posts
bear = "Bearish"
bull = "Bullish"
get_bear = len(re.findall(bear, page.find_element(By.XPATH, "/html/body").text))
get_bull = len(re.findall(bull, page.find_element(By.XPATH, "/html/body").text))
print("Sentiment analysis complete.")
print("Bearish count: ", get_bear)
print("Bullish count: ", get_bull)

# end selenium session
page.quit()

# defining buy and sell market order parameters
market_buy = MarketOrderRequest(
    symbol=random_stonk, qty=1, side=OrderSide.BUY, time_in_force=TimeInForce.GTC
)

market_sell = MarketOrderRequest(
    symbol=random_stonk, qty=1, side=OrderSide.SELL, time_in_force=TimeInForce.GTC
)

# order logic which buys if the overall sentiment is bearish and sells if the overall sentiment is bullish
if get_bear > get_bull:
    print("Inversing StockTwits sentiment....")
    trading_client.submit_order(order_data=market_buy)
    print("Long order for " + random_stonk + " placed.")
elif (
    get_bear < get_bull and trading_client.get_asset(random_stonk).shortable is True
):
    print("Inversing StockTwits sentiment....")
    trading_client.submit_order(order_data=market_sell)
    print("Short order for " + random_stonk + " placed.")
elif (
    get_bear < get_bull and trading_client.get_asset(random_stonk).shortable is False
):
    print("Cannot short this stock on Alpaca. Please choose another stock.")
elif get_bear and get_bull == 0:
    print("Not enough sentiment data to place order." "\n Please try again")
