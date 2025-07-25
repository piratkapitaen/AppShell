import dash
from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import bcrypt
import mysql.connector

dash.register_page(__name__, path="/login")

layout = dmc.Container([
    dmc.Space(h=20),

    dmc.Title("Login", order=3, mt=20),

    dmc.Space(h=20),

    dmc.Stack(
        [
            dmc.TextInput(
                label="Username",
                placeholder="Your username",
                w=250,
            ),
            dmc.PasswordInput(
                label="Password",
                placeholder="Your password",
                w=250,
#                error="Invalid Password",
            ),
            
            dmc.Space(h=10),
            
            dmc.Button("Login", variant="outline", w=250, color="black"),
            
#            dmc.Rating(fractions=2, value=3, readOnly=False),
        ],
    ),
    
    html.H5("Please type in your username and password"),

#    dmc.Space(h=30),

#    dmc.Text(
#        "We look forward to hearing from you or welcoming you in person!",
#        size="sm"
#    )
], px=20)