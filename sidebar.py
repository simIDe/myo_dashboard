from dash import html
import dash_bootstrap_components as dbc


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#e9c46a",
}

sidebar = html.Div(
    [
        html.H2("Myo App", className="display-4"),
        html.Hr(),
        html.P(
            "A basic exemple of an EMG data mining application", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Explore EMG signal",
                            href="/explore-emg", active="exact"),
                dbc.NavLink("Another panel",
                            href="/another-panel", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
