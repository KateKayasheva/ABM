# This is a sample Python script.

from Agent import RandomTrader, MarketMaker, HFT
from Market import Market
import random
import datetime


def generate_agents(param, nrt, nmm=0, nhft=0):
    """

    :param param: parameters for initial values for agents ( min money, max money, number of stocks ) as dictionary
            params = {
                    "RANDOM": [100, 1000, 0, 10], # min money, max money, min stocks, max stocks
                    "MM": [],
                    "HFT": []
                    }
    :param nrt: number of random traders
    :param nmm: number of market makers
    :param nhft: number of high frequency traders
    :return: list of all agents
    """
    agents_list = []

    rt = param["RANDOM"]

    for i in range(0, nrt):
        money = random.randint(rt[0], rt[1])
        stocks = random.randint(rt[2], rt[3])
        agent = RandomTrader(money, stocks)

        agents_list.append(agent)

    mm = param["MM"]
    for i in range(0, nmm):
        money = random.randint(mm[0], mm[1])
        stocks = random.randint(mm[2], mm[3])
        agent = MarketMaker(money, stocks)

        agents_list.append(agent)

    hft = param["HFT"]
    for i in range(0, nhft):
        money = random.randint(hft[0], hft[1])
        stocks = random.randint(hft[2], hft[3])
        agent = HFT(money, stocks)

        agents_list.append(agent)

    return agents_list


def agents_dictionary(agents_list):
    d = {}
    for a in agents_list:
        d[id(a)] = a
    return d


params = {
    "RANDOM": [100, 1000, 0, 10],  # min money, max money, min stocks, max stocks
    "MM": [300, 2000, 0, 20],  # made them richer
    "HFT": [100, 1000, 0, 10]
}

agents = generate_agents(params, nrt=5, nmm=5, nhft=1)

agents_dict = agents_dictionary(agents)
market = Market()
market.create_database()

for day in range(0, 20):

    print('DAY:', day)
    for a in agents:
        if a.money < 0 or a.stocks < 0: print('N------------N')
        print(a)
        print(a.wealth())
        if a.money < 0 or a.stocks < 0: print('N------------N')

        if a.money < 0 or a.stocks < 0: break

        orders = a.order(day=day, market=market)
        time = datetime.datetime.now().timestamp()  # time in seconds
        # print("time:", time)
        # print("\n")
        """
        Need to iterate since market makers can have two orders stored as a list of dictionaries
        """
        # print(orders)
        if type(orders) == list:
            for order in orders:
                market.add_order(order, time)
        elif type(orders) == dict:
            market.add_order(orders, time)
        else:
            try:
                market.add_order(orders, time)
            finally:
                pass
                # print("Cannot add order, Order type:",  type(orders))

    print("BUY:", market.buybook)
    print("SELL:", market.sellbook)

    print('PRICES DAY BEFORE:', market.preprices)

    market.match_orders(agents_dict)
    # print("BUY:", market.buybook)
    # print("SELL:", market.sellbook)
    market.clear_books()
    print('--------------------------------------------')
    print(market.data)

    # for a in agents:
    #     print(a)
    #     print(a.wealth())
