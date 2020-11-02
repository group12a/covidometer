import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
# load the dataset
# dataset_path = "https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset?select=time_series_covid_19_confirmed.csv"
df_conf = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
# print(df_conf)
df_conf = df_conf.sort_values(by=['Province/State','Country/Region'])
df_conf = df_conf.reset_index(drop=True)
# print(df_conf)
dates_conf = df_conf.columns[4:]
# perform unpivoting
df_conf_melted = \
    df_conf.melt(
        id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
        value_vars=dates_conf, 
        var_name='Date',
        value_name='Confirmed')
# print(df_conf_melted)
# # convert the date column to date format
# df_conf_melted[“Date”] = df_conf_melted[“Date”].apply(
#     lambda x: datetime.datetime.strptime(x, ‘%m/%d/%y’).date())
df_conf_melted["Date"]=pd.to_datetime(df_conf_melted["Date"])
# print(df_conf_melted['Date'])
# group by date and country and then sum up based on country
df_daily = df_conf_melted.groupby(["Date", "Country/Region"]).sum()
# print(df_daily)
df_daily_sorted = df_daily.sort_values(['Date','Confirmed'], ascending=[True, False])
# print(df_daily_sorted)
# get the list of all countries
all_countries = list(df_conf['Country/Region'])
top_n = 20
# for date, daily_df in df_daily_sorted.groupby(level=0):
#     print(date)
#     print(daily_df)    # a dataframe
# for date, daily_df in df_daily_sorted.groupby(level=0):       
#     print(date)
#     # print(daily_df)    # a dataframe
#     topn_df = daily_df.head(top_n)
#     # get all the countries from the multi-index of the dataframe
#     countries = list(map(lambda x:(x[1]),topn_df.index))[::-1]    
#     confirmed = list(topn_df.Confirmed)[::-1]    
#     print(countries)
#     print(confirmed)

# plotting using the seaborn-darkgrid style
plt.style.use('seaborn-darkgrid')
# set the size of the chart
fig, ax = plt.subplots(1, 1, figsize=(14,10))
# hide the y-axis labels
ax.yaxis.set_visible(False)
# assign a color to each country
NUM_COLORS = len(all_countries)
cm = plt.get_cmap('Set3')
colors = np.array([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
top_n = 10
for date, daily_df in df_daily_sorted.groupby(level=0):
    # print(date)
    # print(daily_df)    # a dataframe
    topn_df = daily_df.head(top_n)
    
    # get all the countries from the multi-index of the dataframe
    countries = list(map (lambda x:(x[1]),topn_df.index))[::-1]
    confirmed = list(topn_df.Confirmed)[::-1]
    # clear the axes so that countries no longer in top 10 will not 
    # be displayed
    ax.clear()
    # plot the horizontal bars
    plt.barh(
        countries,
        confirmed,
        color = colors[[all_countries.index(n) for n in countries]],
        edgecolor = "black",
        label = "Total Number of Confirmed Cases")
    # display the labels on the bars
    for index, rect in enumerate(ax.patches):
        x_value = rect.get_width()
        y_value = rect.get_y() + rect.get_height() / 2
        # display the country
        ax.text(x_value, y_value, f'{countries[index]} ',
            ha="right", va="bottom",
            color="black", fontweight='bold')
        # display the number
        ax.text(x_value, y_value, f'{confirmed[index]:,} ',
            ha="right", va="top",
            color="black")
    # display the title
    plt.title(f"Top {top_n} Countries with Covid-19 ({date})",
        fontweight="bold",
        fontname="Impact",
        fontsize=25)
    # display the x-axis and y-axis labels
    plt.xlabel("Number of people")
    plt.ylabel("Countries")
    # draw the data and runs the GUI event loop
    plt.pause(0.0002)
# keep the matplotlib window
plt.show(block=True)

