
class BullFlagVerifier:

    def verifyBullFlag(self, entryCandleInformations, transaction):
        for entryCandleInformation in entryCandleInformations:
            try:
                barset = entryCandleInformation.barset;
                position = entryCandleInformation.postion;
                stoploss = entryCandleInformation.stoploss;
                stock = entryCandleInformation.stock
                time = entryCandleInformation.time;
                #print(barset.iloc[position + 2]);
                entry = barset.iloc[position + 2][entryCandleInformation.stock]['open'];
                r = barset.iloc[position + 2][entryCandleInformation.stock]['open'] - stoploss;
                first_target = entry + 2*r;
                print("Stock", stock,"Entry", entry, "first_target", first_target, "time",time, "timeUTC", time.tz_convert('utc') )
                subset = barset.tail(entryCandleInformation.total - position-3);
                for time, currentCandle in subset.iterrows():
                    if currentCandle[stock]['high'] > first_target:
                        money_made = (first_target - entry)
                        transaction.add(money_made)
                        print("True Prediction", "Money Made", money_made, transaction.totalMoneyMade)
                        break;
                    if currentCandle[stock]['low'] < stoploss:
                        money_lost = entry - stoploss;
                        transaction.deduct(money_lost)
                        print("Wrong Prediction", "Money Lost", money_lost, transaction.totalMoneyLost)
                        break
            except Exception:
                pass


class Transaction:
    def __init__(self, totalMoneyMade, totalMoneyLost):
        self.totalMoneyMade = totalMoneyMade
        self.totalMoneyLost = totalMoneyLost
    def add(self, money):
        self.totalMoneyMade = self.totalMoneyMade + money
    def deduct(self, money):
        self.totalMoneyLost = self.totalMoneyLost + money