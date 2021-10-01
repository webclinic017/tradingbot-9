
from finviz.screener import Screener
import pandas as pd

class FinvizScreener:
    def midcap_with_beta_over_1(self):
        filters = ['cap_midover', 'fa_epsyoy_o20','fa_epsyoy1_o20','ta_beta_o2']  # Shows companies in NASDAQ which are in the S&P500
        stock_list = Screener(filters=filters, table='Performance', order='-volume')  # Get the performance table and sort it by price ascending
        # Export the screener results to .csv
        #stock_list.to_csv("stock.csv")
        #print(stock_list)

        #df = pd.read_csv("stock.csv")
        #print(df.head())
        return stock_list;

    def positive_movers_with_beta_over_2(self):
        filters = ['ta_changeopen_u1', 'sh_avgvol_o1000','ta_beta_o2']  # Shows companies in NASDAQ which are in the S&P500
        stock_list = Screener(filters=filters, table='Overview', order='-volume')  # Get the performance table and sort it by price ascending
        # Export the screener results to .csv
        #stock_list.to_csv("stock.csv")
        #print(stock_list)

        #df = pd.read_csv("stock.csv")
        #print(df.head())
        stock_data = pd.DataFrame(stock_list.data)
        ticker_symbols = stock_data['Ticker'].values.tolist()

        print(ticker_symbols)
        return ticker_symbols;


    def positive_movers_above_200sma(self):
        filters = ['cap_midover', 'sh_avgvol_o2000','ta_change_u','ta_sma200_pa']  # Shows companies in NASDAQ which are in the S&P500
        stock_list = Screener(filters=filters, table='Overview', order='-volume')  # Get the performance table and sort it by price ascending
        # Export the screener results to .csv
        #stock_list.to_csv("stock.csv")
        #print(stock_list)

        #df = pd.read_csv("stock.csv")
        #print(df.head())
        stock_data = pd.DataFrame(stock_list.data)
        ticker_symbols = stock_data['Ticker'].values.tolist()

        print(ticker_symbols)
        return ticker_symbols;


    def positive_movers_with_beta_under_2(self):
        filters = ['sh_avgvol_o1000', 'sh_relvol_o1.5','ta_beta_u2','ta_changeopen_u1']  # Shows companies in NASDAQ which are in the S&P500
        stock_list = Screener(filters=filters, table='Overview', order='-volume')  # Get the performance table and sort it by price ascending
        # Export the screener results to .csv
        #stock_list.to_csv("stock.csv")
        #print(stock_list)

        #df = pd.read_csv("stock.csv")
        #print(df.head())
        stock_data = pd.DataFrame(stock_list.data)
        ticker_symbols = stock_data['Ticker'].values.tolist()

        print(ticker_symbols)
        return ticker_symbols;




    def top_gainers(self):
        top_gainers = Screener(signal='ta_topgainers', table='Performance', order='-volume')  # Get the performance table and sort it by price ascending
        #top_gainers.to_csv("top_gainers.csv")
        return top_gainers.data


def main():
    finvizScreener = FinvizScreener()
    print(finvizScreener.positive_movers_above_200sma())
if __name__ == '__main__':
    main()
