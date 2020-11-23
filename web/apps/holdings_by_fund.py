ln = '-'*20
print(f"{ln} {'holdings_by_fund':^30} {ln}")

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import dashapp

import dash_table as dtbl
import core as c
from core import dates, funds, dt, fund, cols

layout = html.Div(children=[
    html.H1(children='Ark Invest Holdings by Fund', style={"textAlign": "center"}),

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

    html.Br(),
    html.H6(id='tt_val'),
    dtbl.DataTable(
        id='holdings',
        columns=cols,
        style_cell={'textAlign': 'left'},
        page_size=20,
    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'right'
        } for c in ['shares', 'value', 'weight']
    ],
    )

    ])

@dashapp.callback(
    Output(component_id='holdings', component_property='data'),
    Output(component_id='tt_val', component_property='children'),
    [Input(component_id='dt', component_property='value'),
     Input(component_id='fund', component_property='value')]
)
def get_holdings(dt, fund):
    df = c.holdings(dt, fund)
    data=df.to_dict('records')
    tt_val = f"$ {sum(df.value):,.2f}"

    return data, tt_val
