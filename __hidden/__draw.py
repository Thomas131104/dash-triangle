import numpy as np
import plotly.graph_objects as go
from triangle import TriangleWithCoords

def _draw_triangle(x1, y1, x2, y2, x3, y3):

    tri_with_coords = TriangleWithCoords(x1, y1, x2, y2, x3, y3)

    A = tri_with_coords.A
    B = tri_with_coords.B
    C = tri_with_coords.C

    centroid = tri_with_coords.centroid()
    orthocenter = tri_with_coords.orthocenter()
    circum = tri_with_coords.circumcircle()
    incircle = tri_with_coords.incircle()

    fig = go.Figure()



    # =========================
    # 1️⃣ TAM GIÁC
    # =========================
    fig.add_trace(go.Scatter(
        x=[A.x, B.x, C.x, A.x],
        y=[A.y, B.y, C.y, A.y],
        mode="lines+markers+text",
        text=["A", "B", "C", ""],
        textposition="top center",
        line=dict(width=3),
        showlegend=False,
        name="Tam giác"
    ))



    # =========================
    # 2️⃣ TRUNG TUYẾN
    # =========================
    for vertex, foot in [
        (A, centroid["feet"]["A_feet"]),
        (B, centroid["feet"]["B_feet"]),
        (C, centroid["feet"]["C_feet"]),
    ]:
        fig.add_trace(go.Scatter(
            x=[vertex.x, foot.x],
            y=[vertex.y, foot.y],
            mode="lines",
            line=dict(dash="dot", width=1.5),
            legendgroup="median",
            name="Trung tuyến",
            showlegend=False,
            visible="legendonly"
        ))

    # giao điểm
    G = centroid["intersect"]
    fig.add_trace(go.Scatter(
        x=[G.x],
        y=[G.y],
        mode="markers",
        marker=dict(size=10, symbol="x"),
        name="Trọng tâm",
        legendgroup="median",
        visible="legendonly"
    ))



    # =========================
    # 3️⃣ ĐƯỜNG CAO
    # =========================
    H = orthocenter["intersect"]

    altitude_vertices = [A, B, C]

    for vertex in altitude_vertices:
        fig.add_trace(go.Scatter(
            x=[vertex.x, H.x],
            y=[vertex.y, H.y],
            mode="lines",
            line=dict(dash="dot", width=1.5),
            legendgroup="altitude",
            name="Đường cao",
            showlegend=False,
            visible="legendonly"
        ))

    # Vẽ trực tâm
    fig.add_trace(go.Scatter(
        x=[H.x],
        y=[H.y],
        mode="markers",
        marker=dict(size=10, symbol="x"),
        name="Đường cao",
        legendgroup="altitude",
        visible="legendonly"
    ))




    # =========================
    # 4️⃣ PHÂN GIÁC
    # =========================
    for vertex, foot in [
        (A, incircle["feet"]["A_feet"]),
        (B, incircle["feet"]["B_feet"]),
        (C, incircle["feet"]["C_feet"]),
    ]:
        fig.add_trace(go.Scatter(
            x=[vertex.x, foot.x],
            y=[vertex.y, foot.y],
            mode="lines",
            line=dict(dash="dot", width=1.5),
            legendgroup="bisector",
            name="Phân giác",
            showlegend=False,
            visible="legendonly"
        ))

    I = incircle["intersect"]
    fig.add_trace(go.Scatter(
        x=[I.x],
        y=[I.y],
        mode="markers",
        marker=dict(size=10, symbol="x"),
        name="Tâm nội tiếp",
        legendgroup="bisector",
        visible="legendonly"
    ))

    r = incircle["radius"]
    I = incircle["intersect"]
    theta = np.linspace(0, 2*np.pi, 200)

    fig.add_trace(go.Scatter(
        x=I.x + r*np.cos(theta),
        y=I.y + r*np.sin(theta),
        mode="lines",
        name="Đường tròn nội tiếp",
        legendgroup="incircle",
        visible="legendonly"
    ))




    # =========================
    # 5️⃣ TRUNG TRỰC
    # =========================
    for line in circum["lines"]:   # bạn tự build list này
        fig.add_trace(go.Scatter(
            x=line["x"],
            y=line["y"],
            mode="lines",
            line=dict(dash="dot", width=1.5),
            legendgroup="perp_bisector",
            name="Trung trực",
            showlegend=False,
            visible="legendonly"
        ))

    O = circum["intersect"]
    fig.add_trace(go.Scatter(
        x=[O.x],
        y=[O.y],
        mode="markers",
        marker=dict(size=10, symbol="x"),
        name="Tâm ngoại tiếp",
        legendgroup="perp_bisector",
        visible="legendonly"
    ))

    R = circum["radius"]
    O = circum["intersect"]
    theta = np.linspace(0, 2*np.pi, 200)

    fig.add_trace(go.Scatter(
        x=O.x + R*np.cos(theta),
        y=O.y + R*np.sin(theta),
        mode="lines",
        name="Đường tròn ngoại tiếp",
        legendgroup="circumcircle",
        visible="legendonly"
    ))




    # =========================
    # LAYOUT
    # =========================
    padding = 1

    min_x = min(A.x, B.x, C.x, O.x, I.x, G.x, H.x)
    max_x = max(A.x, B.x, C.x, O.x, I.x, G.x, H.x)
    min_y = min(A.y, B.y, C.y, O.y, I.y, G.y, H.y)
    max_y = max(A.y, B.y, C.y, O.y, I.y, G.y, H.y)

    width = max(max_x - min_x, max_y - min_y)

    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2

    half = width / 2 + padding

    # =========================
    # 6️⃣ ĐƯỜNG THẲNG EULER
    # =========================

    # Nếu không phải tam giác đều (3 điểm trùng nhau)
    if not (G == H and H == O):

        # Lấy 2 điểm phân biệt trong 3 điểm
        points = [O, G, H]
        unique_points = []

        for p in points:
            if not any(p == q for q in unique_points):
                unique_points.append(p)

        # Đảm bảo có ít nhất 2 điểm khác nhau
        if len(unique_points) >= 2:
            P1 = unique_points[0]
            P2 = unique_points[1]

            # Vector chỉ phương
            dx = P2.x - P1.x
            dy = P2.y - P1.y

            norm = np.hypot(dx, dy)

            if norm != 0:
                dx /= norm
                dy /= norm

                # Kéo dài ra hai phía theo bounding box
                scale = half * 2

                x_vals = [
                    P1.x - dx * scale,
                    P1.x + dx * scale
                ]
                y_vals = [
                    P1.y - dy * scale,
                    P1.y + dy * scale
                ]

                fig.add_trace(go.Scatter(
                    x=x_vals,
                    y=y_vals,
                    mode="lines",
                    line=dict(width=2),
                    name="Đường thẳng Euler",
                    legendgroup="euler",
                    visible="legendonly"
                ))


    fig.update_layout(
        xaxis=dict(range=[center_x - half, center_x + half], scaleanchor="y", scaleratio=1),
        yaxis=dict(range=[center_y - half, center_y + half]),
        showlegend=True,
        height=600,

        legend=dict(
            orientation="h",      # nằm ngang
            yanchor="top",
            y=-0.15,              # đẩy xuống dưới
            xanchor="center",
            x=0.5                 # căn giữa
        ),

        margin=dict(b=120)       # tăng margin dưới để không bị cắt
    )

    return fig
