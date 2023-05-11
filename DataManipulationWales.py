# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 17:06:32 2023

@author: Kasper
"""
import pandas as pd
from requests import Session
from io import BytesIO

"""files from https://www.data.gov.uk/dataset/ca9b8e46-c49c-487b-ad92-fd10c077d05e/national-statistics-postcode-lookup-latest-centroids"""

# Path to zip files
path = r"C:\Users\jaspi\OneDrive - University of Bristol\Documents\Year 3\AI\Loneliness\Data Science\loneliness-master\Wales\\"

data = pd.read_csv(path + "processed_data.csv", index_col=0)

# Read in postcode lookup data
# This is the persistent link to the latest ONS NSPL

#changed imd to uint16 instead of int8 preserves rank order 

field_dtypes = {'objectid': 'int32', 'pcd':'str', 'pcd2': 'str', 'pcds':'str', 'dointr':'str','doterm':'str',
                'usertype':'int8','oseast1m': 'float', 'osnorth1m': 'float', 'osgrdind':'int8', 'lat':'float', 
                'long':'float', 'X':'float', 'Y':'float', 'imd': 'float',
                'oa11':'str', 'cty': 'str', 'ced':'str', 'laua': 'str', 'ward': 'str', 'hlthau':'str',
                'ctry': 'str','pcon': 'str','eer': 'str','teclec': 'str','ttwa': 'str','pct': 'str','nuts': 'str',
                'park': 'str','lsoa11': 'str','msoa11': 'str','wz11': 'str','ccg': 'str','bua11': 'str',
                'buasd11': 'str','ru11ind': 'str','oac11': 'str','lep1': 'str','lep2': 'str','pfa': 'str',
                'ced': 'str','nhser': 'str','rgn': 'str','calncv': 'str','stp': 'str'}

#pc = pd.read_csv(BytesIO(response.content), dtype = field_dtypes) 
pc = pd.read_csv(path + "NSPL_MAY_2022_UK.csv", dtype = field_dtypes)

# create pcstrip for matching
pc['pcstrip'] = pc['pcd'].str.replace("\s","")


data_temp = data.merge(pc[['pcstrip','oseast1m','osnrth1m','lsoa11','msoa11','ru11ind','rgn','laua','imd']], 
                       how = 'left',
                       on = 'pcstrip')

# Check for missing postcodes
data_temp[data_temp['oseast1m'].isnull()]['pcstrip'].value_counts()

# Clean Missing Postcodes - appear to be typos.
new_pcs = {'CF34LG': 'CF33LG',    # Rumney Primary Care Centre
           'LD3OAW': 'LD30AW',    # Haygarth Doctors
           'OO000OO': 'CF433HB'}  # "THE SURGERY, PENRHYS, FERNDALE RHONDDA"(Tylorstown Surgery, in real life)

data['pcstrip'] = data['pcstrip'].map(new_pcs).fillna(data['pcstrip'])

# Merge data
data = data.merge(pc[['pcstrip','oseast1m','osnrth1m','lsoa11','msoa11','ru11ind','rgn','laua','imd']], 
                  how = 'left', 
                  on = 'pcstrip')

# Save aggregated data
data.to_csv(path + "processed_data_with_postcodes.csv")