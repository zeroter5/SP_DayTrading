#import pymysql.cursors
import pymysql
from datetime import date

class dbConnector:
    def __init__(self):
        print("")
    def createConnection(self):
        # Connect to the database

        connection = pymysql.connect(host='10.0.1.14',
                                 user='trade',
                                 password='autotrade',
                                 db='GrandExchange',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
        return connection

    def insertBar(self, symbol, high, low, open, close, volume, connection):
        try:
            with connection.cursor() as cursor:
                # Create a new record
                #print(symbol, high, low, open, close, volume, connection)
                sql = "INSERT INTO `Stonks` (`symbol`, `high`, `low`, `open`, `close`, `volume`) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (symbol, high, low, open, close, volume))
                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connection.commit()
        except Exception as e:
            print(str(e))
            return False
        finally:
            return True
    def insertTrade(self, symbol, high, low, open, close, volume, shareCount, tradeType, connection, takeProfit, takeLoss):
        #try:
            with connection.cursor() as cursor:
                # Create a new record

                sql = "INSERT INTO `Trades` (`symbol`, `high`, `low`, `open`, `close`, `volume`, `shareCount`, `tradeType`, `takeProfit`, `takeLoss`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (symbol, high, low, open, close, volume, shareCount, tradeType, takeProfit, takeLoss))

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connection.commit()
        #except ConnectionError:
         #   print("Connection Error")
          #  return False
        #finally:
            return True
    def insertMention(self, symbol, connection):
        try:
            with connection.cursor() as cursor:
                # Create a new record

                sql = "INSERT INTO `Mentions` (`symbol`) VALUES (%s)"
                cursor.execute(sql, (symbol))

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connection.commit()
        except Exception as e:
            print(str(e))
            return False
        finally:
            return True

    def insertMarketWatchObject(self, symbol, price, change, changePercent, volume, connection):
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `MarketWatch` (`symbol`, `price`, `priceChange`, `changePercent`, `volume`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (symbol, price, change, changePercent, volume))

                # connection is not autocommit by default. So you must commit to saveyour changes.
                connection.commit()
        except Exception as e:
            print(str(e))
            return False
        finally:
            return True


    def getBarsByTime(self, connection, timestamp):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `Stonks` WHERE `timestamp` > %s ORDER BY timestamp DESC"
            cursor.execute(sql, (timestamp))
            result = cursor.fetchall()
        return result
    def getBarsByTimeWindow(self, connection, start, end, symbol):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `Stonks` WHERE `symbol` = %s AND `timestamp` BETWEEN %s AND %s ORDER BY symbol ASC"
            cursor.execute(sql, (symbol, start, end))
            result = cursor.fetchall()
        return result
    def getBarsBySymbol(self, connection, symbol):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `Stonks` WHERE `symbol`=%s"
            cursor.execute(sql, (symbol))
            result = cursor.fetchall()
        return result
    def getBarsByBarType(self, connection, barType):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `Stonks` WHERE `barType`=%s"
            cursor.execute(sql, (barType))
            result = cursor.fetchall()
        return result
    def getTradeByTradeType(self, connection, tradeType):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `Trades` WHERE `tradeType`=%s"
            cursor.execute(sql, (tradeType))
            result = cursor.fetchall()
        return result
    def getTradeBySymbol(self, connection, symbol):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `Trades` WHERE `symbol`=%s"
            cursor.execute(sql, (symbol))
            result = cursor.fetchall()
        return result
    def getTradeRecents(self, connection, time):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `Trades` WHERE `timestamp` > %s ORDER BY timestamp DESC"
            cursor.execute(sql, (time))
            result = cursor.fetchall()
        return result
    def getMentions(self, connection):
        with connection.cursor() as cursor:
            timestamp = date.today()
            sql = "SELECT symbol FROM `Mentions` WHERE `timestamp` > %s "
            cursor.execute(sql, timestamp)
            result = cursor.fetchall()
        return result
    def getAllDistinctMentions(self, connection):
        with connection.cursor() as cursor:
            sql = "SELECT DISTINCT symbol FROM `Mentions`"
            cursor.execute(sql)
            result = cursor.fetchall()
        return result

    def getMarketWatchData(self, connection):
        with connection.cursor() as cursor:
            sql = "SELECT symbol FROM `MarketWatch`"
            cursor.execute(sql)
            result = cursor.fetchall()
        return result

    def purgeMarketWatchDB(self, connection):
        with connection.cursor() as cursor:
            sql = "Delete FROM `MarketWatch`"
            cursor.execute(sql)
        return True
    def purgeMentions(self, connection):
        with connection.cursor() as cursor:
            sql = "Delete FROM `Mentions`"
            cursor.execute(sql)
        return True
    def insertPosition(self, connection, symbol, algo):
        with connection.cursor() as cursor:
            sql = "INSERT INTO `currentPositions` (`symbol`, `position`, `algorithm`) VALUES (%s, 1, %s)"
            cursor.execute(sql, (symbol, algo))
            connection.commit()
        return True
    def modifyPosition(self, connection, symbol,position, algo):
        with connection.cursor() as cursor:
            sql = "UPDATE `currentPositions` SET `position` = %s WHERE `symbol` = %s AND `algorithm` = %s"
            cursor.execute(sql, (position, symbol, algo))
            connection.commit()
        return True
    def getPosition(self,connection,symbol, algo):
        with connection.cursor() as cursor:
            sql = "SELECT position FROM `currentPositions` WHERE `symbol` = %s AND `algorithm` = %s"
            cursor.execute(sql,(symbol, algo))
            result = cursor.fetchall()
        return result
    def insertCash(self, connection, value):
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `currentCash` (cash) VALUES (%s)"
                cursor.execute(sql,value)
                connection.commit()
        except Exception as e:
            print(str(e))
            return False
        finally:
            return True

    def addCash(self, connection, value, id):
        with connection.cursor() as cursor:
            sql = "UPDATE `currentCash` SET `cash` = `cash` + %s WHERE `id` = %s"
            cursor.execute(sql, (value,id))
            connection.commit()
        return True
    def subtractCash(self, connection, value, id):
        with connection.cursor() as cursor:
            sql = "UPDATE `currentCash` SET `cash` = `cash` - %s WHERE `id` = %s"
            cursor.execute(sql, (value,id))
            connection.commit()
        return True
    def getCash(self,connection,id):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT cash FROM `currentCash` WHERE `id` = %s"
                cursor.execute(sql,id)
                result = cursor.fetchall()
        except Exception as e:
            print(str(e))
            return False
        finally:
            return result
    def getSharesFromLastTradeOnSymbol(self, connection, symbol, tradeType):
            with connection.cursor() as cursor:
                sql = "SELECT shareCount FROM `Trades` WHERE `symbol` = %s AND `tradeType` = %s ORDER BY `timestamp` DESC"
                cursor.execute(sql,(symbol,tradeType))
                result = cursor.fetchall()
            return result
    def getLossProfitFromLastTradeOnSymbol(self, connection, symbol, tradeType):
        with connection.cursor() as cursor:
            sql = "SELECT takeProfit, takeLoss FROM `Trades` WHERE `symbol` = %s AND `tradeType` = %s ORDER BY `timestamp` DESC"
            cursor.execute(sql,(symbol,tradeType))
            result = cursor.fetchall()
        return result
    def setStartCash(self, connection, cash, date):
        with connection.cursor() as cursor:
            sql = "INSERT INTO `Results` (`startCash`, `date`) VALUES (%s, %s)"
            cursor.execute(sql, (cash,date))
            connection.commit()
        return True
    def setEndCash(self, connection, cash, date):
        with connection.cursor() as cursor:
            sql = "UPDATE `Results` SET `endCash` = %s WHERE `date` = %s"
            cursor.execute(sql, (cash,date))
            connection.commit()
        return True
    def setResultCash(self, connection):
        with connection.cursor() as cursor:
            sql = "UPDATE `Results` SET `resultCash` = `endCash` - `startCash`"
            cursor.execute(sql)
            connection.commit()
        return True
    def getResultsByDate(self,connection, date):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT startCash, endCash, resultCash, date FROM `Results` WHERE `date` >= %s"
                cursor.execute(sql,date)
                result = cursor.fetchall()
        except Exception as e:
            print(str(e))
            return False
        finally:
            return result
    def getTradesAlgoAndDate(self,connection, tradeType1, tradeType2, tradeType3, tradeType4, tradeType5, tradeType6):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT symbol, close, tradeType, timestamp FROM `Trades` WHERE DATE(`timestamp`) > CURDATE() - INTERVAL 12 DAY and DATE(`timestamp`) < CURDATE() - INTERVAL 6 DAY and (tradeType = %s or tradeType = %s or tradeType = %s or tradeType = %s or tradeType = %s or tradeType = %s)"
                cursor.execute(sql,(tradeType1,tradeType2,tradeType3,tradeType4, tradeType5, tradeType6))
                result = cursor.fetchall()
        except Exception as e:
            print(str(e))
            return False
        finally:
            return result