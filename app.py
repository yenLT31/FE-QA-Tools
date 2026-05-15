import streamlit as st
import json
import os

# ============================================================
#  LOAD TOOLS TỪ config/tools.json
# ============================================================
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "tools.json")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    TOOLS = json.load(f)

# Tự động gán page path
for t in TOOLS:
    t["page"] = f"pages/{t['id']}.py"

# ============================================================
#  PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="FPT QA Tools",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
#  THEME
# ============================================================
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

DARK = dict(
    bg="#080D18", card="#0F1628", card2="#162040", border="#1E2D4A",
    text="#E8EDF5", muted="#8892A4", accent="#00D4AA", accent_dim="#00A882",
    green="#22C55E", gbg="#052E16", gtxt="#22C55E",
    red="#EF4444", rbg="#1C1012", rtxt="#F87171",
    blue="#3B82F6", bbg="#0C1529", btxt="#60A5FA",
    yellow="#EAB308", ybg="#1A1800", ytxt="#FACC15",
)
LIGHT = dict(
    bg="#F0F4F8", card="#FFFFFF", card2="#F7F9FC", border="#E2E8F0",
    text="#1A2540", muted="#64748B", accent="#0A9E7F", accent_dim="#077A62",
    green="#16A34A", gbg="#DCFCE7", gtxt="#15803D",
    red="#DC2626", rbg="#FEF2F2", rtxt="#DC2626",
    blue="#2563EB", bbg="#EFF6FF", btxt="#1D4ED8",
    yellow="#CA8A04", ybg="#FEFCE8", ytxt="#A16207",
)
T = DARK if st.session_state.theme == "dark" else LIGHT

# ============================================================
#  FONT + CSS
# ============================================================
st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">',
    unsafe_allow_html=True,
)

st.markdown(f"""<style>
/* ── Global ── */
.stApp {{ background: {T['bg']} !important; }}
header[data-testid="stHeader"] {{
    background: transparent !important;
    border-bottom: none !important;
    height: 2.875rem !important;
    overflow: visible !important;
}}
.block-container {{
    padding-top: 0 !important;
    max-width: 1200px !important;
}}
[data-testid="stSidebarNav"] {{ display: none !important; }}
[data-testid="stSidebar"] {{
    background: {T['card']} !important;
    border-right: 1px solid {T['border']} !important;
}}

/* ── Typography ── */
.stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
.stMarkdown li, .stMarkdown span, label {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: {T['text']} !important;
}}

/* ── Buttons ── */
.stButton > button {{
    background: {T['accent']} !important;
    color: #080D18 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 22px !important;
    transition: all .2s !important;
}}
.stButton > button:hover {{
    background: {T['accent_dim']} !important;
    transform: translateY(-1px) !important;
}}

/* ── Page links (card style) ── */
a[data-testid="stPageLink-NavLink"] {{
    background: {T['card']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 14px !important;
    padding: 16px 20px !important;
    transition: all 0.25s ease !important;
    text-decoration: none !important;
    display: flex !important;
    align-items: center !important;
    min-height: 72px !important;
}}
a[data-testid="stPageLink-NavLink"]:hover {{
    border-color: {T['accent']} !important;
    background: {T['card2']} !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px {T['accent']}18 !important;
}}
a[data-testid="stPageLink-NavLink"] p {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    color: {T['text']} !important;
    margin: 0 !important;
}}

/* ── Sidebar page links (keep simple) ── */
[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] {{
    background: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 6px 10px !important;
    min-height: auto !important;
}}
[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"]:hover {{
    background: {T['card2']} !important;
    transform: none !important;
    box-shadow: none !important;
}}
</style>""", unsafe_allow_html=True)

# ============================================================
#  SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(f"""
    <div style="padding:16px 0 20px;border-bottom:1px solid {T['border']};margin-bottom:20px">
        <div style="font-size:15px;font-weight:800;color:{T['accent']};
                    font-family:'Plus Jakarta Sans',sans-serif">🔧 FPT QA Tools</div>
        <div style="font-size:10px;color:{T['muted']};font-weight:600;letter-spacing:.9px;
                    text-transform:uppercase;margin-top:3px;font-family:'Plus Jakarta Sans',sans-serif">
            QA Department — FE</div>
    </div>
    <p style="font-size:10px;color:{T['muted']};font-weight:700;letter-spacing:.9px;
              text-transform:uppercase;margin-bottom:8px;font-family:'Plus Jakarta Sans',sans-serif">
        Giao diện</p>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("☀ Sáng", use_container_width=True, key="btn_light"):
            st.session_state.theme = "light"; st.rerun()
    with c2:
        if st.button("🌙 Tối", use_container_width=True, key="btn_dark"):
            st.session_state.theme = "dark"; st.rerun()

    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:18px 0"></div>',
                unsafe_allow_html=True)
    st.markdown(f"""<p style="font-size:10px;color:{T['muted']};font-weight:700;letter-spacing:.9px;
              text-transform:uppercase;margin-bottom:10px;font-family:'Plus Jakarta Sans',sans-serif">
        Công cụ</p>""", unsafe_allow_html=True)

    for t in TOOLS:
        if t["status"] == "live":
            st.page_link(t["page"], label=f"{t['icon']}  {t['name']}")

    st.markdown(f"""
    <div style="height:1px;background:{T['border']};margin:18px 0"></div>
    <div style="font-size:11px;color:{T['muted']};line-height:1.7;font-family:'Plus Jakarta Sans',sans-serif">
        © 2026 YenLT31<br>FPT Education QA Department</div>
    """, unsafe_allow_html=True)

# ============================================================
#  HERO SECTION (compact)
# ============================================================
st.markdown(f"""
<div style="background:linear-gradient(160deg,{T['card']} 0%,{T['card2']} 55%,{T['bg']} 100%);
            border-bottom:1px solid {T['border']};padding:24px 0 20px;
            margin:-1rem -1rem 0;text-align:center">
    <div style="font-size:11px;color:{T['accent']};font-weight:700;letter-spacing:1.4px;
                text-transform:uppercase;margin-bottom:10px;font-family:'Plus Jakarta Sans',sans-serif">
        🔧 FPT QA Tools</div>
    <h1 style="font-size:24px;font-weight:800;color:{T['text']};letter-spacing:-.8px;
               margin:0 0 8px;line-height:1.2;font-family:'Plus Jakarta Sans',sans-serif">
        Hệ sinh thái công cụ
        <span style="color:{T['accent']}">Đảm bảo chất lượng — FE</span></h1>
    <p style="color:{T['muted']};font-size:13px;margin:0 auto;max-width:420px;
              line-height:1.6;font-family:'Plus Jakarta Sans',sans-serif">
        Chọn công cụ bên dưới để bắt đầu</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# ============================================================
#  TOOL CARDS — auto grid từ config/tools.json
# ============================================================
live_tools = [t for t in TOOLS if t["status"] == "live"]
coming_tools = [t for t in TOOLS if t["status"] == "coming"]

# ── Live tools ────────────────────────────────────────────────
if live_tools:
    # Tự động chia cột: tối đa 3 cột, tối thiểu 1
    n_cols = min(len(live_tools), 3)
    cols = st.columns(n_cols)

    for i, t in enumerate(live_tools):
        with cols[i % n_cols]:
            # Card header bằng HTML
            st.markdown(f"""
            <div style="text-align:center;margin-bottom:8px">
                <div style="width:56px;height:56px;border-radius:16px;
                            background:linear-gradient(135deg,{T['accent']}18,{T['accent']}08);
                            border:1.5px solid {T['accent']}33;
                            display:inline-flex;align-items:center;justify-content:center;
                            font-size:26px;margin-bottom:8px">{t['icon']}</div>
                <div style="font-size:11px;color:{T['muted']};line-height:1.5;
                            font-family:'Plus Jakarta Sans',sans-serif;
                            padding:0 8px;
                            display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;
                            overflow:hidden;min-height:33px">{t['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Native Streamlit link — LUÔN HOẠT ĐỘNG
            st.page_link(t["page"], label=f"  {t['name']}  →",
                         use_container_width=True)

            # Status badge
            if t["status"] == "live":
                st.markdown(f"""
                <div style="text-align:center;margin-top:6px">
                    <span style="font-size:10px;color:{T['green']};font-weight:700;
                                font-family:'Plus Jakarta Sans',sans-serif">
                        ● LIVE</span>
                </div>""", unsafe_allow_html=True)

# ── Coming soon tools ─────────────────────────────────────────
if coming_tools:
    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:24px 0 16px"></div>',
                unsafe_allow_html=True)
    st.markdown(f"""<p style="font-size:10px;color:{T['muted']};font-weight:700;letter-spacing:.9px;
              text-transform:uppercase;margin-bottom:12px;text-align:center;
              font-family:'Plus Jakarta Sans',sans-serif">Sắp ra mắt</p>""",
                unsafe_allow_html=True)

    n_cols_c = min(len(coming_tools), 3)
    cols_c = st.columns(n_cols_c)

    for i, t in enumerate(coming_tools):
        with cols_c[i % n_cols_c]:
            st.markdown(f"""
            <div style="text-align:center;opacity:0.5">
                <div style="width:56px;height:56px;border-radius:16px;
                            background:{T['card2']};border:1.5px dashed {T['border']};
                            display:inline-flex;align-items:center;justify-content:center;
                            font-size:26px;margin-bottom:8px">{t['icon']}</div>
                <div style="font-size:13px;font-weight:700;color:{T['muted']};
                            font-family:'Plus Jakarta Sans',sans-serif">{t['name']}</div>
                <div style="font-size:11px;color:{T['muted']};margin-top:4px;
                            font-family:'Plus Jakarta Sans',sans-serif">{t['desc']}</div>
                <div style="margin-top:8px">
                    <span style="font-size:10px;color:{T['yellow']};font-weight:700;
                                font-family:'Plus Jakarta Sans',sans-serif">
                        ⏳ Coming soon</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
#  SECURITY NOTE + FOOTER
# ============================================================
st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

st.markdown(f"""
<div style="background:{T['card']};border:1px solid {T['border']};border-radius:16px;
            padding:12px 20px">
    <div style="font-size:14px;font-weight:700;color:{T['text']};margin-bottom:6px;
                font-family:'Plus Jakarta Sans',sans-serif">💡 Thông tin bảo mật</div>
    <p style="color:{T['muted']};font-size:13px;line-height:1.7;margin:0;
              font-family:'Plus Jakarta Sans',sans-serif">
        Toàn bộ dữ liệu được xử lý tại trình duyệt (Local). Chúng mình không lưu trữ
        bất kỳ thông tin sinh viên nào trên server để đảm bảo an toàn dữ liệu tuyệt đối
        theo quy định của FPT Education.</p>
</div>
<div style="text-align:center;margin-top:16px">
    <span style="color:{T['muted']};font-size:12px;font-family:'Plus Jakarta Sans',sans-serif">
        © 2026 YenLT31 — FPT Education QA Department</span>
</div>
""", unsafe_allow_html=True)
