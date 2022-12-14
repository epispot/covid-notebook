"""Tools for processing data"""

# imports
from . import pd


# functions
def geoid2fips(df):
    """Convert geoid-tagged dataset to FIPS"""
    df['geoid'].fillna(0, inplace=True)
    col = df['geoid'].copy()
    df['fips'] = col.apply(lambda x: x[4:])
    df.drop(columns=['geoid'], inplace=True)
    return df

def populate(df):
    """Add corresponding population data to dataframe"""
    populations = pd.read_csv('data/populations.csv')
    df = df.merge(populations, on='fips', how='left')
    return df

def remaining(df):
    """Process remaining geographic areas (those without a FIPS identifier)"""

    # New York City, New York
    df.loc[df['county'] == 'New York City', 'fips'] = 'unique:nyc'

    # Kansas City, Missouri
    df.loc[df['county'] == 'Kansas City', 'fips'] = 'unique:kc'

    # Joplin, Missouri
    df.loc[df['county'] == 'Joplin', 'fips'] = 'unique:jop'

    # 48999: 'Pending County Assignment'

    return df

def normalize(df):
    """Normalize data by population"""
    p_cases = df['cases'] / df['population']
    p_deaths = df['deaths'] / df['population']
    death_rate = df['deaths'] / df['cases']
    return p_cases, p_deaths, death_rate
