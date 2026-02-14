from dash import dcc, html, Input, Output, callback, register_page
from pages.triangle_solver.ccc import layout as layout1
from pages.triangle_solver.cgc import layout as layout2
from pages.triangle_solver.gcg import layout as layout3


## Đăng ký đường dẫn
register_page(__name__, path="/calc/side")



## Layout toàn phần
layout = html.Div([
    dcc.Dropdown(
        id="mode",
        options=[
            {"label": "Cạnh - Cạnh - Cạnh", "value": "ccc"},
            {"label": "Cạnh - Góc - Cạnh", "value": "cgc"},
            {"label": "Góc - Cạnh - Góc", "value": "gcg"},
        ],
        value="ccc",
        clearable=False
    ),

    html.Div(id="input-area"),
])

@callback(
    Output("input-area", "children"),
    Input("mode", "value")
)
def render_inputs(mode):
    if mode == "ccc":
        return layout1
    elif mode == "cgc":
        return layout2
    elif mode == "gcg":
        return layout3
    else:
        return layout1

