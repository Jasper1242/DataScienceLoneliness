# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 14:17:24 2023

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
path = r"C:\Users\Kasper\Documents\Year 3\Data Science\loneliness-master\\England\\"

# Get drug data (NB some drugs duplicated for illnesses)
drug_data = pd.read_csv(path + r"..\drug_list.csv")

# Function to find loneliness related prescribing
def code_loneliness(x):
    out = {}
    # coding by illness categories
    for illness in drug_data['illness'].unique():
        out[illness] = x['BNF NAME'].str.contains("|".join(drug_data[drug_data['illness'] == illness]['medication']),
                                                  case=False, 
                                                  regex=True).astype('int16')
    # Make dataframe
    out = pd.DataFrame(out)
    # Add loneliness related disease binary - avoids double counting some drugs.
    out['loneliness'] = x['BNF NAME'].str.contains("|".join(drug_data['medication'].unique()),
                                                   case = False, 
                                                   regex = True).astype('int16')
    # Return dataframe multiplied by counts of items.
    return out.multiply(x['ITEMS'], axis=0)

# Make dictionary for aggregation
agg_cols = {col : 'sum' for col in drug_data['illness'].unique()}
agg_cols['ITEMS'] = 'sum'
agg_cols['loneliness'] = 'sum'
for key in ['Date','SHA','PCT','pcstrip','CenterName','Street','Town','Town2','Postcode']:
    agg_cols[key] = 'first'
    
monthly_data = []

for file in os.listdir(path + "zip"):
    with zp.ZipFile(path + "zip\\" + file) as zipf:
        zip_names = zipf.namelist()

        # Deal with Address Files
        addr_name = next((filename for filename in zip_names if "ADDR" in filename), None)
        # Open address file in pandas, set header.
        addr = pd.read_csv(zipf.open(addr_name), 
                           header=0, 
                           names = ["Date", "PracCode", "PracName","CenterName",
                                    "Street", "Town", "Town2", "Postcode"], 
                           usecols = range(8))

        # Deal with prescription info
        prescribe_name = next((filename for filename in zip_names if "PDPI" in filename), None)
        # Open prescribing files in pandas.
        prescribe = pd.read_csv(zipf.open(prescribe_name))
        prescribe.columns = prescribe.columns.str.strip()
        # Get counts of prescribing dataframe for loneliness related diseases
        loneliness_prescribing = code_loneliness(prescribe[['BNF NAME','ITEMS']])
        # merge dataframes
        prescribe = prescribe.merge(loneliness_prescribing, left_index=True, right_index=True)
        del loneliness_prescribing
        
        # merge in address information
        prescribe = prescribe.merge(addr, left_on = 'PRACTICE', right_on = 'PracCode')
        del addr
        
        # Create uniform postcode field
        prescribe['pcstrip'] = prescribe['Postcode'].str.replace("\s","")
        
        # get a summary - grouping by PracCode
        summary = prescribe.groupby('PracCode', as_index=False).agg(agg_cols)
        del prescribe
        
        monthly_data.append(summary)
        print(file)
        
        
# concatenate all the monthly data together.
data = pd.concat(monthly_data, ignore_index = True)

# Save aggregated data
data.to_csv(path + "processed_data.csv")
