
import time
from bear_flag_pattern import BearFlagPattern
from datetime import date

import secrets
from bear_flag_verifier import BearFlagVerifier
from benzinga_screener import BenzingaScreener
from bull_flag_verifier import BullFlagVerifier
from bull_flag_verifier import Transaction
from traderlib import *

def main():
    benzinga_screener = BenzingaScreener();
    realtime = 1
    limit = 10
    interval = '5Min';
    if realtime == 0:
        limit = 78

    stock_alert_filename = "predictions/benzinga/" + "stock_alert_bear_" + str(date.today()) + ".csv"
    trade_executions_filename = "predictions/trade_executions_" + str(date.today()) + ".csv"
    benzinga_stock_alert_file = open(stock_alert_filename, "a+")
    trade_executions_file = open(trade_executions_filename, "a+")

    if os.stat(stock_alert_filename).st_size == 0:
        benzinga_stock_alert_file.write("Stock, Type, Time, Stoploss")
        benzinga_stock_alert_file.write("\n")
    if os.stat(trade_executions_filename).st_size == 0:
        trade_executions_file.write("Stock, Type, Time, Stoploss, Entry Price, R, Target Price, Prediction Type")
        trade_executions_file.write("\n")
        trade_executions_file.flush()

    api = tradeapi.REST(secrets.API_KEY, secrets.API_SECRET_KEY, secrets.ALPACA_API_URL, api_version='v2')

    stock_info = {}
    while True:
        # Get all the gainers for the session
        stocks = benzinga_screener.get_losers_for_session();
        bear_flag_pattern = BearFlagPattern();
        transaction = Transaction(0, 0);
        for stock in stocks:

            # print("Working on stock", stock)
            # Fetch the recent candle information for the given stock
            candle_infos = api.get_barset(stock, interval, limit).df
            if realtime == 1:
                candle_infos = candle_infos[0:-1]

            # Apply Bull flag 1 pattern match. If found, enter the values to benzinga_stock_alert_file
            bear_flag1 = bear_flag_pattern.checkType1BearFlagPattern(stock, candle_infos, benzinga_stock_alert_file,
                                                                     stock_info, limit)
            # Apply Bull flag 2 pattern match. If found, enter the values to benzinga_stock_alert_file
            bear_flag2 = bear_flag_pattern.checkType2BearFlagPattern(stock, candle_infos, benzinga_stock_alert_file,
                                                                     stock_info, limit)

            if realtime == 0:
                bear_flag_verifier = BearFlagVerifier()
                bear_flag_verifier.verifyBearFlag(bear_flag1, transaction)
                bear_flag_verifier.verifyBearFlag(bear_flag2, transaction)

        print("________________________________________________________________________________________________")

        print("Sleeping")
        time.sleep(120)

if __name__ == '__main__':
    main()
