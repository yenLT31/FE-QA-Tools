import streamlit as st

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
)
LIGHT = dict(
    bg="#F0F4F8", card="#FFFFFF", card2="#F7F9FC", border="#E2E8F0",
    text="#1A2540", muted="#64748B", accent="#0A9E7F", accent_dim="#077A62",
    green="#16A34A", gbg="#DCFCE7", gtxt="#15803D",
)
T = DARK if st.session_state.theme == "dark" else LIGHT

# ── Fonts ─────────────────────────────────────────────────────────────────────
st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">',
    unsafe_allow_html=True
)

# ── CSS vars ──────────────────────────────────────────────────────────────────
st.markdown(f"""<style>:root{{
--bg:{T['bg']};--card:{T['card']};--card2:{T['card2']};--border:{T['border']};
--text:{T['text']};--muted:{T['muted']};--accent:{T['accent']};--adim:{T['accent_dim']};
--green:{T['green']};--gbg:{T['gbg']};--gtxt:{T['gtxt']};
}}</style>""", unsafe_allow_html=True)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""<style>
.stApp { background: var(--bg) !important; }
header[data-testid="stHeader"] { display: none !important; }
.block-container { padding-top: 0 !important; max-width: 1300px !important; }

/* FIX 1: Ẩn Streamlit default page navigation trong sidebar */
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebar"] {
    background: var(--card) !important;
    border-right: 1px solid var(--border) !important;
}

/* Typography */
.stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown span {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: var(--text) !important;
}

/* Theme buttons */
.stButton > button {
    background: var(--accent) !important;
    color: #080D18 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 22px !important;
    transition: all .2s !important;
}
.stButton > button:hover {
    background: var(--adim) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(0,212,170,.22) !important;
}

/* FIX 3+4: Tool card hover & CTA via page_link */
[data-testid="stPageLink"] a {
    background: var(--accent) !important;
    color: #080D18 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    border-radius: 9px !important;
    padding: 9px 18px !important;
    text-decoration: none !important;
    display: inline-block !important;
    transition: all .2s !important;
    border: none !important;
    margin-top: 4px !important;
}
[data-testid="stPageLink"] a:hover {
    background: var(--adim) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(0,212,170,.25) !important;
}

/* Card hover — FIX 4 */
.qa-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    transition: border-color .25s, transform .25s, box-shadow .25s;
    height: 100%;
}
.qa-card:hover {
    border-color: var(--accent) !important;
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(0,212,170,.12);
}
</style>""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:16px 0 20px;border-bottom:1px solid {T['border']};margin-bottom:20px">
        <div style="font-size:15px;font-weight:800;color:{T['accent']};letter-spacing:-.3px;
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

    # Navigation — chỉ 1 menu duy nhất
    st.markdown(f"""
    <p style="font-size:10px;color:{T['muted']};font-weight:700;letter-spacing:.9px;
              text-transform:uppercase;margin-bottom:10px;font-family:'Plus Jakarta Sans',sans-serif">
        Công cụ
    </p>
    """, unsafe_allow_html=True)

    nav_items = [
        ("📊", "Graduation Reviewer",  "pages/graduation-reviewer.py"),
        ("📋", "ReplaceCode Manager",  "pages/replacecode-manager.py"),
    ]
    for icon, name, page in nav_items:
        st.page_link(page, label=f"{icon}  {name}")

    st.markdown(f"""
    <div style="height:1px;background:{T['border']};margin:18px 0"></div>
    <div style="font-size:11px;color:{T['muted']};line-height:1.7;
                font-family:'Plus Jakarta Sans',sans-serif">
        © 2026 YenLT31<br>FPT Education QA Department
    </div>
    """, unsafe_allow_html=True)

# ── FIX 2: Hero — full-width banner, không có border card ────────────────────
st.markdown(f"""
<div style="background:linear-gradient(160deg,{T['card']} 0%,{T['card2']} 55%,{T['bg']} 100%);
            border-bottom:1px solid {T['border']};
            padding:56px 48px 48px;margin:-1rem -1rem 0;text-align:center">
    <div style="font-size:12px;color:{T['accent']};font-weight:700;letter-spacing:1.2px;
                text-transform:uppercase;margin-bottom:14px;
                font-family:'Plus Jakarta Sans',sans-serif">
        🔧 FPT QA Tools
    </div>
    <h1 style="font-size:40px;font-weight:800;color:{T['text']};letter-spacing:-.8px;
               margin:0 0 14px;line-height:1.2;font-family:'Plus Jakarta Sans',sans-serif">
        Hệ sinh thái công cụ<br>
        <span style="color:{T['accent']}">Đảm bảo chất lượng — FE</span>
    </h1>
    <p style="color:{T['muted']};font-size:15px;margin:0 auto;max-width:500px;
              line-height:1.7;font-family:'Plus Jakarta Sans',sans-serif">
        Tập hợp các công cụ hỗ trợ QA xử lý dữ liệu đào tạo
        nhanh chóng, chính xác và tự động hóa.
    </p>
</div>
""", unsafe_allow_html=True)

# ── FIX 5: Spacing nhất quán 40px giữa các section ───────────────────────────
st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

# ── Tool cards ────────────────────────────────────────────────────────────────
st.markdown(f"""
<p style="font-size:11px;color:{T['muted']};font-weight:700;letter-spacing:.9px;
           text-transform:uppercase;margin:0 0 16px;
           font-family:'Plus Jakarta Sans',sans-serif">Công cụ hiện có</p>
""", unsafe_allow_html=True)

TOOLS = [
    dict(
        icon="📊",
        name="Graduation Data Reviewer",
        desc="Rà soát dữ liệu xét tốt nghiệp, đối chiếu GPA và điểm số theo phụ lục.",
        tags=["Excel", "Local Processing"],
        status="live",
        page="pages/graduation-reviewer.py",
    ),
    dict(
        icon="📋",
        name="ReplaceCode Manager",
        desc="Quản lý và cập nhật môn thay thế/tương đương từ Quyết định PDF.",
        tags=["PDF", "GitHub Sync", "Searchable"],
        status="live",
        page="pages/replacecode-manager.py",
    ),
    # ── Thêm tool mới vào đây ──────────────────────────────────────────────
    # dict(icon="📈", name="Tool mới", desc="Mô tả...",
    #      tags=["Tag1"], status="coming", page=""),
]

def render_card(tool):
    badge = (
        f'<span style="background:{T["gbg"]};color:{T["gtxt"]};font-size:11px;font-weight:700;'
        f'padding:3px 10px;border-radius:20px;font-family:\'Plus Jakarta Sans\',sans-serif">● LIVE</span>'
        if tool["status"] == "live" else
        f'<span style="background:{T["card2"]};color:{T["muted"]};font-size:11px;font-weight:600;'
        f'padding:3px 10px;border-radius:20px;border:1px solid {T["border"]}">Soon</span>'
    )
    tags = "".join([
        f'<span style="background:{T["card2"]};color:{T["muted"]};font-size:11px;font-weight:600;'
        f'padding:3px 10px;border-radius:6px;border:1px solid {T["border"]};'
        f'font-family:\'Plus Jakarta Sans\',sans-serif">{tag}</span>'
        for tag in tool["tags"]
    ])
    st.markdown(f"""
    <div class="qa-card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px">
            <div style="background:{T['card2']};border:1px solid {T['border']};border-radius:12px;
                        width:46px;height:46px;display:flex;align-items:center;
                        justify-content:center;font-size:22px;flex-shrink:0">{tool['icon']}</div>
            {badge}
        </div>
        <div style="font-size:17px;font-weight:700;color:{T['text']};letter-spacing:-.3px;
                    margin-bottom:8px;font-family:'Plus Jakarta Sans',sans-serif">{tool['name']}</div>
        <p style="color:{T['muted']};font-size:13px;line-height:1.65;margin:0 0 18px;
                  font-family:'Plus Jakarta Sans',sans-serif">{tool['desc']}</p>
        <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:18px">{tags}</div>
    </div>
    """, unsafe_allow_html=True)

# Render 2 cột
live_tools   = [t for t in TOOLS if t["status"] == "live"]
coming_tools = [t for t in TOOLS if t["status"] != "live"]

for i in range(0, len(live_tools), 2):
    cols = st.columns(2, gap="large")
    for j, col in enumerate(cols):
        idx = i + j
        if idx < len(live_tools):
            tool = live_tools[idx]
            with col:
                render_card(tool)
                # FIX 3: CTA rõ ràng dạng button
                st.page_link(tool["page"], label=f"Mở {tool['name']}", icon="↗")

# Coming soon
if coming_tools:
    st.markdown(f"""
    <div style="height:32px"></div>
    <p style="font-size:11px;color:{T['muted']};font-weight:700;letter-spacing:.9px;
               text-transform:uppercase;margin:0 0 16px;
               font-family:'Plus Jakarta Sans',sans-serif">Sắp ra mắt</p>
    """, unsafe_allow_html=True)
    cols = st.columns(2, gap="large")
    for i, tool in enumerate(coming_tools):
        with cols[i % 2]:
            render_card(tool)

# ── Security note ─────────────────────────────────────────────────────────────
st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

st.markdown(f"""
<div style="background:{T['card']};border:1px solid {T['border']};
            border-radius:16px;padding:22px 28px">
    <div style="font-size:15px;font-weight:700;color:{T['text']};margin-bottom:8px;
                font-family:'Plus Jakarta Sans',sans-serif">💡 Thông tin bảo mật</div>
    <p style="color:{T['muted']};font-size:13px;line-height:1.7;margin:0;
              font-family:'Plus Jakarta Sans',sans-serif">
        Toàn bộ dữ liệu được xử lý tại trình duyệt (Local). Chúng mình không lưu trữ
        bất kỳ thông tin sinh viên nào trên server để đảm bảo an toàn dữ liệu tuyệt đối
        theo quy định của FPT Education.
    </p>
</div>

<div style="height:40px"></div>
<div style="text-align:center">
    <span style="color:{T['muted']};font-size:12px;font-family:'Plus Jakarta Sans',sans-serif">
        © 2026 YenLT31 — FPT Education QA Department
    </span>
</div>
<div style="height:24px"></div>
""", unsafe_allow_html=True)
