from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from dash import dcc
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import plotly.io as pio
from dash_bootstrap_templates import load_figure_template
import dash_daq as daq
from dash_extensions import WebSocket

pio.templates.default = 'plotly_white'
load_figure_template(["lux", "cyborg", "minty", "pulse"])

app = Dash(__name__, external_stylesheets=[
           './css/style.css'])

# Sidebar
sidebar = html.Div([
    html.Div([
        html.Div([
            html.Img(
                src="./assets/images/Analytics.png",
                    className="sidebar__img")],
                 style={"width": "30%", "display": "flex"}),

        html.Div([html.Span("DASHBOARD -",
                            style={"display": "block"},
                            className="sidebar__topLine__span"),
                  html.Span("Medidor de Cascão",
                            style={"display": "block"},
                            className="sidebar__topLine__span")])
    ], className="sidebar__topLine"),

    html.Div(
        [html.Span("Painel de controle",
                   className="sidebar__title")],
        style={"text-align": "center", "margin": "3% 0"}),
    html.Div(
        [html.Img(
            src="./assets/images/lupa.png",
                className="sidebar__img")],
        className="sidebar__lupa"),

    html.Div(
        [html.Button([html.Img(
            src="./assets/images/lapis.png",
            style={"width": "10%", "display": "inline-block", "padding-right ": "50%", "margin-right": "3%"}),
            html.Span("Iniciar Segmentação",
                      className="sidebar__button__fonts")],
            className="sidebar__button")],
        style={"width": "74.74%"}),

    html.Div(
        [html.Img(
            src="./assets/images/oficinaC.png",
            className="sidebar__img")],
        className="sidebar__logo",
        style={"height": "5%"}),

    html.Div(
        [html.Img(
            src="./assets/images/arcelor_logo.png",
            className="sidebar__img")],
        className="sidebar__logo",
        style={"height": "8%"}),

    html.Div(
        [html.Img(
            src="./assets/images/ifes_logoC.png",
                className="sidebar__img")],
        className="sidebar__logo",
        style={"height": "15%"}),
], className="sidebar")

# Primeiro Card
card1 = html.Div([
    html.Div(html.H2("Imagem Segmentada", style={"margin": "auto 0", "width": "100%"}), style={
        "display": "flex", "height": "10%", "width": "100%"}),
    # html.Img(src="./assets/images/youtube.png", style={"width": "50%", "max-height": "80%", "display": "block", "margin": "auto"})], className="card", style={"padding": "1.04%", "height": "100%"})
    html.Div(
        [html.Img(id="v1", style={"width": "100%", "max-height": "100%", "display": "block", "margin": "auto", })] +
        [WebSocket(url="ws://127.0.0.1:5000/stream0", id="ws")], style={"height": "90%"})],
    className="card", style={"padding": "1.04%", "height": "100%"})

# Segundo Card
layout = dict(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
card2 = html.Div([
    html.Div([
        html.Div(html.H2("Diâmetro Máximo [mm]:", style={
                 "margin": "auto 0", "width": "100%"}), style={"height": "auto", "display": "block"}),
        html.Div(
            [daq.LEDDisplay(
                id="operator-led",
                value="1704",
                color="#92e0d3",
                backgroundColor="#1e2130",
                size=20)], style={"display": "block", "height": "15%", }),
        html.Div([
            dcc.Graph(figure=go.Figure(go.Indicator(
                value=75,
                mode="gauge+number+delta",
                title={'text': "Diâmetro [mm]"},
                delta={'reference': 40, "suffix": "mm"},
                gauge={'axis': {'range': [40, 80]},
                      'steps': [
                    {'range': [40, 50], 'color': "greenyellow"},
                    {'range': [50, 60], 'color': "yellow"},
                    {'range': [60, 70], 'color': "orange"},
                    {'range': [70, 80], 'color': "red"}],
                    'threshold': {'line': {'color': "black", 'width': 8}, 'thickness': 0.75, 'value': 70},
                    'bar': {'color': "darkblue"},
                }),
                layout=layout),
                responsive=True,
                style={"width": "100%", "overflow": "hidden", "height": "18.22vw", "display": "block"}),
        ], style={"display": "flex", "width": "100%", "height": "70%", "margin": "auto 0"})
    ]),

], className="card", style={"height": "100%"})

# Leitura do dataframe para geração dos gráficos
df = px.data.gapminder().query("country=='Canada'")
fig = px.line(df, x="year", y="lifeExp",
              title='Life expectancy in Canada', color='country', symbol="country", template="lux")

fig.update_layout({
    "plot_bgcolor": "rgba(0, 0, 0, 0)",
    "paper_bgcolor": "rgba(0, 0, 0, 0)",
})

# Terceiro Card
card3 = html.Div([
    dcc.Graph(id='my-graph', figure=fig, responsive=True,
              style={"width": "100%", "height": "100%"})
], className="card2 sidebar__img")

# Montagem do cards
main = html.Div([
    html.Div(
        [card1, card2],
        className="main__c1c2"),
    html.Div(
        card3,
        className="main__c3")
], className="main")

# Inserção dos componentes no body
app.layout = html.Div([
    html.Div([
        sidebar, main
    ], className="desktop"),
], className="container")

# Callback para exibição do video por servidor
app.clientside_callback("function(m){return m? m.data : '';}", Output(
    "v1", "src"), Input("ws", "message"))

if __name__ == '__main__':
    port = "8000"
    print(f"Server rodando em http://127.0.0.1:{port}")
    app.run_server(debug=True, host="0.0.0.0", port=port)
