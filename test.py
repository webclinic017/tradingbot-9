from backtrader import TimeFrame

import gvars
from assetHandler import AssetHandler
from other_functions import create_log_folder
from tbot import MultiHandler, check_account_ok, _L, run_tbot
from traderlib import *
import threading, os, logging, sys
import tulipy as ti
import pandas as pd
import requests
import json

def main(assHand=None):

    # Set up a basic stderr logging; this is nothing fancy.
    log_format = '%(asctime)s %(threadName)12s: %(lineno)-4d %(message)s'
    stderr_handler = logging.StreamHandler()
    stderr_handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger().addHandler(stderr_handler)

    # Set up a logger that creates one file per thread
    todayLogsPath = create_log_folder(gvars.LOGS_PATH)
    multi_handler = MultiHandler(todayLogsPath)
    multi_handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger().addHandler(multi_handler)

    # initialize the API with Alpaca
    api = tradeapi.REST(gvars.API_KEY, gvars.API_SECRET_KEY, gvars.ALPACA_API_URL, api_version='v2')

    # get the Alpaca account ready
    try:
        _L.info("Getting account")
        check_account_ok(api) # check if it is ok to trade
        account = api.get_account()
        _L.info("Got it")
    except Exception as e:
        _L.info(str(e))
    get_gainers()

    #stocks = "NNDM,IQ,FCEL,ZIM,MRO,POWW,RIDE,PLTR,TLRY,DIDI,DM,FUTU,MRNA,BNTX,SAVA,NVAX,FULC,TSLA,BMBL,KNBE,OPEN,ABNB,AMD,AXP,PINS,BA,JMIA,LYFT,TTD,SPLK,RAD,SHOP,BILI,SPCE,RCL,MSTR,PLUG,POSH,WISH,NKLA,DIDI,BEKE,NET,CRWD,AMZN,FUTU,APPS,CVAC,DLO,DOCS,GDRX,MRVI,TME,U,UPST,EDU,CLOV,TAL,FCEL,IQ,FSR,FUBO,M,ME,TIGR,LAC,RIOT,RLX,MARA,TSP,CHPT,OTLY,LAZR,AMEX:GSAT,SONO,ASTR,AMRN,CANO,LTHM,MGNI,BCRX,AMRS,FFIE,MVST,DDD,ARVL,PTRA,ARRY,VRM,ZH,QFIN,NOVA,JKS,AMWL,DQ,PACB,VNET,STEM,SKIN,CELH,CRCT,LPRO,COUT,FIGS,LEV,SLQT,ALLO,SHLS,EDIT,ZIP,IS,CERE,EXPI,AVIR"
    stocks=get_gainers();
    #my_list = stocks.split(",")
    for l in stocks:
        stock = l;
        load_historical_data(stock,interval='5Min',limit=78);


def load_historical_data(stock,interval='1Min',limit=100):
        # this function fetches the data from Alpaca
        # it is important to check whether is updated or not

        timedeltaItv = ceil(int(interval.strip('Min')) * 1.5) # 150% de l'interval, per si de cas
        api = tradeapi.REST(gvars.API_KEY, gvars.API_SECRET_KEY, gvars.ALPACA_API_URL, api_version='v2')

        try: # fetch the data
            #api.get_bars("AAPL", TimeFrame.Hour, "2021-02-08", "2021-02-08", limit=10, adjustment='raw').df

            #df = api.get_bars(stock, interval, "2021-16-08", "2021-16-08",limit, adjustment='raw').df
           # stock.df = self.alpaca.get_barset(stock.name, interval, limit).df[stock.name]

            bar_iter = api.get_barset(stock, interval, limit).df
            prev = None;
            bull = 0;
            bear = 0;
            count = 0;
            upFlag = 0;
            downflag = 0;
            for i, j  in bar_iter.iterrows():
                if(count == 0):
                    prev=j
                    count=count+1
                else:
                    bullOrBearCandle = candleType(stock, j);
                    if bullOrBearCandle == 'green' and isHigherThan(stock,prev, j) == 1:
                        if upFlag == 1 and downflag == 1:
                            #This is the sign of bull flag.
                            print("Stock",stock,"Bull=", bull, " Upflag = ", upFlag, "time", i)
                            print("Stock",stock,"Bear=", bear, " Downflag = ", downflag)
                            print("Stock",stock,"Bull flag detected at time", i, i.tz_convert('utc'))
                            print()
                            downflag = 0
                            upFlag = 0
                            bull = 0
                            bear = 0
                        elif downflag==1:
                            downflag = 0
                            upFlag = 0
                            bull = 0
                            bear = 0

                        bull = bull +1
                        if (bull >= 2):
                            upFlag = 1;
                    elif bullOrBearCandle == 'red' and isLowerThan(stock,prev, j) == 1 and upFlag == 1:
                        bear= bear + 1
                        if (bear >= 2):
                            downflag = 1;
                    elif bullOrBearCandle == 'green':
                        if upFlag == 1 and downflag == 1:
                            #This is the sign of bull flag.
                            print("Stock",stock,"Bull=", bull, " Upflag = ", upFlag, "time", i)
                            print("Stock",stock,"Bear=", bear, " Downflag = ", downflag)
                            print("Stock",stock,"Bull flag dected at time", i, i.tz_convert('utc'))
                            print()
                        downflag=0
                        upFlag=0
                        bull=0
                        bear=0
                    elif bullOrBearCandle == 'red':
                        downflag=0
                        upFlag=0
                        bull=0
                        bear=0
                    #print("Bull=", bull, " Upflag = ", upFlag, "time", i, i.tz_convert('utc'))
                    #print("Bear=", bear, " Downflag = ", downflag)

                    #print(i, bullOrBearCandle)
                    #print(isLowerThan(prev, j))
                    prev = j;
            #values = bar_iter.values.tolist();
            #print(bar_iter['open'].values.tolist());
            #count=0
            #for i in values:
            #    print(i);
            #    count=count+1;
            #print(count)
           # print(bar_iter.index.tolist())
            ##print(bar_iter.columns.tolist());
            #print(bar_iter.values.tolist());
            #print(bar_iter)
            #for index, row in bar_iter:
               #print(bar_iter['open'][bar])
               #print(bar_iter[index]['open'], bar_iter[index]['close'])


            #lastEntry = df.last('5Min').index[0] # entrada (vela) dels últims 5min
            #lastEntry = lastEntry.tz_convert('utc')
            #nowTimeDelta = datetime.now(timezone.utc) # ara - 5min
            #print(lastEntry);


        except Exception as e:
            print(e)



def candleType(stock,candle):
    open = candle[stock]['open'];
    close = candle[stock]['close'];
    high = candle[stock]['high']
    low = candle[stock]['low'];
    if(open > close):
        return "red"
    else:
        return "green"

def isLowerThan(stock, prevCandle, currentCandle):
    if isinstance(prevCandle, type(None)):
        return 1;
    else:
        prevClose = prevCandle[stock]['close'];
        currentClose = currentCandle[stock]['close'];
        if(prevClose > currentClose):
            return 1;
        else:
            return 0;


def isHigherThan(stock, prevCandle, currentCandle):
    if isinstance(prevCandle, type(None)):
        return 1;
    else:
        prevClose = prevCandle[stock]['close'];
        currentClose = currentCandle[stock]['close'];
        if(prevClose < currentClose):
            return 1;
        else:
            return 0;

def process_bar(bar):
    # process bar
    print(bar['open'])

def get_gainers():
    response = requests.get("https://data-api-pro.benzinga.com/rest/movers?apikey=aH0FkLCohY5yxK6OEaJ28Zpv51Ze1GyY&maxResults=100&session=REGULAR&screenerQuery=marketCap_gt_300000000%3BpreviousClose_gt_5&losers=true")
    result = response.json()
    gainers = result["result"]["gainers"]
    losers = result["result"]["losers"]
    gainersSortedByVol = pd.json_normalize(gainers).sort_values(by=['volume'], ascending=False)
    losersSortedByVol = pd.json_normalize(losers).sort_values(by=['volume'], ascending=False)
    print(gainersSortedByVol)
    print(losersSortedByVol)
    gainerSymbols = gainersSortedByVol['symbol'].values.tolist()
    loserSymbols = losersSortedByVol['symbol'].values.tolist()
    return gainerSymbols;
def get_losers():
    response = requests.get("https://data-api-pro.benzinga.com/rest/movers?apikey=aH0FkLCohY5yxK6OEaJ28Zpv51Ze1GyY&from=-5m&maxResults=100&session=AFTER_HOURS&screenerQuery=marketCap_gt_300000000%3BpreviousClose_gt_5&losers=true")
    print(response)


if __name__ == '__main__':
    main()
