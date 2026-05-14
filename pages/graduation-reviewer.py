import streamlit as st
import os

# ── Theme ─────────────────────────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

DARK = dict(
    bg="#080D18", card="#0F1628", border="#1E2D4A",
    text="#E8EDF5", muted="#8892A4", accent="#00D4AA", accent_dim="#00A882",
    green="#22C55E",
    gbg="#052E16", gtxt="#22C55E",
)
LIGHT = dict(
    bg="#F0F4F8", card="#FFFFFF", border="#E2E8F0",
    text="#1A2540", muted="#64748B", accent="#0A9E7F", accent_dim="#077A62",
    green="#16A34A",
    gbg="#DCFCE7", gtxt="#15803D",
)
T = DARK if st.session_state.theme == "dark" else LIGHT

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Graduation Reviewer", page_icon="🎓", layout="wide")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">',
    unsafe_allow_html=True,
)

st.markdown(f"""<style>
:root {{
    --bg:{T['bg']};--card:{T['card']};--border:{T['border']};
    --text:{T['text']};--muted:{T['muted']};--accent:{T['accent']};
}}
.stApp {{ background: var(--bg) !important; }}
header[data-testid="stHeader"] {{ display: none !important; }}
.block-container {{ padding: 0 !important; max-width: 100% !important; }}
[data-testid="stSidebar"] {{
    background: var(--card) !important;
    border-right: 1px solid var(--border) !important;
}}
.stMarkdown p, .stMarkdown span, .stMarkdown div,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: var(--text) !important;
}}
.stButton > button {{
    background: var(--accent) !important;
    color: #080D18 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 22px !important;
    transition: all .2s !important;
}}
.stButton > button:hover {{
    background: {T['accent_dim']} !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(0,212,170,.22) !important;
}}
.stCheckbox span {{ color: var(--text) !important; font-size: 13px !important; }}
iframe {{ border: none !important; }}
</style>""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown(f"""
    <div style="padding:16px 0 20px;border-bottom:1px solid {T['border']};margin-bottom:20px">
        <div style="font-size:15px;font-weight:800;color:{T['accent']};letter-spacing:-.3px">
            🎓 Graduation
        </div>
        <div style="font-size:10px;color:{T['muted']};font-weight:600;letter-spacing:.9px;
                    text-transform:uppercase;margin-top:2px">Reviewer</div>
    </div>
    """, unsafe_allow_html=True)

    # Theme toggle
    st.markdown(f'<p style="font-size:10px;color:{T["muted"]};font-weight:700;letter-spacing:.9px;text-transform:uppercase;margin-bottom:8px">Giao diện</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("☀ Sáng", use_container_width=True, key="btn_light"):
            st.session_state.theme = "light"; st.rerun()
    with c2:
        if st.button("🌙 Tối", use_container_width=True, key="btn_dark"):
            st.session_state.theme = "dark"; st.rerun()

    # Info
    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:18px 0"></div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:10px;color:{T["muted"]};font-weight:700;letter-spacing:.9px;text-transform:uppercase;margin-bottom:10px">Thông tin</p>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:{T['gbg']};border:1px solid {T['green']}33;border-radius:10px;
                padding:9px 13px;margin-bottom:10px">
        <span style="color:{T['green']};font-size:13px;font-weight:600">● Xử lý tại Local</span>
    </div>
    <p style="color:{T['muted']};font-size:11px;line-height:1.5;margin-bottom:0">
        Toàn bộ dữ liệu được xử lý trên trình duyệt.<br>
        Không upload lên server.
    </p>
    """, unsafe_allow_html=True)

    # Hướng dẫn
    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:18px 0"></div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:10px;color:{T["muted"]};font-weight:700;letter-spacing:.9px;text-transform:uppercase;margin-bottom:10px">Hướng dẫn</p>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="color:{T['muted']};font-size:12px;line-height:1.8">
        <b style="color:{T['text']}">1.</b> Upload 5 file Excel<br>
        <b style="color:{T['text']}">2.</b> Bấm "Bắt đầu rà soát"<br>
        <b style="color:{T['text']}">3.</b> Xem kết quả & tải báo cáo
    </div>
    """, unsafe_allow_html=True)

    # Footer — dùng margin thay vì position absolute
    st.markdown(f"""
    <div style="margin-top:40px;padding-top:12px;border-top:1px solid {T['border']}">
        <p style="color:{T['muted']};font-size:10px;text-align:center;margin:0">
            © 2026 YenLT31<br>FE Education QA Department
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── Load & Embed HTML (giữ nguyên file gốc) ──────────────────────────────────
html_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "scripts", "graduation-reviewer.html")
)

try:
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    st.components.v1.html(html_content, height=2000, scrolling=True)

except FileNotFoundError:
    st.error(f"❌ Không tìm thấy file: `scripts/graduation-reviewer.html`")
    st.info("Vui lòng đảm bảo file tồn tại trong repo.")
except Exception as e:
    st.error(f"❌ Lỗi khi load HTML: `{e}`")
