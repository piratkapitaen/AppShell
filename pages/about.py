import dash
from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

dash.register_page(__name__, path="/about")

layout = dmc.Container([
    dmc.Title("Contact", order=2, mt=20),

    dmc.Space(h=20),

    dmc.Group([
        DashIconify(icon="mdi:email-outline", width=24),
        dmc.Text("admin@stdf-me.com", size="md"),
    ], gap="sm"),

    dmc.Group([
        DashIconify(icon="mdi:web", width=24),
        dmc.Text("https://www.stdf-me.com", size="md"),
    ], gap="sm", mt=10),
    
    html.H5("We look forward to hearing from you or welcoming you in person!"),

#    dmc.Space(h=30),

#    dmc.Text(
#        "We look forward to hearing from you or welcoming you in person!",
#        size="sm"
#    )
], px=20)