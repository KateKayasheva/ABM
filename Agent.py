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
       order format dictionary as {'direction': direction, 'price': price, 'quantity': quantity}

       """
       # Determine the direction
       if self.stocks > 0:
           direction = random.choice(("BUY", "SELL"))
       else:
           direction = "BUY"

       #  Determine price
       # TODO: determine the price
       price = 1

       # Determine quantity
       if direction == "SELL":
           maxq = self.stocks
           try:
               quantity = random.randint(1, maxq)
           except ValueError:
               quantity = 1


       elif direction == "BUY":
           quantity = random.randint(1, int(self.money/price)) # TODO: find the lower bound


       order = {'direction': direction, 'price': price, 'quantity': quantity}

       return order









print(RandomTrader(1,2).wealth())