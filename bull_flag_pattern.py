
from traderlib import *

class BullFlagPattern:

    def checkType1BullFlagPattern(self, stock, interval='5Min', limit=100):

        api = tradeapi.REST(gvars.API_KEY, gvars.API_SECRET_KEY, gvars.ALPACA_API_URL, api_version='v2')

        try:  # fetch the data
            bar_iter = api.get_barset(stock, interval, limit).df
            prev = None;
            bull = 0;
            bear = 0;
            count = 0;
            upflag = 0;
            downflag = 0;
            firstBull=0;
            for time, currentCandle in bar_iter.iterrows():
                if (count == 0):
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
                            print()
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
                            #ema10 = ti.ema(stock.df.close.dropna().to_numpy(), 10)

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
                            print("Stock", stock, "Stoploss", prev[stock]['close'])
                            print()
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

        except Exception as e:
            print(e)

    def checkType2BullFlagPattern(self, stock, interval='5Min', limit=100):

        api = tradeapi.REST(gvars.API_KEY, gvars.API_SECRET_KEY, gvars.ALPACA_API_URL, api_version='v2')

        try:  # fetch the data
            bar_iter = api.get_barset(stock, interval, limit).df
            prev = None;
            bull = 0;
            bear = 0;
            count = 0;
            upflag = 0;
            downflag = 0;
            firstBull=0;
            maxClose=0
            for i, j in bar_iter.iterrows():
                if (count == 0):
                    prev = j
                    count = count + 1
                else:
                    bullOrBearCandle = self.candleType(stock, j);
                    if bullOrBearCandle == 'green' and self.isHigherThan(stock, prev, j) == 1:
                        if upflag == 1 and downflag == 1 and maxClose < j[stock]['close']:
                            # This is the sign of bull flag.
                            print("Stock", stock, "Bull=", bull, " Upflag = ", upflag, "time", i)
                            print("Stock", stock, "Bear=", bear, " Downflag = ", downflag)
                            print("Stock", stock, "Bull flag detected at time", i, i.tz_convert('utc'))
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
                            print("Stock", stock, "Bull=", bull, " Upflag = ", upflag, "time", i)
                            print("Stock", stock, "Bear=", bear, " Downflag = ", downflag)
                            print("Stock", stock, "Bull flag dected at time", i, i.tz_convert('utc'))
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
