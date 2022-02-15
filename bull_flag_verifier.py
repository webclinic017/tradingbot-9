import pandas as pd
import datetime

import secrets
from traderlib import *


class BullFlagVerifier:

    def verifyBullFlag(self, entry_candle_infos, transaction, pattern):
        for entry_candle_info in entry_candle_infos:
            try:
                barset = entry_candle_info.barset;
                position = entry_candle_info.postion;
                stoploss = entry_candle_info.stoploss;
                stock = entry_candle_info.stock
                time = entry_candle_info.time;
                entry = barset.iloc[position + 2][entry_candle_info.stock]['open'];
                r = barset.iloc[position + 2][entry_candle_info.stock]['open'] - stoploss;
                first_target = entry + 2 * r;
                print("Stock", stock, "Entry", entry, "first_target", first_target, "time", time, "timeUTC",
                      time.tz_convert('utc'))
                subset = barset.tail(entry_candle_info.total - position - 3);
                for time, currentCandle in subset.iterrows():
                    if currentCandle[stock]['high'] > first_target:
                        money_made = (first_target - entry)
                        transaction.add(money_made)
                        print("True Prediction", stock, pattern, "Money Made", money_made, transaction.totalMoneyMade)
                        break;
                    if currentCandle[stock]['low'] < stoploss:
                        money_lost = entry - stoploss;
                        transaction.deduct(money_lost)
                        print("Wrong Prediction", stock,  pattern, "Money Lost", money_lost, transaction.totalMoneyLost)
                        break
            except Exception:
                pass

    #def verifyBullFlag(self, entry_candle_infos, pattern, stock, stoploss):
     #       try:
      #          entry = entry_candle_infos.iloc[1][entry_candle_infos.stock]['open'];
       #         r = entry - stoploss;
       #         first_target = entry + 2 * r;
       #         print("Stock", stock, "Entry", entry, "first_target", first_target, "time", time, "timeUTC",
       #               time.tz_convert('utc'))
       #         for time, currentCandle in entry_candle_infos.iterrows():
       #             if currentCandle[stock]['high'] > first_target:
       #                 money_made = (first_target - entry)
       #                 print("True Prediction", stock, pattern, "Money Made", money_made)
       #                 break;
       #             if currentCandle[stock]['low'] < stoploss:
       ##                 money_lost = entry - stoploss;
        #                print("Wrong Prediction", stock,  pattern, "Money Lost", money_lost)
        #                break
        #    except Exception:
        #        pass



class Transaction:
    def __init__(self, totalMoneyMade, totalMoneyLost):
        self.totalMoneyMade = totalMoneyMade
        self.totalMoneyLost = totalMoneyLost

    def add(self, money):
        self.totalMoneyMade = self.totalMoneyMade + money

    def deduct(self, money):
        self.totalMoneyLost = self.totalMoneyLost + money


def main():
    df = pd.read_csv("predictions/alerts/stock_alert_bull_2021-09-30.csv")
    print(df.head())
    interval = '5Min';
    end_time = '2021-09-30 20:00:00'
    api = tradeapi.REST(secrets.API_KEY, secrets.API_SECRET_KEY, secrets.ALPACA_API_URL, api_version='v2')
    for time, row in df.iterrows():
        alert_time = row.values[2]
        end = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        alert = datetime.strptime(alert_time, '%Y-%m-%d %H:%M:%S')
        diff = end - alert;
        limit = int(diff.seconds/60/5)
        stock = row.values[0]
        bullType = row.values[1]
        stoploss = row.values[3]
        print("stock",stock,"limit=",limit)
        candle_infos = api.get_barset(stock, interval, limit).df
        bull_flag_verifier = BullFlagVerifier()
        bull_flag_verifier.verifyBullFlag(candle_infos, bullType, stock, stoploss)


if __name__ == '__main__':
    main()
