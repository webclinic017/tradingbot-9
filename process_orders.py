import robin_stocks.robinhood as rs
import pyotp
import pandas as pd


data = pd.read_csv("today.csv")
df = data.groupby(['instrument', 'side']).sum()['executed_notional.amount']

df.to_csv("today_agg_orders.csv")
