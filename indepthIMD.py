# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 20:22:34 2023

@author: jaspi
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

path = r"C:\Users\jaspi\OneDrive - University of Bristol\Documents\Year 3\AI\Loneliness\Data Science\loneliness-master\Wales\\"

df= pd.read_csv(path + 'final_data.csv', index_col=0)

dfIMD = pd.read_csv(path+"IMDfeatures.csv",index_col = 0)
# df = df.sort_values(by=['imd'])

# dropList= []
# for index,row in df.iterrows():
   
#     try:
#         if (row['lsoa11'][0]) == 'E':
#             dropList.append(index)
            
#     except:
#         dropList.append(index)
        

# df.drop(df.index[dropList], inplace = True)
# df = df.reset_index(drop=True)
df = df[df['Date']==2021]

x = df['imd']
x = x.to_frame()
df1 = dfIMD.iloc[0:1909,2:11]
df1 = df1.reset_index(drop=True)
df2 = x.reset_index().merge(df1, how='inner').set_index('index')
df2 = df2.sort_index()
X = df2

y = df['loneills']

X = X.reset_index(drop=True)
y = y.reset_index(drop=True)

X.drop(X.index[[252,277]], inplace = True)
y.drop(y.index[[252,277]], inplace = True)

# box1 = X.index[X['Access to Services'] <= 250].tolist()
# box2 = X.index[(X['Access to Services'] > 250) & (X['Access to Services'] <= 500)].tolist()
# box3  = X.index[(X['Access to Services'] > 500) & (X['Access to Services'] <= 750)].tolist()
# box4 = X.index[(X['Access to Services'] > 750) & (X['Access to Services'] <= 1000)].tolist()
# box5 = X.index[(X['Access to Services'] > 1000) & (X['Access to Services'] <= 1250)].tolist()
# box6 = X.index[(X['Access to Services'] > 1250) & (X['Access to Services'] <= 1500)].tolist()
# box7 = X.index[(X['Access to Services'] > 1500) & (X['Access to Services'] <= 1750)].tolist()
# box8 = X.index[(X['Access to Services'] > 1750) & (X['Access to Services'] <= 2000)].tolist()

# b1values = y[y.index.isin(box1)]
# b2values = y[y.index.isin(box2)]
# b3values = y[y.index.isin(box3)]
# b4values = y[y.index.isin(box4)]
# b5values = y[y.index.isin(box5)]
# b6values = y[y.index.isin(box6)]
# b7values = y[y.index.isin(box7)]
# b8values = y[y.index.isin(box8)]

# data = [b1values,b2values,b3values,b4values,b5values,b6values,b7values,b8values]
# plt.boxplot(data, vert = 0)
# plt.xlabel("Loneliness Variable")
# plt.ylabel("IMD Domain : Access to Services Bins")
# plt.title("Whisker Plot of the Loneliness Variable for Increasing Levels of IMD")
# Ticks =[]
# labels = ["0-250","250-500","500-750","750-1000","1000-1250","1250-1500","1500-1750","1750-2000"]
# plt.yticks(np.arange(0,2000,250))
 
# plt.scatter(y,X.iloc[:,5])
# plt.xlabel('loneliness')
# plt.ylabel('IMD rank')
# plt.show()
# plt.figure()


f, axes = plt.subplots(4, 2,sharex=(True))

# axes.margins(0)
axes[0,0].scatter(y,X.iloc[:,0], s=10, c='green')
# axes[0,0].set_xlabel('Loneliness Variable')
axes[0,0].set_ylabel('IMD rank')

axes[0,1].scatter(y,X.iloc[:,1], s=10)
# axes[0,1].set_xlabel('Loneliness Variable')
axes[0,1].set_ylabel('Income rank')

axes[1,0].scatter(y,X.iloc[:,2], s=10, c='purple')
# axes[0,2].set_xlabel('Loneliness Variable')
axes[1,0].set_ylabel('Employment rank')


axes[1,1].scatter(y,X.iloc[:,3], s=10, c='orange')
# axes[1,0].set_xlabel('Loneliness Variable')
axes[1,1].set_ylabel('Health rank')


axes[2,0].scatter(y,X.iloc[:,4], s=10, c = 'red')
# axes[1,1].set_xlabel('Loneliness Variable')
axes[2,0].set_ylabel('Education rank')

axes[2,1].scatter(y,X.iloc[:,5], s=10, c = 'brown')
# axes[1,2].set_xlabel('Loneliness Variable')
axes[2,1].set_ylabel('Access to services rank')

axes[3,0].scatter(y,X.iloc[:,6], s=10, c='pink')
axes[3,0].set_xlabel('Loneliness Variable')
axes[3,0].set_ylabel('Community Saftey rank')

axes[3,1].scatter(y,X.iloc[:,7], s=10, c = 'gray')
axes[3,1].set_xlabel('Loneliness Variable')
axes[3,1].set_ylabel('Physical Enviroment rank')

# axes[4,0].scatter(y,X.iloc[:,8], s=10, c= 'olive')
# axes[4,0].set_xlabel('Loneliness Variable')
# axes[4,0].set_ylabel('Housing rank')






# axes[1].plot(monthFormatted, itemSum)
# axes[1].set_ylabel('Total Prescription Level')

# axes[2].plot(monthFormatted, monthPercent)
# axes[2].set_ylabel('Loneliness Percentage rate')
# # plt.loglog(monthFormatted,monthPercent)
# # plt.loglog(monthFormatted, itemSum)