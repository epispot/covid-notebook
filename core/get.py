"""Helper functions for fetching relevant data"""

# imports
from . import process
from . import np
from . import pd
import json


# functions
def last_update():
    """Fetch last updated date from artifacts/last-update.txt"""
    with open('artifacts/last-update.txt', 'r') as f:
        return f.read()

def data(date):
    """Fetch most recent county data from the NYTimes COVID-19 dataset"""
    
    # fetch data
    URL = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties-recent.csv'
    df_raw = pd.read_csv(URL, dtype={'fips': str})
    df = df_raw[df_raw['date'] == date].copy()
    df.drop(columns=['date'], inplace=True)
    df.drop(df[df['county'] == 'Unknown'].index, inplace=True)

    # process data
    df = process.remaining(df)
    df = process.populate(df)
    p_cases, p_deaths = process.normalize(df)
    df['p_cases'] = p_cases
    df['p_deaths'] = p_deaths

    # sort data by FIPS
    df['fips'].fillna(0, inplace=True)
    # indexFIPS = lambda fips: fips.astype(int)
    df.sort_values(by=['fips'], inplace=True)
    df.index = np.arange(len(df))

    # write data
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.to_csv('artifacts/data.csv', index=False)

    # change last updated date
    with open('artifacts/last-update.txt', 'w') as f:
        f.write(date)

    return df

def counties():
    """Return county GeoJSON data"""
    with open('data/counties.geojson', 'r') as f:
        return json.load(f)
