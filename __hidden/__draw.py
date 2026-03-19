import numpy as np
import plotly.graph_objects as go
from models.triangle import TriangleWithCoords


def _draw_default():
    fig = go.Figure()
    
    fig.update_layout(
        # Thiết lập tọa độ mặc định (ví dụ từ -10 đến 10)
        xaxis=dict(
            range=[-10, 10],
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.03)',
            zerolinecolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color="#94a3b8"),
            scaleanchor="y",
        ),
        yaxis=dict(
            range=[-10, 10],
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.03)',
            zerolinecolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color="#94a3b8"),
        ),
        
        # Nhuộm đen tuyệt đối
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        
        height=600,
        margin=dict(l=20, r=20, t=20, b=20),
        
        # Chữ hiển thị khi chưa có dữ liệu
        annotations=[{
            "text": "Vui lòng nhập tọa độ để phân tích",
            "xref": "paper", "yref": "paper",
            "showarrow": False,
            "font": {"size": 16, "color": "#94a3b8"}
        }]
    )
    return fig



def _draw_triangle(x1, y1, x2, y2, x3, y3):
    """
    Vẽ đồ thị tam giác tương tác bằng Plotly, bao gồm các đường đặc biệt.

    Args:
    - x1, y1, x2, y2, x3, y3: Tọa độ 3 đỉnh A, B, C
    
    Các thành phần hỗ trợ:
    - Đường trung tuyến & Trọng tâm (G)
    - Đường cao & Trực tâm (H)
    - Đường phân giác & Tâm nội tiếp (I)
    - Đường trung trực & Tâm ngoại tiếp (O)
    - Đường thẳng Euler (O-G-H)
    
    Args:
        x1, y1, x2, y2, x3, y3 (float): Tọa độ 3 đỉnh.
        
    Returns:
        go.Figure: Đối tượng đồ họa Plotly đã được cấu hình Dark Mode.
    """
    tri = TriangleWithCoords(x1, y1, x2, y2, x3, y3)

    A, B, C = tri.A, tri.B, tri.C

    centroid = tri.centroid()
    orthocenter = tri.orthocenter()
    circum = tri.circumcircle()
    incircle = tri.incircle()

    G = centroid["intersect"]
    H = orthocenter["intersect"]
    O = circum["intersect"]
    I = incircle["intersect"]

    fig = go.Figure()


    # =================================
    # Helper: vẽ circle
    # =================================

    def draw_circle(center, r, name, group):

        theta = np.linspace(0, 2*np.pi, 200)

        fig.add_trace(go.Scatter(
            x=center.x + r*np.cos(theta),
            y=center.y + r*np.sin(theta),
            mode="lines",
            name=name,
            legendgroup=group,
            visible="legendonly"
        ))


    # =================================
    # 1 TRIANGLE
    # =================================

    fig.add_trace(go.Scatter(
        x=[A.x, B.x, C.x, A.x],
        y=[A.y, B.y, C.y, A.y],
        mode="lines+markers+text",
        text=["A","B","C",""],
        textposition="top center",
        line=dict(width=3),
        name="Tam giác",
        showlegend=False
    ))


    # =================================
    # 2 MEDIAN
    # =================================

    for v, f in [

        (A, centroid["feet"]["A_feet"]),
        (B, centroid["feet"]["B_feet"]),
        (C, centroid["feet"]["C_feet"])

    ]:

        fig.add_trace(go.Scatter(
            x=[v.x,f.x],
            y=[v.y,f.y],
            mode="lines",
            line=dict(dash="dot"),
            legendgroup="median",
            name="Trung tuyến",
            showlegend=False,
            visible="legendonly"
        ))

    fig.add_trace(go.Scatter(
        x=[G.x],
        y=[G.y],
        mode="markers",
        marker=dict(size=10),
        legendgroup="median",
        name="Trọng tâm",
        text=["G"],
        visible="legendonly"
    ))


    # =================================
    # 3 ALTITUDE
    # =================================
    for i, (v, f, side_start) in enumerate([
        (A, orthocenter["feet"]["A_feet"], B), 
        (B, orthocenter["feet"]["B_feet"], A), 
        (C, orthocenter["feet"]["C_feet"], B)
    ]):
        fig.add_trace(go.Scatter(
            x=[v.x, f.x, H.x], y=[v.y, f.y, H.y],
            mode="lines",
            line=dict(dash="dot", color="#f472b6", width=1),
            legendgroup="altitude", 
            name="Trực tâm (H)",
            showlegend=False,
            visible="legendonly"
        ))

        if f != v:
            fig.add_trace(go.Scatter(
                x=[side_start.x, f.x], y=[side_start.y, f.y],
                mode="lines",
                line=dict(dash="longdash", color="rgba(244, 114, 182, 0.2)"),
                legendgroup="altitude",
                showlegend=False,
                visible="legendonly"
            ))

    fig.add_trace(go.Scatter(
        x=[H.x], y=[H.y],
        mode="markers+text",
        text=["H"], textposition="bottom right",
        marker=dict(size=12, color="#f472b6", symbol="circle"),
        legendgroup="altitude", 
        name="Trực tâm",
        showlegend=True, 
        visible="legendonly"
    ))


    # =================================
    # 4 BISECTOR
    # =================================

    for v,f in [

        (A, incircle["feet"]["A_feet"]),
        (B, incircle["feet"]["B_feet"]),
        (C, incircle["feet"]["C_feet"])

    ]:

        fig.add_trace(go.Scatter(
            x=[v.x,f.x],
            y=[v.y,f.y],
            mode="lines",
            line=dict(dash="dot"),
            legendgroup="bisector",
            name="Phân giác",
            showlegend=False,
            visible="legendonly"
        ))

    fig.add_trace(go.Scatter(
        x=[I.x],
        y=[I.y],
        mode="markers",
        legendgroup="bisector",
        name="Tâm nội tiếp",
        text=["I"],
        visible="legendonly"
    ))

    draw_circle(I, incircle["radius"], "Nội tiếp", "bisector")


    # =================================
    # 5 PERP BISECTOR
    # =================================

    for line in circum["lines"]:

        fig.add_trace(go.Scatter(
            x=line["x"],
            y=line["y"],
            mode="lines",
            line=dict(dash="dot"),
            legendgroup="perp",
            name="Trung trực",
            showlegend=False,
            visible="legendonly"
        ))

    fig.add_trace(go.Scatter(
        x=[O.x],
        y=[O.y],
        mode="markers",
        legendgroup="perp",
        name="Tâm ngoại tiếp",
        text=["O"],
        visible="legendonly"
    ))

    draw_circle(O, circum["radius"], "Ngoại tiếp", "perp")


    # =================================
    # 6 EULER LINE (GỌN HƠN)
    # =================================

    pts = [O,G,H]

    uniq=[]

    for p in pts:
        if not any(p==q for q in uniq):
            uniq.append(p)

    if len(uniq)>=2:

        P1,P2 = uniq[:2]

        dx=P2.x-P1.x
        dy=P2.y-P1.y

        L=np.hypot(dx,dy)

        if L>0:

            dx/=L
            dy/=L

            scale=50

            fig.add_trace(go.Scatter(

                x=[P1.x-dx*scale,P1.x+dx*scale],
                y=[P1.y-dy*scale,P1.y+dy*scale],

                mode="lines",

                name="Euler",
                legendgroup="euler",
                visible="legendonly"

            ))



    # =================================
    # 7 AUTO SCALE (PHIÊN BẢN ƯU TIÊN ĐƯỜNG TRÒN)
    # =================================

    # 1. Nhóm các điểm chính (Đỉnh tam giác)
    core_pts = [A, B, C]
    c_xs = [p.x for p in core_pts]
    c_ys = [p.y for p in core_pts]
    
    # 2. Tính toán biên độ của tam giác
    tri_w = max(c_xs) - min(c_xs)
    tri_h = max(c_ys) - min(c_ys)
    tri_size = max(tri_w, tri_h)

    # 3. Tính toán vùng bao phủ mong muốn (Bao gồm cả đường tròn ngoại tiếp)
    # Ta lấy tâm O và cộng thêm bán kính R để đảm bảo đường tròn không bị cắt
    # circum["radius"] là R, O là tâm
    R = circum["radius"]
    all_visible_xs = c_xs + [O.x - R, O.x + R, I.x, G.x, H.x]
    all_visible_ys = c_ys + [O.y - R, O.y + R, I.y, G.y, H.y]

    # 4. CHỐNG "CHOÁNG": Giới hạn độ giãn nở
    # Nếu đường tròn quá lớn (vượt quá 3 lần tam giác), ta sẽ cap lại để tam giác không quá bé
    limit_factor = 3.0 
    max_allowed_size = tri_size * limit_factor

    minx, maxx = min(all_visible_xs), max(all_visible_xs)
    miny, maxy = min(all_visible_ys), max(all_visible_ys)

    # Tính toán Center và Size tạm thời
    temp_cx = (minx + maxx) / 2
    temp_cy = (miny + maxy) / 2
    temp_size = max(maxx - minx, maxy - miny) / 2

    # Áp dụng giới hạn
    final_size = min(temp_size, max_allowed_size / 2)
    # Nếu bị giới hạn, ta ưu tiên tập trung vào tâm của tam giác thay vì tâm của đường tròn khổng lồ
    if temp_size > final_size:
        cx = sum(c_xs) / 3
        cy = sum(c_ys) / 3
    else:
        cx, cy = temp_cx, temp_cy

    # Thêm chút padding cho thoáng
    final_size *= 1.1 

    # 5. Tính toán bước chia lưới (dtick) đồng nhất
    if final_size > 0:
        exponent = np.floor(np.log10(final_size))
        base = 10 ** exponent
        if final_size / base < 2: step = base / 2
        elif final_size / base < 5: step = base
        else: step = base * 2
    else:
        step = 1

    fig.update_layout(
        xaxis=dict(
            range=[cx - final_size, cx + final_size],
            dtick=step,
            tick0=0,
            gridcolor='rgba(255, 255, 255, 0.03)',
            zerolinecolor='rgba(255, 255, 255, 0.1)',
            scaleanchor="y",
            scaleratio=1,
            constrain="domain",
        ),
        yaxis=dict(
            range=[cy - final_size, cy + final_size],
            dtick=step,
            tick0=0,
            gridcolor='rgba(255, 255, 255, 0.03)',
            zerolinecolor='rgba(255, 255, 255, 0.1)',
            constrain="domain",
        ),
        width=700,
        height=700,
        dragmode="pan",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=40, b=40),
    )

    return fig