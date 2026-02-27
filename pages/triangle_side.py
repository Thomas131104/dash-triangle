from dash import dcc, html, Input, Output, callback, register_page
import dash_bootstrap_components as dbc
from pages.triangle_solver.ccc import layout as layout1
from pages.triangle_solver.cgc import layout as layout2
from pages.triangle_solver.gcg import layout as layout3


## Đăng ký đường dẫn
register_page(__name__, path="/calc/side")



## Layout toàn phần
layout = dbc.Container([

    dbc.Tabs(
        id="mode",
        active_tab="ccc",
        className="mb-4",
        children=[
            dbc.Tab(label="Cạnh - Cạnh - Cạnh", tab_id="ccc"),
            dbc.Tab(label="Cạnh - Góc - Cạnh", tab_id="cgc"),
            dbc.Tab(label="Góc - Cạnh - Góc", tab_id="gcg"),
        ],
    ),

    html.Div(id="input-area")

], fluid=True)


@callback(
    Output("input-area", "children"),
    Input("mode", "active_tab")
)
def render_inputs(mode):
    if mode == "ccc":
        return layout1
    elif mode == "cgc":
        return layout2
    elif mode == "gcg":
        return layout3
    return layout1
