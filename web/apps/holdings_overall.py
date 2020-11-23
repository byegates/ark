print(f"{'-'*20} {'holdings overall':^30} {'-'*20}")

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app

import dash_table as dtbl
import core as c
from core import dates, funds, dt, fund, cols

df = c.holdings(dt)
tt_val = f"$ {sum(df.value):,.2f}"

layout = html.Div(children=[
    html.H1(children='Ark Invest Holdings', style={"textAlign": "center"}),

    html.H6(children=f'''
        Total AUM: {tt_val} (as of {dt} market close) 
    '''),

    dtbl.DataTable(
        id='All Ark Latest Holdings',
        columns=cols,
        data=df.to_dict('records'),
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
