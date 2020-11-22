import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dtbl

dash_app = dash.Dash(__name__)
dash_app.title = 'Ark Invest'
app = dash_app.server

from core import holdings_overall, trade_dates

cur_dt = trade_dates()[0]
df = holdings_overall(cur_dt)

dash_app.layout = html.Div(children=[
    html.H1(children='Ark Invest Holdings', style={"textAlign": "center"}),

    html.H4(children=f'''
        As of {cur_dt} (market close)
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

if __name__ == '__main__':
    dash_app.run_server(debug=True)
