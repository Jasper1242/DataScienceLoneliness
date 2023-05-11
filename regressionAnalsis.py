# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 12:33:52 2023

@author: Kasper
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression
import seaborn as sns; sns.set()


df = pd.read_csv('IMDdata2.csv')
df['lonelinessPercent'] = df['loneliness']/df['Items']



"""
Two Problems:
1)IMD data has NAN's appearing throughout, need to decide how to deal with them

2)IMD data has really high values way above the 1909 threshold for wales

Solution 2) drop all rows containing high scores seems they as been assigned to English LSOA's 
Example: row 14 contains postcode SY1 3GZ which is in shrewsbury and wouldnt be valid to compare agaisnt welsh ranks
"""

#Dropping rows with English LSOA's
dropList= []
for index,row in df.iterrows():
   
    try:
        if (row['lsoa11'][0]) == 'E':
            dropList.append(index)
            
    except:
        dropList.append(index)
        
df.drop(df.index[dropList], inplace = True)
y1 = df['loneliness']
y2 = df['lonelinessPercent']

x = df['imd']



# print(type(x))
# y.interpolate()
# x.fillna(0, inplace=True)
# threshold = 1909
# mask = x > threshold 

# print(x[2981])
# iList = []
# for (i,v) in enumerate(x):
#     if v >1909:
#         iList.append(i)


plt.figure()
f, axes = plt.subplots(2,1)
f.suptitle('Loneliness prescription rates and percentage of total against IMD ranking', fontsize=16)
# s = [20*4**n for n in range(len(y))]
axes[0].scatter(x,y1, s=10, c='red')
axes[0].set_ylabel('Loneliness Prescription Rate')
axes[0].set_xlabel('IMD rank (Lower is worse)')
a,b = np.polyfit(x,y1,1)
axes[0].plot(x,a*x+b, c='g')

axes[1].scatter(x,y2, s=10, c='red')
axes[1].set_ylabel('Loneliness Prescription as % of total prescriptions')
axes[1].set_xlabel('IMD rank (Lower is worse)')
c,d = np.polyfit(x,y2,1)
axes[1].plot(x,c*x+d, c='g')

# plt.scatter(x,y, s= 10, c= 'r')
# plt.ylabel('Loneliness Prescription Level')
# plt.xlabel('IMD rank')
# plt.title("Prescription Level against IMD ranking, with line of best fit")
# plt.plot(x,a*x+b, c='g')
plt.show()