import datetime
import time
from datetime import time
import sys
from numpy import float as floaty
import numpy as np
sys.path.append('/Users/ryan/IdeaProjects/SP_DayTrading/')

import dbConnector as db
import alpacaDrip as ad


def isMorningStar(bar):

    if True == np.where (bar[0]['open'] > bar[1]['open'] and bar[2]['open'] < bar[1]['open'], True,False):

        if True == np.where(bar[0]['volume'] > bar[1]['volume'] and bar[2]['volume'] > bar[1]['volume'], True, False):

            if True == np.where(bar[2]['volume'] >= (.96 * bar[1]['volume']), True, False):

                if True == np.where(bar[0]['low'] >= bar[1]['low'] and bar[2]['low'] < bar[0]['low'], True, False):

                    return True

if __name__ == "__main__":

        #start this strategy at 9:35 AM
            #start_time = time()
            if datetime.datetime.now().time() > datetime.time(9,35):
                #print("here")
                # Connect to the database
                connector = db.dbConnector()
                connection = connector.createConnection()

                #create time window (5min intervals updated each minute)
                now = datetime.datetime.now()
                window = datetime.datetime.now() - datetime.timedelta(minutes=3)
                symbols = connector.getMentions(connection)
                strategy = ad.Strategy()
                ############ make value dynamic
                #cash = 25000
                cash = connector.getCash(connection,8)
                cash = cash[0]['cash']
                ############

                #barNumber = 0
                buyPrice = 0
                shares = 0
                takeProfitPercent = 1.03
                lossProfitPercent = .97
                maxPosition = cash * .1
                buyClose = datetime.time(15,00)
                alltrades = []

                takeProfit = floaty()
                lossProfit = floaty()
                for x in symbols[0:50]:
                    workingSet = connector.getBarsByTimeWindow(connection, window, now, x['symbol'])


                    if len(workingSet) == 3:
                        #print(workingSet)
                        currentBar = len(workingSet)-1
                        #print(workingSet[0]['close'])

                        currentPosition = connector.getPosition(connection, x['symbol'],'morningStar')
                        existingPosition = 0
                        if len(currentPosition) == 0:
                            currentPosition = 0
                        else:
                            currentPosition = currentPosition[0]['position']
                            targets = connector.getLossProfitFromLastTradeOnSymbol(connection, x['symbol'], 'morningStarBuy')
                            if targets:
                                takeProfit = targets[0]['takeProfit']
                                lossProfit = targets[0]['takeLoss']
                            existingPosition = 1
                        closePrice = workingSet[currentBar]['close']
                        print("pre buy conditionalg")
                        if isMorningStar(workingSet) and currentPosition != 1 and buyClose > workingSet[currentBar]['timestamp'].time():
                                    print("mbuy")
                                    buyPrice = workingSet[currentBar]['close']
                                    shares = int(maxPosition / closePrice)
                                    cash = shares * closePrice
                                    connector.subtractCash(connection, cash, 8)
                                    takeProfit = takeProfitPercent * buyPrice
                                    lossProfit = lossProfitPercent * buyPrice
                                    #if strategy.submitBuyOrder(x['symbol'], shares, buyPrice):
                                    if existingPosition == 0:
                                            connector.insertPosition(connection,workingSet[currentBar]['symbol'], 'morningStar')
                                    else:
                                            connector.modifyPosition(connection,workingSet[currentBar]['symbol'], 1, 'morningStar')
                                    connector.insertTrade(workingSet[currentBar]['symbol'], workingSet[currentBar]['high'], workingSet[currentBar]['low'], workingSet[currentBar]['open'], workingSet[currentBar]['close'], workingSet[currentBar]['volume'], shares, workingSet[currentBar]['barType'], 'morningStarBuy', connection, takeProfit, lossProfit)


                        if currentPosition == 1:
                                    if closePrice >= takeProfit:
                                            print("msell")
                                            uncleanShareCount = connector.getSharesFromLastTradeOnSymbol(connection,workingSet[currentBar]['symbol'], 'morningStarBuy')
                                            shares = uncleanShareCount[0]['shareCount']
                                            cashChange = (shares * closePrice)
                                            #if strategy.submitSellOrder(x['symbol'], shares):
                                            connector.addCash(connection, cashChange, 8)
                                            connector.modifyPosition(connection,workingSet[currentBar]['symbol'], 0,'morningStar')
                                            connector.insertTrade(workingSet[currentBar]['symbol'], workingSet[currentBar]['high'], workingSet[currentBar]['low'], workingSet[currentBar]['open'], workingSet[currentBar]['close'], workingSet[currentBar]['volume'], shares, workingSet[currentBar]['barType'], 'morningStarSellAtTakeProfit', connection,0,0)



                                    elif closePrice <= lossProfit:
                                        print("msell")
                                        uncleanShareCount = connector.getSharesFromLastTradeOnSymbol(connection,workingSet[currentBar]['symbol'], 'morningStarBuy')
                                        shares = uncleanShareCount[0]['shareCount']
                                        cashChange = (shares * closePrice)
                                        #if strategy.submitSellOrder(x['symbol'], shares):
                                        connector.addCash(connection, cashChange, 8)
                                        connector.modifyPosition(connection,workingSet[currentBar]['symbol'],0,'morningStar')
                                        connector.insertTrade(workingSet[currentBar]['symbol'], workingSet[currentBar]['high'], workingSet[currentBar]['low'], workingSet[currentBar]['open'], workingSet[currentBar]['close'], workingSet[currentBar]['volume'], shares, workingSet[currentBar]['barType'], 'morningStarSellAtLossStop', connection,0,0)


                                    elif buyClose <= workingSet[currentBar]['timestamp'].time():
                                        print("msell")
                                        uncleanShareCount = connector.getSharesFromLastTradeOnSymbol(connection,workingSet[currentBar]['symbol'], 'morningStarBuy')
                                        shares = uncleanShareCount[0]['shareCount']
                                        cashChange = (shares * closePrice)
                                        #if strategy.submitSellOrder(x['symbol'], shares):
                                        connector.addCash(connection, cashChange, 8)
                                        connector.modifyPosition(connection,workingSet[currentBar]['symbol'],0, 'morningStar')
                                        connector.insertTrade(workingSet[currentBar]['symbol'], workingSet[currentBar]['high'], workingSet[currentBar]['low'], workingSet[currentBar]['open'], workingSet[currentBar]['close'], workingSet[currentBar]['volume'], shares, workingSet[currentBar]['barType'], 'morningStarSellAtBuyClose', connection,0,0)

            #print("--- %s seconds ---" % (time() - start_time))


