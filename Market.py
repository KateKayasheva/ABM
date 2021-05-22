class Market:
    """
    Class for  the market. Stores buy/sell books
    """

    def __init__(self):
        self.buybook = []
        self.sellbook = []
        self.prebuy = []
        self.presell = []

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
            self.sellbook.sort()
        elif order['direction'] == "BUY":
            self.buybook.append(
                [order['price'], -time, order['quantity'], order['agent']])
            self.buybook.sort()
        else:
            print("Error in add_order: direction is not in correct format:",
                    order['direction'], '-> Order from agent:', order['agent'])


market = Market()
market.add_order({'direction': 'SELL', 'quantity': 2, 'price': 3, 'agent': 1}, 1)
market.add_order({'direction': 'SELL', 'quantity': 2, 'price': 4, 'agent': 2}, 2)
market.add_order({'direction': 'SELL', 'quantity': 2, 'price': 1, 'agent': 3}, 1)
print(market.sellbook)
print(market.buybook)
