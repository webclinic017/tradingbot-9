import time
from bear_flag_pattern import BearFlagPattern
from finviz_screener import FinvizScreener

def main():
    finvizScreener = FinvizScreener();
    while True:
        stocks = finvizScreener.positive_movers_with_beta_over_2();
        bearFlagPattern = BearFlagPattern();
        for stock in stocks:
            print("Working on stock", stock)
            bearFlagPattern.checkType2BearFlagPattern(stock, interval='5Min',limit=78)
        print("________________________________________________________________________________________________")

        print("Sleeping")
        time.sleep(320)

if __name__ == '__main__':
    main()
