print('')
print(f"{'-'*20} {'main.py':^30} {'-'*20}")
print('')

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import dashapp
from app import app

# Connect to your app pages
from apps import holdings, trades_daily, trades

print('dashapp.layout = html.Div([')
dashapp.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Holdings|', href='/apps/holdings'),
        dcc.Link('Trades|', href='/apps/trades'),
        dcc.Link('Trades by Fund', href='/apps/trades_daily'),
    ], className="row"),
    html.Div(id='page-content', children=[])
])


print('@dashapp.callback, display_page')
@dashapp.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    print(f"{'-'*20} {pathname:^30} {'-'*20}")
    if pathname == '/apps/holdings':
        return holdings.layout
    if pathname == '/apps/trades':
        return trades.layout
    if pathname == '/apps/trades_daily':
        return trades_daily.layout
    else:
        return holdings.layout


if __name__ == '__main__':
    print('dashapp.run_server(debug=True)')
    dashapp.run_server(debug=True)