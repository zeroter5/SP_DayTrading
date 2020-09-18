import sys
sys.path.append('/Users/ryan/IdeaProjects/SP_DayTrading/')
import dbConnector as db
from Scrapers import redditScraper as rs
from Scrapers import marketwatchScraper as ms



if __name__ == '__main__':

    # Connect to the database
    connector = db.dbConnector()
    connection = connector.createConnection()

    #get stocks from reddit
    redditScraperStocks = rs.scrape()
    symbols = [i[0] for i in redditScraperStocks]
    print(symbols)

    #marketWatch
    marketWatchObjects = ms.scrape()
    marketWatchStocks = []
    for stockObject in marketWatchObjects:
        marketWatchStocks.append(stockObject.symbol)
    print(marketWatchStocks)

    for x in marketWatchStocks[1:75]:
        connector.insertMention(x,connection)
    for x in symbols[1:75]:
        connector.insertMention(x,connection)
    print("daily scrape executed")
