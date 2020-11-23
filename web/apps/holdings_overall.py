print(f"{'-'*20} {'holdings overall':^30} {'-'*20}")

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import dashapp

import dash_table as dtbl
import core as c
from core import dates, dt, cols, right_cols

layout = html.Div(children=[
    html.H2(children='Ark Invest Holdings', style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.Pre(children="Trading Day", style={"fontSize":"150%"}),
            dcc.Dropdown(
            id='dt', value=dt, clearable=False,
            persistence=True, persistence_type='session',
            options=[{'label': x, 'value': x} for x in dates]
        )], className='two columns'),
    ], className='row'),

    html.H6(id='title_h'),

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
    Output(component_id='title_h', component_property='children'),
    [Input(component_id='dt', component_property='value'),]
)
def get_holdings(dt):
    df = c.holdings(dt)
    title = html.Div([html.H6(children=f"Total AUM: $ {sum(df.value):,.2f}"),])

    return df.to_dict('records'), title
