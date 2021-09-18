class BullFlagVerifier:

    def verifyBullFlag(self, entry_candle_infos, transaction, pattern):
        for entry_candle_info in entry_candle_infos:
            try:
                barset = entry_candle_info.barset;
                position = entry_candle_info.postion;
                stoploss = entry_candle_info.stoploss;
                stock = entry_candle_info.stock
                time = entry_candle_info.time;
                entry = barset.iloc[position + 2][entry_candle_info.stock]['open'];
                r = barset.iloc[position + 2][entry_candle_info.stock]['open'] - stoploss;
                first_target = entry + 2 * r;
                print("Stock", stock, "Entry", entry, "first_target", first_target, "time", time, "timeUTC",
                      time.tz_convert('utc'))
                subset = barset.tail(entry_candle_info.total - position - 3);
                for time, currentCandle in subset.iterrows():
                    if currentCandle[stock]['high'] > first_target:
                        money_made = (first_target - entry)
                        transaction.add(money_made)
                        print("True Prediction", pattern, "Money Made", money_made, transaction.totalMoneyMade)
                        break;
                    if currentCandle[stock]['low'] < stoploss:
                        money_lost = entry - stoploss;
                        transaction.deduct(money_lost)
                        print("Wrong Prediction", pattern, "Money Lost", money_lost, transaction.totalMoneyLost)
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
