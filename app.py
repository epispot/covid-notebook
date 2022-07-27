
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# imports
import json
from csv import reader
from datetime import date
from urllib.request import urlopen

import numpy as np
import pandas as pd
import epispot as epi
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc


# create app
app = Dash(__name__)


# fetch data
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df_raw = pd.read_csv(
    'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties-recent.csv',
    dtype={ 'fips': str }
)
update = date.today() - date.resolution
df = df_raw[df_raw['date'] == update.strftime('%Y-%m-%d')]


# process data
p_cases = []
p_deaths = []

with open('data/populations.csv', 'r') as f:

    read = reader(f)
    header = next(read)
    index = -1

    for row in read:

        index += 1
        pop = int(row[1])

        if pop == 0:
            p_cases.append(None)
            p_deaths.append(None)
            continue

        df_row = df.iloc[index]
        p_cases.append(df_row['cases'] / pop)
        p_deaths.append(df_row['deaths'] / pop)

df.insert(6, 'p_cases', p_cases)
df.insert(7, 'p_deaths', p_deaths)


# create main figure
fig = go.Figure(go.Choroplethmapbox(
    geojson=counties, 
    locations=df.fips, 
    z=df.p_cases,
    zmin=0, zmax=0.5,
    colorscale=[
        [0, '#adffc2'],
        # [0.25, '#d4ff78'],
        [0.5, '#ff9382'],
        # [0.75, '#ff2200'],
        [1, '#c90061']
    ],
    marker_line_width=0
))
fig.update_layout(
    mapbox_style='carto-positron',
    mapbox_zoom=3, 
    mapbox_center = {'lat': 37.0902, 'lon': -95.7129}
)
fig.update_layout(
    margin={ 'r': 0, 't': 0, 'l': 0, 'b': 0 }
)


# create app layout
app.layout = html.Div(children=[
    html.H1(children='covid-notebook'),
    html.Div(children='''
        An interactive notebook for examining trends in confirmed COVID-19 cases
    '''),
    dcc.Graph(
        id='COVID-19 cases by county',
        figure=fig
    )
])


# run app
if __name__ == '__main__':
    app.run_server(debug=True)
