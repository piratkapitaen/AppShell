import dash
from dash import html, dcc, callback, Input, Output
import dash_mantine_components as dmc
import requests
import pandas as pd
import plotly.graph_objects as go
from urllib.parse import parse_qs, urlparse
from dash_iconify import DashIconify
import numpy as np
from scipy.signal import find_peaks, argrelextrema

dash.register_page(__name__, path="/asset-details", name="Asset Details")

layout = html.Div(
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "right": 0,
        "bottom": 0,
        "backgroundColor": "#000",  # Schwarzer Hintergrund
        "padding": "20px",
        "overflowY": "auto",
        "zIndex": 2000,
        "display": "flex",
        "flexDirection": "column"
    },
    children=[
        html.Div(
            style={"marginBottom": "20px"},
            children=[
            dcc.Link(
                dmc.Button(
                    leftSection=DashIconify(icon="mdi:arrow-left", width=20),
                    children="Back",
                    variant="outline",
                    color="gray",
                    radius="xl",
                    size="md",
                ),
                href="/assets",  # Zielseite
                style={"textDecoration": "none"},
            ),
            ]
        ),
        dcc.Location(id="asset-url", refresh=False),

        # Spinner und Inhalt
        dcc.Loading(
            type="circle",
            color="#666",
            fullscreen=True,
            children=html.Div(
                id="asset-details-container",
                style={"flex": "1"}
            )
        ),

        # Radiobuttons unter dem Chart
        html.Div(
            style={"marginTop": "15px", "color": "white"},
            children=[
                dcc.Checklist(
                    id="indicator-select",
                    options=[
                        {"label": "triple SMA", "value": "triple_sma"},
                        {"label": "triple EMA", "value": "triple_ema"},
                        {"label": "Trendlines", "value": "trendlines"},
                    ],
                    value=[""],  # Default ausgewählt (optional)
                    labelStyle={"display": "inline-block", "marginRight": "20px", "cursor": "pointer"},
                    inputStyle={"marginRight": "6px"},
                    style={"fontSize": "16px"},
                )
            ]
        )
    ]
)



@callback(
    Output("asset-details-container", "children"),
    Input("asset-url", "search"),
    Input("indicator-select", "value")  # 👈 This line is essential!
)
def display_asset_details(search, selected_indicators):
    if not search:
        return "No query parameters found."

    query_params = parse_qs(urlparse(search).query)
    symbol = query_params.get("symbol", [None])[0]

    if not symbol:
        return "No 'symbol' parameter found."

    binance_symbol = symbol.upper() + "USDT"
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": binance_symbol,
        "interval": "1h",
        "limit": 500
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        columns = [
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "num_trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ]
        df = pd.DataFrame(data, columns=columns)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)
        df = df[["open", "high", "low", "close", "volume"]].astype(float)

        close_hourly = df["close"]
        daily_close = df["close"].resample("1D").last()
        window_5d = 5 * 24
        window_10d = 10 * 24
        window_20d = 20 * 24
        # Step 2: Calculate daily SMAs
        daily_sma_5 = daily_close.rolling(window=5).mean()
        daily_sma_10 = daily_close.rolling(window=10).mean()
        daily_sma_20 = daily_close.rolling(window=20).mean()
        hourly_index = df.index
#        df["Daily_SMA_5"] = daily_sma_5.reindex(hourly_index, method='ffill').interpolate(method='time')
#        df["Daily_SMA_10"] = daily_sma_10.reindex(hourly_index, method='ffill').interpolate(method='time')
#        df["Daily_SMA_20"] = daily_sma_20.reindex(hourly_index, method='ffill').interpolate(method='time')
        df["Daily_SMA_5"] = close_hourly.rolling(window=window_5d, min_periods=1).mean()
        df["Daily_SMA_10"] = close_hourly.rolling(window=window_10d, min_periods=1).mean()
        df["Daily_SMA_20"] = close_hourly.rolling(window=window_20d, min_periods=1).mean()
        
#        daily_ema_20 = daily_close.ewm(span=20, adjust=False).mean()
#        daily_ema_50 = daily_close.ewm(span=50, adjust=False).mean()        
#        df["daily_ema_20"] = df["close"].ewm(span=20*24, adjust=False).mean()
#        df["daily_ema_50"] = df["close"].ewm(span=50*24, adjust=False).mean()
#        df["EMA20"] = daily_ema_20.reindex(df.index, method='ffill').interpolate(method='time')
#        df["EMA50"] = daily_ema_50.reindex(df.index, method='ffill').interpolate(method='time')
        df["EMA20"] = df["close"].ewm(span=20*24, adjust=False).mean()
        df["EMA50"] = df["close"].ewm(span=50*24, adjust=False).mean()              

        fig = go.Figure(data=[go.Candlestick(
            x=df.index,
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            increasing=dict(line=dict(color='limegreen'), fillcolor='limegreen'),
            decreasing=dict(line=dict(color='red'), fillcolor='red'),
            name="Price"
        )])

        if "triple_ema" in selected_indicators:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df["EMA20"],
                line=dict(color="cyan", width=1),
                name="EMA 20"
            ))
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df["EMA50"],
                line=dict(color="coral", width=1),
                name="EMA 50"
            ))
        if "triple_sma" in selected_indicators:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df["Daily_SMA_5"],
                line=dict(color="yellow", width=1),
                name="Daily SMA 5"
            ))
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df["Daily_SMA_10"],
                line=dict(color="lightblue", width=1),
                name="Daily SMA 10"
            ))
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df["Daily_SMA_20"],
                line=dict(color="magenta", width=1),
                name="Daily SMA 20"
            ))


        fig.update_layout(
            legend=dict(
                orientation="h",         # horizontal
                yanchor="top",
                y=1.02,                  # über dem Chart
                xanchor="left",
                x=0,
                bgcolor="rgba(0,0,0,0)", # transparenter Hintergrund
                font=dict(color="white") # bei dunklem Hintergrund
            ),
            title=f"{binance_symbol} - 1h Chart, Price in USDT",
            xaxis_title="Time",
#            yaxis_title="Price (USDT)",
            xaxis_rangeslider_visible=False,
            template="plotly_dark",  # dark base
            plot_bgcolor="black",
            paper_bgcolor="black",
            font=dict(color="white"),
            height=None,
            margin=dict(l=40, r=40, t=60, b=40)
        )
        fig.update_xaxes(gridcolor='#e0e0e0')
        fig.update_yaxes(gridcolor='#e0e0e0')

        return dcc.Graph(figure=fig)

    except Exception as e:
        return html.Div([
            html.P(f"Error loading data for {binance_symbol}: {e}")
        ], style={"color": "red"})
