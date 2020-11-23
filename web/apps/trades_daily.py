print(f"{'-'*20} {'Trades daily':^30} {'-'*20}")

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import dashapp

import dash_table as dtbl
import core as c
from core import dates, funds, dt, cols2, right_cols

layout = html.Div(children=[
    html.H2(children='Ark Invest Trades by Fund', style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.Pre(children="Trading Day", style={"fontSize":"150%"}),
            dcc.Dropdown(
            id='dt', value=dt, clearable=False,
            persistence=True, persistence_type='session',
            options=[{'label': x, 'value': x} for x in dates]
        )], className='two columns'),

        html.Div([
            html.Pre(children="Fund", style={"fontSize":"150%"}),
            dcc.Dropdown(
            id='fund', value='ARKK', clearable=False,
            persistence=True, persistence_type='session',
            options=[{'label': x, 'value': x} for x in funds]
        )], className='two columns'),
    ], className='row'),

    html.H6(children=f'''BUYS'''),
    dtbl.DataTable(
        id='buyf',
        columns=cols2,
        style_cell={'textAlign': 'left'},
        page_size=20,
    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'right'
        } for c in right_cols
    ],
    ),

    html.H6(children=f'''SELLS'''),
    dtbl.DataTable(
        id='sellf',
        columns=cols2,
        style_cell={'textAlign': 'left'},
        page_size=20,
    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'right'
        } for c in right_cols
    ],
    ),

    html.H6(children=f'''New position(s)'''),
    dtbl.DataTable(
        id='new_buyf',
        columns=cols2,
        style_cell={'textAlign': 'left'},
        page_size=20,
    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'right'
        } for c in right_cols
    ],
    ),

    html.H6(children=f'''Closed position(s)'''),
    dtbl.DataTable(
        id='all_soldf',
        columns=cols2,
        style_cell={'textAlign': 'left'},
        page_size=20,
    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'right'
        } for c in right_cols
    ],
    ),

    html.H6(children=f'''No Change'''),
    dtbl.DataTable(
        id='no_chgf',
        columns=cols2,
        style_cell={'textAlign': 'left'},
        page_size=20,
    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'right'
        } for c in right_cols
    ],
    ),

    ])

@dashapp.callback(
    Output(component_id='buyf', component_property='data'),
    Output(component_id='sellf', component_property='data'),
    Output(component_id='no_chgf', component_property='data'),
    Output(component_id='new_buyf', component_property='data'),
    Output(component_id='all_soldf', component_property='data'),
    [Input(component_id='dt', component_property='value'),
     Input(component_id='fund', component_property='value')]
)
def get_holdings(dt, fund):
    buy, sell, no_change, new_buy, all_sold = c.compare_position(dt, fund)
    return buy.to_dict('records'), sell.to_dict('records'), no_change.to_dict('records'), new_buy.to_dict('records'), all_sold.to_dict('records')
