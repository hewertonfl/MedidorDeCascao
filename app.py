from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from dash import dcc
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

app = Dash(__name__, external_stylesheets=['./css/style.css'])

sidebar = html.Div([
    html.Div([
        html.Div([
            html.Img(src="./assets/images/Analytics.png",
                     className="sidebar__img")
        ], style={"width": "30%"}),
        html.Div([html.Span("DASHBOARD", style={"display": "block"}),
                  html.Span("Medidor de Cascão", style={"display": "block"})],
                 className="sidebar__topLine__span")
    ], className="sidebar__topLine"),
    html.Div(
        [html.Span("Painel de controle")], className="sidebar__title", style={"text-align": "center"}),
    html.Div(
        [html.Img(src="./assets/images/lupa.png",
                  className="sidebar__img")], className="sidebar__lupa"),
    html.Div(
        [html.Img(src="./assets/images/lapis.png",
                  style={"width": "9%"}), html.Button(
            "Iniciar Segmentação", className="sidebar__button__fonts")], className="sidebar__button sidebar__button__box"),
    html.Div(
        [html.Img(src="./assets/images/oficina41.png",
                  className="sidebar__img")], className="sidebar__logo", style={"height": "5%"}),
    html.Div(
        [html.Img(src="./assets/images/arcelor_logo1.png",
                  className="sidebar__img")], className="sidebar__logo", style={"height": "8%"}),
    html.Div(
        [html.Img(src="./assets/images/ifes_logo.png",
                  className="sidebar__img")], className="sidebar__logo", style={"height": "15%"}),
], className="sidebar")


card1 = html.Div([
    html.Img(src="./assets/images/youtube.png")
], className="card")
card2 = html.Div([
    html.Img(src="./assets/images/card2a.png", className="sidebar__img")
], className="card")

df = px.data.gapminder().query("country=='Canada'")
fig = px.line(df, x="year", y="lifeExp",
              title='Life expectancy in Canada', color='country', symbol="country")

card3 = html.Div([
    dcc.Graph(id='my-graph', figure=fig, responsive=True,
              style={"width": "100%", "height": "100%"})
], className="card2 sidebar__img")

main = html.Div([
    html.Div([card1, card2], style={
             "display": "flex", "height": "60%", "justify-content": "space-between"}),
    card3
], className="main")

app.layout = html.Div([
    html.Div([
        sidebar, main
    ], className="desktop"),
], className="container")


# @app.callback(
#     Output('my-graph', 'figure'),
#     Input('dropdown', 'value')

# )
# def update_side_graph(input_data):
#     grafico = {
#         'data': [{'x': [1, 2, 3], 'y': [4, 1, 2], 'name':'Gráfico X'}],
#         'layout': {
#             'title': 'Dash Data Visualization'
#         }
#     }
#     return grafico


if __name__ == '__main__':
    port = "8050"
    print(f"Server rodando em http://127.0.0.1:{port}")
    app.run_server(debug=True, host="0.0.0.0", port=port)
