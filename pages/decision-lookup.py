import streamlit as st
import pdfplumber
import pandas as pd
import re
import io
import os

# ============================================================
#  PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Decision Lookup | FE QA Tools",
    page_icon="🔍",
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
    yellow="#EAB308", ybg="#1A1800", ytxt="#FACC15",
    blue="#3B82F6", bbg="#0C1529", btxt="#60A5FA",
)
LIGHT = dict(
    bg="#F0F4F8", card="#FFFFFF", card2="#F7F9FC", border="#E2E8F0",
    text="#1A2540", muted="#64748B", accent="#0A9E7F", accent_dim="#077A62",
    green="#16A34A", gbg="#DCFCE7", gtxt="#15803D",
    red="#DC2626", rbg="#FEF2F2", rtxt="#DC2626",
    yellow="#CA8A04", ybg="#FEFCE8", ytxt="#A16207",
    blue="#2563EB", bbg="#EFF6FF", btxt="#1D4ED8",
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
/* Background */
.stApp {{ background: {T['bg']} !important; }}
.block-container {{ padding-top: 1rem !important; max-width: 1200px !important; }}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: {T['card']} !important;
    border-right: 1px solid {T['border']} !important;
}}
[data-testid="stSidebarNav"] {{ display: none !important; }}

/* Typography */
.stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown li,
.stMarkdown span, label {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: {T['text']} !important;
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    gap: 0px;
    background: {T['card']} !important;
    border-radius: 12px;
    padding: 4px;
    border: 1px solid {T['border']};
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 8px;
    padding: 8px 20px;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600;
    font-size: 13px;
    color: {T['muted']} !important;
}}
.stTabs [aria-selected="true"] {{
    background: {T['accent']} !important;
    color: #080D18 !important;
}}
.stTabs [data-baseweb="tab-panel"] {{
    padding-top: 1.5rem;
}}

/* File uploader */
[data-testid="stFileUploader"] {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}}
[data-testid="stFileUploader"] section {{
    border: 2px dashed {T['border']} !important;
    border-radius: 12px !important;
    background: {T['card2']} !important;
    padding: 20px !important;
}}
[data-testid="stFileUploader"] section:hover {{
    border-color: {T['accent']} !important;
    background: {T['card']} !important;
}}

/* Buttons */
.stButton > button {{
    background: {T['accent']} !important; color: #080D18 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important; font-size: 14px !important;
    border: none !important; border-radius: 10px !important;
    padding: 12px 28px !important;
}}
.stButton > button:hover {{ background: {T['accent_dim']} !important; }}
.stButton > button:disabled {{
    background: {T['border']} !important;
    color: {T['muted']} !important;
    cursor: not-allowed !important;
}}

/* Dataframe */
[data-testid="stDataFrame"] {{
    border: 1px solid {T['border']} !important;
    border-radius: 12px !important;
    overflow: hidden;
}}

/* Metrics */
[data-testid="stMetric"] {{
    background: {T['card']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 12px !important;
    padding: 16px !important;
}}
[data-testid="stMetricLabel"] {{
    color: {T['muted']} !important;
}}

/* Expander */
.streamlit-expanderHeader {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    color: {T['text']} !important;
    background: {T['card']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 12px !important;
}}

/* Scrollbar */
::-webkit-scrollbar {{ width:6px; height:6px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {T['border']}; border-radius:3px; }}

/* Download button */
.stDownloadButton > button {{
    background: {T['card']} !important;
    color: {T['accent']} !important;
    border: 1px solid {T['accent']} !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
}}
.stDownloadButton > button:hover {{
    background: {T['accent']} !important;
    color: #080D18 !important;
}}
</style>""", unsafe_allow_html=True)

# ============================================================
#  SESSION STATE
# ============================================================
for key in ["mssv_df", "pdf_files", "results", "search_done"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ============================================================
#  HELPER FUNCTIONS
# ============================================================
def extract_mssv_from_excel(file):
    """Đọc file Excel và trả về danh sách MSSV."""
    df = pd.read_excel(file)
    # Tìm cột chứa MSSV (tìm cột có tên chứa 'mssv', 'MSSV', 'ma_sv', 'Mã SV', etc.)
    mssv_col = None
    for col in df.columns:
        col_lower = str(col).lower().strip()
        if any(kw in col_lower for kw in ['mssv', 'masv', 'mã sv', 'ma sv', 'student', 'rollnumber', 'roll_number', 'roll number']):
            mssv_col = col
            break
    if mssv_col is None:
        # Nếu không tìm thấy, lấy cột đầu tiên
        mssv_col = df.columns[0]
    
    mssv_list = df[mssv_col].dropna().astype(str).str.strip().tolist()
    return mssv_list, mssv_col, df


def search_mssv_in_pdf(pdf_file, mssv_list):
    """Tìm MSSV trong file PDF, trả về dict {mssv: [pages]}."""
    found = {}
    pdf_name = pdf_file.name
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text() or ""
                for mssv in mssv_list:
                    if mssv in text:
                        if mssv not in found:
                            found[mssv] = []
                        found[mssv].append({
                            "file": pdf_name,
                            "page": page_num,
                        })
    except Exception as e:
        st.error(f"Lỗi đọc PDF `{pdf_name}`: {e}")
    return found


def to_excel_bytes(df):
    """Chuyển DataFrame thành bytes Excel."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Kết quả')
    return output.getvalue()


# ============================================================
#  SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(f"""
    <div style="padding:16px 0 20px;border-bottom:1px solid {T['border']};margin-bottom:20px">
        <div style="font-size:15px;font-weight:800;color:{T['accent']};
                    font-family:'Plus Jakarta Sans',sans-serif">🔍 Decision Lookup</div>
        <div style="font-size:10px;color:{T['muted']};font-weight:600;letter-spacing:.9px;
                    text-transform:uppercase;margin-top:3px;font-family:'Plus Jakarta Sans',sans-serif">
            Tra cứu MSSV trong Quyết định PDF
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Theme
    st.markdown(f"""<p style="font-size:10px;color:{T['muted']};font-weight:700;letter-spacing:.9px;
              text-transform:uppercase;margin-bottom:8px;font-family:'Plus Jakarta Sans',sans-serif">Giao diện</p>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("☀ Sáng", use_container_width=True, key="btn_light"):
            st.session_state.theme = "light"; st.rerun()
    with c2:
        if st.button("🌙 Tối", use_container_width=True, key="btn_dark"):
            st.session_state.theme = "dark"; st.rerun()

    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:18px 0"></div>', unsafe_allow_html=True)

    # Hướng dẫn
    st.markdown(f"""
    <p style="font-size:10px;color:{T['muted']};font-weight:700;letter-spacing:.9px;
              text-transform:uppercase;margin-bottom:10px;font-family:'Plus Jakarta Sans',sans-serif">
        Hướng dẫn
    </p>
    <div style="font-size:12px;color:{T['muted']};line-height:2;font-family:'Plus Jakarta Sans',sans-serif">
        <div style="margin-bottom:6px">
            <span style="display:inline-flex;align-items:center;justify-content:center;
                width:20px;height:20px;border-radius:6px;background:{T['accent']};color:#080D18;
                font-size:10px;font-weight:800;margin-right:8px">1</span>
            Upload file Excel chứa MSSV
        </div>
        <div style="margin-bottom:6px">
            <span style="display:inline-flex;align-items:center;justify-content:center;
                width:20px;height:20px;border-radius:6px;background:{T['accent']};color:#080D18;
                font-size:10px;font-weight:800;margin-right:8px">2</span>
            Upload các file PDF Quyết định
        </div>
        <div style="margin-bottom:6px">
            <span style="display:inline-flex;align-items:center;justify-content:center;
                width:20px;height:20px;border-radius:6px;background:{T['accent']};color:#080D18;
                font-size:10px;font-weight:800;margin-right:8px">3</span>
            Bấm "Bắt đầu tra cứu"
        </div>
        <div>
            <span style="display:inline-flex;align-items:center;justify-content:center;
                width:20px;height:20px;border-radius:6px;background:{T['accent']};color:#080D18;
                font-size:10px;font-weight:800;margin-right:8px">4</span>
            Xem kết quả & tải báo cáo
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:18px 0"></div>', unsafe_allow_html=True)

    # Bảo mật
    st.markdown(f"""
    <div style="background:{T['accent']}11;border:1px solid {T['accent']}33;
                border-radius:10px;padding:12px;margin-bottom:16px">
        <div style="font-size:12px;font-weight:700;color:{T['accent']};margin-bottom:4px;
                    font-family:'Plus Jakarta Sans',sans-serif">🔒 Bảo mật</div>
        <div style="font-size:11px;color:{T['muted']};line-height:1.5;
                    font-family:'Plus Jakarta Sans',sans-serif">
            Dữ liệu xử lý 100% local.<br>Không gửi lên server.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation
    st.page_link("app.py", label="🏠  Trang chủ")

    st.markdown(f"""
    <div style="height:1px;background:{T['border']};margin:18px 0"></div>
    <div style="font-size:11px;color:{T['muted']};line-height:1.7;font-family:'Plus Jakarta Sans',sans-serif">
        © 2026 YenLT31<br>FE Education QA Department
    </div>""", unsafe_allow_html=True)

# ============================================================
#  MAIN CONTENT
# ============================================================

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="margin-bottom:32px">
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:8px">
        <div style="width:44px;height:44px;border-radius:14px;
                    background:linear-gradient(135deg,{T['accent']},{T['accent_dim']});
                    display:flex;align-items:center;justify-content:center;font-size:22px">
            🔍
        </div>
        <div>
            <h1 style="font-size:28px;font-weight:800;color:{T['text']};margin:0;line-height:1.2;
                        font-family:'Plus Jakarta Sans',sans-serif">
                Decision Lookup
            </h1>
            <p style="font-size:13px;color:{T['muted']};margin:0;
                      font-family:'Plus Jakarta Sans',sans-serif">
                Tra cứu MSSV trong các Quyết định PDF — nhanh chóng & chính xác
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_config, tab_result = st.tabs(["⚙️  Cấu hình", "📊  Kết quả"])

# ── TAB 1: CẤU HÌNH ──────────────────────────────────────────────────────────
with tab_config:

    # Step 01 — Upload files
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px">
        <span style="display:inline-flex;align-items:center;justify-content:center;
            width:28px;height:28px;border-radius:8px;background:{T['accent']};color:#080D18;
            font-size:12px;font-weight:800;font-family:'Plus Jakarta Sans',sans-serif">01</span>
        <span style="font-size:18px;font-weight:700;color:{T['text']};
                     font-family:'Plus Jakarta Sans',sans-serif">Tải lên file</span>
    </div>
    <p style="font-size:13px;color:{T['muted']};margin-bottom:20px;margin-left:38px;
              font-family:'Plus Jakarta Sans',sans-serif">
        Upload file danh sách MSSV và các file Quyết định PDF
    </p>
    """, unsafe_allow_html=True)

    col_excel, col_pdf = st.columns(2)

    with col_excel:
        st.markdown(f"""<p style="font-size:11px;color:{T['muted']};font-weight:700;
            letter-spacing:.8px;text-transform:uppercase;margin-bottom:8px;
            font-family:'Plus Jakarta Sans',sans-serif">📋 File Excel — Danh sách MSSV</p>""",
            unsafe_allow_html=True)
        excel_file = st.file_uploader(
            "Upload file Excel",
            type=["xlsx", "xls"],
            key="excel_upload",
            label_visibility="collapsed",
        )

    with col_pdf:
        st.markdown(f"""<p style="font-size:11px;color:{T['muted']};font-weight:700;
            letter-spacing:.8px;text-transform:uppercase;margin-bottom:8px;
            font-family:'Plus Jakarta Sans',sans-serif">📄 File PDF Quyết định</p>""",
            unsafe_allow_html=True)
        pdf_files = st.file_uploader(
            "Upload file PDF",
            type=["pdf"],
            accept_multiple_files=True,
            key="pdf_upload",
            label_visibility="collapsed",
        )

    # Preview uploaded files
    if excel_file or pdf_files:
        st.markdown(f'<div style="height:1px;background:{T["border"]};margin:24px 0"></div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px">
            <span style="display:inline-flex;align-items:center;justify-content:center;
                width:28px;height:28px;border-radius:8px;background:{T['accent']};color:#080D18;
                font-size:12px;font-weight:800;font-family:'Plus Jakarta Sans',sans-serif">02</span>
            <span style="font-size:18px;font-weight:700;color:{T['text']};
                         font-family:'Plus Jakarta Sans',sans-serif">Xác nhận dữ liệu</span>
        </div>
        """, unsafe_allow_html=True)

        info_col1, info_col2, info_col3 = st.columns(3)

        with info_col1:
            if excel_file:
                try:
                    mssv_list, mssv_col, mssv_df = extract_mssv_from_excel(excel_file)
                    st.session_state.mssv_df = mssv_df
                    st.markdown(f"""
                    <div style="background:{T['card']};border:1px solid {T['border']};
                                border-radius:12px;padding:16px">
                        <div style="font-size:11px;color:{T['muted']};font-weight:600;
                                    text-transform:uppercase;letter-spacing:.8px;margin-bottom:4px;
                                    font-family:'Plus Jakarta Sans',sans-serif">MSSV tìm thấy</div>
                        <div style="font-size:28px;font-weight:800;color:{T['accent']};
                                    font-family:'Plus Jakarta Sans',sans-serif">{len(mssv_list)}</div>
                        <div style="font-size:11px;color:{T['muted']};margin-top:2px;
                                    font-family:'Plus Jakarta Sans',sans-serif">
                            Cột: <strong>{mssv_col}</strong>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Lỗi đọc Excel: {e}")
                    mssv_list = []
            else:
                st.markdown(f"""
                <div style="background:{T['card']};border:1px dashed {T['border']};
                            border-radius:12px;padding:16px;text-align:center">
                    <div style="font-size:13px;color:{T['muted']};font-family:'Plus Jakarta Sans',sans-serif">
                        Chưa upload file MSSV
                    </div>
                </div>""", unsafe_allow_html=True)
                mssv_list = []

        with info_col2:
            st.markdown(f"""
            <div style="background:{T['card']};border:1px solid {T['border']};
                        border-radius:12px;padding:16px">
                <div style="font-size:11px;color:{T['muted']};font-weight:600;
                            text-transform:uppercase;letter-spacing:.8px;margin-bottom:4px;
                            font-family:'Plus Jakarta Sans',sans-serif">File PDF</div>
                <div style="font-size:28px;font-weight:800;color:{T['blue']};
                            font-family:'Plus Jakarta Sans',sans-serif">{len(pdf_files) if pdf_files else 0}</div>
                <div style="font-size:11px;color:{T['muted']};margin-top:2px;
                            font-family:'Plus Jakarta Sans',sans-serif">file được upload</div>
            </div>
            """, unsafe_allow_html=True)

        with info_col3:
            ready = bool(excel_file and pdf_files and len(mssv_list) > 0)
            status_color = T['green'] if ready else T['yellow']
            status_text = "Sẵn sàng tra cứu" if ready else "Thiếu dữ liệu"
            status_icon = "✅" if ready else "⚠️"
            st.markdown(f"""
            <div style="background:{T['card']};border:1px solid {T['border']};
                        border-radius:12px;padding:16px">
                <div style="font-size:11px;color:{T['muted']};font-weight:600;
                            text-transform:uppercase;letter-spacing:.8px;margin-bottom:4px;
                            font-family:'Plus Jakarta Sans',sans-serif">Trạng thái</div>
                <div style="font-size:28px;margin-bottom:2px">{status_icon}</div>
                <div style="font-size:11px;color:{status_color};font-weight:600;
                            font-family:'Plus Jakarta Sans',sans-serif">{status_text}</div>
            </div>
            """, unsafe_allow_html=True)

    # Step 03 — Bắt đầu tra cứu
    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:24px 0"></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px">
        <span style="display:inline-flex;align-items:center;justify-content:center;
            width:28px;height:28px;border-radius:8px;background:{T['accent']};color:#080D18;
            font-size:12px;font-weight:800;font-family:'Plus Jakarta Sans',sans-serif">03</span>
        <span style="font-size:18px;font-weight:700;color:{T['text']};
                     font-family:'Plus Jakarta Sans',sans-serif">Bắt đầu tra cứu</span>
    </div>
    <p style="font-size:13px;color:{T['muted']};margin-bottom:20px;margin-left:38px;
              font-family:'Plus Jakarta Sans',sans-serif">
        Hệ thống đọc từng PDF, tìm MSSV trong hàng rồi chuyển sang tab Kết quả
    </p>
    """, unsafe_allow_html=True)

    can_search = bool(excel_file and pdf_files)

    if not can_search:
        st.markdown(f"""
        <div style="background:{T['ybg']};border:1px solid {T['yellow']}33;
                    border-radius:10px;padding:12px 16px;margin-bottom:16px">
            <span style="font-size:13px;color:{T['ytxt']};font-family:'Plus Jakarta Sans',sans-serif">
                ⚠️ Cần upload: file Excel MSSV và file PDF Quyết định
            </span>
        </div>
        """, unsafe_allow_html=True)

    if st.button(
        "🔍  Bắt đầu tra cứu",
        use_container_width=True,
        disabled=not can_search,
        key="btn_search",
    ):
        mssv_list, mssv_col, mssv_df = extract_mssv_from_excel(excel_file)

        all_results = {}  # {mssv: [{file, page}, ...]}
        progress = st.progress(0, text="Đang xử lý...")

        for i, pdf_file in enumerate(pdf_files):
            progress.progress(
                (i + 1) / len(pdf_files),
                text=f"Đang đọc: {pdf_file.name} ({i+1}/{len(pdf_files)})"
            )
            found = search_mssv_in_pdf(pdf_file, mssv_list)
            for mssv, locations in found.items():
                if mssv not in all_results:
                    all_results[mssv] = []
                all_results[mssv].extend(locations)

        progress.empty()

        # Build result DataFrame
        rows = []
        for mssv in mssv_list:
            if mssv in all_results:
                for loc in all_results[mssv]:
                    rows.append({
                        "MSSV": mssv,
                        "Trạng thái": "✅ Tìm thấy",
                        "File PDF": loc["file"],
                        "Trang": loc["page"],
                    })
            else:
                rows.append({
                    "MSSV": mssv,
                    "Trạng thái": "❌ Không tìm thấy",
                    "File PDF": "—",
                    "Trang": "—",
                })

        st.session_state.results = pd.DataFrame(rows)
        st.session_state.search_done = True
        st.session_state.mssv_total = len(mssv_list)
        st.session_state.mssv_found = len(all_results)
        st.session_state.mssv_not_found = len(mssv_list) - len(all_results)
        st.session_state.pdf_count = len(pdf_files)

        st.success("✅ Tra cứu hoàn tất! Chuyển sang tab **Kết quả** để xem.")

# ── TAB 2: KẾT QUẢ ───────────────────────────────────────────────────────────
with tab_result:

    if not st.session_state.search_done:
        st.markdown(f"""
        <div style="text-align:center;padding:60px 20px">
            <div style="font-size:48px;margin-bottom:16px">📭</div>
            <h3 style="font-size:18px;font-weight:700;color:{T['text']};margin-bottom:8px;
                        font-family:'Plus Jakarta Sans',sans-serif">
                Chưa có kết quả
            </h3>
            <p style="font-size:13px;color:{T['muted']};font-family:'Plus Jakarta Sans',sans-serif">
                Quay lại tab <strong>Cấu hình</strong>, upload file và bấm <strong>Bắt đầu tra cứu</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

    else:
        results_df = st.session_state.results

        # Summary cards
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:28px">
            <div style="background:{T['card']};border:1px solid {T['border']};border-radius:12px;padding:16px">
                <div style="font-size:10px;color:{T['muted']};font-weight:700;text-transform:uppercase;
                            letter-spacing:.8px;margin-bottom:4px;font-family:'Plus Jakarta Sans',sans-serif">
                    Tổng MSSV</div>
                <div style="font-size:28px;font-weight:800;color:{T['text']};
                            font-family:'Plus Jakarta Sans',sans-serif">{st.session_state.mssv_total}</div>
            </div>
            <div style="background:{T['gbg']};border:1px solid {T['green']}33;border-radius:12px;padding:16px">
                <div style="font-size:10px;color:{T['gtxt']};font-weight:700;text-transform:uppercase;
                            letter-spacing:.8px;margin-bottom:4px;font-family:'Plus Jakarta Sans',sans-serif">
                    Tìm thấy</div>
                <div style="font-size:28px;font-weight:800;color:{T['green']};
                            font-family:'Plus Jakarta Sans',sans-serif">{st.session_state.mssv_found}</div>
            </div>
            <div style="background:{T['rbg']};border:1px solid {T['red']}33;border-radius:12px;padding:16px">
                <div style="font-size:10px;color:{T['rtxt']};font-weight:700;text-transform:uppercase;
                            letter-spacing:.8px;margin-bottom:4px;font-family:'Plus Jakarta Sans',sans-serif">
                    Không tìm thấy</div>
                <div style="font-size:28px;font-weight:800;color:{T['red']};
                            font-family:'Plus Jakarta Sans',sans-serif">{st.session_state.mssv_not_found}</div>
            </div>
            <div style="background:{T['bbg']};border:1px solid {T['blue']}33;border-radius:12px;padding:16px">
                <div style="font-size:10px;color:{T['btxt']};font-weight:700;text-transform:uppercase;
                            letter-spacing:.8px;margin-bottom:4px;font-family:'Plus Jakarta Sans',sans-serif">
                    File PDF đã quét</div>
                <div style="font-size:28px;font-weight:800;color:{T['blue']};
                            font-family:'Plus Jakarta Sans',sans-serif">{st.session_state.pdf_count}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Filter
        filter_col1, filter_col2, filter_col3 = st.columns([2, 2, 1])
        with filter_col1:
            search_text = st.text_input("🔍 Tìm MSSV", placeholder="Nhập MSSV...", key="search_mssv")
        with filter_col2:
            status_filter = st.selectbox(
                "Trạng thái",
                ["Tất cả", "✅ Tìm thấy", "❌ Không tìm thấy"],
                key="status_filter"
            )
        with filter_col3:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            st.download_button(
                "📥 Tải Excel",
                data=to_excel_bytes(results_df),
                file_name="decision_lookup_result.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

        # Apply filters
        filtered_df = results_df.copy()
        if search_text:
            filtered_df = filtered_df[filtered_df["MSSV"].str.contains(search_text, case=False, na=False)]
        if status_filter != "Tất cả":
            filtered_df = filtered_df[filtered_df["Trạng thái"] == status_filter]

        # Display
        st.markdown(f"""
        <div style="font-size:12px;color:{T['muted']};margin-bottom:8px;
                    font-family:'Plus Jakarta Sans',sans-serif">
            Hiển thị <strong style="color:{T['text']}">{len(filtered_df)}</strong> / {len(results_df)} kết quả
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=500,
            hide_index=True,
        )

        # Reset
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        if st.button("🔄 Làm lại tra cứu mới", key="btn_reset"):
            for key in ["mssv_df", "pdf_files", "results", "search_done",
                        "mssv_total", "mssv_found", "mssv_not_found", "pdf_count"]:
                st.session_state[key] = None
            st.rerun()
