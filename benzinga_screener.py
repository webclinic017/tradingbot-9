import requests
import pandas as pd

import secrets


class BenzingaScreener:

    def get_gainers(self):
        response = requests.get("https://data-api-pro.benzinga.com/rest/movers?apikey="+secrets.BENZINGA_KEY+"&from=-60m&maxResults=100&session=REGULAR&screenerQuery=marketCap_gt_300000000&gainers=true")
        result = response.json()
        gainers = result["result"]["gainers"]
        gainersSortedByVol = pd.json_normalize(gainers).sort_values(by=['volume'], ascending=False)
        print(gainersSortedByVol)
        gainerSymbols = gainersSortedByVol['symbol'].values.tolist()
        return gainerSymbols;

    def get_losers(self):
        response = requests.get(
                "https://data-api-pro.benzinga.com/rest/movers?apikey="+secrets.BENZINGA_KEY+"&from=-60m&maxResults=100&session=REGULAR&screenerQuery=marketCap_gt_300000000&gainers=true")
        result = response.json()
        losers = result["result"]["losers"]
        losersSortedByVol = pd.json_normalize(losers).sort_values(by=['volume'], ascending=False)
        print(losersSortedByVol)
        loserSymbols = losersSortedByVol['symbol'].values.tolist()
        return loserSymbols;

    def get_gainers_for_session(self):
        response = requests.get("https://data-api-pro.benzinga.com/rest/movers?apikey="+secrets.BENZINGA_KEY+"&maxResults=100&session=REGULAR&screenerQuery=marketCap_gt_300000000&gainers=true")
        result = response.json()
        gainers = result["result"]["gainers"]
        gainersSortedByVol = pd.json_normalize(gainers).sort_values(by=['volume'], ascending=False)
        print(gainersSortedByVol)
        gainerSymbols = gainersSortedByVol['symbol'].values.tolist()
        return gainerSymbols;

    def get_losers_for_session(self):
        response = requests.get("https://data-api-pro.benzinga.com/rest/movers?apikey="+secrets.BENZINGA_KEY+"&maxResults=100&session=REGULAR&screenerQuery=marketCap_gt_300000000&gainers=true")
        result = response.json()
        gainers = result["result"]["losers"]
        gainersSortedByVol = pd.json_normalize(gainers).sort_values(by=['volume'], ascending=False)
        print(gainersSortedByVol)
        gainerSymbols = gainersSortedByVol['symbol'].values.tolist()
        return gainerSymbols;



