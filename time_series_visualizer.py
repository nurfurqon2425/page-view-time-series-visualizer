import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df['date'] = pd.to_datetime(df['date'])
# print(df.shape[0])

# Clean data
df = df.loc[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]
# print(df.shape[0])

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(12,4))
    ax.plot(df['date'], df['value'], color='red', linewidth=1)
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['month'] = df_bar['date'].dt.month_name()
    df_bar['month_num'] = df_bar['date'].dt.month
    df_bar['year'] = df_bar['date'].dt.year
    # df_bar = df_bar.sort_values(by='date')
    # df.rename(columns={'value' : 'values'}, inplace=True)
    # print(df_bar[['month','month_num']].sort_values(by=['month_num'])['month'].unique())
    month_order = df_bar.loc[df_bar['year'] == 2017, 'month'].unique().copy()
    year_order = df_bar['year'].unique().copy()
    # print(year_order)
    # df_bar = pd.melt(df, id_vars=['date'], value_vars=['month', 'year'])
    df_bar = df_bar.groupby(['year','month','month_num']).agg(values=('value','mean'))
    df_bar = df_bar.sort_values(by=['year', 'month_num'])
    df_bar = df_bar.reset_index()
    # print(df_bar)
    

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(10,10))

    dfl = pd.DataFrame()
    bar_width = 0.05
    x = np.arange(year_order.shape[0])
    x_bar = 0
    for m in month_order:
        temp = pd.Series(df_bar.loc[df_bar['month'] == m, 'values'])         
        
        if temp.shape[0] < year_order.shape[0]:
            temp = pd.concat([pd.Series([0]),temp])

        plt.bar(x + x_bar , temp, width=bar_width, label=m)
        # print(x)
        # print(x_bar)
        x_bar += bar_width
        # print(temp)
        # print(df_bar.loc[df_bar['month'] == m, 'values'], m)
    # print(dfl)
    plt.xticks(x, year_order)
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(month_order, title='Months')
    

    # cp = sns.barplot(ax=ax, data=df_bar, x='year', y='values', hue='month', hue_order=month_order,width=.4)
    # cp.set_xlabel('Years')
    # cp.set_ylabel('Average Page Views')
    # cp.legend()
    # fig = cp.figure 
    

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    month_order = df_box.loc[df_box['year'] == 2017, 'month'].unique().copy()
    # print(month_order)
    # print(df_box.head())
    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1,2,figsize=(12,6))

    year_plot = sns.boxplot(data=df_box,ax=ax[0], x='year', y='value', hue='year')
    year_plot.set_title('Year-wise Box Plot (Trend)')
    year_plot.set_xlabel('Year')
    year_plot.set_ylabel('Page Views')

    month_plot = sns.boxplot(data=df_box,ax=ax[1], x='month', y='value', order=month_order, hue='month')
    month_plot.set_title('Month-wise Box Plot (Seasonality)')
    month_plot.set_xlabel('Month')
    month_plot.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

# draw_line_plot()
# draw_bar_plot()
# draw_box_plot()