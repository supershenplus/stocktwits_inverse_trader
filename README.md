# stocktwits_inverser
A script thats find a random stock, then invereses the sentiment of StockTwits users. The logic behind this is that the average StockTwits user is more wrong than right :D. 

This is done on a paper trading account and is just for fun.

This script utilizies Selenium, a web automation tool, and Alpaca Markets, an API for Crypto and Stock Trading. We can pull a random stock using this neat site ttps://raybb.github.io/random-stock-picker/ and then verify it is listed on StockTwits. Once we have a valid stock, the script will automatically scroll through the stock tickers feed and count the number of posts tagged with Bullish and Bearish. Once the count has been finished it will place a trade based on the opposite overall sentiment displayed by StockTwits users.

I plan on improving the code and adding more features soon! 
