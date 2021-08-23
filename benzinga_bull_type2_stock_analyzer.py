from backtrader import TimeFrame

import gvars
from assetHandler import AssetHandler
from other_functions import create_log_folder
from tbot import MultiHandler, check_account_ok, _L, run_tbot
from traderlib import *
import threading, os, logging, sys
import tulipy as ti
import pandas as pd

import time
from bull_flag_pattern import BullFlagPattern
from benzinga_screener import BenzingaScreener
from bull_flag_verifier import BullFlagVerifier
from bull_flag_verifier import Transaction
import os
from datetime import date

def main(assHand=None):
    benzingaScreener = BenzingaScreener();
    realtime = 1
    limit = 10
    if (realtime == 0):
        limit = 78

    stock_alert_filename = "predictions/benzinga/"+"stock_alert_bull_type_2_" + str(date.today()) + ".csv"
    trade_executions_filename = "predictions/trade_executions_" + str(date.today()) + ".csv"
    bull_flag_2_alert_file = open(stock_alert_filename, "a+")
    trade_executions_file = open(trade_executions_filename, "a+")

    if (os.stat(stock_alert_filename).st_size == 0):
        bull_flag_2_alert_file.write("Stock, Type, Time, Stoploss")
        bull_flag_2_alert_file.write("\n")
    if (os.stat(trade_executions_filename).st_size == 0):
        trade_executions_file.write("Stock, Type, Time, Stoploss, Entry Price, R, Target Price, Prediction Type")
        trade_executions_file.write("\n")
        trade_executions_file.flush()

    while True:
        stocks = benzingaScreener.get_gainers_for_session();
        bullFlatPattern = BullFlagPattern();
        transaction = Transaction(0, 0);
        for stock in stocks:
            # print("Working on stock", stock)
            bullFlagInformation = bullFlatPattern.checkType2BullFlagPattern(stock, bull_flag_2_alert_file,
                                                                            interval='5Min', limit=limit)
            if (realtime == 0):
                bull_flag_verifier = BullFlagVerifier()
                bull_flag_verifier.verifyBullFlag(bullFlagInformation, transaction)
        print("________________________________________________________________________________________________")

        print("Sleeping")
        time.sleep(120)
if __name__ == '__main__':
    main()
