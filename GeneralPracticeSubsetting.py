# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 15:17:34 2023

@author: Kasper
"""



"""files from https://nwssp.nhs.wales/ourservices/primary-care-services/general-information/data-and-publications/prescribing-data-extracts/gp-practice-analysis/
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


path = r"C:\Users\jaspi\OneDrive - University of Bristol\Documents\Year 3\AI\Loneliness\Data Science\loneliness-master\Wales\\"


data = pd.read_csv(path + "processed_data_with_postcodes.csv", index_col = 0)

# Get GP files
gp_path = path + r"GP data\\"
file = "PracticeItemsDecember2022.xlsx"

gp_data = pd.read_excel(gp_path + file)
gp_data.rename(columns = {'Total Number of Patients (Including Temporary Residents)': 'Number_of_Patients'}, inplace = True)

gp_data = gp_data[['PracticeID', 'Number_of_Patients']]

# Get the unique codes for GP surgeries and subset the prescribing data according to these codes.
gp_ids = gp_data['PracticeID'].unique()
data = data[data['PracticeID'].isin(gp_ids)].copy()

# Merge on the basis of PracticeID - some patient counts are missing (zero)
data = data.merge(gp_data, how = 'left', on = ['PracticeID'])


dropList= []
for index,row in data.iterrows():
   
    try:
        if (row['lsoa11'][0]) == 'E':
            dropList.append(index)
            
    except:
        dropList.append(index)
        
data.drop(data.index[dropList], inplace = True)
# Save aggregated data
data.to_csv(path + "processed_data_with_postcodes_GPs.csv")