import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import holdings_overall, holdings_by_fund, trades_daily


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Holdings|', href='/apps/holdings_overall'),
        dcc.Link('Holdings by Fund|', href='/apps/holdings_by_fund'),
        dcc.Link('Trades', href='/apps/trades_daily'),
    ], className="row"),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/holdings_overall':
        return holdings_overall.layout
    if pathname == '/apps/holdings_by_fund':
        return holdings_by_fund.layout
    if pathname == '/apps/trades_daily':
        return trades_daily.layout
    else:
        return "This is a 404, don't mess with me!"


if __name__ == '__main__':
    app.run_server(debug=True, port=8888)