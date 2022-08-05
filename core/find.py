"""Utilities for finding files and directories."""

# imports
import os
from datetime import datetime, timedelta

from . import get, np, pd


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
        full = pd.read_csv(
            f'artifacts/{source}.csv',
            dtype={'fips': str}
        )
        relevant = full[full['date'] == last_update].copy()
        relevant.drop(columns=['date'], inplace=True)
        return relevant

def historical(fips, source='cumulative'):
    """Fetch historical data for a given county"""

    # check if artifacts/{source}.csv exists
    if not os.path.exists(f'artifacts/{source}.csv'):
        data()

    # fetch data and sort by date
    full = pd.read_csv(f'artifacts/{source}.csv', dtype={'fips': str})
    full.sort_values(by=['date'], inplace=True)
    full.index = np.arange(len(full))
    return full[full['fips'] == fips]
