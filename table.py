import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('TestData2/test_2.csv')
print(df)
last = df.sort_values('TIME').groupby('DAY').tail(1)
print(last)

pct0 = last['PRICE'].pct_change()
pct = pd.DataFrame()

pct['DAY'] = last['DAY']
pct['PRICE'] = pct0
print(pct)
print(pct[pct['PRICE'] == 0].iloc[0]['DAY'])
# first zero change day

d0 = int(pct[pct['PRICE'] == 0].iloc[0]['DAY'])
l = 'Zero price change at day ' + str(d0)

d = pct[pct['PRICE'] == 0]['DAY']

days = []
p = 0
for i in d:
    if p + 1 != i:
        p = i
        days.append(i)
    else:
        p = i


top = plt.subplot2grid((6,8), (0, 0), rowspan=3, colspan=8)
top.plot(last["DAY"], last["PRICE"], c='navy')
for i in days:
    l = 'Zero price change at day ' + str(i)
    top.axvline(i, c='maroon', label=l)
top.legend()
plt.xlabel('DAY')
plt.ylabel('PRICE')

plt.title('TEST_2 Prices')

bottom = plt.subplot2grid((6,8), (3,0), rowspan=1, colspan=8)
bottom.bar(last["DAY"], last['Q'], color='navy')
for i in days:
    l = 'Zero price change at day ' + str(i)
    bottom.axvline(i, c='maroon', label=l)

plt.xlabel('DAY')
plt.ylabel('Volume (QUANTITY)')
plt.title('TEST_2 Trading Volume')

bottom2 = plt.subplot2grid((6,8), (4,0), rowspan=2, colspan=8)
bottom2.plot(pct["DAY"], pct['PRICE'], c='navy')
for i in days:
    l = 'Zero price change at day ' + str(i)
    bottom2.axvline(i, c='maroon', label=l)

plt.title('TEST_2 Price change')
plt.xlabel('DAY')
plt.ylabel('Percentage price change')


plt.gcf().set_size_inches(15,10)


plt.tight_layout(pad=3.0)
plt.show()



