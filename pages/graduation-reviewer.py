import streamlit as st
import os

# ============================================================
#  THEME
# ============================================================
DARK = {
    "bg": "#0f172a", "card": "#1e293b", "card2": "#334155",
    "border": "#334155", "text": "#e2e8f0", "muted": "#94a3b8",
    "accent": "#10b981", "accent_hover": "#059669",
    "accent_light": "rgba(16,185,129,0.12)",
    "sidebar_bg": "#0f172a", "sidebar_border": "#1e293b",
    "input_bg": "#1e293b", "input_border": "#475569",
    "shadow": "0 1px 3px rgba(0,0,0,0.4)",
}
LIGHT = {
    "bg": "#f8fafc", "card": "#ffffff", "card2": "#f1f5f9",
    "border": "#e2e8f0", "text": "#1e293b", "muted": "#64748b",
    "accent": "#059669", "accent_hover": "#047857",
    "accent_light": "rgba(5,150,105,0.08)",
    "sidebar_bg": "#ffffff", "sidebar_border": "#e2e8f0",
    "input_bg": "#f8fafc", "input_border": "#cbd5e1",
    "shadow": "0 1px 3px rgba(0,0,0,0.06)",
}

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

T = DARK if st.session_state.theme == "dark" else LIGHT

# ============================================================
#  PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Graduation Reviewer | FE QA Tools",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
#  GOOGLE FONT + GLOBAL CSS
# ============================================================
st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">',
    unsafe_allow_html=True,
)

st.markdown(f"""
<style>
    :root {{
        --bg: {T["bg"]};
        --card: {T["card"]};
        --card2: {T["card2"]};
        --border: {T["border"]};
        --text: {T["text"]};
        --muted: {T["muted"]};
        --accent: {T["accent"]};
        --accent-hover: {T["accent_hover"]};
        --accent-light: {T["accent_light"]};
        --sidebar-bg: {T["sidebar_bg"]};
        --sidebar-border: {T["sidebar_border"]};
        --input-bg: {T["input_bg"]};
        --input-border: {T["input_border"]};
        --shadow: {T["shadow"]};
    }}

    /* ---- Ẩn menu, footer, deploy ---- */
    #MainMenu, footer, .stDeployButton,
    div[data-testid="stDecoration"] {{
        display: none !important;
    }}

    /* ---- Header trong suốt, giữ nút toggle ---- */
    header[data-testid="stHeader"] {{
        background: transparent !important;
        border: none !important;
        height: auto !important;
    }}

    /* ---- Nút toggle sidebar luôn hiển thị ---- */
    button[data-testid="stSidebarCollapseButton"],
    button[data-testid="stSidebarCollapsedControl"] {{
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        z-index: 999999 !important;
        background: {T["card"]} !important;
        border: 1px solid {T["border"]} !important;
        border-radius: 8px !important;
        width: 36px !important;
        height: 36px !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        box-shadow: {T["shadow"]} !important;
        transition: all 0.2s ease !important;
    }}

    button[data-testid="stSidebarCollapseButton"]:hover,
    button[data-testid="stSidebarCollapsedControl"]:hover {{
        background: {T["card2"]} !important;
        border-color: {T["accent"]} !important;
    }}

    button[data-testid="stSidebarCollapseButton"] svg,
    button[data-testid="stSidebarCollapsedControl"] svg {{
        fill: {T["accent"]} !important;
        stroke: {T["accent"]} !important;
        width: 18px !important;
        height: 18px !important;
    }}

    /* ---- Global ---- */
    html, body, [data-testid="stAppViewContainer"],
    .main .block-container {{
        background-color: var(--bg) !important;
        color: var(--text) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }}
    .main .block-container {{
        padding: 1rem 1rem 2rem 1rem !important;
        max-width: 100% !important;
    }}

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] {{
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid var(--sidebar-border) !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: var(--text) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }}
    section[data-testid="stSidebar"] .stMarkdown p {{
        margin-bottom: 0.3rem;
    }}

    /* ---- Ẩn sidebar nav mặc định ---- */
    section[data-testid="stSidebar"] ul[data-testid="stSidebarNavItems"],
    section[data-testid="stSidebar"] nav[data-testid="stSidebarNav"],
    [data-testid="stSidebarNav"] {{
        display: none !important;
    }}

    /* ---- Buttons ---- */
    .stButton > button {{
        background-color: var(--accent) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        transition: background-color 0.2s ease;
    }}
    .stButton > button:hover {{
        background-color: var(--accent-hover) !important;
    }}

    /* ---- iframe ---- */
    iframe {{
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
    }}

    /* ---- Scrollbar ---- */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{
        background: {T["border"]};
        border-radius: 3px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: {T["muted"]};
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================
#  SIDEBAR
# ============================================================
with st.sidebar:

    # ---------- Logo & Title ----------
    st.markdown(f"""
    <div style="
        display:flex; align-items:center; gap:12px;
        padding:8px 0 16px 0; border-bottom:1px solid {T['border']};
        margin-bottom:20px;">
        <div style="
            width:40px; height:40px; border-radius:12px;
            background:linear-gradient(135deg, {T['accent']}, #34d399);
            display:flex; align-items:center; justify-content:center;
            font-size:20px; flex-shrink:0;">
            🎓
        </div>
        <div>
            <div style="font-size:15px; font-weight:800; color:{T['text']}; line-height:1.2;">
                Graduation Reviewer
            </div>
            <div style="font-size:11px; color:{T['muted']}; font-weight:500;">
                FE Education QA Department
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- Theme toggle ----------
    st.markdown(f"""
    <div style="
        font-size:12px; font-weight:700; color:{T['muted']};
        text-transform:uppercase; letter-spacing:1px;
        margin-bottom:8px;">
        Giao diện
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("☀ Sáng", use_container_width=True,
                      type="primary" if st.session_state.theme == "light" else "secondary"):
            st.session_state.theme = "light"
            st.rerun()
    with col2:
        if st.button("🌙 Tối", use_container_width=True,
                      type="primary" if st.session_state.theme == "dark" else "secondary"):
            st.session_state.theme = "dark"
            st.rerun()

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ---------- Security info ----------
    st.markdown(f"""
    <div style="
        background: {T['accent_light']};
        border:1px solid {T['accent']}33;
        border-radius:10px; padding:14px; margin-bottom:20px;">
        <div style="font-size:13px; font-weight:700; color:{T['accent']}; margin-bottom:6px;">
            🔒 Bảo mật dữ liệu
        </div>
        <div style="font-size:12px; color:{T['muted']}; line-height:1.5;">
            Mọi dữ liệu được xử lý <strong>100% tại trình duyệt</strong> của bạn.
            Không có thông tin nào được gửi lên server.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- Hướng dẫn nhanh ----------
    st.markdown(f"""
    <div style="
        font-size:12px; font-weight:700; color:{T['muted']};
        text-transform:uppercase; letter-spacing:1px;
        margin-bottom:10px;">
        Hướng dẫn sử dụng
    </div>
    <div style="font-size:12.5px; color:{T['muted']}; line-height:1.8;">
        <div style="margin-bottom:8px;">
            <span style="
                display:inline-flex; align-items:center; justify-content:center;
                width:22px; height:22px; border-radius:6px;
                background:{T['accent']}; color:#fff;
                font-size:11px; font-weight:800; margin-right:8px;">
                1
            </span>
            Upload 5 file Excel đầu vào
        </div>
        <div style="margin-bottom:8px;">
            <span style="
                display:inline-flex; align-items:center; justify-content:center;
                width:22px; height:22px; border-radius:6px;
                background:{T['accent']}; color:#fff;
                font-size:11px; font-weight:800; margin-right:8px;">
                2
            </span>
            Nhấn "Bắt đầu rà soát"
        </div>
        <div style="margin-bottom:8px;">
            <span style="
                display:inline-flex; align-items:center; justify-content:center;
                width:22px; height:22px; border-radius:6px;
                background:{T['accent']}; color:#fff;
                font-size:11px; font-weight:800; margin-right:8px;">
                3
            </span>
            Chờ hệ thống xử lý (7 bước)
        </div>
        <div style="margin-bottom:0;">
            <span style="
                display:inline-flex; align-items:center; justify-content:center;
                width:22px; height:22px; border-radius:6px;
                background:{T['accent']}; color:#fff;
                font-size:11px; font-weight:800; margin-right:8px;">
                4
            </span>
            Xem kết quả & tải báo cáo Excel
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ---------- Files cần upload ----------
    st.markdown(f"""
    <div style="
        font-size:12px; font-weight:700; color:{T['muted']};
        text-transform:uppercase; letter-spacing:1px;
        margin-bottom:10px;">
        Files đầu vào
    </div>
    <div style="
        background: {T['card2']};
        border:1px solid {T['border']};
        border-radius:10px; padding:14px;">
        <div style="font-size:12px; color:{T['muted']}; line-height:2;">
            📋 <strong>cancheck</strong> – DS ứng viên tốt nghiệp<br>
            👤 <strong>currstudent</strong> – DS sinh viên hiện tại<br>
            📚 <strong>currsubject</strong> – DS môn học đang mở<br>
            📊 <strong>mark</strong> – Bảng điểm<br>
            🔄 <strong>replacecode</strong> – DS mã học phần thay thế
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- Quay về trang chủ ----------
    st.markdown(f"""
    <div style="height:1px;background:{T['border']};margin:20px 0 16px"></div>
    """, unsafe_allow_html=True)

    st.page_link("app.py", label="🏠  Quay về trang chủ")

    # ---------- Footer ----------
    st.markdown(f"""
    <div style="
        margin-top:24px;
        padding-top:16px;
        border-top:1px solid {T['border']};
        text-align:center;">
        <div style="font-size:11px; color:{T['muted']};">
            © 2026 <strong style="color:{T['accent']}">YenLT31</strong>
        </div>
        <div style="font-size:10px; color:{T['muted']}; margin-top:2px;">
            FE Education QA Department
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
#  MAIN – Load HTML gốc (100% không thay đổi)
# ============================================================
html_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'scripts', 'graduation-reviewer.html')
)

try:
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    st.components.v1.html(html_content, height=2000, scrolling=True)

except FileNotFoundError:
    st.error("❌ Không tìm thấy file: `scripts/graduation-reviewer.html`")
    st.info("Hãy đảm bảo file HTML nằm tại đường dẫn: `scripts/graduation-reviewer.html`")
except Exception as e:
    st.error(f"❌ Lỗi khi load HTML: `{e}`")
