from backtrader import TimeFrame

import gvars
from assetHandler import AssetHandler
from other_functions import create_log_folder
from tbot import MultiHandler, check_account_ok, _L, run_tbot
from traderlib import *
import threading, os, logging, sys
import tulipy as ti
import pandas as pd


from bullFlagPattern import BullFlagPattern
from benzinga import Benzinga

def main(assHand=None):
    benzinga = Benzinga();
    stocks = benzinga.get_gainers();
    bullFlatPattern = BullFlagPattern();
    for stock in stocks:
        print("Working on stock", stock)
        bullFlatPattern.checkBullFlagPattern(stock, interval='5Min',limit=78)

if __name__ == '__main__':
    main()
