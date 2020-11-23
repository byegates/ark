print(f"{'-'*20} {'Trades daily':^30} {'-'*20}")

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app

import dash_table as dtbl
import core as c
from core import dates, funds, dt, fund, cols2, right_cols

layout = html.Div(children=[
    html.H1(children='Position Changes by Fund', style={"textAlign": "center"}),

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

    html.H6(children=f'''Increased position(s)'''),
    dtbl.DataTable(
        id='buy',
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

    html.H6(children=f'''Decreased position(s)'''),
    dtbl.DataTable(
        id='sell',
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
        id='new_buy',
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
        id='all_sold',
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

    html.H6(children=f'''Position(s) with no change'''),
    dtbl.DataTable(
        id='no_change',
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

@app.callback(
    Output(component_id='buy', component_property='data'),
    Output(component_id='sell', component_property='data'),
    Output(component_id='no_change', component_property='data'),
    Output(component_id='new_buy', component_property='data'),
    Output(component_id='all_sold', component_property='data'),
    [Input(component_id='dt', component_property='value'),
     Input(component_id='fund', component_property='value')]
)
def get_holdings(dt, fund):
    buy, sell, no_change, new_buy, all_sold = c.compare_position(dt, fund)
    return buy.to_dict('records'), sell.to_dict('records'), no_change.to_dict('records'), new_buy.to_dict('records'), all_sold.to_dict('records')
