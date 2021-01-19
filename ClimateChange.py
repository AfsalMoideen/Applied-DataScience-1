__author__ = "Afsal Moideen"
__date__ = "2020-12-14"
__version__ = "1.0.1" 
__maintainer__ = "Afsal Moideen" 
__email__ = "ac20adi@herts.ac.uk"

from scipy import stats
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot
import matplotlib.pyplot as plt

df = pd.read_csv('raw_data.csv')

DF1 = df[df["Indicator Code"] == "SP.URB.TOTL.IN.ZS"]
DF2 = df[df["Indicator Code"] == "EN.ATM.CO2E.SF.ZS"]
DF3 = df[df["Indicator Code"] == "EN.ATM.CO2E.LF.ZS"]
DF4 = df[df["Indicator Code"] == "EN.ATM.CO2E.GF.ZS"]

# Define function to pull value from raw data, using DateIndex from new DataFrame row
def populate_df(row):
    index = str(row['date'].year)
    value = DF1_world.loc[index]
    return value

def populate_df1(row):
    index = str(row['date'].year)
    value = DF2_world.loc[index]
    return value  

def populate_df2(row):
    index = str(row['date'].year)
    value = DF3_world.loc[index]
    return value

def populate_df3(row):
    index = str(row['date'].year)
    value = DF4_world.loc[index]
    return value

DF1_world = DF1[DF1['Country Name']=='World'].loc[:,'1980':'2018']
DF2_world = DF2[DF2['Country Name']=='World'].loc[:,'1980':'2018']
DF3_world = DF3[DF3['Country Name']=='World'].loc[:,'1980':'2018']
DF4_world = DF4[DF4['Country Name']=='World'].loc[:,'1980':'2018']


# 'Traspose' the resulting slice, making the columns become rows and vice versa
DF1_world = DF1_world.T
DF1_world.columns = ['value']

DF2_world = DF2_world.T
DF2_world.columns = ['value']

DF3_world = DF3_world.T
DF3_world.columns = ['value']

DF4_world = DF4_world.T
DF4_world.columns = ['value']

# Create a new DataFrame with a daterange the same the range for.. 
# the Temperature data (after resampling to years)
date_rng = pd.date_range(start='31/12/1980', end='31/12/2018', freq='y')
date_time = pd.DataFrame(date_rng, columns=['date'])

# Populate the new DataFrame using the values from the raw data slice
newDF1 = date_time.apply(lambda row: populate_df(row), axis=1)
newDF2 = date_time.apply(lambda row: populate_df1(row), axis=1)
newDF3 = date_time.apply(lambda row: populate_df2(row), axis=1)
newDF4 = date_time.apply(lambda row: populate_df3(row), axis=1)
date_time['UrbanPopulation'] = newDF1
date_time['CO2Solid'] = newDF2
date_time['CO2Liquid'] = newDF3
date_time['CO2Gas'] = newDF4
date_time.fillna(method='ffill', inplace=True)
date_time.set_index('date', inplace=True)
date_time.describe()


stats.kurtosis(date_time)

stats.skew(date_time)

date_time.corr(method='spearman', min_periods=1)

f, ax = pyplot.subplots(figsize=(14, 8))
corr = date_time.corr()
sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool), cmap=sns.diverging_palette(220, 10, as_cmap=True),
            square=True, annot=True, ax=ax)

date_time['AvgCO2Emission'] = date_time.mean(axis=1)
df = date_time.drop(columns=['CO2Solid','CO2Liquid','CO2Gas'])
df.head()

# Create figures and axes
fig, ax = plt.subplots(figsize=(10,8))

ax.plot(df, color='#3393FF', linewidth=2.5)

# Set axis labels and graph title
ax.set(xlabel='Time (years)', ylabel='Global urban population and CO2 Emission ',
       title='Increase in CO2 emission over Time')

# Enable grid
ax.grid()