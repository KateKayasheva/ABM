import random

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
        return "Agent is of type {}".format(self.type)


    def record(self, direction, price, quantity):
        """
        Record transaction
        """
        if direction == "SELL":
            self.stocks -= quantity
            self.money += quantity*price
        elif direction == "BUY":
            self.stocks += quantity
            self.money -= quantity*price


class RandomTrader(Agent):
    """
    Random trader
    """
    def __init__(self, money, stocks):
        Agent.__init__(self, money, stocks)
        self.type = "RANDOM"


   def order(self):
       """
       Set the order
       BUY if no stocks on hand
       If stocks > 0 choose direction at random

       """
       if self.stocks > 0:
           direction = random.choice(("BUY", "SELL"))
       else:
           direction = "BUY"






print(RandomTrader(1,2).wealth())