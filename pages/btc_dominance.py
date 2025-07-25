import dash
from dash import html, dcc, Output, Input, callback
import requests
import pandas as pd
import plotly.graph_objects as go
from time import sleep

dash.register_page(__name__, path="/btc-dominance", name="BTC Dominance")

layout = html.Div(
    style={"padding": "20px", "maxWidth": "600px", "margin": "auto"},
    children=[
        html.H2("Current Bitcoin Dominance"),
        dcc.Loading(
            type="circle",
            children=html.Div(id="btc-dominance-current-content")
        ),
        dcc.Interval(id="interval-update", interval=5*60*1000, n_intervals=0)  # alle 5 Minuten aktualisieren
    ]
)

@callback(
    Output("btc-dominance-current-content", "children"),
    Input("interval-update", "n_intervals")
)
def update_current_dominance(n):
    try:
        url = "https://api.coingecko.com/api/v3/global"
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()

        btc_dominance = data["data"]["market_cap_percentage"]["btc"]
        other_dominance = 100 - btc_dominance

        fig = go.Figure(go.Pie(
            labels=["Bitcoin", "Andere Coins"],
            values=[btc_dominance, other_dominance],
            hole=0.5,
            marker_colors=["#f2a900", "#444"]
        ))
        fig.update_layout(
            title=f"Bitcoin Dominanz: {btc_dominance:.2f}%",
            template="plotly_dark",
            height=400
        )

        return dcc.Graph(figure=fig)

    except Exception as e:
        return html.Div(f"Fehler beim Laden der Daten: {e}", style={"color": "red"})