"""Utilities for finding files and directories."""

# imports
from . import pd
from . import get
from datetime import datetime, timedelta


# functions
def data():
    """Fetch most recent county data from the NYTimes COVID-19 dataset"""
    
    # get last updated date
    last_update = datetime.utcnow() - timedelta(hours=29)
    last_update = last_update.strftime('%Y-%m-%d')
    
    # fetch data
    df = False
    if last_update != get.last_update():  # cached data is outdated
        df = get.data(last_update)
    else:  # cached data is up-to-date
        df = pd.read_csv('artifacts/data.csv')

    return df
