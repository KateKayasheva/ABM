class Market:
    """
    Class for  the market. Stores buy/sell books
    """

    def __init__(self):
        self.buybook = []
        self.sellbook = []
        self.prebuy = []
        self.presell = []
        self.preprices = []

    def clear_books(self):
        """
        Reset books to an empty state and copy data for 1 day backup
        """
        self.prebuy = self.buybook
        self.presell = self.sellbook

        self.sellbook = []
        self.buybook = []


    def add_order(self, order, time):
        """
        Adds order to either sellbook or buybook

        :param order: order from agent.order()
        order format dictionary as {'direction': direction, 'price': price, 'quantity': quantity, 'agent': id(self)}
        :param time: time at which the order gets to the market
        :return:
        """
        # Allow only one order per agent
        for book in (self.sellbook, self.buybook):
            for line in book:
                if order['agent'] == line[3]:
                    book.remove(line)
                    break
        # Separate orders into BUY / SELL
        if order['direction'] == "SELL":
            self.sellbook.append(
                [order['price'], time, order['quantity'], order['agent']])
            self.sellbook.sort(key=lambda x: -x[0]) # now sorts on price high to low (-)
        elif order['direction'] == "BUY":
            self.buybook.append(
                [order['price'], -time, order['quantity'], order['agent']])
            self.buybook.sort(key=lambda x: -x[0])
        else:
            print("Error in add_order: direction is not in correct format:",
                    order['direction'], '-> Order from agent:', order['agent'])


    def match_orders(self, agents_dict):
        """
        run after orders are added
        Go through buybook if price in sellbook is not higher - match

        agents_dict: dictionary mapping ids of agents with objects
        :return:
        """
        prices = []
        for order_buy in self.buybook:
            price_buy = order_buy[0]
            time_buy = order_buy[1]
            quantity_buy = order_buy[2]
            agent_buy = agents_dict[order_buy[3]]
            for order_sell in self.sellbook:
                price_sell = order_sell[0]
                time_sell = order_sell[1]
                quantity_sell = order_sell[2]
                agent_sell = agents_dict[order_sell[3]]
                if price_sell <= price_buy:
                    # TODO: at what price to match
                    agent_sell.record(direction="SELL", price=price_sell, quantity=min(quantity_sell, quantity_buy))
                    agent_buy.record(direction="BUY", price=price_sell, quantity=min(quantity_sell, quantity_buy))
                    prices.append(price_sell)
                    break


        self.preprices = prices


# market = Market()
# market.add_order({'direction': 'SELL', 'quantity': 2, 'price': 3, 'agent': 1}, 1)
# market.add_order({'direction': 'SELL', 'quantity': 2, 'price': 4, 'agent': 2}, 2)
# market.add_order({'direction': 'SELL', 'quantity': 2, 'price': 1, 'agent': 3}, 1)
# print(market.sellbook)
# print(market.preprices)
