class BullFlagPattern:

    def checkType1BullFlagPattern(self, stock, barset, stock_alert_file, stock_info, limit):

        try:  # fetch the data
            prev = None;
            bull = 0;
            bear = 0;
            count = 0;
            upflag = 0;
            downflag = 0;
            first_bull = 0;
            return_object = []
            counter = 0
            for time, current_candle in barset.iterrows():
                if count == 0:
                    prev = current_candle
                    count = count + 1
                else:
                    bull_or_bear_candle = self.candleType(stock, current_candle);
                    if bull_or_bear_candle == 'green' and self.isHigherThan(stock, prev, current_candle) == 1:
                        if upflag == 1 and downflag == 1 and first_bull < current_candle[stock]['close']:
                            # This is the sign of bull flag.
                            print("Type 1 Bull flag detected for Stock", stock, "Bull=", bull, " Upflag = ", upflag, "time", time, "Bear=", bear, " Downflag = ", downflag, " UTC Time = ", time.tz_convert('utc'), "Stoploss", prev[stock]['low'])
                            stock_name = stock + ":" + str(time.tz_convert('utc'))
                            if stock_name not in stock_info:
                                current_stock_info = stock + ", " + "BullFlag1, " + str(
                                    time.tz_convert('utc')) + ", " + str(
                                    prev[stock]['low'])
                                stock_info[stock_name] = current_stock_info
                                stock_alert_file.write(current_stock_info)
                                stock_alert_file.write("\n")
                                stock_alert_file.flush()
                            else:
                                print("Key already present")

                            print()
                            return_object.append(
                                EntryCandleInformation(counter, prev[stock]['low'], barset, stock, limit, time))
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
                            first_bull = current_candle[stock]['close'];
                        bull = bull + 1
                        if (bull >= 2):
                            upflag = 1;
                    elif bull_or_bear_candle == 'red' and self.isLowerThan(stock, prev,
                                                                           current_candle) == 1 and upflag == 1:
                        bear = bear + 1
                        if (bear >= 2):
                            downflag = 1;
                    elif bull_or_bear_candle == 'green':
                        if upflag == 1 and downflag == 1 and first_bull < current_candle[stock]['close']:
                            # This is the sign of bull flag.
                            print("Type 1 Bull flag detected for Stock", stock, "Bull=", bull, " Upflag = ", upflag, "time", time, "Bear=", bear, " Downflag = ", downflag, " UTC Time = ", time.tz_convert('utc'), "Stoploss", prev[stock]['low'])
                            stock_name = stock + ":" + str(time.tz_convert('utc'))
                            if stock_name not in stock_info:
                                current_stock_info = stock + ", " + "BullFlag1, " + str(
                                    time.tz_convert('utc')) + ", " + str(
                                    prev[stock]['low'])
                                stock_info[stock_name] = current_stock_info
                                stock_alert_file.write(current_stock_info)
                                stock_alert_file.write("\n")
                                stock_alert_file.flush()
                            else:
                                print("Key already present")
                            print()
                            return_object.append(
                                EntryCandleInformation(counter, prev[stock]['low'], barset, stock, limit, time))
                        downflag = 0
                        upflag = 0
                        bull = 0
                        bear = 0
                    elif bull_or_bear_candle == 'red':
                        downflag = 0
                        upflag = 0
                        bull = 0
                        bear = 0
                    prev = current_candle;
                    counter = counter + 1
        except Exception as e:
            print(e)
        return return_object

    def checkType2BullFlagPattern(self, stock, barset, stock_alert_file, stock_info, limit):
        try:  # fetch the data
            prev = None;
            bull = 0;
            bear = 0;
            count = 0;
            upflag = 0;
            downflag = 0;
            max_close = 0
            return_object = []
            counter = 0
            for time, current_candle in barset.iterrows():
                if count == 0:
                    prev = current_candle
                    count = count + 1
                else:
                    bull_or_bear_candle = self.candleType(stock, current_candle);
                    if bull_or_bear_candle == 'green' and self.isHigherThan(stock, prev, current_candle) == 1:
                        if upflag == 1 and downflag == 1 and max_close < current_candle[stock]['close']:
                            # This is the sign of bull flag.
                            print("Type 2 Bull flag detected for Stock", stock, "Bull=", bull, " Upflag = ", upflag, "time", time, "Bear=", bear, " Downflag = ", downflag, " UTC Time = ", time.tz_convert('utc'), "Stoploss", prev[stock]['low'])
                            stock_name = stock + ":" + str(time.tz_convert('utc'))
                            if stock_name not in stock_info:
                                current_stock_info = stock + ", " + "BullFlag2, " + str(
                                    time.tz_convert('utc')) + ", " + str(
                                    prev[stock]['low'])
                                stock_info[stock_name] = current_stock_info
                                stock_alert_file.write(current_stock_info)
                                stock_alert_file.write("\n")
                                stock_alert_file.flush()
                            else:
                                print("Key already present")
                            return_object.append(
                                EntryCandleInformation(counter, prev[stock]['low'], barset, stock, limit, time))
                            print()
                            downflag = 0
                            upflag = 0
                            bull = 0
                            bear = 0
                            max_close = 0
                        elif downflag == 1:
                            downflag = 0
                            upflag = 0
                            bull = 0
                            bear = 0
                            max_close = 0
                        if bull == 0:
                            max_close = current_candle[stock]['close'];
                        bull = bull + 1
                        if bull >= 2:
                            upflag = 1;
                            max_close = current_candle[stock]['close'];

                    elif bull_or_bear_candle == 'red' and self.isLowerThan(stock, prev,
                                                                           current_candle) == 1 and upflag == 1:
                        bear = bear + 1
                        downflag = 1;
                        if (bear >= 2):
                            downflag = 0;
                            max_close = 0

                    elif bull_or_bear_candle == 'green':
                        if upflag == 1 and downflag == 1 and max_close < current_candle[stock]['close']:
                            # This is the sign of bull flag.
                            print("Type 2 Bull flag detected for Stock", stock, "Bull=", bull, " Upflag = ", upflag, "time", time, "Bear=", bear, " Downflag = ", downflag, " UTC Time = ", time.tz_convert('utc'), "Stoploss", prev[stock]['low'])
                            stock_name = stock + ":" + str(time.tz_convert('utc'))
                            if stock_name not in stock_info:
                                current_stock_info = stock + ", " + "BullFlag2, " + str(
                                    time.tz_convert('utc')) + ", " + str(
                                    prev[stock]['low'])
                                stock_info[stock_name] = current_stock_info
                                stock_alert_file.write(current_stock_info)
                                stock_alert_file.write("\n")
                                stock_alert_file.flush()
                            else:
                                print("Key already present")
                            return_object.append(
                                EntryCandleInformation(counter, prev[stock]['low'], barset, stock, limit, time))
                            print()
                        downflag = 0
                        upflag = 0
                        bull = 0
                        bear = 0
                        max_close = 0

                    elif bull_or_bear_candle == 'red':
                        downflag = 0
                        upflag = 0
                        bull = 0
                        bear = 0
                        max_close = 0

                    prev = current_candle;
                    counter = counter + 1
        except Exception as e:
            print(e)
        return return_object

    def candleType(self, stock, candle):
        open_price = candle[stock]['open'];
        close_price = candle[stock]['close'];
        if open_price > close_price:
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
            prev_close = prevCandle[stock]['close'];
            current_close = currentCandle[stock]['close'];
            if prev_close < current_close:
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
