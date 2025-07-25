import dash
from dash import html, dcc, Dash, Output, Input, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import datetime

dash.register_page(__name__, path="/unlock")

layout = dmc.Container(
    [
        dmc.Title("🔓 Full App unlock 1,99 €", order=2, mb=20),
        html.Div(id="paypal-container-M8R5865HUP2VE"),  # <<< gleiche ID wie im Script!
        dmc.Text("App will be unlocked after succesful payment.", mt="md"),
    ],
    size="sm",
    pt=50,
)


#layout = dmc.Container(
#    [
#        dmc.Title("🔓 Freischalten für 1,99 €", order=2, mb=20),
#        html.Div(id="paypal-container-M8R5"),  # <<< gleiche ID wie im Script!
#        dmc.Text("Nach erfolgreicher Zahlung wird die App freigeschaltet.", mt="md"),
#    ],
#    size="sm",
#    pt=50,
#)