import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dtbl
import core

dash_app = dash.Dash()
app = dash_app.server

cur_dt, pri_dt = core.get_two_latest_dates()
df = core.holdings_by_date(cur_dt)
val_float = df.value.str.strip('$ ').str.replace(',', '').astype(float)
df['weight'] = val_float/sum(val_float)


dash_app.layout = html.Div(children=[
    html.H1(children='Ark Holdings Analytics'),

    html.H2(children=f'''
        Ark Investments Latest Holdings as of {cur_dt}
    '''),

    dtbl.DataTable(
        id='All Ark Latest Holdings',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    )
])

if __name__ == '__main__':
    dash_app.run_server(debug=True)
