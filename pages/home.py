import dash
from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

dash.register_page(__name__, path="/")

layout = dmc.Container([
    dmc.Title("Welcome to Crypto Chart", order=1, mt=20),

    dmc.Space(h=20),

    dmc.Text(
        "This app allows you to explore and analyze various cryptocurrencies "
        "with interactive charts and dynamic tools. "
        "Use the sidebar menu to browse assets and gain deeper insights into market trends.",
        size="md"
    ),

    dmc.Space(h=30),

    dmc.Alert(
        "Note: All data is sourced from public APIs and is intended for analytical purposes only.",
        title="Info",
        color="blue",
        withCloseButton=False
    )
], px=20)