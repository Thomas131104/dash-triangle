import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")

layout = html.Div([

    # ===== HEADER =====
    html.Div([
        html.H1("Chương trình phân tích tam giác"),
        html.P("Ứng dụng tính toán, trực quan hóa và lưu trữ dữ liệu hình học")
    ], className="mb-4"),

    # ===== SUMMARY SECTION (4 phần) =====
    dbc.Row([

        # 1️⃣ Giới thiệu
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4("📘 Giới thiệu"),
                    html.P(
                        "Ứng dụng cho phép nhập tọa độ hoặc độ dài cạnh "
                        "để tính toán đầy đủ thông số của tam giác."
                    ),
                ])
            ], className="h-100"),
            md=6
        ),

        # 2️⃣ Chức năng chính 1
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4("📍 Tính theo tọa độ"),
                    html.P("Nhập 3 điểm trong hệ trục Oxy."),
                    dcc.Link("Truy cập", href="/calc/coord")
                ])
            ], className="h-100"),
            md=6
        ),

        # 3️⃣ Chức năng chính 2
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4("📐 Tính theo độ dài cạnh"),
                    html.P("Nhập 3 cạnh để xác định tam giác."),
                    dcc.Link("Truy cập", href="/calc/side")
                ])
            ], className="h-100"),
            md=6
        ),

        # 4️⃣ Lịch sử
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4("📜 Lịch sử tính toán"),
                    html.P(
                        "Xem lại các tam giác đã lưu trong cơ sở dữ liệu."
                    ),
                    dcc.Link("Xem lịch sử", href="/history")
                ])
            ], className="h-100"),
            md=6
        ),

    ], className="g-4")

])
