import time

import secrets
from bull_flag_pattern import BullFlagPattern, tradeapi
from finviz_screener import FinvizScreener
from bull_flag_verifier import BullFlagVerifier
from bull_flag_verifier import Transaction
import os
from datetime import date

def main():
    finvizScreener = FinvizScreener();
    realtime = 1
    limit = 10
    interval = '5Min';
    if realtime == 0:
        limit = 78

    stock_alert_filename= "predictions/finviz/"+"stock_alert_bull_"+str(date.today())+".csv"
    trade_executions_filename = "predictions/trade_executions_" + str(date.today()) + ".csv"

    finviz_flag_1_alert_file = open(stock_alert_filename, "a+")
    trade_executions_file = open(trade_executions_filename, "a+")

    if(os.stat(stock_alert_filename).st_size == 0):
        finviz_flag_1_alert_file.write("Stock, Type, Time, Stoploss")
        finviz_flag_1_alert_file.write("\n")
    if (os.stat(trade_executions_filename).st_size == 0):
        trade_executions_file.write("Stock, Type, Time, Stoploss, Entry Price, R, Target Price, Prediction Type")
        trade_executions_file.write("\n")
        trade_executions_file.flush()

    api = tradeapi.REST(secrets.API_KEY, secrets.API_SECRET_KEY, secrets.ALPACA_API_URL, api_version='v2')

    stock_info = {}
    while True:
        stocks = finvizScreener.positive_movers_with_beta_over_2();
        bull_flat_pattern = BullFlagPattern();
        transaction = Transaction(0, 0);
        for stock in stocks:

            # print("Working on stock", stock)
            # Fetch the recent candle information for the given stock
            candle_infos = api.get_barset(stock, interval, limit).df
            if realtime == 1:
                candle_infos = candle_infos[0:-1]
                limit = limit-1
            # Apply Bull flag 1 pattern match. If found, enter the values to benzinga_stock_alert_file
            bull_flag1 = bull_flat_pattern.checkType1BullFlagPattern(stock, candle_infos, finviz_flag_1_alert_file,
                                                                     stock_info, limit)
            # Apply Bull flag 2 pattern match. If found, enter the values to benzinga_stock_alert_file
            bull_flag2 = bull_flat_pattern.checkType2BullFlagPattern(stock, candle_infos, finviz_flag_1_alert_file,
                                                                     stock_info, limit)

            if realtime == 0:
                bull_flag_verifier = BullFlagVerifier()
                bull_flag_verifier.verifyBullFlag(bull_flag1, transaction)
                bull_flag_verifier.verifyBullFlag(bull_flag2, transaction)

        print("________________________________________________________________________________________________")

        print("Sleeping")
        time.sleep(120)


if __name__ == '__main__':
    main()

