from dash import html
import dash
from server import app

app.layout = html.Div([

    # ===== HEADER =====
    html.Header([
        html.Div([
            html.H1("Chương trình tam giác"),
            html.P("Tính toán – Phân tích – Lưu trữ dữ liệu hình học")
        ], className="container header-content")
    ]),

    # ===== MAIN =====
    html.Main([
        html.Div(
            dash.page_container,
            className="container main-content"
        )
    ]),

    # ===== FOOTER =====
    html.Footer([
        html.Div([
            html.Small("© 2026 Mus · Triangle Analysis App")
        ], className="container footer-content")
    ])

])

if __name__ == "__main__":
    app.run(debug=True)
