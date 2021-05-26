import random
from statistics import mean, stdev


class Agent:
    """
    Agent class
    - money (float) amount of money in the pocket
    - stocks (int) number of stocks owned
    """

    def __init__(self, money, stocks):
        self.money = money
        self.stocks = stocks
        self.type = None

    def wealth(self):
        return "Agent owns {} stocks and {} of money".format(self.stocks, self.money)

    def __str__(self):
        return "Agent is of type {}, id: {}".format(self.type, id(self))

    # def __str__(self):
    #     return "<Agent %s>" % id(self)

    def record(self, direction, price, quantity):
        """
        Record transaction
        """
        if direction == "SELL":
            self.stocks -= quantity
            self.money += quantity * price
        elif direction == "BUY":
            self.stocks += quantity
            self.money -= quantity * price



class RandomTrader(Agent):
    """
    Random trader
    """

    def __init__(self, money, stocks):
        Agent.__init__(self, money, stocks)

        self.type = "RANDOM"

    def order(self, day, previous_prices=[]):
        """
        Set the order
        BUY if no stocks on hand
        If stocks > 0 choose direction at random
        order format dictionary as {'direction': direction, 'price': price, 'quantity': quantity, 'agent': id(self)}
        Day - simulation day number
        previous_prices: list of price for previous day
        """
        # Determine the direction
        if self.stocks > 0:
            direction = random.choice(("BUY", "SELL"))
        else:
            direction = "BUY"

        #  Determine price

        if day == 0:
            price = random.randint(1, self.money * 100) / 100  # From 0.01 to money
        elif len(previous_prices) >= 2: #to be able to compute sigma and mu
            # determine the price (add average +- sigma)
            mu = mean(previous_prices)
            sd = stdev(previous_prices)
            print(mu, sd)
            price = round(random.uniform(mu - sd, mu + sd), 2) # to avoid infinite decimal points
            print("WWWWWWWWWWWWWWWWWWWWW")
            print(price)
        else:
            price = random.randint(1, self.money * 100) / 100  # From 0.01 to money

        # Determine quantity
        quantity = 0
        if direction == "SELL":
            maxq = self.stocks
            try:
                quantity = random.randint(1, maxq)
            except ValueError:
                quantity = 1
        elif direction == "BUY":
            try:
                quantity = random.randint(1, int(self.money / price))  # TODO: find the lower bound (seems fine)
            except ValueError:
                quantity = 1

        order = {'direction': direction, 'price': price, 'quantity': quantity, 'agent': id(self)}
        print("Printing order from order function:", order)
        return order


class MarketMaker(Agent):

    def __init__(self, money, stocks):
        Agent.__init__(self, money, stocks)

        self.type = "MM"
