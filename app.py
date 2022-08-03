
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# imports
import core

import numpy as np
# import epispot as epi
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, ctx, no_update


# create app
app = Dash(__name__)
server = app.server


# get data
source = 'cumulative'
df = core.find.data(source=source)
counties = core.get.counties()


# globals
data = [df.p_cases, df.p_deaths, df.death_rate]
zmax = [0.5, 0.01, 0.035]


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
            + np.round(100 * df.p_deaths, 1).astype(str) + '%'
        + '<br>fatality rate: '
            + np.round(100 * df.death_rate, 1).astype(str) + '%',
    hoverinfo='text',
))
fig.update_layout(
    mapbox_style='open-street-map',
    mapbox_zoom=3,
    mapbox_center={'lat': 37.0902, 'lon': -95.7129},
)
fig.update_layout(
    margin={ 'r': 0, 't': 0, 'l': 0, 'b': 0 }
)


# helper funcs
def update_source(value, key='Cases'):
    """Change data sources to fit selection"""
    global df, source, data, zmax

    # match selection
    match value:
        case 'Cumulative': source = 'cumulative'
        case 'Current': source = 'rolling'

    # update source
    df = core.find.data(source=source)

    # configure parameters
    data = [df.p_cases, df.p_deaths, df.death_rate]
    if source == 'rolling':
        data = [
            df['cases_avg_per_100k'], 
            df['deaths_avg_per_100k'], 
            df['death_rate']
        ]
    zmax = [0.5, 0.01, 0.035]
    if source == 'rolling': zmax = [75, 1, 0.035]

    # get appropriate data source
    src = data[0]
    src_zmax = zmax[0]

    match key:
        case 'Cases': pass
        case 'Fatalities':
            src = data[1]
            src_zmax = zmax[1]
        case 'Fatality Rate':
            src = data[2]
            src_zmax = zmax[2]

    fig.update_traces(
        locations=df.fips,
        z=src,
        zmax=src_zmax,
        text=
            df.county + ', ' + df.state
            + '<br>cases: '
                + data[0].astype(str) + '/100k'
            + '<br>deaths: '
                + data[1].astype(str) + '/100k'
            + '<br>fatality rate: '
                + np.round(100 * data[2], 1).astype(str) + '%',
    )

    return fig

def change_map_view(value):
    """Change map center and zoom depending on selection"""

    # default center, zoom
    center = {'lat': 37.0902, 'lon': -95.7129}
    zoom = 3

    # match selection
    match value:
        case 'Contiguous U.S.':
            pass
        case 'Alaska':
            center = {'lat': 63.3850, 'lon': -152.2683}
            zoom = 2
        case 'Hawaii':
            center = {'lat': 19.8983, 'lon': -155.5822}
            zoom = 5
        case 'Puerto Rico & the U.S. Virgin Islands':
            center = {'lat': 18.4389, 'lon': -66.0079}
            zoom = 6.5
        case 'Northern Mariana Islands':
            center = {'lat': 15.2, 'lon': 145.75}
            zoom = 7

    # update layout
    fig.update_layout(
        mapbox_style='open-street-map',
        mapbox_zoom=zoom,
        mapbox_center=center,
    )

    return fig

def change_choropleth(value):
    """Change choropleth data to match selection"""
    global data, zmax

    # get appropriate data source
    src = data[0]
    src_zmax = zmax[0]

    # match selection
    match value:
        case 'Cases': pass
        case 'Fatalities':
            src = data[1]
            src_zmax = zmax[1]
        case 'Fatality Rate':
            src = data[2]
            src_zmax = zmax[2]

    # change choropleth data
    fig.update_traces(
        z=src,
        zmax=src_zmax,
    )

    return fig

def generate_info(src, map, choro):
    """Generate info text based on selection"""
    
    # defaults
    grouping = 'cumulative totals'
    subdivision = 'counties'
    region = 'the contiguous U.S'
    data = 'cases'
    format = 'as percentage of total population'

    # match data source
    match src:
        case 'Cumulative': pass
        case 'Current':
            grouping = 'rolling averages from the past 7 days'
            format = 'per 100k people'

    # match map view
    match map:
        case 'Contiguous U.S.': pass
        case 'Alaska':
            subdivision = 'boroughs and census-designated areas'
            region = 'Alaska'
        case 'Hawaii':
            region = 'Hawaii'
        case 'Puerto Rico & the U.S. Virgin Islands':
            subdivision = 'municipalities'
            region = 'Puerto Rico & the U.S. Virgin Islands'
        case 'Northern Mariana Islands':
            subdivision = 'municipalities'
            region = 'the Northern Mariana Islands'

    # match choropleth data
    match choro:
        case 'Cases': pass
        case 'Fatalities': data = 'deaths'
        case 'Fatality Rate':
            data = 'fatality rate'
            format = 'as percentage of total cases'

    # generate info text
    text = [
        f'Viewing {grouping} for all {subdivision} in {region}.',
        html.Br(), f'Showing {data} {format}.',
    ]

    return text


# callbacks
@app.callback(
    [
        Output('graph', 'figure'),
        Output('info', 'children'),
    ],
    [
        Input('source-dropdown', 'value'),
        Input('map-dropdown', 'value'),
        Input('choropleth-dropdown', 'value')
    ]
)
def update_figure(src_drop, map_drop, choro_drop):
    """Responsible for all updates to the main figure"""
    
    IDs = list(ctx.triggered_prop_ids.values())
    if len(IDs) == 0: return no_update
    ID = IDs[0]

    out = no_update

    match ID:
        case 'source-dropdown':
            out = update_source(src_drop, key=choro_drop)
        case 'map-dropdown':
            out = change_map_view(map_drop)
        case 'choropleth-dropdown':
            out = change_choropleth(choro_drop)

    info_out = generate_info(src_drop, map_drop, choro_drop)    
    return out, info_out

@app.callback(
    Output('county-info-name', 'children'),
    Input('graph', 'clickData')
)
def update_county(clickData):
    """Responsible for updating the county info box"""

    # default info
    FIPS = 'Click on a county to see its data.'

    # get info
    if clickData is None:
        return no_update
    
    FIPS = clickData['points'][0]['location']

    # process county data
    data = df[df['fips'] == FIPS]
    name = data['county'].values[0] + ', ' + data['state'].values[0]

    return name


# create app layout
app.layout = html.Div(children=[
    html.H1(children='COVID-19 Notebook'),
    html.Div(children='''
        An interactive notebook for examining trends in COVID-19 cases
    ''', id='subtitle'),
    dcc.Dropdown(
        ['Cumulative', 'Current'], 'Cumulative', 
        id='source-dropdown'
    ),
    dcc.Dropdown([
        'Contiguous U.S.', 'Alaska', 'Hawaii', 
        'Puerto Rico & the U.S. Virgin Islands', 
        'Northern Mariana Islands'
    ], 'Contiguous U.S.', id='map-dropdown'),
    dcc.Dropdown(
        ['Cases', 'Fatalities', 'Fatality Rate'], 'Cases', 
        id='choropleth-dropdown'
    ),
    dcc.Graph(
        id='graph',
        figure=fig
    ),
    html.Div(children=[
       html.H2(children='No county selected.', id='county-info-name') 
    ], id='county-info'),
    html.Div(children=[
        'Viewing cumulative totals for all counties in the contiguous U.S.',
        html.Br(), 'Showing cases as percentage of total population.'
    ], id='info'),    
    dcc.Markdown(children=f'''
        Data from *The New York Times*, based on reports from state and local health agencies.  
        See also: <https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html>  
        Last updated {core.get.last_update()}, at midnight UTC.
    ''', id='footer'),
])


# run app
if __name__ == '__main__':
    app.run_server(debug=True)
