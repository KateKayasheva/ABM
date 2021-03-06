import pandas as pd
import datetime

class Market:
    """
    Class for  the market.
    Stores buy/sell books for today and the previous day.
    Prices the day before.
    And data needed to be exported for analysis as Pandas.DataFrame
    """

    def __init__(self):
        self.buybook = []
        self.sellbook = []
        self.prebuy = []
        self.presell = []
        self.preprices = []
        self.data = None

    def create_database(self):
        COLUMNS = ['DAY', 'TIME', 'PRICE', 'Q',
                   'BUYER_ID', 'SELLER_ID',
                   'BUYER_TYPE', 'SELLER_TYPE',
                   'BUY_ORDER_TYPE', 'SELL_ORDER_TYPE']
        self.data = pd.DataFrame(columns=COLUMNS)
        print(self.data)

    def add_to_db(self, row):
        """
        :param row:  list of data (should be in the same order as columns)
        :return:
        """
        COLUMNS = ['DAY', 'TIME', 'PRICE', 'Q',
                   'BUYER_ID', 'SELLER_ID',
                   'BUYER_TYPE', 'SELLER_TYPE',
                   'BUY_ORDER_TYPE', 'SELL_ORDER_TYPE']
        df1 = self.data.copy()

        a_series = pd.Series(row, index=df1.columns)
        self.data = df1.append(a_series, ignore_index=True)

    def export_db(self, name):
        path = '/Users/kate/Documents/Programming/ABM/TestData4/'

        df = self.data
        df.to_csv(path + name, index=False, header=True)

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
        if order is None:
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
                [order['price'], time, order['quantity'], order['agent'], order['order_type'], order['day']])
            self.sellbook.sort(key=lambda x: x[1], reverse=True)  # now sorts on time high to low
            # TODO: sorting with nones inside
        elif order['direction'] == "BUY":
            self.buybook.append(
                [order['price'], -time, order['quantity'], order['agent'], order['order_type'], order['day']])
            self.buybook.sort(key=lambda x: x[1], reverse=True)
        else:
            print("Error in add_order: direction is not in correct format:",
                  order['direction'], '-> Order from agent:', order['agent'])

    def change_q_in_order(self, id, delta_q, book='SELL'):
        """
        Mainly for modifying sell orders when parts were already sold
        :param id: id of the agent
        :param delta_q: amount by which the order should be changed
        :return:
        """
        if book == "SELL":
            binary = [id == order[3] for order in self.sellbook]
            try:
                index = binary.index(True)  # index of an order which is needed to be modified
                order = self.sellbook[index]  # order which should be modified
                order[2] -= delta_q
            except ValueError:
                print('ID_SELL:', id)

        elif book == "BUY":
            binary = [id == order[3] for order in self.buybook]
            try:
                index = binary.index(True)  # index of an order which is needed to be modified
                order = self.buybook[index]  # order which should be modified
                order[2] -= delta_q
            except ValueError:
                print('ID_BUY:', id)

    def remove_zero_q_orders(self):
        """
        If the books contain orders with zero quantity, remove those orders.
        :return:
        """
        sell = self.sellbook.copy()
        for order in sell:
            if order[2] == 0:  # quantity is zero
                self.sellbook.remove(order)

        buy = self.buybook.copy()
        for order in buy:
            if order[2] == 0:  # quantity is zero
                self.buybook.remove(order)

    def match_orders(self, agents_dict):
        """
        run after orders are added
        Go through buybook if prices are equal try to match

        agents_dict: dictionary mapping ids of agents with objects
        :return:
        """
        prices = []
        buy = self.buybook.copy()
        for order_buy in buy:
            price_buy = order_buy[0]
            time_buy = order_buy[1]
            quantity_buy = order_buy[2]
            buy_id = order_buy[3]
            agent_buy = agents_dict[buy_id]
            order_type_buy = order_buy[4]
            day = order_buy[5]

            print('BUY ORDER:', order_buy)

            len_sellbook = len(self.sellbook)
            if len_sellbook == 0:
                break

            sell = self.sellbook.copy()
            remaining_stocks = quantity_buy
            for order_sell in sell:

                print('first87', remaining_stocks)
                if remaining_stocks == 0:
                    continue

                price_sell = order_sell[0]
                time_sell = order_sell[1]
                quantity_sell = order_sell[2]
                sell_id = order_sell[3]
                agent_sell = agents_dict[sell_id]
                order_type_sell = order_sell[4]
                print('SELL ORDER:', order_sell)
                Q_mod = '*'
                if sell_id == buy_id:
                    print('Cannot match orders from the same agent')
                    continue

                if quantity_sell == 0:
                    print('Skipped due to q=0')
                    continue

                if order_type_buy == 'L':
                    print('in l1')
                    """
                    For now limit orders only match at equal price and also matched with market orders on the sell side
                    """
                    if order_type_sell == 'L':
                        print('in l12')
                        if price_sell == price_buy:

                            if remaining_stocks <= quantity_sell:
                                quantity = remaining_stocks
                                agent_sell.record(direction="SELL", price=price_sell, quantity=quantity)
                                agent_buy.record(direction="BUY", price=price_sell, quantity=quantity)
                                prices.append(price_sell)
                                print("DEAL1", 'buyid:', id(agent_buy), 'sellid:', id(agent_sell), price_sell)
                                remaining_stocks = 0
                                Q_mod = quantity
                                self.change_q_in_order(id=sell_id, delta_q=Q_mod, book="SELL")
                                row = [day, datetime.datetime.now().timestamp(), price_sell, quantity,
                                       id(agent_buy), id(agent_sell),
                                       agent_buy.type, agent_sell.type,
                                       order_type_buy, order_type_sell]
                                self.add_to_db(row)

                            elif remaining_stocks > quantity_sell:
                                quantity = quantity_sell
                                agent_sell.record(direction="SELL", price=price_sell, quantity=quantity)
                                agent_buy.record(direction="BUY", price=price_sell, quantity=quantity)
                                prices.append(price_sell)
                                remaining_stocks = remaining_stocks - quantity
                                Q_mod = quantity
                                self.change_q_in_order(id=sell_id, delta_q=Q_mod, book="SELL")

                                print("DEAL2", 'buyid:', id(agent_buy), 'sellid:', id(agent_sell), price_sell)
                                row = [day, datetime.datetime.now().timestamp(), price_sell, quantity,
                                       id(agent_buy), id(agent_sell),
                                       agent_buy.type, agent_sell.type,
                                       order_type_buy, order_type_sell]
                                self.add_to_db(row)

                        elif price_sell < price_buy:
                            # TODO: quantity should be adjusted since the price is changed
                            if remaining_stocks <= quantity_sell:
                                quantity = remaining_stocks
                                agent_sell.record(direction="SELL", price=price_sell, quantity=quantity)
                                agent_buy.record(direction="BUY", price=price_sell, quantity=quantity)
                                prices.append(price_sell)

                                remaining_stocks = 0
                                Q_mod = quantity
                                self.change_q_in_order(id=sell_id, delta_q=Q_mod, book="SELL")
                                print("DEAL3", 'buyid:', id(agent_buy), 'sellid:', id(agent_sell), price_sell)
                                row = [day, datetime.datetime.now().timestamp(), price_sell, quantity,
                                       id(agent_buy), id(agent_sell),
                                       agent_buy.type, agent_sell.type,
                                       order_type_buy, order_type_sell]
                                self.add_to_db(row)

                            elif remaining_stocks > quantity_sell:
                                quantity = quantity_sell
                                agent_sell.record(direction="SELL", price=price_sell, quantity=quantity)
                                agent_buy.record(direction="BUY", price=price_sell, quantity=quantity)
                                prices.append(price_sell)
                                remaining_stocks = remaining_stocks - quantity
                                Q_mod = quantity
                                self.change_q_in_order(id=sell_id, delta_q=Q_mod, book="SELL")
                                print('DEAL4', 'buyid:', id(agent_buy), 'sellid:', id(agent_sell), price_sell)
                                row = [day, datetime.datetime.now().timestamp(), price_sell, quantity,
                                       id(agent_buy), id(agent_sell),
                                       agent_buy.type, agent_sell.type,
                                       order_type_buy, order_type_sell]
                                self.add_to_db(row)


                    elif order_type_sell == 'M':
                        print('in M11')

                        if remaining_stocks <= quantity_sell:

                            print('in d3')
                            quantity = remaining_stocks
                            agent_sell.record(direction="SELL", price=price_buy, quantity=quantity)
                            agent_buy.record(direction="BUY", price=price_buy, quantity=quantity)
                            prices.append(price_buy)
                            remaining_stocks = 0
                            Q_mod = quantity
                            self.change_q_in_order(id=sell_id, delta_q=Q_mod, book="SELL")
                            print("DEAL5", 'buyid:', id(agent_buy), 'sellid:', id(agent_sell), price_buy)
                            row = [day, datetime.datetime.now().timestamp(), price_buy, quantity,
                                   id(agent_buy), id(agent_sell),
                                   agent_buy.type, agent_sell.type,
                                   order_type_buy, order_type_sell]
                            self.add_to_db(row)


                        elif remaining_stocks > quantity_sell:
                            print('in d4')
                            quantity = quantity_sell
                            agent_sell.record(direction="SELL", price=price_buy, quantity=quantity)
                            agent_buy.record(direction="BUY", price=price_buy, quantity=quantity)
                            prices.append(price_buy)
                            remaining_stocks = remaining_stocks - quantity
                            print('DEAL6', 'buyid:', id(agent_buy), 'sellid:', id(agent_sell), price_buy)
                            Q_mod = quantity
                            self.change_q_in_order(id=sell_id, delta_q=Q_mod, book="SELL")
                            row = [day, datetime.datetime.now().timestamp(), price_buy, quantity,
                                   id(agent_buy), id(agent_sell),
                                   agent_buy.type, agent_sell.type,
                                   order_type_buy, order_type_sell]
                            self.add_to_db(row)
                    else:
                        print(order_type_buy, order_type_sell, 'skipped L1')

                elif order_type_buy == 'M':
                    print(agent_buy.money)
                    if order_type_sell == 'L':
                        print('in m2')
                        """
                        For market orders any sell order is applicable
                        """
                        if agent_buy.money >= price_sell * quantity_sell:
                            quantity = quantity_sell
                            agent_sell.record(direction="SELL", price=price_sell, quantity=quantity)
                            agent_buy.record(direction="BUY", price=price_sell, quantity=quantity)
                            prices.append(price_sell)
                            Q_mod = quantity
                            self.change_q_in_order(id=sell_id, delta_q=Q_mod, book="SELL")
                            print('DEAL7', 'buyid:', id(agent_buy), 'sellid:', id(agent_sell), price_sell)
                            row = [day, datetime.datetime.now().timestamp(), price_sell, quantity,
                                   id(agent_buy), id(agent_sell),
                                   agent_buy.type, agent_sell.type,
                                   order_type_buy, order_type_sell]
                            self.add_to_db(row)

                        elif agent_buy.money <= price_sell * quantity_sell:
                            quantity = int(agent_buy.money / price_sell)
                            if quantity > 0:
                                agent_sell.record(direction="SELL", price=price_sell, quantity=quantity)
                                agent_buy.record(direction="BUY", price=price_sell, quantity=quantity)
                                prices.append(price_sell)
                                Q_mod = quantity
                                self.change_q_in_order(id=sell_id, delta_q=Q_mod, book="SELL")
                                print('DEAL8', 'buyid:', id(agent_buy), 'sellid:', id(agent_sell), price_sell)
                                row = [day, datetime.datetime.now().timestamp(), price_sell, quantity,
                                       id(agent_buy), id(agent_sell),
                                       agent_buy.type, agent_sell.type,
                                       order_type_buy, order_type_sell]
                                self.add_to_db(row)

                    elif order_type_sell == 'M':
                        pass

                    else:
                        print('skipped m2')
                else:
                    print('skipped everything: order_type is not in correct format',
                          order_type_buy, order_type_sell)
                print('REMAINS TO BUY', remaining_stocks)
                # print(Q_mod)

                """
                Modifying sellers quantity to avoid double selling
                Removing orders with quantity equal to zero
                """
                # if Q_mod != '*':
                #     self.change_q_in_order(id=sell_id, delta_q=Q_mod, book="SELL")
                self.remove_zero_q_orders()
                # print(self.buybook)
                # print(self.sellbook)

        self.preprices = prices

# market = Market()
# market.add_order({'direction': 'SELL', 'quantity': 2, 'price': 3, 'agent': 1}, 1)
# market.add_order({'direction': 'SELL', 'quantity': 2, 'price': 4, 'agent': 2}, 2)
# market.add_order({'direction': 'SELL', 'quantity': 2, 'price': 1, 'agent': 3}, 1)
# print(market.sellbook)
# print(market.preprices)
