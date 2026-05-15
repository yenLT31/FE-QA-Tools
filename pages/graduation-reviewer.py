import streamlit as st
import os

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

st.set_page_config(
    page_title="Graduation Reviewer | FE QA Tools",
    page_icon="QA",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DARK = dict(bg="#080D18", card="#0F1628", border="#1E2D4A",
            text="#E8EDF5", muted="#8892A4", accent="#00D4AA")
LIGHT = dict(bg="#F0F4F8", card="#FFFFFF", border="#E2E8F0",
             text="#1A2540", muted="#64748B", accent="#0A9E7F")
T = DARK if st.session_state.theme == "dark" else LIGHT

st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">',
    unsafe_allow_html=True
)

st.markdown(f"""<style>:root{{
--bg:{T['bg']};--card:{T['card']};--border:{T['border']};
--text:{T['text']};--muted:{T['muted']};--accent:{T['accent']};
}}</style>""", unsafe_allow_html=True)

st.markdown("""<style>
/* Ẩn hoàn toàn sidebar và mọi toggle của nó */
[data-testid="stSidebar"],
[data-testid="stSidebarNav"],
[data-testid="collapsedControl"] { display: none !important; }

/* Header trong suốt, giữ chiều cao để nút toggle không bị ẩn */
header[data-testid="stHeader"] {
    background: transparent !important;
    border-bottom: none !important;
    height: 2.875rem !important;
    overflow: visible !important;
}

/* Full-width, no padding */
.stApp { background: var(--bg) !important; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* Ẩn modebar plotly nếu có */
.modebar { display: none !important; }

/* iframe fill toàn bộ chiều cao còn lại */
iframe {
    border: none !important;
    border-radius: 0 !important;
    height: calc(100vh - 56px) !important;
    width: 100% !important;
    display: block !important;
}
[data-testid="stCustomComponentV1"] {
    height: calc(100vh - 56px) !important;
}
</style>""", unsafe_allow_html=True)

# ── Top nav bar ───────────────────────────────────────────────────────────────
col_back, col_title, col_theme = st.columns([1, 4, 1])

with col_back:
    st.page_link("app.py", label="← Trang chủ", icon=None)

with col_title:
    st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:center;gap:10px;
                padding:10px 0;font-family:'Plus Jakarta Sans',sans-serif">
        <span style="font-size:20px">🎓</span>
        <span style="font-size:16px;font-weight:700;color:{T['text']}">Graduation Data Reviewer</span>
        <span style="background:{T['card']};border:1px solid {T['accent']}44;
                     border-radius:20px;padding:2px 10px;font-size:11px;
                     font-weight:700;color:{T['accent']}">● LIVE</span>
    </div>
    """, unsafe_allow_html=True)

with col_theme:
    c1, c2 = st.columns(2)
    with c1:
        if st.button("☀", use_container_width=True, key="light"):
            st.session_state.theme = "light"; st.rerun()
    with c2:
        if st.button("🌙", use_container_width=True, key="dark"):
            st.session_state.theme = "dark"; st.rerun()

# ── Load HTML ─────────────────────────────────────────────────────────────────
html_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'scripts', 'graduation-reviewer.html')
)

try:
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=800, scrolling=True)
except FileNotFoundError:
    st.error("❌ Không tìm thấy file: `scripts/graduation-reviewer.html`")
except Exception as e:
    st.error(f"❌ Lỗi: `{e}`")
