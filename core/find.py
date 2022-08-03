"""Utilities for finding files and directories."""

# imports
from . import pd
from . import get
from datetime import datetime, timedelta


# functions
def data(source='cumulative'):
    """Fetch county data from the NYTimes COVID-19 dataset"""
    
    # get last updated date
    last_update = datetime.utcnow() - timedelta(hours=29)
    last_update = last_update.strftime('%Y-%m-%d')

    # fetch data
    if last_update != get.last_update():  # cached data is outdated

        cumulative, rolling = get.data(last_update)
        match source:
            case 'cumulative': return cumulative
            case 'rolling': return rolling
    
    else:  # cached data is up-to-date
        return pd.read_csv(f'artifacts/{source}.csv')
