
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# imports
import core

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


# get data
df = core.find.data()
counties = core.get.counties()


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
