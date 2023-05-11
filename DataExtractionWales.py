# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 13:49:41 2023

@author: Kasper
"""

import zipfile as zp
import pandas as pd
#from pypac import PACSession as Session #or use requests below if non-ONS
from requests import Session
from io import BytesIO
import os
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

"""files from https://nwssp.nhs.wales/ourservices/primary-care-services/general-information/data-and-publications/prescribing-data-extracts/general-practice-prescribing-data-extract/
"""

# Path to zip files
path = r"C:\Users\jaspi\OneDrive - University of Bristol\Documents\Year 3\AI\Loneliness\Data Science\loneliness-master\Wales\\"

# Get drug data (NB some drugs duplicated for illnesses)
drug_data = pd.read_csv(path + r"\drug_list.csv")

# names of data files
fn_addr = "Address"
fn_prescribe = "GPData"

# column names
col_bnfname = "BNFName"
col_items = "Items"

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
for key in ['Date','HB','pcstrip','Street','Area','Posttown','Postcode']:
    agg_cols[key] = 'first'
    
monthly_data = []

for file in os.listdir(path + "Prescriptions"):
    with zp.ZipFile(path + "Prescriptions\\" + file) as zipf:
        zip_names = zipf.namelist()
        
        # Deal with Address Files
        addr_name = next((filename for filename in zip_names if fn_addr in filename), None)
        # Open address file in pandas, set header.
        
      
        addr = pd.read_csv(zipf.open(addr_name), 
                            #header=1, 
                            #names = ["Date", "PracCode", "PracName","CenterName",
                            #         "Street", "Town", "Town2", "Postcode"], 
                            
                            #Changed code to manually select columns as new column was introduced in 2022 which affect the read
                            usecols = ["Period","PracticeId","Locality","Street","Area","Posttown","County","Postcode"])
                
        print(addr.head())
        # Deal with prescription info
        prescribe_name = next((filename for filename in zip_names if fn_prescribe in filename), None)
        # Open prescribing files in pandas.
        prescribe = pd.read_csv(zipf.open(prescribe_name))
        prescribe.columns = prescribe.columns.str.strip()
        # Rename 'period' column to 'date'
        prescribe.rename(columns = {'Period': 'Date'}, inplace = True) 
        # Get counts of prescribing dataframe for loneliness related diseases
        loneliness_prescribing = code_loneliness(prescribe[[col_bnfname, col_items]])
        # merge dataframes
        prescribe = prescribe.merge(loneliness_prescribing, left_index=True, right_index=True)
        del loneliness_prescribing

        # merge in address information
        prescribe = prescribe.merge(addr, left_on = 'PracticeID', right_on = 'PracticeId')
        del addr
        
        # Create uniform postcode field
        prescribe['pcstrip'] = prescribe['Postcode'].str.replace("\s","")

        # get a summary - grouping by PracCode
        summary = prescribe.groupby('PracticeID', as_index=False).agg(agg_cols)
        del prescribe

        monthly_data.append(summary)
        print(file)
        
# concatenate all the monthly data together.
data = pd.concat(monthly_data, ignore_index = True)

# Save aggregated data
data.to_csv(path + "processed_data.csv")

