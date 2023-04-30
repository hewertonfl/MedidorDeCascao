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

sidebar = html.Div([
    html.Div([
        html.Div([
            html.Img(src="./assets/images/Analytics.png",
                     className="sidebar__img")
        ], style={"width": "30%", "display": "flex"}),
        html.Div([html.Span("DASHBOARD -", style={"display": "block"},
                 className="sidebar__topLine__span"),
                  html.Span("Medidor de Cascão", style={"display": "block"},
                 className="sidebar__topLine__span")])
    ], className="sidebar__topLine"),
    html.Div(
        [html.Span("Painel de controle", className="sidebar__title")], style={"text-align": "center", "margin": "3% 0"}),
    html.Div(
        [html.Img(src="./assets/images/lupa.png",
                  className="sidebar__img")], className="sidebar__lupa"),
    html.Div(
        [html.Button([html.Img(src="./assets/images/lapis.png",
                               style={"width": "10%", "display": "inline-block", "padding-right ": "50%", "margin-right": "3%"}),
                     html.Span("Iniciar Segmentação", className="sidebar__button__fonts")], className="sidebar__button")], style={"width": "74.74%"}),
    html.Div(
        [html.Img(src="./assets/images/oficinaC.png",
                  className="sidebar__img")], className="sidebar__logo", style={"height": "5%"}),
    html.Div(
        [html.Img(src="./assets/images/arcelor_logo.png",
                  className="sidebar__img")], className="sidebar__logo", style={"height": "8%"}),
    html.Div(
        [html.Img(src="./assets/images/ifes_logoC.png",
                  className="sidebar__img")], className="sidebar__logo", style={"height": "15%"}),
], className="sidebar")


card1 = html.Div(
    [#html.Span("Imagem Segmentada", style={"display":"block"}),
    html.Img(src="./assets/images/youtube.png",style={"max-width":"100%","max-height":"100%","display":"block"})], className="card")
# [html.Img(style={"width": "100%", "max-height": "100%"}, id=f"v{i}") for i in range(1)] +
# [WebSocket(
#     url=f"ws://127.0.0.1:5000/stream{i}", id=f"ws{i}") for i in range(1)], className="card")

# Medidor
layout = dict(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
fig = html.Div([
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
        style={"max-height": "100%", "width": "100%", "display": "block","overflow":"hidden"}),
], style={"display": "flex", "width": "100%", "justify-content": "center"})

card2 = html.Div([
    html.Div([
        html.H2("Diâmetro Máximo [mm]:"),
        daq.LEDDisplay(
            id="operator-led",
            value="1704",
            color="#92e0d3",
            backgroundColor="#1e2130",
            size=20,
        )], className="diam"), fig,

], className="card")

# DataFrame
df = px.data.gapminder().query("country=='Canada'")
fig = px.line(df, x="year", y="lifeExp",
              title='Life expectancy in Canada', color='country', symbol="country", template="lux")

fig.update_layout({
    "plot_bgcolor": "rgba(0, 0, 0, 0)",
    "paper_bgcolor": "rgba(0, 0, 0, 0)",
})

card3 = html.Div([
    dcc.Graph(id='my-graph', figure=fig, responsive=True,
              style={"width": "100%", "height": "100%"})
], className="card2 sidebar__img")

main = html.Div([
    html.Div([card1, card2], style={
             "display": "flex", "height": "60%", "width": "100%", "justify-content": "space-between", "padding": "2% 0 0", "box-sizing": "border-box"}),
    html.Div(card3, style={"height": "40%",
             "padding": "2% 0", "box-sizing": "border-box"})
], className="main")

app.layout = html.Div([
    html.Div([
        sidebar, main
    ], className="desktop"),
], className="container")


# for i in range(1):
#     app.clientside_callback("function(m){return m? m.data : '';}", Output(
#         f"v{i}", "src"), Input(f"ws{i}", "message"))

if __name__ == '__main__':
    port = "8000"
    print(f"Server rodando em http://127.0.0.1:{port}")
    app.run_server(debug=True, host="0.0.0.0", port=port)
