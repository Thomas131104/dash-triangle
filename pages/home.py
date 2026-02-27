import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")

# ===== COMPONENT TÁI SỬ DỤNG =====
def make_feature_card(icon, title, desc, link, color):
    return dbc.Card(
        dbc.CardBody([
            html.Div(icon, className="feature-icon"),
            html.H5(title, className="mt-3"),
            html.P(desc, className="text-muted"),
            dcc.Link(
                dbc.Button("Truy cập", color=color, className="w-100"),
                href=link
            )
        ]),
        className="feature-card h-100 text-center"
    )


layout = dbc.Container(
    [
        # ===== TITLE =====
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H3(
                            "Chọn phương thức phân tích",
                            className="fw-bold text-center mb-5"
                        ),
                    ]
                ),
                md=12
            )
        ),

        # ===== FEATURE CARDS =====
        dbc.Row(

            [

                dbc.Col(make_feature_card(
                    "📍",
                    "Theo tọa độ",
                    "Nhập 3 điểm A, B, C trong mặt phẳng Oxy.",
                    "/calc/coord",
                    "primary"
                ), md=4),

                dbc.Col(make_feature_card(
                    "📐",
                    "Theo cạnh / góc",
                    "Nhập độ dài cạnh hoặc góc để xác định tam giác.",
                    "/calc/side",
                    "primary"
                ), md=4),

                dbc.Col(make_feature_card(
                    "📜",
                    "Lịch sử",
                    "Xem lại các tam giác đã phân tích.",
                    "/history",
                    "secondary"
                ), md=4),

            ],

            className="g-4 mb-5"

        )

    ],

    fluid=True
)

