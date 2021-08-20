import time
from bull_flag_pattern import BullFlagPattern
from finviz_screener import FinvizScreener

def main(assHand=None):
    finvizScreener = FinvizScreener();
    while True:
        stocks = finvizScreener.midcap_with_beta_over_1point5();
        bullFlatPattern = BullFlagPattern();
        for stock in stocks:
            print("Working on stock", stock)
            bullFlatPattern.checkType2BullFlagPattern(stock, interval='5Min',limit=78)
        print("________________________________________________________________________________________________")

        print("Sleeping")
        time.sleep(320)

if __name__ == '__main__':
    main()
