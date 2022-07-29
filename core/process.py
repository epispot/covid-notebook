"""Tools for processing data"""

# imports
from . import pd


# functions
def populate(df):
    """Add corresponding population data to dataframe"""
    populations = pd.read_csv('data/populations.csv')
    df['population'] = populations['pop']
    return df

def remaining(df):
    """Process remaining geographic areas (those without a FIPS identifier)"""

    # New York City, New York
    df.loc[df['county'] == 'New York City', 'fips'] = 'unique:nyc'
    df.loc[df['county'] == 'New York City', 'population'] = 8467513

    # Kansas City, Missouri
    df.loc[df['county'] == 'Kansas City', 'fips'] = 'unique:kc'
    df.loc[df['county'] == 'Kansas City', 'population'] = 508394

    # Joplin, Missouri
    df.loc[df['county'] == 'Joplin', 'fips'] = 'unique:jop'
    df.loc[df['county'] == 'Joplin', 'population'] = 51846

    # Bristol Bay & Lake and Peninsula, Alaska
    df.loc[
        df['county'] == 'Bristol Bay plus Lake and Peninsula',
        'fips'
    ] = 'unique:bblp'
    df.loc[
        df['county'] == 'Bristol Bay plus Lake and Peninsula',
        'population'
    ] = 2254

    return df
    
def normalize(df):
    """Normalize data by population"""
    p_cases = df['cases'] / df['population']
    p_deaths = df['deaths'] / df['population']
    return p_cases, p_deaths
