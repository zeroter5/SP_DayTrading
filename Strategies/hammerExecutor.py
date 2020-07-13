import datetime
import time
import sys
from numpy import float as floaty

sys.path.append('/home/trade/Desktop/SP_DayTrading/')

import dbConnector as db
import alpacaDrip as ad



if __name__ == "__main__":

        #start this strategy at 9:35 AM
            start_time = time.time()
        #if datetime.datetime.now().time() > datetime.time(9,35) and datetime.datetime.now().time() < datetime.time(4,00):
            # Connect to the database
            connector = db.dbConnector()
            connection = connector.createConnection()

            #create time window (5min intervals updated each minute)
            now = datetime.datetime.now()
            window = datetime.datetime.now() - datetime.timedelta(minutes=5)
            symbols = connector.getMentions(connection)
            strategy = ad.Strategy()
            ############ make value dynamic
            #cash = 25000
            cash = connector.getCash(connection,9)
            cash = cash[0]['cash']
            ############
            sma = 0
            #barNumber = 0
            buyPrice = 0
            shares = 0
            takeProfitPercent = 1.06
            lossProfitPercent = .96
            maxPosition = cash * .1
            buyClose = datetime.time(hour=3, minute=0, second=0, microsecond=0)
            alltrades = []

            takeProfit = floaty()
            lossProfit = floaty()
            for x in symbols[0:100]:
                workingSet = connector.getBarsByTimeWindow(connection, window, now, x['symbol'])
                if len(workingSet) == 5:
                    #print(workingSet)
                    currentBar = len(workingSet)-1
                    #print(workingSet[0]['close'])
                    sma = strategy.simpleMovingAverageAcrossTime(workingSet,0,currentBar)
                    barNumber = 0
                    currentPosition = connector.getPosition(connection, x['symbol'])
                    #print(sma)
                    if len(currentPosition) == 0:
                        currentPosition = 0
                    else:
                        currentPosition = currentPosition[0]['position']
                        closePrice = workingSet[barNumber]['close']
                        if strategy.isHammerBar(workingSet[currentBar]) and sma < 0:
                                alltrades.append(str((x[currentBar])) + ' Buy at: ' + str(closePrice))
                                buyPrice = x[currentBar]['close']
                                shares = int(maxPosition / closePrice)
                                cash = cash - shares * closePrice
                                connector.modifyCash(connection, cash, 1)
                                takeProfit = takeProfitPercent * buyPrice
                                lossProfit = lossProfitPercent * buyPrice
                                connector.modifyPosition(connection,workingSet[currentBar]['symbol'])
                                connector.insertTrade(workingSet[currentBar]['symbol'], workingSet[currentBar]['high'], workingSet[currentBar]['low'], workingSet[currentBar]['open'], workingSet[currentBar]['close'], workingSet[currentBar]['volume'], 0, workingSet[currentBar]['barType'], 'hammerBuy', connection)


                        if currentPosition == 1:
                                if closePrice >= takeProfit:
                                    if (buyPrice < closePrice):
                                        alltrades.append(str((x[currentBar])) + ' Sell at: ' + str(closePrice))
                                        cash += (shares * closePrice)
                                        connector.modifyCash(connection, cash, 1)
                                        print(alltrades[len(alltrades)-1])
                                        connector.modifyPosition(connection,workingSet[currentBar]['symbol'])
                                        connector.insertTrade(workingSet[currentBar]['symbol'], workingSet[currentBar]['high'], workingSet[currentBar]['low'], workingSet[currentBar]['open'], workingSet[currentBar]['close'], workingSet[currentBar]['volume'], 0, workingSet[currentBar]['barType'], 'hammerSell', connection)



                        elif closePrice <= lossProfit:
                                    alltrades.append(str((x[currentBar])) + ' Sell at: ' + str(closePrice))
                                    cash += (shares * closePrice)
                                    connector.modifyCash(connection, cash, 1)
                                    connector.modifyPosition(connection,x['symbol'])
                                    print(alltrades[len(alltrades)-1])
                                    connector.insertTrade(workingSet[currentBar]['symbol'], workingSet[currentBar]['high'], workingSet[currentBar]['low'], workingSet[currentBar]['open'], workingSet[currentBar]['close'], workingSet[currentBar]['volume'], 0, workingSet[currentBar]['barType'], 'hammerSell', connection)


                        elif buyClose <= workingSet[barNumber]['timestamp'].time():
                                    alltrades.append(str((df.index[currentBar])) + ' Sell at: ' + str(closePrice))
                                    cash += (shares * closePrice)
                                    connector.modifyCash(connection, cash, 1)
                                    connector.modifyPosition(connection,workingSet[currentBar]['symbol'])
                                    print(alltrades[len(alltrades)-1])
                                    connector.insertTrade(workingSet[currentBar]['symbol'], workingSet[currentBar]['high'], workingSet[currentBar]['low'], workingSet[currentBar]['open'], workingSet[currentBar]['close'], workingSet[currentBar]['volume'], 0, workingSet[currentBar]['barType'], 'hammerSell', connection)

            print("--- %s seconds ---" % (time.time() - start_time))
