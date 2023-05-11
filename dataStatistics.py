# -*- coding: utf-8 -*-
"""
Created on Tue May  9 14:33:25 2023

@author: Kasper
"""

import pandas as pd
import matplotlib.pyplot as plt


path = r"C:\Users\jaspi\OneDrive - University of Bristol\Documents\Year 3\AI\Loneliness\Data Science\loneliness-master\Wales\\"


data = pd.read_csv(path + "processed_data_with_postcodes_GPs.csv", index_col = 0)
drug_data = pd.read_csv(path + r"..\drug_list.csv")
col_items = "Items"


# Make dictionary for aggregation
# counts to sum
agg_cols = {col : 'sum' for col in drug_data['illness'].unique()}
agg_cols[col_items] = 'sum'
agg_cols['loneliness'] = 'sum'
agg_cols['Number_of_Patients'] = 'sum'

# Other data to preserve
for key in ['HB','Street','Area','Posttown','Postcode',
            'oseast1m', 'osnrth1m', 'lsoa11', 'msoa11','ru11ind', 'rgn', 'laua', 'imd']:
    agg_cols[key] = 'first'
    
data = data.groupby(['lsoa11','Date'], as_index=False).agg(agg_cols)
# remove english msoa's

data = data.drop(data.index[0:24])
#remove outliers
data = data[data['Number_of_Patients']!=0]

# Generate percentages
perc_cols = drug_data['illness'].unique()
target_cols = perc_cols + '_perc'

# Percentages for discrete illness groups
data[target_cols] = data[perc_cols].divide(data[col_items], axis=0) * 100

# Overall percentage for loneliness realted disease prescribing
data['loneliness_perc'] = data['loneliness'].divide(data[col_items], axis=0) * 100


# Firstly aggregate percentages by postcodes by year.
# data['Year'] = data['Date'].dt.year
data['Date'] = data['Date'].map(lambda x: str(x)[:-2])
# data['Year'] = 2022

# Aggregation
cols = {'Number_of_Patients': 'mean', 'HB': 'first', 'oseast1m': 'first', 'osnrth1m': 'first',
        'lsoa11': 'first', 'msoa11': 'first', 'ru11ind': 'first', 'rgn': 'first', 'laua':'first', 'imd': 'first',
        'depression_perc': 'mean', 'alzheimers_perc': 'mean', 'blood pressure_perc': 'mean', 'hypertension_perc': 'mean',
        'diabeties_perc': 'mean', 'cardiovascular disease_perc': 'mean', 'insomnia_perc': 'mean', 'addiction_perc': 'mean',
        'social anxiety_perc': 'mean', 'loneliness_perc': 'mean'}

data = data.groupby(['lsoa11','Date'], as_index=False).agg(cols)

# The mean value returns a value broadly in the centre of the distribution of respective disease classes.
# Therefore we'll go with an un-truncated arithmetic mean.
# Can always revisit this assumption later.

per_cols = ['depression_perc', 'alzheimers_perc', 'blood pressure_perc', 'hypertension_perc', 
            'diabeties_perc', 'cardiovascular disease_perc', 'insomnia_perc', 'addiction_perc',
            'social anxiety_perc', 'loneliness_perc']

# Get mean and std for baseline (2022)
mean_std = data[data['Date'] == "2021"][per_cols].agg(['mean','std'])

# Make new column names.
std_cols = [col[:-4] + 'zscore' for col in per_cols]

zscores = []    
# z-score standardise for each year by baseline mean and std 
for year in ["2018","2019","2020","2021","2022","2023"]:
    zscores.append((data.loc[data['Date'] == year, per_cols] - mean_std.loc['mean', per_cols]) / mean_std.loc['std', per_cols])

zscores = pd.concat(zscores).sort_index()
data[std_cols] = zscores
# data.drop(data.index[[696,692,691,695,693,694]], inplace = True)

# plot zscores for loneliness
f, ax = plt.subplots(1,1, figsize = (14,6), sharey = True)#

# sum function ignores NAs
data['loneills'] =  data[['depression_zscore', 'alzheimers_zscore', 'hypertension_zscore', 'insomnia_zscore',
                      'addiction_zscore','social anxiety_zscore']].sum(axis=1)

data[data['Date'] == "2023"]['loneliness_zscore'].hist(bins=100, ax = ax)

# Save aggregated data
data.to_csv(path + "final_data.csv")
