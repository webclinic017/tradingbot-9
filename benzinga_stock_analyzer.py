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

def main(assHand=None):
    benzingaScreener = BenzingaScreener();
    while True:
        stocks = benzingaScreener.get_gainers();
        loserStocks = benzingaScreener.get_losers();
        bullFlatPattern = BullFlagPattern();
        for stock in stocks:
            print("Working on stock", stock)
            bullFlatPattern.checkType1BullFlagPattern(stock, interval='5Min',limit=78)

        for stock in loserStocks:
            print("Working on stock", stock)
            bullFlatPattern.checkType1BullFlagPattern(stock, interval='5Min',limit=78)
        print("________________________________________________________________________________________________")
        for stock in stocks:
            print("Working on stock", stock)
            bullFlatPattern.checkType2BullFlagPattern(stock, interval='5Min',limit=78)

        for stock in loserStocks:
            print("Working on stock", stock)
            bullFlatPattern.checkType2BullFlagPattern(stock, interval='5Min',limit=78)
        print("Sleeping")
        time.sleep(120)

if __name__ == '__main__':
    main()
