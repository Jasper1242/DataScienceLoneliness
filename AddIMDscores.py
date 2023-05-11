# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 18:57:51 2023

@author: jaspi
"""

import pandas as pd
path = r"C:\Users\jaspi\OneDrive - University of Bristol\Documents\Year 3\AI\Loneliness\Data Science\loneliness-master\Wales\\"
IMD = pd.read_csv(path + 'Index_of_Multiple_Deprivation_(Dec_2019)_Lookup_in_Wales.csv')
print(IMD.head())
IMDdomains = pd.read_excel(path + 'export.xlsx')
# keys1 = wimd_2019
df1 = IMD[['wimd_2019','lsoa11cd']]
df1 = df1.sort_values(by=['wimd_2019'])
df1 = df1.set_index(['wimd_2019'])



df2 = IMDdomains[['Unnamed: 1','WIMD ', 'Income ',
       'Employment ', 'Health ', 'Education ', 'Access to Services ',
       'Community Safety ', 'Physical Environment ', 'Housing ']]
df2 = df2[df2['Unnamed: 1'].notna()]
df2 = df2.sort_values(by=['WIMD '])
df2 = df2.set_index(['WIMD '])


df3 = df1.join(df2)
df3 = df3.rename(columns={'Unnamed: 1': "Area", 'Income ':'Income', 'Employment ':'Employment' , 'Health ':'Health',
       'Education ':'Education', 'Access to Services ':'Access to Services', 'Community Safety ':'Community Safety',
       'Physical Environment ':'Physical Environment', 'Housing ': 'Housing'})
df3['imd'] = df3.index

df3.to_csv(path + "IMDfeatures.csv")