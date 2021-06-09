import pandas as pd
import matplotlib.pyplot as plt

test = 'Test_5'
df = pd.read_csv('TestData/test_5.csv')
print(df)
last = df.sort_values('TIME').groupby('DAY').tail(1)
print(last)

pct0 = last['PRICE'].pct_change()
pct = pd.DataFrame()

pct['DAY'] = last['DAY']
pct['PRICE'] = pct0 * 100
print(pct)
print(pct[pct['PRICE'] == 0].iloc[0]['DAY'])
# first zero change day
d0 = int(pct[pct['PRICE'] == 0].iloc[0]['DAY'])


def price_change(c, e=1):
    if e == 1:
        d = pct[pct['PRICE'] == c]['DAY']
    elif e == 0:
        d = pct[pct['PRICE'] >= c]['DAY']

    days = []
    p = 0
    for i in d:
        if p + 1 != i:
            p = i
            days.append(i)
        else:
            p = i
    return days


days0 = price_change(0)
days7 = price_change(7, e=0)

top = plt.subplot2grid((6, 8), (0, 0), rowspan=3, colspan=8)
top.plot(last["DAY"], last["PRICE"], c='navy')
for i in days0:
    l = str(0) + '% price change at day ' + str(i)
    top.axvline(i, c='maroon', label=l)

for i in days7:
    l = str(7) + '% price change at day ' + str(i)
    top.axvline(i, c='darkgreen', label=l, ls='--')

top.legend()
plt.xlabel('DAY')
plt.ylabel('PRICE')

plt.title('{} Prices'.format(test))

bottom = plt.subplot2grid((6, 8), (3, 0), rowspan=1, colspan=8)
bottom.bar(last["DAY"], last['Q'], color='navy')

for i in days0:
    l = '0% price change at day ' + str(i)
    bottom.axvline(i, c='maroon', label=l)

for i in days7:
    l = str(7) + '% price change at day ' + str(i)
    bottom.axvline(i, c='darkgreen', label=l, ls='--')

plt.xlabel('DAY')
plt.ylabel('Volume (QUANTITY)')
plt.title('{} Trading Volume'.format(test))

bottom2 = plt.subplot2grid((6, 8), (4, 0), rowspan=2, colspan=8)
bottom2.plot(pct["DAY"], pct['PRICE'], c='navy')

for i in days0:
    l = '0% price change at day ' + str(i)
    bottom2.axvline(i, c='maroon', label=l)

for i in days7:
    l = str(7) + '% price change at day ' + str(i)
    bottom2.axvline(i, c='darkgreen', label=l, ls='--')

plt.title('{} Price change'.format(test))
plt.xlabel('DAY')
plt.ylabel('% price change')

plt.gcf().set_size_inches(15, 10)

plt.tight_layout(pad=3.0)
plt.show()
