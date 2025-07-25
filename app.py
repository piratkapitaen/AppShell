"""
Mobile only navbar
"""
from dotenv import load_dotenv
load_dotenv()

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback, clientside_callback, page_container, dcc
from dash_iconify import DashIconify

app = Dash(__name__, use_pages=True)

logo = "assets/btc.png"

buttons = [
    dcc.Link(dmc.Button("Home", variant="subtle", color="gray"), href="/"),
    dcc.Link(dmc.Button("Assets", variant="subtle", color="gray"), href="/assets"),
    dcc.Link(dmc.Button("Bitcoin Dominance", variant="subtle", color="gray"), href="/btc-dominance"),
    dcc.Link(dmc.Button("Liquidation Heatmap", variant="subtle", color="gray"), href="/heatmap"),
    dcc.Link(dmc.Button("Unlock", variant="subtle", color="gray"), href="/unlock"),
    dcc.Link(dmc.Button("Login", variant="subtle", color="gray"), href="/login"),
#    dcc.Link(dmc.Button("Chat", variant="subtle", color="gray"), href="/chat"),
    dcc.Link(dmc.Button("About", variant="subtle", color="gray"), href="/about"),
]

theme_toggle = dmc.Switch(
    offLabel=DashIconify(
        icon="radix-icons:sun", width=15, color=dmc.DEFAULT_THEME["colors"]["yellow"][8]
    ),
    onLabel=DashIconify(
        icon="radix-icons:moon",
        width=15,
        color=dmc.DEFAULT_THEME["colors"]["yellow"][6],
    ),
    id="color-scheme-toggle",
    persistence=True,
    color="grey",
)

layout = dmc.AppShell(
    [
        dcc.Location(id="url"),
		dmc.AppShellHeader(
#            style={"borderBottom": "none"},
            children=[dmc.Group(
                [
                    dmc.Burger(
                        id="burger",
                        size="sm",
                        hiddenFrom="sm",
                        opened=False,
                    ),
                    dmc.Image(src=logo, h=40, flex=0),
                    dmc.Title("Crypto App", c="orange"),
                    dmc.Box(style={"flexGrow": 1}),
                    theme_toggle,
                ],
                h="100%",
                px="md",
            ),
            
            ],
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=buttons,
            p="md",
        ),
        dmc.AppShellMain(children=page_container),
    ],
    header={
        "height": {"base": 60, "md": 70, "lg": 80},
    },
    navbar={
        "width": {"base": 200, "md": 300, "lg": 400},
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    padding="md",
    id="appshell",
)

app.layout = dmc.MantineProvider(layout)


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def toggle_navbar(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar

@callback(
    Output("appshell", "navbar", allow_duplicate=True),
    Output("burger", "opened", allow_duplicate=True),
    Input("url", "pathname"),
    prevent_initial_call="initial_duplicate"
)
def close_navbar_on_navigation(_):
    navbar = {
        "collapsed": {"mobile": True, "desktop": True},
        "width": 300,
        "breakpoint": "sm"
    }
    return navbar, False  # ← Burger-Icon zurücksetzen

clientside_callback(
    """ 
    (switchOn) => {
       document.documentElement.setAttribute('data-mantine-color-scheme', switchOn ? 'dark' : 'light');  
       return window.dash_clientside.no_update
    }
    """,
    Output("color-scheme-toggle", "id"),
    Input("color-scheme-toggle", "checked"),
)

if __name__ == "__main__":
    app.run(debug=True)
    