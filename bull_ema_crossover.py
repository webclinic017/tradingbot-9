import tulipy as ti

class BullEMACrossover:

    def checkBullEMACrossOverPattern(self, stock, barset, stock_alert_file, stock_info, limit):
        ema10 = barset[stock].close.ewm(span=10, adjust=False).mean();
        ema20 = barset[stock].close.ewm(span=20, adjust=False).mean();

        #ema10 = ti.ema(df.close.dropna().to_numpy(), 10)
        #ema20 = ti.ema(df.close.dropna().to_numpy(), 20)
        pattern = "UN"
        if(ema10[1] < ema20[1]):
            pattern = "LO"
        elif ema10[1] > ema20[1]:
            pattern = "HI"
        i = 0
        for e1, e2 in zip(ema10, ema20):
            if((pattern =="LO") &  (e1 > e2)):
                print(stock,"EMA10 crossover at",i)
                pattern = "HI"
            elif ((pattern=="HI") & (e1 < e2)):
                print(stock,"EMA20 crossover at",i)
                pattern = "LO"
            i = i+1


        #print(stock,"10EMA",ema10, len(ema10));
        #print(stock,"20EMA",ema20, len(ema20));

