
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
        [0.5, '#ff9382'],
        [1, '#c90061']
    ],
    marker_line_width=0,
    marker_opacity=0.75,
    text=
        df.county + ', ' + df.state
        + '<br>cases: '
            + np.round(100 * df.p_cases, 1).astype(str) + '%'
        + '<br>deaths: '
            + np.round(100 * df.p_deaths, 1).astype(str) + '%',
    hoverinfo='text',
))
fig.update_layout(
    mapbox_style='open-street-map',
    mapbox_zoom=3,
    mapbox_center = {'lat': 37.0902, 'lon': -95.7129},
)
fig.update_layout(
    margin={ 'r': 0, 't': 0, 'l': 0, 'b': 0 }
)


# create app layout
app.layout = html.Div(children=[
    html.H1(children='COVID-19 Notebook'),
    html.Div(children='''
        An interactive notebook for examining trends in COVID-19 cases
    ''', id='subtitle'),
    dcc.Graph(
        id='graph',
        figure=fig
    ),
    dcc.Markdown(children=f'''
        Data from The New York Times, based on reports from state and local health agencies.  
        See also: <https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html>  
        Last updated {core.get.last_update()}, at midnight UTC.
    ''', id='footer'),
])


# run app
if __name__ == '__main__':
    app.run_server(debug=True)
