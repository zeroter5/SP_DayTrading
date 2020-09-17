import dbConnector as db
import alpaca_trade_api as tradeapi
from Scrapers import redditScraper as rs
import datetime
from datetime import time
import alpacaDrip as ad
import pandas as pd
from numpy import float as floaty


if __name__ == '__main__':

    start = datetime.datetime.now()

    if datetime.datetime.now().time() > datetime.time(9,30):
        #initialize API information
        ALPACA_KEY_ID = 'PKQQ0N228HPEPFXJPNK1'
        ALPACA_SECRET_KEY = r'xGc19Nv8yzUTCJ7ISmf5h0U8pqxSzHAnxVwn5zp3'
        APCA_RETRY_MAX=1
        api = tradeapi.REST(
            key_id=ALPACA_KEY_ID,
            secret_key=ALPACA_SECRET_KEY,
            base_url='https://paper-api.alpaca.markets'
        )

        # Connect to the database
        connector = db.dbConnector()
        connection = connector.createConnection()

        #Create time window to make api call for
        window = datetime.datetime.now() - datetime.timedelta(minutes=1)
        unscreened_stocks = connector.getMentions(connection)
        count = 0
        barType = 'barType'
        strategy = ad.Strategy()
        # iterate through symbols getting bar info for each symbol of last minute
        for x in unscreened_stocks[0:50]:
            df = pd.DataFrame()
            tryCounter = 0
            # check if df has a value to account for API response time
            while df.empty and tryCounter < 5:
                df = api.get_barset(unscreened_stocks[count]["symbol"], '1Min', limit=1, after=window).df
                tryCounter +=1
            if not df.empty:
                # symbol - high - low - open - close - volume - shareCount - timestamp - barType
                try:
                    symbol = unscreened_stocks[count]["symbol"]
                    count += 1
                    connector.insertBar(str(symbol), floaty(df[symbol]['high'][0]), floaty(df[symbol]['low'][0]), floaty(df[symbol]['open'][0]),floaty(df[symbol]['close'][0]), floaty(df[symbol]['volume'][0]), connection)

                except Exception as e:
                    print(str(e))

    print("--- %s seconds ---" % (datetime.datetime.now() - start))
