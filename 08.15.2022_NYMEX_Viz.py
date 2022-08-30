#!/usr/bin/env python
# coding: utf-8

# In[96]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages


# In[175]:


# curves_df = pd.read_csv('08.09.2022_NYMEX_curves.csv')
# strips_df = pd.read_csv('08.09.2022_NYMEX_strips.csv')

curves_df = pd.read_csv('/root/NYMEX_Charts/08.09.2022_NYMEX_curves.csv')
strips_df = pd.read_csv('/root/NYMEX_Charts/08.09.2022_NYMEX_strips.csv')
curves_df


# In[3]:


strips_df


# In[82]:


from datetime import datetime
from datetime import date

strips = pd.DataFrame(set(strips_df['Strip']))
strips = strips.rename(columns={0:'Strip',})
strips['From'] = strips['Strip'].str[:5]
strips['To'] = strips['Strip'].str[6:]
strips = strips[strips['Strip']!='1']
strips['From'] = pd.to_datetime(strips['From'],format='%b%y')
strips['To'] = pd.to_datetime(strips['To'],format='%b%y')
strips['Today'] = pd.to_datetime(date.today())
strips['Days Away'] = (strips['To']-strips['Today']).dt.days
strips = strips[strips['Days Away'] > 0]
strips = strips.sort_values(by=['Days Away'])
strips = strips.reset_index()
strips = strips.drop(['index'], axis=1)
strips.loc[strips['Strip'].str[6:9] == 'Oct', 'Season'] = 's' 
strips.loc[strips['Strip'].str[6:9] != 'Oct', 'Season'] = 'w' 

print('The Nearest Strips Available')
strips
# print(strips['Strip'].values.tolist())


# In[98]:


strips_df['Keep'] = strips_df['Strip'].isin(strips['Strip'])
strips_df = strips_df[strips_df['Keep'] == True]
strips_df = strips_df.drop(['Keep'], axis=1)
strips_df['Trade Date'] = strips_df['Trade Date'].str[:9]
strips_df = strips_df.groupby(by=['Trade Date','Strip']).agg({'Price':np.average})
# strips_df = np.round(strips_df['Price'],4)
# strips_df = strips_df.rename(index=None, columns={'Date':'Trade Date'})
strips_df = strips_df.reset_index()
strips_df['Trade Date'] = pd.to_datetime(strips_df['Trade Date'])


days_df = pd.DataFrame(pd.date_range(strips_df['Trade Date'].min(),strips_df['Trade Date'].max(),freq='D'))
days_df = days_df.loc[days_df.index.repeat(len(strips))]
days_df = days_df.reset_index(drop=True)
days_df['Trade Date'] = days_df.iloc[:,0]
days_df = days_df.iloc[: , 1:]
days_df['Strip'] = pd.Series(strips['Strip'].values.tolist()*int(len(days_df)/len(strips)))

strips_df= pd.merge(days_df,strips_df,on=['Trade Date','Strip'],how='outer')


# In[176]:


curves_df['Keep'] = curves_df['Strip'].isin(strips['Strip'])
curves_df = curves_df[curves_df['Keep'] == True]
curves_df = curves_df.drop(['Keep'], axis=1)
curves_df['Len'] = curves_df['Trade Date'].map(len)

curves_df['Date'] = curves_df['Trade Date'].str[:9]
curves_df.loc[curves_df['Len']==14, 'Date']= curves_df['Trade Date'].str[:9]
curves_df.loc[curves_df['Len']==16, 'Date']= curves_df['Trade Date'].str[:10]
curves_df = curves_df.drop(['Len'], axis=1)

curves_df['Price'] = curves_df['Price'].astype(float)
# curves_df = curves_df.groupby(by=['Date', 'Contract Month', 'Strip']).agg({'Price':np.average})
# curves_df = np.round(curves_df['Price'],4)

curves_df = curves_df.reset_index()
# days_df
curves_df

# print(days_df.dtypes)
# print(strips_df.dtypes)


# In[6]:


# last_trades = pd.DataFrame(set(curves_df['Trade Date']))
# last_trades = last_trades.sort_values(by=[0])

# last_trades


# In[6]:


now_curve = pd.DataFrame(set(curves_df['Contract Month']))
now_curve = now_curve.sort_values(by=[0])

now_curve


# In[177]:


# strips_df[strips_df['Strip'].isin(strips['Strip'][0:3])]
curves_df['Date'] = pd.to_datetime(curves_df['Date'])
curves_df


# In[9]:


years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
yearsFmt = mdates.DateFormatter('%Y')

fig1 = plt.figure(figsize=(20,7))

sp1 = fig1.add_subplot(1,1,1)

# plot 1
sp1 = sns.lineplot(data = strips_df[strips_df['Strip'].isin(strips['Strip'][:])], x='Trade Date', y='Price', hue='Strip').set(title='All Live Strips')
ax = plt.gca()

ax.xaxis.set_major_locator(plt.MaxNLocator(20))
plt.xticks(rotation = 45)

# plot 2
sp2 = 0

# plt.gca().xaxis.set_major_formatter(dtFmt) # apply the format to the desired axis

# ymin, ymax = ax.get_ylim()
# custom_ticks = np.linspace(ymin, ymax, N, dtype=int)
# ax.set_yticks(custom_ticks)
# ax.set_yticklabels(custom_ticks)


# need to change these charts to be daily averages - done
# fill in the empty rows with a straight line

# plt.savefig('fig1.png')
plt.savefig('/root/GitHub/energynewz.github.io/fig1.png')
plt.show()


# In[10]:


fig2 = plt.figure(figsize=(20,7))

sp1 = fig2.add_subplot(1,1,1)

# plot 1
sp1 = sns.lineplot(data = strips_df[strips_df['Strip'].isin(strips['Strip'][0:3])], x='Trade Date', y='Price', hue='Strip').set(title='Prompt 3 Seasons')
ax = plt.gca()

ax.xaxis.set_major_locator(plt.MaxNLocator(20))
plt.xticks(rotation = 45)

# plot 2
sp2 = 0

# plt.gca().xaxis.set_major_formatter(dtFmt) # apply the format to the desired axis

# ymin, ymax = ax.get_ylim()
# custom_ticks = np.linspace(ymin, ymax, N, dtype=int)
# ax.set_yticks(custom_ticks)
# ax.set_yticklabels(custom_ticks)

# plt.savefig('fig2.png')
plt.savefig("/root/GitHub/energynewz.github.io/fig2.png")
plt.show()


# In[11]:


fig3 = plt.figure(figsize=(20,7))

sp1 = fig3.add_subplot(1,1,1)

# plot 1
sp1 = sns.lineplot(data = strips_df[strips_df['Strip'].isin(strips['Strip'][3:])], x='Trade Date', y='Price', hue='Strip').set(title='4th Season and Beyond')
ax = plt.gca()

ax.xaxis.set_major_locator(plt.MaxNLocator(20))
plt.xticks(rotation = 45)

# plot 2
sp2 = 0

# plt.gca().xaxis.set_major_formatter(dtFmt) # apply the format to the desired axis

# ymin, ymax = ax.get_ylim()
# custom_ticks = np.linspace(ymin, ymax, N, dtype=int)
# ax.set_yticks(custom_ticks)
# ax.set_yticklabels(custom_ticks)

# plt.savefig('fig3.png')
plt.savefig("/root/GitHub/energynewz.github.io/fig3.png")
plt.show()


# In[179]:


curves_df[curves_df['Trade Date'] == curves_df['Trade Date'].max()]
curves_df['Date'] = pd.to_datetime(curves_df['Date'])
curves_df['Trade Date'] = pd.to_datetime(curves_df['Trade Date'])
curves_df['Contract Month'] = pd.to_datetime(curves_df['Contract Month'])
curves_df = curves_df.sort_values(by=['Trade Date','Contract Month'], ascending=[False, True])
curves_df = curves_df.reset_index(drop=True)
curves_df


# In[180]:


fig4 = plt.figure(figsize=(20,7))

sp5 = fig4.add_subplot(1,1,1)

# plot 1
sp5 = sns.lineplot(data = curves_df[curves_df['Date'] == curves_df['Date'].max()],
                   x='Contract Month',
                   y='Price',
                   sort=True).set(title=str('Current NYMEX Henry Hub Curve\n'+str(curves_df['Trade Date'].max())))

plt.xticks(ticks=(curves_df[curves_df['Trade Date'] == curves_df['Trade Date'].max()]['Contract Month']), labels = curves_df[curves_df['Trade Date'] == curves_df['Trade Date'].max()]['Contract Month'].dt.strftime('%b%y'),rotation = 45)

# plot 2
sp2 = 0

# plt.gca().xaxis.set_major_formatter(dtFmt) # apply the format to the desired axis

# ymin, ymax = ax.get_ylim()
# custom_ticks = np.linspace(ymin, ymax, N, dtype=int)
# ax.set_yticks(custom_ticks)
# ax.set_yticklabels(custom_ticks)
print(curves_df['Date'].max())

# plt.savefig('fig4.png')
plt.savefig("/root/GitHub/energynewz.github.io/fig4.png")
plt.show()


# In[172]:


curves_df[curves_df['Trade Date'] == curves_df['Trade Date'].max()]['Contract Month'].dt.strftime('%b%y')


# In[ ]:


import datetime
today = datetime.datetime.now()

# wflows_log = pd.read_csv("wflows_log.csv")
wflows_log = pd.read_csv("/root/wflows_log.csv")

update_item = {'Process': ["NYMEX Viz"],
                'Time': [today],
                'Note': ['New Charts']
}
update_item = pd.DataFrame(update_item)

wflows_log = pd.concat([wflows_log,update_item])

# wflows_log.to_csv('wflows_log.csv', index=False)

wflows_log.to_csv("/root/wflows_log.csv", index=False)


# In[8]:


today = datetime.datetime.now()
print(today)

