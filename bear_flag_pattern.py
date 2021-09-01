from bull_flag_pattern import EntryCandleInformation


class BearFlagPattern:

    def checkType1BearFlagPattern(self, stock, barset, stock_alert_file, stock_info, limit):

        try:  # fetch the data
            prev = None;
            bull = 0;
            bear = 0;
            count = 0;
            upflag = 0;
            downflag = 0;
            first_bear = 0;
            return_object = []
            counter = 0
            for time, current_candle in barset.iterrows():
                if count == 0:
                    prev = current_candle
                    count = count + 1
                else:
                    bull_or_bear_candle = self.candleType(stock, current_candle);
                    if bull_or_bear_candle == 'red' and self.isLowerThan(stock, prev, current_candle) == 1:
                        if upflag == 1 and downflag == 1 and first_bear > current_candle[stock]['close']:
                            # This is the sign of bull flag.
                            print("Stock", stock, "Bear=", bull, " Downflag = ", downflag, "time", time)
                            print("Stock", stock, "Bull=", bear, " Upflag = ", upflag)
                            print("Stock", stock, "Bear flag detected at time", time, time.tz_convert('utc'))
                            print("Stock", stock, "Stoploss", prev[stock]['high'])
                            stock_name = stock + ":" + str(time.tz_convert('utc'))
                            if stock_name not in stock_info:
                                current_stock_info = stock + ", " + "BearFlag1, " + str(
                                    time.tz_convert('utc')) + ", " + str(
                                    prev[stock]['high'])
                                stock_info[stock_name] = current_stock_info
                                stock_alert_file.write(current_stock_info)
                                stock_alert_file.write("\n")
                                stock_alert_file.flush()
                            else:
                                print("Key already present")
                            print()
                            return_object.append(
                                EntryCandleInformation(counter, prev[stock]['high'], barset, stock, limit, time))
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
                            first_bear = current_candle[stock]['close'];
                        bear = bear + 1
                        if (bear >= 2):
                            downflag = 1;
                    elif bull_or_bear_candle == 'green' and self.isHigherThan(stock, prev,
                                                                              current_candle) == 1 and downflag == 1:
                        bull = bull + 1
                        if (bull >= 2):
                            upflag = 1;
                    elif bull_or_bear_candle == 'red':
                        if upflag == 1 and downflag == 1 and first_bear > current_candle[stock]['close']:
                            # This is the sign of bull flag.
                            print("Stock", stock, "Bear=", bull, " Downflag = ", downflag, "time", time)
                            print("Stock", stock, "Bull=", bear, " Upflag = ", upflag)
                            print("Stock", stock, "Bear flag detected at time", time, time.tz_convert('utc'))
                            print("Stock", stock, "Stoploss", prev[stock]['high'])
                            stock_name = stock + ":" + str(time.tz_convert('utc'))
                            if stock_name not in stock_info:
                                current_stock_info = stock + ", " + "BearFlag1, " + str(
                                    time.tz_convert('utc')) + ", " + str(
                                    prev[stock]['high'])
                                stock_info[stock_name] = current_stock_info
                                stock_alert_file.write(current_stock_info)
                                stock_alert_file.write("\n")
                                stock_alert_file.flush()
                            else:
                                print("Key already present")
                            print()
                            return_object.append(
                                EntryCandleInformation(counter, prev[stock]['high'], barset, stock, limit, time))

                        downflag = 0
                        upflag = 0
                        bull = 0
                        bear = 0
                    elif bull_or_bear_candle == 'green':
                        downflag = 0
                        upflag = 0
                        bull = 0
                        bear = 0
                    prev = current_candle;
                    counter = counter + 1

        except Exception as e:
            print(e)
        return return_object

    def checkType2BearFlagPattern(self, stock, barset, stock_alert_file, stock_info, limit):
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
                    if bull_or_bear_candle == 'red' and self.isLowerThan(stock, prev, current_candle) == 1:
                        if upflag == 1 and downflag == 1 and max_close > current_candle[stock]['close']:
                            # This is the sign of bull flag.
                            print("Stock", stock, "Bear=", bull, " Downflag = ", downflag, "time", time)
                            print("Stock", stock, "Bull=", bear, " Upflag = ", upflag)
                            print("Stock", stock, "Bear flag detected at time", time, time.tz_convert('utc'))
                            print("Stock", stock, "Stoploss", prev[stock]['high'])
                            stock_name = stock + ":" + str(time.tz_convert('utc'))
                            if stock_name not in stock_info:
                                current_stock_info = stock + ", " + "BearFlag2, " + str(
                                    time.tz_convert('utc')) + ", " + str(
                                    prev[stock]['high'])
                                stock_info[stock_name] = current_stock_info
                                stock_alert_file.write(current_stock_info)
                                stock_alert_file.write("\n")
                                stock_alert_file.flush()
                            else:
                                print("Key already present")
                            return_object.append(
                                    EntryCandleInformation(counter, prev[stock]['high'], barset, stock, limit, time))
                            print()
                            downflag = 0
                            upflag = 0
                            bull = 0
                            bear = 0
                            max_close = 0
                        elif upflag == 1:
                            downflag = 0
                            upflag = 0
                            bull = 0
                            bear = 0
                            max_close = 0
                        if bear == 0:
                            max_close = current_candle[stock]['close'];
                        bear = bear + 1
                        if (bear >= 2):
                            downflag = 1;
                            max_close = current_candle[stock]['close'];

                    elif bull_or_bear_candle == 'green' and self.isHigherThan(stock, prev,
                                                                           current_candle) == 1 and downflag == 1:
                        bull = bull + 1
                        upflag = 1;
                        if (bull >= 2):
                            upflag = 0;
                            max_close = 0

                    elif bull_or_bear_candle == 'red':
                        if upflag == 1 and downflag == 1 and max_close > current_candle[stock]['close']:
                            print("Stock", stock, "Bear=", bull, " Downflag = ", downflag, "time", time)
                            print("Stock", stock, "Bull=", bear, " Upflag = ", upflag)
                            print("Stock", stock, "Bear flag detected at time", time, time.tz_convert('utc'))
                            print("Stock", stock, "Stoploss", prev[stock]['high'])
                            stock_name = stock + ":" + str(time.tz_convert('utc'))
                            if stock_name not in stock_info:
                                current_stock_info = stock + ", " + "BearFlag2, " + str(
                                    time.tz_convert('utc')) + ", " + str(
                                    prev[stock]['high'])
                                stock_info[stock_name] = current_stock_info
                                stock_alert_file.write(current_stock_info)
                                stock_alert_file.write("\n")
                                stock_alert_file.flush()
                            else:
                                print("Key already present")
                            return_object.append(
                                EntryCandleInformation(counter, prev[stock]['high'], barset, stock, limit, time))
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
