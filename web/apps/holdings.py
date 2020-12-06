import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import dashapp

import dash_table as dtbl
from core import dates, funds, dt0, cols, right_cols, tickers, holdings

layout = html.Div(children=[
    html.H3(children='Ark Invest Holdings', style={"textAlign": "center"}),

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
        
    ], className='row'),

    html.H6(id='title'),

    dtbl.DataTable(
        id='holdings',
        columns=cols,
        style_cell={'textAlign': 'left'},
        page_size=20,
    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'right'
        } for c in right_cols
    ],
    )

    ])

@dashapp.callback(
    Output(component_id='holdings', component_property='data'),
    Output(component_id='title', component_property='children'),
    [Input(component_id='dt0', component_property='value'),
     Input(component_id='fund', component_property='value'),
     Input(component_id='ticker', component_property='value')
     ]
)
def get_holdings(dt0, fund, ticker):
    use_fd = True if fund == 'All' and ticker != 'All' or fund != 'All' else False
    df = holdings(dt0=dt0, fd=fund, tk=ticker, use_fd=use_fd)
    title = html.Div([html.H6(children=f"Total AUM: $ {sum(df.value):,.2f}"),])

    return df.to_dict('records'), title
