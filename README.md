# 📐 Triangle Analyzer with Plotly Dash

A high-precision, interactive web application for geometric triangle analysis.

---

# ✨ Key Features

Interactive Coordinates: Input vertices (A, B, C) to instantly visualize the triangle.

Special Points & Lines:

- Centroid (G) with Medians.

- Orthocenter (H) with Altitudes (including extended lines for obtuse triangles).

- Incenter (I) with Angle Bisectors and Incircle.

- Circumcenter (O) with Perpendicular Bisectors and Circumcircle.

- Euler Line: Visualizing the collinearity of O, G, and H.

Advanced Visualization:

- 1:1 Aspect Ratio: Ensures geometric shapes (like circles) are perfectly rendered without distortion.

- Smart Auto-scaling: Intelligently adjusts the viewport to keep the triangle visible while handling far-off points (like H or O in obtuse cases).

- Dark Mode UI: A clean, modern interface built with dash-bootstrap-components.

---

# 🛠 Tech Stack

Backend/Logic: Python, NumPy (for vector geometry).

Frontend: Dash, Plotly (for interactive graphing).

Styling: Dash Bootstrap Components (Slate/Dark theme).

Deployment: Render.

---

# Pictures

![]()

---

# 🚀 Installation & Running Locally

1. Clone the repo:

```bash
git clone https://github.com/mus-gramming/dash-triangle.git
cd dash-triangle
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

- With Windows: 

```bash
python run.py
```

- With Linux:

```bash
gunicorn server:server
```

Open http://127.0.0.1:5000 in your browser.

---

# About the project

This isn't just another geometry tool. This project is a deep dive into the precision of coordinate geometry. I built it to solve a common frustration: distorted shapes in web-based graphing. By implementing custom auto-scaling logic and strict aspect ratio controls, I ensured that every incircle and circumcircle is mathematically and visually perfect. It's my way of blending Information Systems logic with the elegance of Mathematics.