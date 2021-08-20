
import time
from bear_flag_pattern import BearFlagPattern
from benzinga_screener import BenzingaScreener

def main(assHand=None):
    benzingaScreener = BenzingaScreener();
    while True:
        stocks = benzingaScreener.get_gainers();
        loserStocks = benzingaScreener.get_losers();
        bearFlatPattern = BearFlagPattern();
        for stock in stocks:
            print("Working on stock", stock)
            bearFlatPattern.checkType1BearFlagPattern(stock, interval='5Min',limit=78)

        for stock in loserStocks:
            print("Working on stock", stock)
            bearFlatPattern.checkType1BearFlagPattern(stock, interval='5Min',limit=78)
        print("________________________________________________________________________________________________")
        print("Sleeping")
        time.sleep(120)

if __name__ == '__main__':
    main()
