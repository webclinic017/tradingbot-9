import secrets
from traderlib import *

class BullFlagPattern:

    def checkType1BullFlagPattern(self, stock, barset, stock_alert_file, stock_info, limit):

        try:  # fetch the data
            prev = None;
            bull = 0;
            bear = 0;
            count = 0;
            upflag = 0;
            downflag = 0;
            firstBull=0;
            returnObject = []
            counter=0
            for time, currentCandle in barset.iterrows():
                if count == 0:
                    prev = currentCandle
                    count = count + 1
                else:
                    bullOrBearCandle = self.candleType(stock, currentCandle);
                    if bullOrBearCandle == 'green' and self.isHigherThan(stock, prev, currentCandle) == 1:
                        if upflag == 1 and downflag == 1 and firstBull < currentCandle[stock]['close'] :
                            # This is the sign of bull flag.
                            print("Stock", stock, "Bull=", bull, " Upflag = ", upflag, "time", time)
                            print("Stock", stock, "Bear=", bear, " Downflag = ", downflag)
                            print("Stock", stock, "Bull flag detected at time", time, time.tz_convert('utc'))
                            print("Stock", stock, "Stoploss", prev[stock]['low'])
                            stock_name = stock+":"+str(time.tz_convert('utc'))
                            if stock_name not in stock_info:
                                current_stock_info = stock + ", " + "BullFlag1, " + str(time.tz_convert('utc')) + ", " + str(
                                    prev[stock]['low'])
                                stock_info[stock_name] = current_stock_info
                                stock_alert_file.write(current_stock_info)
                                stock_alert_file.write("\n")
                                stock_alert_file.flush()
                            else:
                                print("Key already present")

                            print()
                            returnObject.append(EntryCandleInformation(counter, prev[stock]['low'], barset, stock, limit, time))
                            downflag = 0
                            upflag = 0
                            bull = 0
                            bear = 0
                        elif downflag == 1:
                            downflag = 0
                            upflag = 0
                            bull = 0
                            bear = 0
                        if bull == 0:
                            firstBull = currentCandle[stock]['close'];
                        bull = bull + 1
                        if (bull >= 2):
                            upflag = 1;
                    elif bullOrBearCandle == 'red' and self.isLowerThan(stock, prev, currentCandle) == 1 and upflag == 1:
                        bear = bear + 1
                        if (bear >= 2):
                            downflag = 1;
                    elif bullOrBearCandle == 'green':
                        if upflag == 1 and downflag == 1 and firstBull < currentCandle[stock]['close'] :
                            # This is the sign of bull flag.
                            print("Stock", stock, "Bull=", bull, " Upflag = ", upflag, "time", time)
                            print("Stock", stock, "Bear=", bear, " Downflag = ", downflag)
                            print("Stock", stock, "Bull flag dected at time", time, time.tz_convert('utc'))
                            print("Stock", stock, "Stoploss", prev[stock]['low'])
                            stock_name = stock+":"+str(time.tz_convert('utc'))
                            if stock_name not in stock_info:
                                current_stock_info = stock + ", " + "BullFlag1, " + str(time.tz_convert('utc')) + ", " + str(
                                    prev[stock]['low'])
                                stock_info[stock_name] = current_stock_info
                                stock_alert_file.write(current_stock_info)
                                stock_alert_file.write("\n")
                                stock_alert_file.flush()
                            else:
                                print("Key already present")
                            print()
                            returnObject.append(EntryCandleInformation(counter, prev[stock]['low'], barset, stock, limit, time))
                        downflag = 0
                        upflag = 0
                        bull = 0
                        bear = 0
                    elif bullOrBearCandle == 'red':
                        downflag = 0
                        upflag = 0
                        bull = 0
                        bear = 0
                    prev = currentCandle;
                    counter = counter+1
        except Exception as e:
            print(e)
        return returnObject


    def checkType2BullFlagPattern(self, stock, barset, stock_alert_file, stock_info, limit):
        try:  # fetch the data
            prev = None;
            bull = 0;
            bear = 0;
            count = 0;
            upflag = 0;
            downflag = 0;
            firstBull=0;
            maxClose=0
            returnObject = []
            counter=0
            for time, j in barset.iterrows():
                if (count == 0):
                    prev = j
                    count = count + 1
                else:
                    bullOrBearCandle = self.candleType(stock, j);
                    if bullOrBearCandle == 'green' and self.isHigherThan(stock, prev, j) == 1:
                        if upflag == 1 and downflag == 1 and maxClose < j[stock]['close']:
                            # This is the sign of bull flag.
                            print("Stock", stock, "Bull=", bull, " Upflag = ", upflag, "time", time)
                            print("Stock", stock, "Bear=", bear, " Downflag = ", downflag)
                            print("Stock", stock, "Bull flag detected at time", time, time.tz_convert('utc'))
                            print("Stock", stock, "Stoploss", prev[stock]['low'])
                            stock_name = stock+":"+str(time.tz_convert('utc'))
                            if stock_name not in stock_info:
                                current_stock_info = stock + ", " + "BullFlag2, " + str(time.tz_convert('utc')) + ", " + str(
                                    prev[stock]['low'])
                                stock_info[stock_name] = current_stock_info
                                stock_alert_file.write(current_stock_info)
                                stock_alert_file.write("\n")
                                stock_alert_file.flush()
                            else:
                                print("Key already present")
                            returnObject.append(EntryCandleInformation(counter, prev[stock]['low'], barset, stock, limit, time))
                            print()
                            downflag = 0
                            upflag = 0
                            bull = 0
                            bear = 0
                            maxClose = 0
                        elif downflag == 1:
                            downflag = 0
                            upflag = 0
                            bull = 0
                            bear = 0
                            maxClose = 0
                        if bull == 0:
                            firstBull = j[stock]['close'];
                            maxClose = j[stock]['close'];
                        bull = bull + 1
                        if (bull >= 2):
                            upflag = 1;
                            maxClose = j[stock]['close'];

                    elif bullOrBearCandle == 'red' and self.isLowerThan(stock, prev, j) == 1 and upflag == 1:
                        bear = bear + 1
                        downflag=1;
                        if (bear >= 2):
                            downflag = 0;
                            maxClose = 0

                    elif bullOrBearCandle == 'green':
                        if upflag == 1 and downflag == 1 and maxClose < j[stock]['close']:
                            # This is the sign of bull flag.
                            print("Stock", stock, "Bull=", bull, " Upflag = ", upflag, "time", time)
                            print("Stock", stock, "Bear=", bear, " Downflag = ", downflag)
                            print("Stock", stock, "Bull flag dected at time", time, time.tz_convert('utc'))
                            print("Stock", stock, "Stoploss", prev[stock]['low'])
                            stock_name = stock+":"+str(time.tz_convert('utc'))
                            if stock_name not in stock_info:
                                current_stock_info = stock + ", " + "BullFlag2, " + str(time.tz_convert('utc')) + ", " + str(
                                    prev[stock]['low'])
                                stock_info[stock_name] = current_stock_info
                                stock_alert_file.write(current_stock_info)
                                stock_alert_file.write("\n")
                                stock_alert_file.flush()
                            else:
                                print("Key already present")
                            returnObject.append(EntryCandleInformation(counter, prev[stock]['low'], barset, stock, limit, time))
                            print()
                        downflag = 0
                        upflag = 0
                        bull = 0
                        bear = 0
                        maxClose = 0

                    elif bullOrBearCandle == 'red':
                        downflag = 0
                        upflag = 0
                        bull = 0
                        bear = 0
                        maxClose = 0

                    prev = j;
                    counter = counter + 1
        except Exception as e:
            print(e)
        return returnObject


    def candleType(self, stock, candle):
        open = candle[stock]['open'];
        close = candle[stock]['close'];
        high = candle[stock]['high']
        low = candle[stock]['low'];
        if (open > close):
            return "red"
        else:
            return "green"

    def isLowerThan(self, stock, prevCandle, currentCandle):
        if isinstance(prevCandle, type(None)):
            return 1;
        else:
            prevClose = prevCandle[stock]['close'];
            currentClose = currentCandle[stock]['close'];
            if (prevClose > currentClose):
                return 1;
            else:
                return 0;

    def isHigherThan(self, stock, prevCandle, currentCandle):
        if isinstance(prevCandle, type(None)):
            return 1;
        else:
            prevClose = prevCandle[stock]['close'];
            currentClose = currentCandle[stock]['close'];
            if (prevClose < currentClose):
                return 1;
            else:
                return 0;

    def isVolumeHigherThanPrev(self, stock, prevCandle, currentCandle):
        if isinstance(prevCandle, type(None)):
            return 1;
        else:
            prevVol = prevCandle[stock]['volume'];
            currentVol = currentCandle[stock]['volume'];
            if (prevVol < currentVol):
                return 1;
            else:
                return 0;


class EntryCandleInformation:
    def __init__(self, postion, stoploss, barset, stock, total, time):
        self.stock = stock
        self.postion = postion
        self.stoploss = stoploss
        self.barset = barset
        self.total = total;
        self.time = time;

