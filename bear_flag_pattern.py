import secrets
from traderlib import *

class BearFlagPattern:

    def checkType1BearFlagPattern(self, stock, interval='5Min', limit=100):

        api = tradeapi.REST(secrets.API_KEY, secrets.API_SECRET_KEY, secrets.ALPACA_API_URL, api_version='v2')

        try:  # fetch the data
            bar_iter = api.get_barset(stock, interval, limit).df
            prev = None;
            bull = 0;
            bear = 0;
            count = 0;
            upflag = 0;
            downflag = 0;
            firstBear=0;
            for timeStamp, currentCandle in bar_iter.iterrows():
                if (count == 0):
                    prev = currentCandle
                    count = count + 1
                else:
                    bullOrBearCandle = self.candleType(stock, currentCandle);
                    if bullOrBearCandle == 'red' and self.isLowerThan(stock, prev, currentCandle) == 1:
                        if upflag == 1 and downflag == 1 and firstBear > currentCandle[stock]['close'] :
                            # This is the sign of bull flag.
                            print("Stock", stock, "Bear=", bull, " Downflag = ", downflag, "time", timeStamp)
                            print("Stock", stock, "Bull=", bear, " Upflag = ", upflag)
                            print("Stock", stock, "Bear flag detected at time", timeStamp, timeStamp.tz_convert('utc'))
                            print("Stock", stock, "Stoploss", prev[stock]['high'])
                            print()
                            downflag = 0
                            upflag = 0
                            bull = 0
                            bear = 0
                        elif upflag == 1:
                            downflag = 0
                            upflag = 0
                            bull = 0
                            bear = 0
                        if bear == 0:
                            firstBear = currentCandle[stock]['close'];
                            #ema10 = ti.ema(stock.df.close.dropna().to_numpy(), 10)

                        bear = bear + 1
                        if (bear >= 2):
                            downflag = 1;
                    elif bullOrBearCandle == 'green' and self.isHigherThan(stock, prev, currentCandle) == 1 and downflag == 1:
                        bull = bull + 1
                        if (bull >= 2):
                            upflag = 1;
                    elif bullOrBearCandle == 'red':
                        if upflag == 1 and downflag == 1 and firstBear > currentCandle[stock]['close'] :
                            # This is the sign of bull flag.
                            print("Stock", stock, "Bear=", bull, " Downflag = ", downflag, "time", timeStamp)
                            print("Stock", stock, "Bull=", bear, " Upflag = ", upflag)
                            print("Stock", stock, "Bear flag detected at time", timeStamp, timeStamp.tz_convert('utc'))
                            print("Stock", stock, "Stoploss", prev[stock]['high'])
                            print()
                        downflag = 0
                        upflag = 0
                        bull = 0
                        bear = 0
                    elif bullOrBearCandle == 'green':
                        downflag = 0
                        upflag = 0
                        bull = 0
                        bear = 0
                    prev = currentCandle;

        except Exception as e:
            print(e)

    def checkType2BearFlagPattern(self, stock, interval='5Min', limit=100):

        api = tradeapi.REST(secrets.API_KEY, secrets.API_SECRET_KEY, secrets.ALPACA_API_URL, api_version='v2')

        try:  # fetch the data
            bar_iter = api.get_barset(stock, interval, limit).df
            prev = None;
            bull = 0;
            bear = 0;
            count = 0;
            upflag = 0;
            downflag = 0;
            firstBear=0;
            maxClose=0
            for timeStamp, currentCandle in bar_iter.iterrows():
                if (count == 0):
                    prev = currentCandle
                    count = count + 1
                else:
                    bullOrBearCandle = self.candleType(stock, currentCandle);
                    if bullOrBearCandle == 'red' and self.isLowerThan(stock, prev, currentCandle) == 1:
                        if upflag == 1 and downflag == 1 and maxClose > currentCandle[stock]['close']:
                            # This is the sign of bull flag.
                            print("Stock", stock, "Bear=", bull, " Downflag = ", downflag, "time", timeStamp)
                            print("Stock", stock, "Bull=", bear, " Upflag = ", upflag)
                            print("Stock", stock, "Bear flag detected at time", timeStamp, timeStamp.tz_convert('utc'))
                            print("Stock", stock, "Stoploss", prev[stock]['high'])
                            print()
                            downflag = 0
                            upflag = 0
                            bull = 0
                            bear = 0
                            maxClose = 0
                        elif upflag == 1:
                            downflag = 0
                            upflag = 0
                            bull = 0
                            bear = 0
                            maxClose = 0
                        if bear == 0:
                            firstBear = currentCandle[stock]['close'];
                            maxClose = currentCandle[stock]['close'];
                        bear = bear + 1
                        if (bear >= 2):
                            downflag = 1;
                            maxClose = currentCandle[stock]['close'];

                    elif bullOrBearCandle == 'green' and self.isHigherThan(stock, prev, currentCandle) == 1 and downflag == 1:
                        bull = bull + 1
                        upflag=1;
                        if (bull >= 2):
                            upflag = 0;
                            maxClose = 0

                    elif bullOrBearCandle == 'red':
                        if upflag == 1 and downflag == 1 and maxClose > currentCandle[stock]['close']:
                            print("Stock", stock, "Bear=", bull, " Downflag = ", downflag, "time", time)
                            print("Stock", stock, "Bull=", bear, " Upflag = ", upflag)
                            print("Stock", stock, "Bear flag detected at time", timeStamp, timeStamp.tz_convert('utc'))
                            print("Stock", stock, "Stoploss", prev[stock]['high'])
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

                    prev = currentCandle;

        except Exception as e:
            print(e)


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
