from datetime import date

import secrets
from benzinga_screener import BenzingaScreener
from bull_ema_crossover import BullEMACrossover
from bull_flag_pattern import BullFlagPattern
from bull_flag_verifier import BullFlagVerifier
from bull_flag_verifier import Transaction
from finviz_screener import FinvizScreener
from traderlib import *


def main():
    benzinga_screener = BenzingaScreener();
    finvizScreener = FinvizScreener();

    realtime = 0
    limit = 10
    interval = '5Min';
    if realtime == 0:
        limit = 78

    stock_alert_filename = "predictions/" + "alerts/stock_alert_bull_" + str(date.today()) + ".csv"
    trade_executions_filename = "predictions/trade_executions_" + str(date.today()) + ".csv"
    stock_alert_file = open(stock_alert_filename, "a+")
    trade_executions_file = open(trade_executions_filename, "a+")

    if os.stat(stock_alert_filename).st_size == 0:
        stock_alert_file.write("Stock, Type, Time, Stoploss")
        stock_alert_file.write("\n")
    if os.stat(trade_executions_filename).st_size == 0:
        trade_executions_file.write("Stock, Type, Time, Stoploss, Entry Price, R, Target Price, Prediction Type")
        trade_executions_file.write("\n")
        trade_executions_file.flush()

    api = tradeapi.REST(secrets.API_KEY, secrets.API_SECRET_KEY, secrets.ALPACA_API_URL, api_version='v2')

    stock_info = {}
    while True:
        # Get all the gainers for the session
        benzinga_stocks = benzinga_screener.get_gainers_for_session();
        stocks = benzinga_stocks;
        try:
            finviz_stocks = finvizScreener.positive_movers_with_beta_over_2()
            stocks = stocks + finviz_stocks;
        except Exception as e:
            print("Exception fetching finviz stocks", e)
        print("Total Stocks", len(stocks))

        stocks = list(dict.fromkeys(stocks))
        print("After removing duplicates Total Stocks", len(stocks))

        bull_flat_pattern = BullEMACrossover();
        transaction = Transaction(0, 0);
        for stock in stocks:
            candle_infos = api.get_barset(stock, interval, limit).df
            if realtime == 1:
                candle_infos = candle_infos[0:-1]
                
            bull_flag1 = bull_flat_pattern.checkBullEMACrossOverPattern(stock, candle_infos, stock_alert_file,
                                                                     stock_info, limit)


        print("________________________________________________________________________________________________")

        print("Sleeping")
        time.sleep(120)


if __name__ == '__main__':
    main()
