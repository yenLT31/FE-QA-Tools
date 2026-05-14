import streamlit as st
import plotly.graph_objects as go
import math
import json

st.set_page_config(
    page_title="FPT QA Tools",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Theme ─────────────────────────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

DARK = dict(
    bg="#080D18", card="#0F1628", card2="#162040", border="#1E2D4A",
    text="#E8EDF5", muted="#8892A4", accent="#00D4AA", accent_dim="#00A882",
    green="#22C55E", gbg="#052E16", gtxt="#22C55E",
    plot_bg="#080D18", plot_template="plotly_dark",
)
LIGHT = dict(
    bg="#F0F4F8", card="#FFFFFF", card2="#F7F9FC", border="#E2E8F0",
    text="#1A2540", muted="#64748B", accent="#0A9E7F", accent_dim="#077A62",
    green="#16A34A", gbg="#DCFCE7", gtxt="#15803D",
    plot_bg="#F0F4F8", plot_template="plotly_white",
)
T = DARK if st.session_state.theme == "dark" else LIGHT

# ── Data ──────────────────────────────────────────────────────────────────────
TOOLS = [
    dict(
        id="graduation-reviewer",
        name="Graduation Reviewer",
        desc="Rà soát dữ liệu xét tốt nghiệp, đối chiếu GPA và điểm số theo phụ lục.",
        icon="📊", status="live",
        page="pages/graduation-reviewer.py",
        uses=150,
    ),
    dict(
        id="replacecode-manager",
        name="ReplaceCode Manager",
        desc="Quản lý và cập nhật môn thay thế / tương đương từ Quyết định PDF.",
        icon="📋", status="live",
        page="pages/replacecode-manager.py",
        uses=80,
    ),
    # Thêm tool mới vào đây:
    # dict(id="new-tool", name="Tool mới", desc="...", icon="📈",
    #      status="coming", page="pages/new-tool.py", uses=0),
]

RELATIONS = [
    dict(
        from_id="graduation-reviewer",
        to_id="replacecode-manager",
        label="dùng dữ liệu",
    ),
]

# ── Tính degree & size ────────────────────────────────────────────────────────
for t in TOOLS:
    t["degree"] = sum(
        1 for r in RELATIONS
        if r["from_id"] == t["id"] or r["to_id"] == t["id"]
    )

max_deg  = max((t["degree"] for t in TOOLS), default=1)
max_uses = max((t["uses"]   for t in TOOLS), default=1)
MIN_R, MAX_R = 40, 72

for t in TOOLS:
    ds = t["degree"] / max_deg
    us = t["uses"]   / max_uses
    t["r"] = MIN_R + (ds * 0.45 + us * 0.55) * (MAX_R - MIN_R)

# ── Layout ────────────────────────────────────────────────────────────────────
n = len(TOOLS)
CX, CY = 0, 0

if n == 1:
    TOOLS[0]["x"] = CX; TOOLS[0]["y"] = CY
elif n == 2:
    TOOLS[0]["x"] = -1.8; TOOLS[0]["y"] = 0
    TOOLS[1]["x"] =  1.8; TOOLS[1]["y"] = 0
else:
    spread = 2.0
    for i, t in enumerate(TOOLS):
        angle = (i / n) * 2 * math.pi - math.pi / 2
        t["x"] = spread * math.cos(angle)
        t["y"] = spread * math.sin(angle)

# ── Fonts + CSS ───────────────────────────────────────────────────────────────
st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">',
    unsafe_allow_html=True
)
st.markdown(f"""<style>:root{{
--bg:{T['bg']};--card:{T['card']};--card2:{T['card2']};--border:{T['border']};
--text:{T['text']};--muted:{T['muted']};--accent:{T['accent']};--adim:{T['accent_dim']};
--green:{T['green']};--gbg:{T['gbg']};--gtxt:{T['gtxt']};
}}</style>""", unsafe_allow_html=True)

st.markdown("""<style>
.stApp { background: var(--bg) !important; }
header[data-testid="stHeader"] { background: transparent !important; border-bottom: none !important; height: 0 !important; min-height: 0 !important; overflow: visible !important; }
.block-container { padding-top: 0 !important; max-width: 1300px !important; }
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebar"] { background: var(--card) !important; border-right: 1px solid var(--border) !important; }
.stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    font-family: 'Plus Jakarta Sans', sans-serif !important; color: var(--text) !important;
}
.stButton > button {
    background: var(--accent) !important; color: #080D18 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 700 !important;
    font-size: 14px !important; border: none !important; border-radius: 10px !important;
    padding: 10px 22px !important; transition: all .2s !important;
}
.stButton > button:hover { background: var(--adim) !important; transform: translateY(-1px) !important; }
/* Ẩn Plotly modebar */
.modebar { display: none !important; }
/* Đảm bảo nút >> mở sidebar không bị che */
section[data-testid="stMain"] { padding-left: 1rem !important; }

</style>""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:16px 0 20px;border-bottom:1px solid {T['border']};margin-bottom:20px">
        <div style="font-size:15px;font-weight:800;color:{T['accent']};
                    font-family:'Plus Jakarta Sans',sans-serif">🔧 FPT QA Tools</div>
        <div style="font-size:10px;color:{T['muted']};font-weight:600;letter-spacing:.9px;
                    text-transform:uppercase;margin-top:3px;font-family:'Plus Jakarta Sans',sans-serif">
            QA Department — FE
        </div>
    </div>
    <p style="font-size:10px;color:{T['muted']};font-weight:700;letter-spacing:.9px;
              text-transform:uppercase;margin-bottom:8px;font-family:'Plus Jakarta Sans',sans-serif">
        Giao diện
    </p>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("☀ Sáng", use_container_width=True, key="btn_light"):
            st.session_state.theme = "light"; st.rerun()
    with c2:
        if st.button("🌙 Tối", use_container_width=True, key="btn_dark"):
            st.session_state.theme = "dark"; st.rerun()

    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:18px 0"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <p style="font-size:10px;color:{T['muted']};font-weight:700;letter-spacing:.9px;
              text-transform:uppercase;margin-bottom:10px;font-family:'Plus Jakarta Sans',sans-serif">
        Công cụ
    </p>""", unsafe_allow_html=True)

    for t in TOOLS:
        if t["status"] == "live":
            st.page_link(t["page"], label=f"{t['icon']}  {t['name']}")

    st.markdown(f"""
    <div style="height:1px;background:{T['border']};margin:18px 0"></div>
    <div style="font-size:11px;color:{T['muted']};line-height:1.7;font-family:'Plus Jakarta Sans',sans-serif">
        © 2026 YenLT31<br>FPT Education QA Department
    </div>""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(160deg,{T['card']} 0%,{T['card2']} 55%,{T['bg']} 100%);
            border-bottom:1px solid {T['border']};padding:48px 0 36px;
            margin:-1rem -1rem 0;text-align:center">
    <div style="font-size:12px;color:{T['accent']};font-weight:700;letter-spacing:1.2px;
                text-transform:uppercase;margin-bottom:12px;font-family:'Plus Jakarta Sans',sans-serif">
        🔧 FPT QA Tools
    </div>
    <h1 style="font-size:36px;font-weight:800;color:{T['text']};letter-spacing:-.8px;
               margin:0 0 12px;line-height:1.2;font-family:'Plus Jakarta Sans',sans-serif">
        Hệ sinh thái công cụ<br>
        <span style="color:{T['accent']}">Đảm bảo chất lượng — FE</span>
    </h1>
    <p style="color:{T['muted']};font-size:14px;margin:0 auto;max-width:460px;
              line-height:1.7;font-family:'Plus Jakarta Sans',sans-serif">
        Các công cụ kết nối với nhau thành một hệ thống —
        click vào từng sao để khám phá.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── Plotly Constellation ──────────────────────────────────────────────────────
fig = go.Figure()

accent     = T["accent"]
muted      = T["muted"]
text_color = T["text"]
card_color = T["card"]
card2      = T["card2"]
border     = T["border"]
bg_color   = T["plot_bg"]

# Decorative background dots
import random
random.seed(42)
bg_x = [random.uniform(-4, 4) for _ in range(60)]
bg_y = [random.uniform(-2, 2) for _ in range(60)]
bg_s = [random.uniform(1, 4)  for _ in range(60)]
fig.add_trace(go.Scatter(
    x=bg_x, y=bg_y, mode="markers",
    marker=dict(
        size=bg_s,
        color=accent,
        opacity=0.12,
    ),
    hoverinfo="skip", showlegend=False
))

# Connection lines + arrow + label
for rel in RELATIONS:
    frm = next((t for t in TOOLS if t["id"] == rel["from_id"]), None)
    to  = next((t for t in TOOLS if t["id"] == rel["to_id"]),   None)
    if not frm or not to:
        continue

    # Dashed line
    fig.add_trace(go.Scatter(
        x=[frm["x"], to["x"]], y=[frm["y"], to["y"]],
        mode="lines",
        line=dict(color=accent, width=1.8, dash="dot"),
        hoverinfo="skip", showlegend=False,
        opacity=0.6,
    ))

    # Arrow annotation
    fig.add_annotation(
        x=to["x"], y=to["y"],
        ax=frm["x"], ay=frm["y"],
        axref="x", ayref="y",
        xref="x", yref="y",
        showarrow=True,
        arrowhead=2, arrowsize=1.2, arrowwidth=1.5,
        arrowcolor=accent,
        opacity=0.7,
    )

    # Midpoint label
    mx = (frm["x"] + to["x"]) / 2
    my = (frm["y"] + to["y"]) / 2 + 0.18
    fig.add_annotation(
        x=mx, y=my,
        text=f'<span style="font-size:10px;color:{muted}">{rel["label"]}</span>',
        showarrow=False,
        bgcolor=card2,
        bordercolor=border,
        borderwidth=1,
        borderpad=4,
        opacity=0.92,
        font=dict(size=10, color=muted, family="Plus Jakarta Sans"),
    )

# Tool nodes
for t in TOOLS:
    r     = t["r"]
    color = accent if t["status"] == "live" else muted
    alpha = 1.0    if t["status"] == "live" else 0.5

    # Outer halo
    fig.add_trace(go.Scatter(
        x=[t["x"]], y=[t["y"]],
        mode="markers",
        marker=dict(
            size=r * 2.6,
            color=color,
            opacity=0.08,
            line=dict(width=0),
        ),
        hoverinfo="skip", showlegend=False,
    ))

    # Main circle (ring)
    fig.add_trace(go.Scatter(
        x=[t["x"]], y=[t["y"]],
        mode="markers",
        marker=dict(
            size=r * 2,
            color=card_color,
            opacity=alpha,
            line=dict(color=color, width=2.5),
        ),
        hoverinfo="skip", showlegend=False,
    ))

    # Hover node (invisible, carries tooltip + click)
    tooltip = (
        f"<b style='font-family:Plus Jakarta Sans;color:{text_color}'>{t['name']}</b><br>"
        f"<span style='font-size:12px;color:{muted};font-family:Plus Jakarta Sans'>{t['desc']}</span><br>"
        f"<span style='color:{accent};font-size:11px'>● LIVE</span>"
        if t["status"] == "live" else
        f"<b>{t['name']}</b><br>Sắp ra mắt"
    )
    fig.add_trace(go.Scatter(
        x=[t["x"]], y=[t["y"]],
        mode="markers+text",
        name=t["id"],
        marker=dict(size=r * 1.9, color="rgba(0,0,0,0)", opacity=0.01),
        text=[t["icon"]],
        textposition="middle center",
        textfont=dict(size=int(r * 0.55), family="Plus Jakarta Sans"),
        hovertemplate=tooltip + "<extra></extra>",
        customdata=[[t["page"], t["name"]]],
        showlegend=False,
    ))

    # Name label below
    fig.add_annotation(
        x=t["x"], y=t["y"] - r / 55 - 0.52,
        text=f'<b style="font-family:Plus Jakarta Sans;font-size:13px;color:{text_color}">{t["name"]}</b>',
        showarrow=False,
        font=dict(size=13, color=text_color, family="Plus Jakarta Sans"),
    )

    # Live dot
    if t["status"] == "live":
        fig.add_trace(go.Scatter(
            x=[t["x"] + r / 95 + 0.35],
            y=[t["y"] + r / 95 + 0.35],
            mode="markers",
            marker=dict(size=9, color=T["green"], opacity=0.9,
                        line=dict(color=card_color, width=1.5)),
            hoverinfo="skip", showlegend=False,
        ))

# Layout
fig.update_layout(
    template=T["plot_template"],
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=20, t=20, b=20),
    height=380,
    xaxis=dict(visible=False, range=[-4, 4]),
    yaxis=dict(visible=False, range=[-2, 2], scaleanchor="x", scaleratio=1),
    dragmode=False,
    hoverlabel=dict(
        bgcolor=T["card"],
        bordercolor=accent,
        font=dict(family="Plus Jakarta Sans", size=13, color=text_color),
    ),
)

# ── Render + Handle click ──────────────────────────────────────────────────────
clicked = st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False, "scrollZoom": False},
    on_select="rerun",
    key="constellation",
)

# Xử lý click chuyển trang
if clicked and clicked.get("selection") and clicked["selection"].get("points"):
    pts = clicked["selection"]["points"]
    for pt in pts:
        curve = pt.get("curve_number", -1)
        # Tìm trace nào là hover node (có customdata)
        cd = pt.get("customdata")
        if cd and len(cd) > 0:
            page_path = cd[0]
            st.switch_page(page_path)

# ── Security note ─────────────────────────────────────────────────────────────
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
st.markdown(f"""
<div style="background:{T['card']};border:1px solid {T['border']};border-radius:16px;padding:20px 26px">
    <div style="font-size:14px;font-weight:700;color:{T['text']};margin-bottom:6px;
                font-family:'Plus Jakarta Sans',sans-serif">💡 Thông tin bảo mật</div>
    <p style="color:{T['muted']};font-size:13px;line-height:1.7;margin:0;
              font-family:'Plus Jakarta Sans',sans-serif">
        Toàn bộ dữ liệu được xử lý tại trình duyệt (Local). Chúng mình không lưu trữ
        bất kỳ thông tin sinh viên nào trên server để đảm bảo an toàn dữ liệu tuyệt đối
        theo quy định của FPT Education.
    </p>
</div>
<div style="height:32px"></div>
<div style="text-align:center">
    <span style="color:{T['muted']};font-size:12px;font-family:'Plus Jakarta Sans',sans-serif">
        © 2026 YenLT31 — FPT Education QA Department
    </span>
</div>
<div style="height:20px"></div>
""", unsafe_allow_html=True)
