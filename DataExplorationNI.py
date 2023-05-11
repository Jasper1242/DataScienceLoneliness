# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 13:38:07 2023

@author: Kasper
"""

import zipfile as zp
import pandas as pd
#from pypac import PACSession as Session #or use requests below if non-ONS
from requests import Session
from io import BytesIO
import os
import matplotlib.pyplot as plt


# Path to zip files
path = r"C:\Users\Kasper\Documents\Year 3\Data Science\loneliness-master\NI\\"


# Get drug data (NB some drugs duplicated for illnesses)
drug_data = pd.read_csv(path + r"..\drug_list.csv")

# column names
col_bnfname = "VTM_NM"
col_items = "Total Items"

# Function to find loneliness related prescribing
def code_loneliness(x):
    out = {}
    # coding by illness categories
    for illness in drug_data['illness'].unique():
        out[illness] = x[col_bnfname].str.contains("|".join(drug_data[drug_data['illness'] == illness]['medication']),
                                                 case=False, 
                                                 regex=True).astype('int16')
    # Make dataframe
    out = pd.DataFrame(out)
    # Add loneliness related disease binary - avoids double counting some drugs.
    out['loneliness'] = x[col_bnfname].str.contains("|".join(drug_data['medication'].unique()),
                                                  case = False, 
                                                  regex = True).astype('int16')
    # Return dataframe multiplied by counts of items.
    return out.multiply(x[col_items], axis=0)


# Make dictionary for aggregation
agg_cols = {col : 'sum' for col in drug_data['illness'].unique()}
agg_cols[col_items] = 'sum'
agg_cols['loneliness'] = 'sum'
for key in ['Date']:
    agg_cols[key] = 'first'
    
# Open prescribing files in pandas.
prescribe = pd.read_csv(path + "Prescriptions\\gp-prescribing---january-2023.csv", encoding = "ISO-8859-1")

# at least one of the NI prescription files has a blank row at the end - drop it
prescribe.dropna(inplace = True)

prescribe.columns = prescribe.columns.str.strip()


# make a date column
prescribe['Date'] = prescribe['Year'].astype(int).astype(str) + "-" + prescribe['Month'].astype(int).astype(str)
print(prescribe['Year'].iloc[1], prescribe['Month'].iloc[1])
print(prescribe['Date'].iloc[1])