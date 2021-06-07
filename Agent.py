import random
from statistics import mean, stdev

# Round parameter for prices

r = 0


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
        print("DIRECTION {}, AGENT: {}, STOCKS: {}, MONEY: {}".format(direction, id(self), self.stocks, self.money))
        if direction == "SELL":
            self.stocks -= quantity
            self.money += quantity * price
        elif direction == "BUY":
            self.stocks += quantity
            self.money -= quantity * price

        print("RECORDING ORDER: DIRECTION {}, PRICE {}, Q {}".format(direction, price, quantity))
        print("DIRECTION {}, AGENT: {}, STOCKS: {}, MONEY: {}".format(direction, id(self), self.stocks, self.money))


class RandomTrader(Agent):
    """
    Random trader
    """

    def __init__(self, money, stocks):
        Agent.__init__(self, money, stocks)

        self.type = "RANDOM"

    def order(self, day, market):
        """
        Set the order
        BUY if no stocks on hand
        If stocks > 0 choose direction at random
        order format dictionary as
                                    {'direction': direction,
                                    'price': price,
                                    'quantity': quantity,
                                    'agent': id(self),
                                    'order_type': order_type}
        Day - simulation day number
        previous_prices: list of price for previous day
        """
        # Determine the direction
        if self.stocks > 0 and self.money > 0:
            direction = random.choices(population=("BUY", "SELL"), weights=[0.5, 0.5], k=1)[0]
        elif self.stocks == 0 and self.money > 0:
            direction = "BUY"
        elif self.money == 0 and self.stocks > 0:
            direction = "SELL"
        else:
            return None

        # determine type of the order

        order_type = random.choices(population=("L", "M"), weights=[0.65, 0.35], k=1)[0]
        # print(order_type)
        # print(direction)

        #  Determine price
        previous_prices = market.preprices
        # print(previous_prices)
        price = 0

        if order_type == 'L':
            """
            For limit orders, agent chooses some price to add submit the order at
            """
            while price == 0:  # try finding price
                if day == 0:
                    price = round(random.uniform(1.01, self.money), r)  # From 1.01 to money
                    # print('1', price)
                elif day > 0:
                    if len(previous_prices) < 2:
                        price = round(random.uniform(1.01, self.money), r)  # From 1.01 to money
                        # print('2', price)
                    elif len(previous_prices) >= 2:  # to be able to compute sigma and mu
                        # determine the price (add average +- sigma)
                        mu = mean(previous_prices)
                        sd = stdev(previous_prices)

                        # print(mu, sd)
                        if mu > sd:
                            price = round(random.uniform(mu - sd, mu + sd), r)  # to avoid infinite decimal points
                        else:
                            price = round(random.uniform(1.01, mu + sd), r)

                        # print("WWWWWWWWWWWWWWWWWWWWW")
                        # print('3', price)



                # print('price', price)
                # Determine quantity for limit order
                quantity = 0
                if direction == "SELL":
                    maxq = self.stocks
                    try:
                        quantity = random.randint(1, maxq)
                    except ValueError:
                        if maxq == 1:
                            quantity = 1
                        else:
                            order = None
                            return order
                elif direction == "BUY":
                    try:

                        quantity = random.randint(1, int(self.money / price))
                    except ValueError:
                        if int(self.money / price) == 1:
                            quantity = 1
                        else:
                            order = None
                            return order


        elif order_type == 'M':
            """
            For market orders, agent will not choose the price
            """
            price = None

            # Determine quantity for limit order
            quantity = 0
            if direction == "SELL":
                maxq = self.stocks
                try:
                    quantity = random.randint(1, maxq)
                except ValueError:
                    if maxq == 1:
                        quantity = 1
                    else:
                        order = None
                        return order

            elif direction == "BUY":

                """
                Will assume for know that the agent is willing to spend everything on the BUY market order
                (can set this parameter later)
                Everything is handled in match orders
                """
                quantity = None


        else:
            print('Type of the order is invalid')

        order = {'direction': direction,
                 'price': price,
                 'quantity': quantity,
                 'agent': id(self),
                 'order_type': order_type}
        # print("Printing order from order function:", order, "type: RANDOM")
        return order


class MarketMaker(Agent):

    def __init__(self, money, stocks):
        Agent.__init__(self, money, stocks)

        self.type = "MM"

    def order(self, day, market):
        """
        Market makers assumed to submit only limit orders.
        Can place two orders on the same day: 1 SELL, 1 BUY
        :param day: day number of simulation
        :param market: Market from Market.py to access values
        :return: list of orders for the market maker (will need to itterate over it later
        """
        if day == 0:
            """
            in our model MM will not act on the first day
            Orders with None are skipped when adding to sell/buy book
            """
            return None
        # print("MM", market.prebuy, market.presell)
        prebuyprices = list(filter(None, [x[0] for x in market.prebuy]))  # Do not include market orders
        presellprices = list(filter(None, [x[0] for x in market.presell]))

        if len(prebuyprices) < 2 or len(presellprices) < 2:
            """
            Not able to calculate sigma 
            """
            # print(len(market.prebuy), len(market.presell))
            return None

        order_type = 'L'

        # Determine prices

        prebuyprices.sort()
        presellprices.sort()
        sigma_buy = stdev(prebuyprices)
        sigma_sell = stdev(presellprices)
        pricebuy = round(presellprices[0] - sigma_sell, r)
        pricesell = round(prebuyprices[len(prebuyprices) - 1] + sigma_buy, r)
        # print(sigma_sell, sigma_buy, presellprices[0], prebuyprices[len(prebuyprices) - 1])

        # Determine the direction

        # if self.stocks > 0:
        #     direction = random.choice(("BUY", "SELL"))
        # else:
        #     direction = "BUY"

        # Determine quantity
        orders = []
        for direction in ("BUY", "SELL"):
            quantity = 0
            if direction == "SELL":
                maxq = self.stocks
                price = pricesell
                # print(price)
                if price == 0:  # Sometimes after rounding price can be zero, thus there is no order
                    order = None
                    continue
                try:
                    quantity = random.randint(1, maxq)
                except ValueError:
                    if maxq == 1:
                        quantity = 1
                    else:
                        continue

            elif direction == "BUY":
                price = pricebuy
                # print(price)
                if price == 0:  # Sometimes after rounding price can be zero, thus there is no order
                    order = None
                    continue
                try:

                    quantity = random.randint(1, int(self.money / price))
                except ValueError:
                    if int(self.money / price) == 1:
                        quantity = 1
                    else:
                        continue
            else:
                print('Direction is not specified for the market maker:', id(self))

            order = {'direction': direction,
                     'price': price,
                     'quantity': quantity,
                     'agent': id(self),
                     'order_type': order_type}
            # print("Printing order from order function:", order, "type: MM")
            orders.append(order)
        # print('MM: ', orders)
        return orders


class HFT(Agent):

    def __init__(self, money, stocks):
        Agent.__init__(self, money, stocks)

        self.type = "HFT"

    def order(self, day, market):
        """
                   HFT place limit orders on both sides of the book
                   Wish to maintain net inventory close to zero
                   Have lower limit (LL) and upper limit (UL) for the inventory
                   """
        if day == 0:
            return None

        UL = 5
        LL = 0
        order_type = 'L'
        inventory = self.stocks

        # TODO: HFT can have negative stocks, this can be a problem

        # Determine prices

        prebuyprices = list(filter(None, [x[0] for x in market.prebuy]))  # Do not include market orders
        presellprices = list(filter(None, [x[0] for x in market.presell]))
        if len(prebuyprices) < 1 or len(presellprices) < 1:
            """
            Empty is not useful
            """
            return None

        prebuyprices.sort()
        presellprices.sort()
        best_buy = round(presellprices[0], r)
        best_sell = round(prebuyprices[len(prebuyprices) - 1], r)

        sigma = -(((best_sell - best_buy) - 1) * inventory / UL)

        orders = []
        for direction in ("BUY", "SELL"):
            quantity = 0
            if direction == "SELL":
                quantity = max(0, UL - 1 - inventory)
                price = best_sell + sigma

            elif direction == "BUY":
                quantity = max(0, inventory - LL - 1)
                price = best_buy + sigma
            else:
                print('Direction is not specified for the market maker:', id(self))

            order = {'direction': direction,
                     'price': price,
                     'quantity': quantity,
                     'agent': id(self),
                     'order_type': order_type}
            # print("Printing order from order function:", order, "type: MM")
            orders.append(order)
        print('HFT: ', orders)
        return orders
