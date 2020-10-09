# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 14:36:09 2020

@author: FischerBA
"""

# To begin, the following libraries are imported and the CSV data file is loaded.

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

source = 'https://raw.githubusercontent.com/BFischer-GH/Coursera_Capstone/master/data/Data-Collisions.csv'
df_raw = pd.read_csv(source, index_col = False, low_memory=False)

print('Data-Collisions.csv loaded')

# All required script for prep work of 3. Data Prep
df_raw.drop(['OBJECTID','INCKEY'
             ,'COLDETKEY', 'REPORTNO'
             , 'INTKEY','SDOT_COLCODE'
             , 'SDOTCOLNUM' , 'SEGLANEKEY'
             ,'CROSSWALKKEY', 'STATUS'
             , 'ADDRTYPE', 'EXCEPTRSNCODE'
             , 'EXCEPTRSNDESC', 'SEVERITYCODE.1', 'SEVERITYDESC']
            ,axis=1, inplace=True)

print('Non-relevant attributs removed!')

df_clean = df_raw.dropna(subset=['X', 'Y', 'LOCATION'
                     ,'INCDATE' ,'INCDTTM'])

print('A total of', (df_raw.shape[0]-df_clean.shape[0]), 'incomplete accidents removed!')
print('A total of', (df_clean.shape[0]), 'accidents remain!')

df_clean.drop(['ST_COLDESC','ST_COLCODE', 'SPEEDING', 'PEDROWNOTGRNT', 'INATTENTIONIND'], axis=1)

print(df_clean['SEVERITYCODE'].value_counts())

df_time = df_clean[["INCDATE", "SEVERITYCODE"]]

dummy_variable_1 = pd.get_dummies(df_time["SEVERITYCODE"])
dummy_variable_1.rename(columns={1:'Sev.Code 1', 2:'Sev.Code 2'}, inplace=True)
# merge data frame "df_time" and "dummy_variable_1" 
df_time = pd.concat([df_time, dummy_variable_1], axis=1)
# drop original column "SEVERITYCODE" from "df_time"
df_time.drop("SEVERITYCODE", axis = 1, inplace=True)
# Change INCDATE to useable date
df_time['INCDATE'] =  pd.to_datetime(df_time['INCDATE'])

# To plot
# set index to time, this makes df a time series df and then you can apply pandas time series functions.  
df_time.set_index(df_time['INCDATE'], drop=True, inplace=True)   

# create another df by resampling the original df and counting the instance column by Month ('M' is resample by month)
#ufo2 = pd.DataFrame(df_time['Sev.Code 1'].resample('M').count() )
#ufo3 =  pd.DataFrame(df_time['Sev.Code 2'].resample('M').count() )

df_time_resamp = pd.DataFrame(df_time.resample('M').sum() )

# Now let's plot this

fig, ax = plt.subplots(figsize=(16,10))
df_time_resamp.plot(ax=ax)

ax.grid(b=True, which='major',  linestyle='--')
fig.autofmt_xdate()



plt.ylabel('# Accidents')
plt.xlabel('Years')

