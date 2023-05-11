# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 20:22:34 2023

@author: jaspi
"""

import pandas as pd

path = r"C:\Users\jaspi\OneDrive - University of Bristol\Documents\Year 3\AI\Loneliness\Data Science\loneliness-master\Wales\\"

df= pd.read_csv(path + 'processed_data_with_postcodes.csv')#
df = df.sort_values(by=['imd'])