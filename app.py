import streamlit as st
import json
import os

# ============================================================
#  LOAD TOOLS TỪ config/tools.json
# ============================================================
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "tools.json")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    TOOLS = json.load(f)

for t in TOOLS:
    t["page"] = f"pages/{t['id']}.py"

# ============================================================
#  PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="FE QA Tools",
    page_icon="🛠",
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
    green="#22C55E", gbg="#0A2618", gtxt="#22C55E",
    yellow="#EAB308", ybg="#1A1800", ytxt="#FACC15",
)
LIGHT = dict(
    bg="#F0F4F8", card="#FFFFFF", card2="#F7F9FC", border="#E2E8F0",
    text="#1A2540", muted="#64748B", accent="#0A9E7F", accent_dim="#077A62",
    green="#16A34A", gbg="#DCFCE7", gtxt="#15803D",
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
    max-width: 1100px !important;
}}
[data-testid="stSidebarNav"] {{ display: none !important; }}
[data-testid="stSidebar"] {{
    background: {T['card']} !important;
    border-right: 1px solid {T['border']} !important;
}}

/* ── Typography ── */
*, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
.stMarkdown li, .stMarkdown span, label {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}}
.stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
.stMarkdown li, .stMarkdown span, label {{
    color: {T['text']} !important;
}}

/* ── Sidebar buttons ── */
.stButton > button {{
    background: {T['accent']} !important;
    color: #080D18 !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 8px 18px !important;
    transition: all .2s !important;
}}
.stButton > button:hover {{
    background: {T['accent_dim']} !important;
}}

/* ── Tool card container ── */
div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > div > div > [data-testid="stPageLink-NavLink"]) {{
    background: {T['card']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 16px !important;
    padding: 20px 16px 14px !important;
    transition: all 0.3s ease !important;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > div > div > [data-testid="stPageLink-NavLink"]):hover {{
    border-color: {T['accent']} !important;
    box-shadow: 0 8px 32px {T['accent']}15 !important;
    transform: translateY(-3px) !important;
}}

/* ── Page link inside card ── */
a[data-testid="stPageLink-NavLink"] {{
    background: {T['accent']} !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    transition: all 0.2s !important;
    justify-content: center !important;
}}
a[data-testid="stPageLink-NavLink"]:hover {{
    background: {T['accent_dim']} !important;
    transform: none !important;
    box-shadow: none !important;
}}
a[data-testid="stPageLink-NavLink"] p {{
    color: #080D18 !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    text-align: center !important;
}}

/* ── Sidebar page links (simple) ── */
[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] {{
    background: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 6px 10px !important;
    justify-content: flex-start !important;
}}
[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"]:hover {{
    background: {T['card2']} !important;
}}
[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] p {{
    color: {T['text']} !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    text-align: left !important;
}}
</style>""", unsafe_allow_html=True)

# ============================================================
#  SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(f"""
    <div style="padding:16px 0 20px;border-bottom:1px solid {T['border']};margin-bottom:20px">
        <div style="font-size:15px;font-weight:800;color:{T['accent']}">🔧 FE QA Tools</div>
        <div style="font-size:10px;color:{T['muted']};font-weight:600;letter-spacing:.9px;
                    text-transform:uppercase;margin-top:3px">QA Department — FE</div>
    </div>
    <p style="font-size:10px;color:{T['muted']};font-weight:700;letter-spacing:.9px;
              text-transform:uppercase;margin-bottom:8px">Giao diện</p>
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
              text-transform:uppercase;margin-bottom:10px">Công cụ</p>""",
                unsafe_allow_html=True)

    for t in TOOLS:
        if t["status"] == "live":
            st.page_link(t["page"], label=f"{t['icon']}  {t['name']}")

    st.markdown(f"""
    <div style="height:1px;background:{T['border']};margin:18px 0"></div>
    <div style="font-size:11px;color:{T['muted']};line-height:1.7">
        © 2026 YenLT31<br>FPT Education QA Department</div>
    """, unsafe_allow_html=True)

# ============================================================
#  HERO
# ============================================================
st.markdown(f"""
<div style="background:linear-gradient(160deg,{T['card']} 0%,{T['card2']} 55%,{T['bg']} 100%);
            border-bottom:1px solid {T['border']};padding:28px 0 22px;
            margin:-1rem -1rem 0;text-align:center">
    <div style="font-size:11px;color:{T['accent']};font-weight:700;letter-spacing:1.4px;
                text-transform:uppercase;margin-bottom:10px">🔧 FE QA Tools</div>
    <h1 style="font-size:24px;font-weight:800;color:{T['text']};letter-spacing:-.8px;
               margin:0 0 8px;line-height:1.3">
        Hệ sinh thái công cụ
        <span style="color:{T['accent']}">Đảm bảo chất lượng — FE</span></h1>
    <p style="color:{T['muted']};font-size:13px;margin:0 auto;max-width:400px;line-height:1.6">
        Chọn công cụ bên dưới để bắt đầu</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

# ============================================================
#  TOOL CARDS
# ============================================================
live_tools = [t for t in TOOLS if t["status"] == "live"]
coming_tools = [t for t in TOOLS if t["status"] == "coming"]

if live_tools:
    n_cols = min(len(live_tools), 3)
    cols = st.columns(n_cols, gap="medium")

    for i, t in enumerate(live_tools):
        with cols[i % n_cols]:
            with st.container(border=True):
                # Row 1: Icon + Badge
                st.markdown(f"""
                <div style="display:flex;align-items:flex-start;justify-content:space-between;
                            margin-bottom:14px">
                    <div style="width:48px;height:48px;border-radius:12px;
                                background:linear-gradient(135deg,{T['accent']}20,{T['accent']}08);
                                border:1.5px solid {T['accent']}30;
                                display:flex;align-items:center;justify-content:center;
                                font-size:22px">{t['icon']}</div>
                    <span style="font-size:10px;font-weight:700;color:{T['green']};
                                 background:{T['gbg']};padding:3px 10px;border-radius:20px;
                                 letter-spacing:.5px">● LIVE</span>
                </div>
                """, unsafe_allow_html=True)

                # Row 2: Name
                st.markdown(f"""
                <div style="font-size:15px;font-weight:800;color:{T['text']};
                            margin-bottom:6px;line-height:1.3">{t['name']}</div>
                """, unsafe_allow_html=True)

                # Row 3: Description
                st.markdown(f"""
                <div style="font-size:12px;color:{T['muted']};line-height:1.6;
                            margin-bottom:16px;min-height:38px;
                            display:-webkit-box;-webkit-line-clamp:2;
                            -webkit-box-orient:vertical;overflow:hidden">{t['desc']}</div>
                """, unsafe_allow_html=True)

                # Row 4: Link button
                st.page_link(t["page"], label=f"Mở {t['name']}  →",
                             use_container_width=True)

# ── Coming soon ───────────────────────────────────────────────
if coming_tools:
    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:20px 0 16px"></div>',
                unsafe_allow_html=True)
    st.markdown(f"""<p style="font-size:10px;color:{T['muted']};font-weight:700;letter-spacing:.9px;
              text-transform:uppercase;margin-bottom:12px;text-align:center">Sắp ra mắt</p>""",
                unsafe_allow_html=True)

    n_cols_c = min(len(coming_tools), 3)
    cols_c = st.columns(n_cols_c, gap="medium")

    for i, t in enumerate(coming_tools):
        with cols_c[i % n_cols_c]:
            with st.container(border=True):
                st.markdown(f"""
                <div style="opacity:0.5">
                    <div style="display:flex;align-items:flex-start;justify-content:space-between;
                                margin-bottom:14px">
                        <div style="width:48px;height:48px;border-radius:12px;
                                    background:{T['card2']};border:1.5px dashed {T['border']};
                                    display:flex;align-items:center;justify-content:center;
                                    font-size:22px">{t['icon']}</div>
                        <span style="font-size:10px;font-weight:700;color:{T['yellow']};
                                     background:{T['ybg']};padding:3px 10px;border-radius:20px;
                                     letter-spacing:.5px">⏳ Soon</span>
                    </div>
                    <div style="font-size:15px;font-weight:800;color:{T['muted']};
                                margin-bottom:6px">{t['name']}</div>
                    <div style="font-size:12px;color:{T['muted']};line-height:1.6;
                                min-height:38px">{t['desc']}</div>
                </div>
                """, unsafe_allow_html=True)

# ============================================================
#  SECURITY + FOOTER
# ============================================================
st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

st.markdown(f"""
<div style="background:{T['card']};border:1px solid {T['border']};border-radius:16px;
            padding:14px 20px">
    <div style="font-size:14px;font-weight:700;color:{T['text']};margin-bottom:6px">
        💡 Thông tin bảo mật</div>
    <p style="color:{T['muted']};font-size:12px;line-height:1.7;margin:0">
        Toàn bộ dữ liệu được xử lý tại trình duyệt (Local). Chúng mình không lưu trữ
        bất kỳ thông tin sinh viên nào trên server để đảm bảo an toàn dữ liệu tuyệt đối
        theo quy định của FPT Education.</p>
</div>
<div style="text-align:center;margin-top:14px">
    <span style="color:{T['muted']};font-size:11px">
        © 2026 YenLT31 — FPT Education QA Department</span>
</div>
""", unsafe_allow_html=True)
