class Stock:
    def __init__(self, buy: int, amt: int):
        self.tax = 0.20315
        self.buy = buy
        self.amt = amt

    """
    損益分岐点
    """
    def zero(self):
        spent = self.buy * self.amt
        commission1 = self.commission(spent)
        commission2 = commission1

        while True:
            earned = spent + commission1 + commission2
            if commission2 == self.commission(earned):
                break
            commission2 = self.commission(earned)
        return earned/self.amt

    def profit(self, sell):
        spent = self.buy * self.amt
        print("投資額:" + str(spent))
        chspent = self.commission(spent)
        earns = sell * self.amt
        print("収益:" + str(earns))
        coms = []
        coms.append(self.commission(earns))
        coms.append(self.commission(earns/2)*2)
        print(str(coms.index(min(coms))+1) + '回売り')
        profit = earns - spent - (chspent + min(coms))
        taxed = profit if profit < 0 else profit*(1-self.tax)
        return taxed

    """
    input: 金額
    output: 税額
    """
    def commission(self, cost):
        if cost <= 5e4:
            c = 55
        elif cost <= 10e4:
            c = 99
        elif cost <= 20e4:
            c = 115
        elif cost <= 50e4:
            c = 275
        elif cost <= 100e4:
            c = 535
        return c


a = Stock(2358, 100)
print(a.zero())
