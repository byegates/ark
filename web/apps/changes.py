import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import dashapp

import dash_table as dtbl
from core import dates, funds, dt0, cols2, right_cols, tickers, compare_position

page_size = 10

layout = html.Div(children=[
    html.H2(children='Ark Invest Holding Changes', style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.Pre(children="Trading Day", style={"fontSize":"150%"}),
            dcc.Dropdown(
            id='dt0', value=dt0, clearable=False,
            persistence=True, persistence_type='session',
            options=[{'label': x, 'value': x} for x in dates]
        )], className='two columns'),

        html.Div([
            html.Pre(children="Fund", style={"fontSize":"150%"}),
            dcc.Dropdown(
            id='fund', value='All', clearable=False,
            persistence=True, persistence_type='session',
            options=[{'label': x, 'value': x} for x in funds + ['All']]
        )], className='two columns'),

        html.Div([
            html.Pre(children="Ticker", style={"fontSize":"150%"}),
            dcc.Dropdown(
            id='ticker', value='All', clearable=False,
            persistence=True, persistence_type='session',
            options=[{'label': x, 'value': x} for x in tickers + ['All']]
        )], className='two columns'),
        
        html.Div([
            html.Pre(children="Compare with", style={"fontSize":"150%"}),
            dcc.Dropdown(
            id='dt1', value=dates[1], clearable=False,
            persistence=True, persistence_type='session',
            options=[{'label': x, 'value': x} for x in dates]
        )], className='two columns'),
        
    ], className='row'),

    html.H6(children=f'''Buys'''),
    dtbl.DataTable(
        id='buy',
        columns=cols2,
        style_cell={'textAlign': 'left'},
        page_size=page_size,
    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'right'
        } for c in right_cols
    ],
    ),

    html.Plaintext(children=f'''* Shares * Trade Price, sorted in Descending Order'''),
    html.Plaintext(children=f'''** Using Close Price for now'''),

    html.H6(children=f'''Sells'''),
    dtbl.DataTable(
        id='sell',
        columns=cols2,
        style_cell={'textAlign': 'left'},
        page_size=page_size,
    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'right'
        } for c in right_cols
    ],
    ),

    html.H6(children=f'''New Buys'''),
    dtbl.DataTable(
        id='new_buy',
        columns=cols2,
        style_cell={'textAlign': 'left'},
        page_size=page_size,
    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'right'
        } for c in right_cols
    ],
    ),

    html.H6(children=f'''All Sold'''),
    dtbl.DataTable(
        id='all_sold',
        columns=cols2,
        style_cell={'textAlign': 'left'},
        page_size=page_size,
    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'right'
        } for c in right_cols
    ],
    ),

    html.H6(children=f'''No Change'''),
    dtbl.DataTable(
        id='no_chg',
        columns=cols2,
        style_cell={'textAlign': 'left'},
        page_size=page_size,
    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'right'
        } for c in right_cols
    ],
    ),

    ])

@dashapp.callback(
    Output(component_id='buy', component_property='data'),
    Output(component_id='sell', component_property='data'),
    Output(component_id='no_chg', component_property='data'),
    Output(component_id='new_buy', component_property='data'),
    Output(component_id='all_sold', component_property='data'),
    [Input(component_id='dt0', component_property='value'),
     Input(component_id='fund', component_property='value'),
     Input(component_id='ticker', component_property='value'),
     Input(component_id='dt1', component_property='value')]
)
def get_holdings(dt0, fund, ticker, dt1):
    use_fd = True if fund == 'All' and ticker != 'All' or fund != 'All' else False
    buy, sell, no_change, new_buy, all_sold = compare_position(dt0, dt1, fund, ticker, use_fd)
    return buy.to_dict('records'), sell.to_dict('records'), no_change.to_dict('records'), new_buy.to_dict('records'), all_sold.to_dict('records')
