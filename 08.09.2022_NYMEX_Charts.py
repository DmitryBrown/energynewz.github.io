#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re
import urllib.request
import pandas as pd
import copy
from datetime import datetime
import numpy as np

#pull the html/xml data from site into a giant string
url=('https://www.teletrader.com/quickbar/Henry_Hub_Natural_Gas_Futures_ETH_Energy_NYMEX_Futures')

items=re.compile(r"<tr class.*?</tr>")
answeritems=[]
allcontracts=[]
today=datetime.today()
today = today.strftime("%Y-%m-%d %H:%M")

f = urllib.request.urlopen(url)

contents = str(f.readlines())

f.close()


# In[ ]:


#parse the giant string of site data with regular expressions to pull out the pricing data
#the product of thiese lines is a list of lists 
answeritems=items.findall(contents)[8:]

for i in answeritems:
    tts=re.compile(r'-\d\d\d\d\d\d\d\d')
    monthyear=re.compile(r'-\d-\d\d')
    twomonthyear=re.compile(r'-\d\d-\d\d')
    price=re.compile(r'delayed">.*?<')

    ttsnumber=str(set(tts.findall(i)))[3:11]
    monthy=(str(set(monthyear.findall(i)))[3:7]+str(set(twomonthyear.findall(i)))[3:8]).replace("()","").replace("-","-01-")
    contractprice=float(str(set(price.findall(i)))[11:].replace("<'}",""))
    strip=int(monthy[:2].replace("-",""))
    stripm=int(monthy[:2].replace("-",""))

    if strip == 11 or strip==12:
        strip="Nov"+str(monthy[-2:])+"-Mar"+str(int(monthy[-2:])+1)
    elif strip == 1 or strip==2 or strip==3:
        strip="Nov"+str(int(monthy[-2:])-1)+"-Mar"+str(monthy[-2:])
    else:
        strip="Apr"+str(monthy[-2:])+"-Oct"+str(monthy[-2:])
   
    allcontracts.append((ttsnumber,monthy,contractprice,strip))

#print(allcontracts)

#Convert the list into a Pandas dataframe
#give the columns some names
df=pd.DataFrame(allcontracts)
df.columns=["TTS","Contract Month","Price","Strip"]

#Create Average Strip Table
dfstrips=copy.deepcopy(df)

dfstrips.drop("TTS",1, inplace=True)
dfstrips.drop("Contract Month",1,inplace=True)

dfstrips=dfstrips.groupby(['Strip']).mean()

TradeDate=[today]*len(dfstrips)
TradeDatedf=[today]*(len(df))

Index=np.linspace(0,len(dfstrips)-1,len(dfstrips))

dfstrips['Trade Date']=TradeDate
df['Trade Date']=TradeDatedf
dfstrips=dfstrips.reset_index()


# In[ ]:


#find the first empty row in NYMEX_curves csv file

wks = pd.read_csv('/root/NYMEX_Charts/08.09.2022_NYMEX_curves.csv')
wks2 = pd.read_csv('/root/NYMEX_Charts/08.09.2022_NYMEX_strips.csv')

wks = pd.concat([wks,df])
wks2 = pd.concat([wks2,dfstrips])

wks2


# In[ ]:


# wks.to_csv('08.09.2022_NYMEX_curves.csv', index=False)
# wks2.to_csv('08.09.2022_NYMEX_strips.csv', index=False)

wks.to_csv('/root/NYMEX_Charts/08.09.2022_NYMEX_curves.csv', index=False)
wks2.to_csv("/root/NYMEX_Charts/08.09.2022_NYMEX_strips.csv", index=False)


# In[ ]:


# wflows_log = pd.read_csv("wflows_log.csv")
wflows_log = pd.read_csv("/root/wflows_log.csv")


# In[ ]:


update_item = {'Process': ["NYMEX Charts"],
                'Time': [today],
                'Note': ['Updated Curves and Strips']
}
update_iem = pd.DataFrame(update_item)

wflows_log = pd.concat([wflows_log,update_iem])

# wflows_log.to_csv('wflows_log.csv', index=False)

wflows_log.to_csv("/root/wflows_log.csv", index=False)

