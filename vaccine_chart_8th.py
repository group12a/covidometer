import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import plotly.express as px
import pyttsx3

'''This function is used to speak'''
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


speak('Data Visualization related to covid vaccine')

df=pd.read_csv(r'https://raw.githubusercontent.com/group12a/covidometer/main/country_vaccinations.csv')

df.head()

df.info()

df.describe()

df.columns

#df.date = pd.to_datetime(df.date,infer_datetime_format=True,format='%Y-%b-%d')
df.fillna(0, inplace = True)
df['iso_code'].fillna('GBR', inplace=True)
df.drop(df.index[df['iso_code'] == 0], inplace = True)

df.drop(["source_name","source_website","people_fully_vaccinated","daily_vaccinations_raw","people_fully_vaccinated_per_hundred","daily_vaccinations_per_million","people_vaccinated_per_hundred"],axis=1, inplace=True)

df

sns.set_style('darkgrid')
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['figure.figsize'] = (9, 6)
matplotlib.rcParams['figure.facecolor'] = '#00000000'
plt.rc('font', size=12)

cols = ['country', 'total_vaccinations', 'iso_code', 'vaccines','total_vaccinations_per_hundred']
vacc_amount = df[cols].groupby('country').max().sort_values('total_vaccinations', ascending=False).dropna(subset=['total_vaccinations'])
vacc_amount = vacc_amount.iloc[:10]

vacc_amount = vacc_amount.sort_values('total_vaccinations_per_hundred', ascending=False)


plt.figure(figsize=(9, 12))
sns.barplot(vacc_amount.total_vaccinations_per_hundred, vacc_amount.index, color = 'r')

speak('Top 10 countries with highest people vaccinated per hundred')
plt.title('Top 10 countries with highest people vaccinated per hundred')
#plt.xticks(rotation = 90)    #not needed
plt.xlabel('Number of vaccinated people per hundred')
plt.ylabel('Countries')
plt.show();

cols = ['country', 'total_vaccinations', 'iso_code', 'vaccines']
vacc_amount = df[cols].groupby('country').max().sort_values('total_vaccinations', ascending=False).dropna(subset=['total_vaccinations'])
vacc_amount = vacc_amount.iloc[:10]

plt.figure(figsize=(16, 7))
plt.bar(vacc_amount.index, vacc_amount.total_vaccinations, color = 'c')

speak('Top 10 countries having highest vaccinated people')
plt.title('Top 10 countries having highest vaccinated people')
plt.xticks(rotation = 90)
plt.ylabel('Number of vaccinated citizens (per 10 Million)')
plt.xlabel('Countries')
plt.show();


plt.figure(figsize=(16,7))
grp = ['country', 'total_vaccinations', 'iso_code', 'vaccines']
vacc_no = df[grp].groupby('vaccines').max().sort_values('total_vaccinations', ascending=False).dropna(subset=['total_vaccinations'])


sns.barplot(vacc_no.index, vacc_no.total_vaccinations, color ='m')

speak('Various categories of COVID-19 vaccines offered')
plt.title('Various categories of COVID-19 vaccines offered')
plt.xticks(rotation = 90)
plt.ylabel('Number of vaccinated citizens (per 10 millions)')
plt.xlabel('Vaccines')
plt.show();

speak('Vaccines used by different countries')
fig = px.choropleth(df, locations="iso_code",
                    color="vaccines",
                    hover_name="country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma,
                   title= "Vaccines used by different countries")
fig.update_layout(showlegend=False)
fig.show()

speak('lets proceed for the next part')