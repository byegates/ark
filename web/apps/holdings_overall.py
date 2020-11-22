import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app

import dash_table as dtbl
from core import holdings_overall, get_two_latest_dates

cur_dt, _ = get_two_latest_dates()
df = holdings_overall(cur_dt)

layout = html.Div(children=[
    html.H1(children='Ark Invest Holdings', style={"textAlign": "center"}),

    html.H3(children=f'''
        As of {cur_dt} market close
    '''),

    dtbl.DataTable(
        id='All Ark Latest Holdings',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_cell={'textAlign': 'left'},
        page_size=20,  # we have less data in this example, so setting to 20
        #style_table={'height': '600px', 'overflowY': 'auto'}
    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'right'
        } for c in ['shares', 'value', 'weight']
    ],
    )
])
