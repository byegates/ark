import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dtbl
import core

dash_app = dash.Dash(__name__)
dash_app.title = 'Ark Invest'
app = dash_app.server

# Latest all holdings
cur_dt, pri_dt = core.get_two_latest_dates()
df = core.holdings_by_date(cur_dt)
val_float = df.value.str.strip('$ ').str.replace(',', '').astype(float)
df['weight'] = (val_float/sum(val_float)).round(8)
df.insert(0, 'Seq', df.index+1) # Add number sequence of holdings


dash_app.layout = html.Div(children=[
    html.H1(children='Ark Invest Holdings'),

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

if __name__ == '__main__':
    dash_app.run_server(debug=True)
