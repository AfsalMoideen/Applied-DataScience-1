__author__ = "Afsal Moideen"
__date__ = "2021-01-18"
__version__ = "1.0.1" 
__maintainer__ = "Afsal Moideen" 
__email__ = "ac20adi@herts.ac.uk"

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import scipy.cluster.hierarchy as shc
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score

df = pd.read_csv("World_Covid19_cases.csv", sep = ',')
df.head()

# Select ONLY the following columns for further processing: 
# Country, Total Cases, Total Deaths, Total Recovered, Active Cases, Critical Cases, Total Tests, Population.

cols = ['Country', 'Total Cases', 'Total Deaths', 'Total Recovered', 
        'Active Cases', 'Critical Cases', 'Total Tests', 'Population']
countryCol = df['Country']
df1 = df[cols]

# Remove the comma (i.e., “,”) number separater from numeric columns.

df1['Total Cases'] = df1['Total Cases'].str.replace(',', '')
df1['Total Deaths'] = df1['Total Deaths'].str.replace(',', '')
df1['Total Recovered'] = df1['Total Recovered'].str.replace(',', '')
df1['Active Cases'] = df1['Active Cases'].str.replace(',', '')
df1['Critical Cases'] = df1['Critical Cases'].str.replace(',', '')
df1['Total Tests'] = df1['Total Tests'].str.replace(',', '')
df1['Population'] = df1['Population'].str.replace(',', '')
df1.head()

# Temporarily drop the Country column and convert the other columns to numeric values 
# (note: use the errors='coerce' option to coerce missing values to be converted to np.nan).

df2 = df1.drop(['Country'], axis = 1)

df2 = df2.apply(pd.to_numeric, errors = 'coerce')

df2.head()

# Re-append the Country column to the data frame.
df2['Country'] = countryCol
df2.head()

# Use the fillna() function to fill in missing values in the following two columns: 
# Total Deaths and Critical Cases. Fill in the missing values using 0 (i.e., Zero)
df2['Total Deaths'].fillna(0,inplace=True)
df2['Critical Cases'].fillna(0,inplace=True)
df2.head()

# Thereafter, check whether there are any columns with missing values and use dropna() 
# function to drop rows with missing values.
# check first
df2.isnull().sum()
# drop na values   
df2 = df2.dropna() 
# check again  
df2.isnull().sum()   

# Add/Append the following computed column to the data frame: Pop_ml = Population/1000000 
# (i.e., convert country population numbers to millions by dividing by 1 million).

df2['Pop_ml'] = df2['Population'] / 1000000
df2.head()

# add/append the following computed columns to the data frame:
df2['Mortality_rate'] = df2['Total Deaths'] / df2['Total Cases']
df2['Cases_per_ml'] = df2['Total Cases'] / df2['Pop_ml']
df2['Deaths_per_ml'] = df2['Total Deaths'] / df2['Pop_ml']
df2['Recovered_per_ml'] = df2['Total Recovered'] / df2['Pop_ml']
df2['Active_per_ml'] = df2['Active Cases'] / df2['Pop_ml']
df2['Critical_per_ml'] = df2['Critical Cases'] / df2['Pop_ml']
df2['Tests_per_ml'] = df2['Total Tests'] / df2['Pop_ml']
df2.head()

# Select the following columns for subsequent analysis:
# Country, Mortality_rate, Cases_per_ml, Deaths_per_ml, Recovered_per_ml, Active_per_ml, Critical_per_ml, Tests_per_ml.

df_final = df2[['Country', 'Mortality_rate', 'Cases_per_ml', 'Deaths_per_ml', 
         'Recovered_per_ml', 'Active_per_ml', 'Critical_per_ml', 'Tests_per_ml']]
df_final.head()
df_final.shape

# For now, drop the Country column (you’ll need later); so keep your data frame from step i) intact!
df4 = df_final.drop(['Country'], axis = 1)
df4.head()

# After dropping the country column, scale the data using StandardSCaler.
scaler = StandardScaler()
scale_df = df4.copy()
scale_df[['Mortality_rate', 'Cases_per_ml', 'Deaths_per_ml', 'Recovered_per_ml', 'Active_per_ml', 'Critical_per_ml', 'Tests_per_ml']] = scaler.fit_transform(scale_df[['Mortality_rate', 'Cases_per_ml', 'Deaths_per_ml', 'Recovered_per_ml', 'Active_per_ml', 'Critical_per_ml', 'Tests_per_ml']])
scale_df.head()

# function definition for dendogram
def show_dendrogram(data):                      
    plt.figure(figsize=(10, 7))
    plt.title("COVID 19 cases details - Dendrogram")
    dend = shc.dendrogram(shc.linkage(data, method='ward'))
   
# generate the dendrogram    
show_dendrogram(scale_df)                       
# function definition - compute withinness sum of squares (wss)
def calculate_wcss(data):
    wcss = []
    for n in range(2, 16):
        kmeans = KMeans(n_clusters=n, random_state=0)
        kmeans.fit(X=data)
        wcss.append(kmeans.inertia_)
    
    return wcss

# compute wss
wcss1 = calculate_wcss(scale_df)     
    
# scree plot (elbow method)
plt.plot(range(2,16), wcss1, '-bo')
plt.xlabel('k')
plt.ylabel('Sum_of_squared_distances')
plt.title('Elbow Method to determine optimal number of clusters (k)')
plt.show()    

run kmeans with number of clusters obtained earlier
kmeans = KMeans(n_clusters=3, random_state=0)
clusters = kmeans.fit_predict(scale_df)

print(clusters)
# generate cluster centers
centers = kmeans.cluster_centers_
print(centers)