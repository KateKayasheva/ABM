# This is a sample Python script.

from Agent import RandomTrader, MarketMaker
from Market import Market
import random
import datetime


# class Engine():
#
#     def __init__(self):
#         pass
#
#     def __str__(self):
#         return "%s engine %s" % (self.__class__, id(self))
#
#     def run(self, agents, market):
#         pass

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

    for i in range(1, nmm):
        money = random.randint(rt[0], rt[1])
        stocks = random.randint(rt[2], rt[3])
        agent = MarketMaker(money, stocks)

        agents_list.append(agent)

    for i in range(1, nhft):
        pass

    return agents_list


def agents_dictionary(agents_list):
    d = {}
    for a in agents_list:
        d[id(a)] = a
    return d


params = {
    "RANDOM": [100, 1000, 0, 10],  # min money, max money, min stocks, max stocks
    "MM": [300, 2000, 0, 20],  # made them richer
    "HFT": []
}

agents = generate_agents(params, nrt=5, nmm=5)

agents_dict = agents_dictionary(agents)
market = Market()

for day in range(0, 4):

    print('DAY:', day)
    for i in agents:
        # print(i)
        # print(i.wealth())

        order = i.order(day=day, market=market)
        time = datetime.datetime.now().timestamp()  # time in seconds
        # print("time:", time)
        # print("\n")
        market.add_order(order, time)
    print("BUY:", market.buybook)
    print("SELL:", market.sellbook)

    print('PRICES DAY BEFORE:', market.preprices)

    market.match_orders(agents_dict)
    market.clear_books()
    print('--------------------------------------------')

    # for i in agents:
    #     print(i)
    #     print(i.wealth())
