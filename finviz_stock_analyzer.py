import time
from bullFlagPattern import BullFlagPattern
from finvizScreener import FinvizScreener

def main(assHand=None):
    finvizScreener = FinvizScreener();
    while True:
        stocks = finvizScreener.midcap_with_beta_over_1point5();
        bullFlatPattern = BullFlagPattern();
        for stock in stocks:
            #print("Working on stock", stock)
            bullFlatPattern.checkType1BullFlagPattern(stock, interval='5Min',limit=78)
        print("________________________________________________________________________________________________")
        for stock in stocks:
            print("Working on stock", stock)
            bullFlatPattern.checkType2BullFlagPattern(stock, interval='5Min',limit=78)

        print("Sleeping")
        time.sleep(320)

if __name__ == '__main__':
    main()
