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
        order format dictionary as
                                    {'direction': direction,
                                    'price': price,
                                    'quantity': quantity,
                                    'agent': id(self),
                                    'order_type': order_type}
        :param time: time at which the order gets to the market
        :return:
        """
        # skipping None orders
        if order == None:
            return None

        # Allow only one order per agent
        for book in (self.sellbook, self.buybook):
            for line in book:

                if order['agent'] == line[3]:
                    book.remove(line)
                    break

        # Separate orders into BUY / SELL
        if order['direction'] == "SELL":
            self.sellbook.append(
                [order['price'], time, order['quantity'], order['agent'], order['order_type']])
            # self.sellbook.sort(key=lambda x: x[0], reverse=True)  # now sorts on price high to low
            # TODO: sorting with nones inside
        elif order['direction'] == "BUY":
            self.buybook.append(
                [order['price'], -time, order['quantity'], order['agent'], order['order_type']])
            # self.buybook.sort(key=lambda x: x[0], reverse=True)
        else:
            print("Error in add_order: direction is not in correct format:",
                  order['direction'], '-> Order from agent:', order['agent'])

    def match_orders(self, agents_dict):
        """
        run after orders are added
        Go through buybook if prices are equal try to match

        agents_dict: dictionary mapping ids of agents with objects
        :return:
        """
        prices = []

        for order_buy in self.buybook:
            price_buy = order_buy[0]
            time_buy = order_buy[1]
            quantity_buy = order_buy[2]
            agent_buy = agents_dict[order_buy[3]]
            order_type_buy = order_buy[4]
            print('BUY ORDER:', order_buy)

            remaining_stocks = quantity_buy
            len_sellbook = len(self.sellbook)
            i = 0
            while remaining_stocks > 0 and i < len_sellbook:
                for order_sell in self.sellbook:
                    i += 1
                    price_sell = order_sell[0]
                    time_sell = order_sell[1]
                    quantity_sell = order_sell[2]
                    agent_sell = agents_dict[order_sell[3]]
                    order_type_sell = order_sell[4]
                    print('SELL ORDER:', order_sell)

                # TODO: need to modify the sell/buy book after matching the order
                if order_type_buy == 'L':
                    """
                    For now limit orders only match at equal price and also matched with market orders on the sell side
                    """
                    if order_type_sell == 'L':
                        if price_sell == price_buy:

                            if quantity_buy <= quantity_sell:
                                quantity = quantity_buy
                                agent_sell.record(direction="SELL", price=price_sell, quantity=quantity)
                                agent_buy.record(direction="BUY", price=price_sell, quantity=quantity)
                                prices.append(price_sell)
                                print("DEAL")
                                remaining_stocks = 0

                            elif quantity_buy > quantity_sell:
                                quantity = quantity_sell
                                agent_sell.record(direction="SELL", price=price_sell, quantity=quantity)
                                agent_buy.record(direction="BUY", price=price_sell, quantity=quantity)
                                prices.append(price_sell)
                                remaining_stocks = remaining_stocks - quantity_sell

                                print("DEAL")

                    if order_type_sell == 'M':

                        if quantity_buy <= quantity_sell:
                            quantity = quantity_buy
                            agent_sell.record(direction="SELL", price=price_buy, quantity=quantity)
                            agent_buy.record(direction="BUY", price=price_buy, quantity=quantity)
                            prices.append(price_buy)
                            remaining_stocks = 0
                            print("DEAL")
                            break
                        elif quantity_buy > quantity_sell:
                            quantity = quantity_sell
                            agent_sell.record(direction="SELL", price=price_buy, quantity=quantity)
                            agent_buy.record(direction="BUY", price=price_buy, quantity=quantity)
                            prices.append(price_buy)
                            remaining_stocks = remaining_stocks - quantity_sell

                if order_type_buy == 'M':
                    """
                    For market orders any sell order is applicable
                    """

                    if quantity_buy <= quantity_sell:
                        quantity = quantity_buy
                        agent_sell.record(direction="SELL", price=price_sell, quantity=quantity)
                        agent_buy.record(direction="BUY", price=price_sell, quantity=quantity)
                        prices.append(price_sell)
                        remaining_stocks = 0
                        print("DEAL")
                        break
                    elif quantity_buy > quantity_sell:
                        quantity = quantity_sell
                        agent_sell.record(direction="SELL", price=price_sell, quantity=quantity)
                        agent_buy.record(direction="BUY", price=price_sell, quantity=quantity)
                        prices.append(price_sell)
                        remaining_stocks = remaining_stocks - quantity_sell
                        print("DEAL")

        self.preprices = prices

# market = Market()
# market.add_order({'direction': 'SELL', 'quantity': 2, 'price': 3, 'agent': 1}, 1)
# market.add_order({'direction': 'SELL', 'quantity': 2, 'price': 4, 'agent': 2}, 2)
# market.add_order({'direction': 'SELL', 'quantity': 2, 'price': 1, 'agent': 3}, 1)
# print(market.sellbook)
# print(market.preprices)
