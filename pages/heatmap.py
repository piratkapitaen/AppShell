import dash
from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

dash.register_page(__name__, path="/heatmap", name="Liquidation Heatmap")

layout = dmc.Container(
    [
        dmc.Title("Bitcoin Liquidation Heatmap", order=2, mt=20),
        dmc.Space(h=20),
        # Eingebettetes CoinAnk Widget
        html.Iframe(
            src="https://coinank.com/liqHeatMapChart/btcusdt/3d",
            style={"width": "100%", "height": "700px", "border": "none"},
        ),
        dmc.Text("Source: CoinAnk", c="gray", size="sm", mt=10),
    ],
    fluid=True,
    p=20,
)