# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 12:38:37 2023

@author: Kasper
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime



df = pd.read_csv("monthAnalysis.csv")
#df['Date'] = pd.to_datetime(df['Date']).dt.date


df2 = df[df['Items']>100]
df2['lonelinessPercent'] = df2['loneliness']/df2['Items']



#split into months
months = df2['Date'].unique()
monthFormatted=[]
for date in months:
    
    date_time_str = str(date)
    
    date_time_obj = datetime.strptime(date_time_str, '%Y%m').date()
    monthFormatted.append(date_time_obj)
    
monthSum = []
monthPercent = []
itemSum = []
for index,month in enumerate(months):
    dfTemp = len(df[df["Date"]==month])
    itemSum.append((df2.loc[df2['Date'] == month, 'Items'].sum()))
    monthSum.append(df2.loc[df2['Date'] == month, 'loneliness'].sum())
        
    monthPercent.append(df2.loc[df2['Date'] == month, 'lonelinessPercent'].sum()/dfTemp)

    
plt.figure()
f, axes = plt.subplots(3, 1)
axes[0].plot(monthFormatted,monthSum)
axes[0].set_ylabel('Loneliness Prescription Level')

axes[1].plot(monthFormatted, itemSum)
axes[1].set_ylabel('Total Prescription Level')

axes[2].plot(monthFormatted, monthPercent)
axes[2].set_ylabel('Loneliness Percentage rate')
# plt.loglog(monthFormatted,monthPercent)
# plt.loglog(monthFormatted, itemSum)