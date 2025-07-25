import dash
from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

dash.register_page(__name__, path="/assets")

assets = ["BTC", "ETH", "XRP", "SOL", "LINK", "ADA", "DOGE", "TRX", "SUI", "HBAR", "PEPE", "DOT", "AVAX", "SHIB"]

layout = dmc.Container(
    children=[
        dmc.Title("Assets", order=2, mt=20),
        dmc.Space(h=20),
        dmc.Stack(
            [
                dmc.NavLink(
                    label=asset,
                    href=f"/asset-details?symbol={asset}",
#                    icon=DashIconify(icon="mdi:coin", width=16, color="#c2c7d0")
                )
                for asset in assets
            ],
            gap="xs"
        )
    ],
    px=20
)
