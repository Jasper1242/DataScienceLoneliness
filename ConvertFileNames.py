# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 15:35:26 2023

@author: Kasper
"""
import os
from datetime import datetime 

path = r"C:\Users\jaspi\OneDrive - University of Bristol\Documents\Year 3\AI\Loneliness\Data Science\loneliness-master\Wales\Prescriptions"

for file in os.listdir(path):
    
    
    if file[0:6] == "GPData":
        pass
    else:
        filePrefix = 'GPData'
        date = file[18:-4]
        ext = file.split('.')[-1]
        date_time_str = str(date)
        date_time_obj = datetime.strptime(date_time_str, '%B %Y').date()
        newFileDate = date_time_obj.strftime("%Y%m")
        new_file_name = filePrefix + newFileDate +  "." + ext
        os.rename(os.path.join(path, file), os.path.join(path, new_file_name))
