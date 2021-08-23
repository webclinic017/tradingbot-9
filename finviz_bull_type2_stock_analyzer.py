import time
from bull_flag_pattern import BullFlagPattern
from finviz_screener import FinvizScreener
from bull_flag_verifier import BullFlagVerifier
from bull_flag_verifier import Transaction
import os
from datetime import date
def main():
    finvizScreener = FinvizScreener();
    realtime=0
    limit=10
    if(realtime == 0):
        limit=78

    stock_alert_filename= "stock_alert_bull_type_2_"+str(date.today())+".csv"
    stoploss_alert_filename= "stoploss_alert_bull_type_2_"+str(date.today())+".csv"
    target_achieved_filename =  "target_achieved_bull_type_2_"+str(date.today())+".csv"
    bull_flag_2_alert_file = open(stock_alert_filename, "a+")
    stoploss_alert_file = open(stoploss_alert_filename, "a+")
    target_achieved_alert_file  = open(target_achieved_filename, "a+")

    if(os.stat(stock_alert_filename).st_size == 0):
        bull_flag_2_alert_file.write("Stock, Type, Time, Stoploss")
        bull_flag_2_alert_file.write("\n")
    if(os.stat(stoploss_alert_filename).st_size == 0):
        stoploss_alert_file.write("Stock, Type, Time, Stoploss")
        stoploss_alert_file.write("\n")
    if(os.stat(target_achieved_filename).st_size == 0):
        target_achieved_alert_file.write("Stock, Type, Time, Stoploss")
        target_achieved_alert_file.write("\n")

    while True:
        stocks = finvizScreener.midcap_with_beta_over_1point5();
        bullFlatPattern = BullFlagPattern();
        transaction = Transaction(0,0);
        for stock in stocks:
            #print("Working on stock", stock)
            bullFlagInformation = bullFlatPattern.checkType2BullFlagPattern(stock, bull_flag_2_alert_file, interval='5Min',limit=limit)
            if(realtime == 0):
                bull_flag_verifier = BullFlagVerifier()
                bull_flag_verifier.verifyBullFlag(bullFlagInformation, transaction)
        print("________________________________________________________________________________________________")

        print("Sleeping")
        time.sleep(120)

if __name__ == '__main__':
    main()
