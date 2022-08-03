"""Helper functions for fetching relevant data"""

# imports
from . import process
from . import np
from . import pd
import json
import os


# functions
def last_update():
    """Fetch last updated date from artifacts/last-update.txt"""
    
    # check if file exists
    if not os.path.isfile('artifacts/last-update.txt'):
        if not os.path.isdir('artifacts'):  # create containing directory
            os.mkdir('artifacts')
        with open('artifacts/last-update.txt', 'w+') as f:  # create file
            f.write('never')
    
    # read file
    with open('artifacts/last-update.txt', 'r') as f:
        return f.read()

def cumulative(date):
    """Fetch and process cumulative county data"""

    # fetch data
    URL = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties-recent.csv'
    df_raw = pd.read_csv(URL, dtype={'fips': str})
    df = df_raw[df_raw['date'] == date].copy()
    df.drop(columns=['date'], inplace=True)
    df.drop(df[df['county'] == 'Unknown'].index, inplace=True)

    # process data
    df = process.remaining(df)
    df = process.populate(df)
    p_cases, p_deaths, death_rate = process.normalize(df)
    df['p_cases'] = p_cases
    df['p_deaths'] = p_deaths
    df['death_rate'] = death_rate

    # sort data by FIPS
    df['fips'].fillna(0, inplace=True)
    indexFIPS = lambda fips: fips.astype(str)
    df.sort_values(by=['fips'], inplace=True, key=indexFIPS)
    df.index = np.arange(len(df))

    # replace data
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    return df

def rolling(date):
    """Fetch and process rolling averages of new county data"""

    # fetch data
    URL = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/us-counties-recent.csv'
    df_raw = pd.read_csv(URL, dtype={'fips': str})
    df = df_raw[df_raw['date'] == date].copy()
    df.drop(columns=['date', 'cases', 'deaths'], inplace=True)
    df['cases'] = df['cases_avg']
    df['deaths'] = df['deaths_avg']
    df.drop(columns=['cases_avg', 'deaths_avg'], inplace=True)
    df.drop(df[df['county'] == 'Unknown'].index, inplace=True)

    # process data
    df = process.geoid2fips(df)
    df = process.remaining(df)
    df = process.populate(df)
    p_cases, p_deaths, death_rate = process.normalize(df)
    df['p_cases'] = p_cases
    df['p_deaths'] = p_deaths
    df['death_rate'] = death_rate

    # sort data by FIPS
    indexFIPS = lambda fips: fips.astype(str)
    df.sort_values(by=['fips'], inplace=True, key=indexFIPS)
    df.index = np.arange(len(df))

    # replace data
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    return df

def data(date):
    """Fetch most recent data from the NYTimes COVID-19 dataset"""
    
    # get data
    df1 = cumulative(date)
    df2 = rolling(date)

    # write data
    df1.to_csv('artifacts/cumulative.csv', index=False)
    df2.to_csv('artifacts/rolling.csv', index=False)

    # change last updated date
    with open('artifacts/last-update.txt', 'w') as f:
        f.write(date)

    return df1, df2

def counties():
    """Return county GeoJSON data"""
    with open('data/counties.geojson', 'r') as f:
        return json.load(f)
