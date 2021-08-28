
import time
from bull_flag_pattern import BullFlagPattern
from benzinga_screener import BenzingaScreener

def main():
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
