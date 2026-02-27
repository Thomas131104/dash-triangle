from dash import html
import dash
import dash_bootstrap_components as dbc
from server import app

navbar = dbc.NavbarSimple(
    brand="Triangle Analyzer",
    brand_href="/",
    children=[
        dbc.NavItem(dbc.NavLink("Trang chủ", href="/", active="exact")),
        dbc.NavItem(dbc.NavLink("Theo tọa độ", href="/calc/coord", active="exact")),
        dbc.NavItem(dbc.NavLink("Theo cạnh", href="/calc/side", active="exact")),
        dbc.NavItem(dbc.NavLink("Lịch sử", href="/history", active="exact")),
    ],
    color="white",
    dark=False,
    className="shadow-sm",
    fixed="top"
)



app.layout = html.Div([

    navbar,

    html.Header([
        dbc.Row(
            dbc.Col(
                html.Div([
                    html.H1("Triangle Analyzer", className="hero-title"),
                    html.P(
                        "Phân tích – Tính toán – Lưu trữ dữ liệu hình học phẳng",
                        className="hero-subtitle",
                    ),
                ], className="hero-section text-center")
            )
        )
    ]),

    html.Main([
        html.Div(
            dash.page_container,
            className="container main-content"
        )
    ]),

    html.Footer([
        html.Div([
            html.Small("© 2026 Mus · Triangle Analysis App")
        ], className="container footer-content")
    ])

])


if __name__ == "__main__":
    app.run(debug=True)
