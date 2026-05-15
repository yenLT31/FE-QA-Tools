import streamlit as st
import importlib.util
import pandas as pd
import os
import io

# ============================================================
#  LOAD LOGIC
# ============================================================
SCRIPT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'scripts', 'decision-lookup.py')
)
spec = importlib.util.spec_from_file_location("decision_lookup_logic", SCRIPT_PATH)
logic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(logic)

# ============================================================
#  PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Decision Lookup | FE QA Tools",
    page_icon="QA",
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
    orange="#F97316", obg="#1A1008", otxt="#FB923C",
)
LIGHT = dict(
    bg="#F0F4F8", card="#FFFFFF", card2="#F7F9FC", border="#E2E8F0",
    text="#1A2540", muted="#64748B", accent="#0A9E7F", accent_dim="#077A62",
    green="#16A34A", gbg="#DCFCE7", gtxt="#15803D",
    red="#DC2626", rbg="#FEF2F2", rtxt="#DC2626",
    yellow="#CA8A04", ybg="#FEFCE8", ytxt="#A16207",
    blue="#2563EB", bbg="#EFF6FF", btxt="#1D4ED8",
    orange="#EA580C", obg="#FFF7ED", otxt="#C2410C",
)
T = DARK if st.session_state.theme == "dark" else LIGHT

# ============================================================
#  SESSION STATE
# ============================================================
defaults = {
    "dl_results": None, "dl_summary": None, "dl_detail": None,
    "dl_mssv_list": None, "dl_errors": [], "dl_done": False,
    "dl_tab": "config", "dl_stats": {},
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
#  CSS
# ============================================================
st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">',
    unsafe_allow_html=True,
)

st.markdown(f"""<style>
.stApp {{ background: {T['bg']} !important; }}
.block-container {{ padding-top: 1rem !important; max-width: 1200px !important; }}
[data-testid="stSidebar"] {{
    background: {T['card']} !important;
    border-right: 1px solid {T['border']} !important;
}}
[data-testid="stSidebarNav"] {{ display: none !important; }}
.stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
.stMarkdown li, .stMarkdown span, label {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: {T['text']} !important;
}}
.stTabs [data-baseweb="tab-list"] {{
    gap: 0; background: {T['card']} !important; border-radius: 12px;
    padding: 4px; border: 1px solid {T['border']};
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 8px; padding: 8px 24px;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600; font-size: 13px; color: {T['muted']} !important;
    border: none !important;
}}
.stTabs [aria-selected="true"] {{
    background: {T['accent']} !important; color: #080D18 !important;
}}
[data-testid="stFileUploader"] section {{
    border: 2px dashed {T['border']} !important; border-radius: 12px !important;
    background: {T['card2']} !important; padding: 20px !important;
}}
[data-testid="stFileUploader"] section:hover {{ border-color: {T['accent']} !important; }}
.stButton > button {{
    background: {T['accent']} !important; color: #080D18 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important; border: none !important; border-radius: 10px !important;
    padding: 12px 28px !important;
}}
.stButton > button:hover {{ background: {T['accent_dim']} !important; }}
.stDownloadButton > button {{
    background: {T['card']} !important; color: {T['accent']} !important;
    border: 1px solid {T['accent']} !important; border-radius: 10px !important;
}}
.stDownloadButton > button:hover {{
    background: {T['accent']} !important; color: #080D18 !important;
}}
[data-testid="stDataFrame"] {{
    border: 1px solid {T['border']} !important; border-radius: 12px !important;
}}
.stTextInput > div > div > input {{
    background: {T['card']} !important; border-color: {T['border']} !important;
    border-radius: 8px !important; color: {T['text']} !important;
}}
.stSelectbox > div > div {{
    background: {T['card']} !important; border-color: {T['border']} !important;
    border-radius: 8px !important; color: {T['text']} !important;
}}
</style>""", unsafe_allow_html=True)


# ============================================================
#  HELPERS
# ============================================================
def step_badge(num, title, desc=""):
    st.markdown(f"""
    <div style="display:flex;align-items:flex-start;gap:12px;margin-bottom:16px">
        <span style="display:inline-flex;align-items:center;justify-content:center;
            width:30px;height:30px;border-radius:9px;background:{T['accent']};color:#080D18;
            font-size:13px;font-weight:800;flex-shrink:0">{num:02d}</span>
        <div>
            <div style="font-size:17px;font-weight:700;color:{T['text']}">{title}</div>
            {'<div style="font-size:12.5px;color:'+T['muted']+';margin-top:3px">'+desc+'</div>' if desc else ''}
        </div>
    </div>""", unsafe_allow_html=True)


def card_metric(label, value, color, bg):
    return f"""
    <div style="background:{bg};border:1px solid {color}33;border-radius:12px;padding:18px">
        <div style="font-size:10px;color:{color};font-weight:700;text-transform:uppercase;
                    letter-spacing:.8px;margin-bottom:6px">{label}</div>
        <div style="font-size:30px;font-weight:800;color:{color}">{value}</div>
    </div>"""


def divider():
    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:28px 0"></div>',
                unsafe_allow_html=True)


# ============================================================
#  SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(f"""
    <div style="padding:16px 0 20px;border-bottom:1px solid {T['border']};margin-bottom:20px">
        <div style="display:flex;align-items:center;gap:10px">
            <div style="width:36px;height:36px;border-radius:10px;
                        background:linear-gradient(135deg,{T['accent']},{T['accent_dim']});
                        display:flex;align-items:center;justify-content:center;font-size:18px">🔍</div>
            <div>
                <div style="font-size:14px;font-weight:800;color:{T['accent']}">Decision Lookup</div>
                <div style="font-size:10px;color:{T['muted']};font-weight:600;letter-spacing:.8px;
                            text-transform:uppercase">Tra cứu MSSV trong QĐ PDF</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"<p style='font-size:10px;color:{T['muted']};font-weight:700;letter-spacing:.9px;"
                f"text-transform:uppercase;margin-bottom:8px'>Giao diện</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("☀ Sáng", use_container_width=True, key="btn_light"):
            st.session_state.theme = "light"; st.rerun()
    with c2:
        if st.button("🌙 Tối", use_container_width=True, key="btn_dark"):
            st.session_state.theme = "dark"; st.rerun()

    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:18px 0"></div>',
                unsafe_allow_html=True)

    st.markdown(f"""
    <p style="font-size:10px;color:{T['muted']};font-weight:700;letter-spacing:.9px;
              text-transform:uppercase;margin-bottom:10px">Hướng dẫn nhanh</p>
    <div style="font-size:12px;color:{T['muted']};line-height:2.1">
        <div>① Upload Excel danh sách MSSV</div>
        <div>② Upload các file PDF Quyết định</div>
        <div>③ Bấm "Bắt đầu tra cứu"</div>
        <div>④ Xem kết quả & tải báo cáo</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:18px 0"></div>',
                unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:{T['accent']}11;border:1px solid {T['accent']}33;
                border-radius:10px;padding:12px">
        <div style="font-size:12px;font-weight:700;color:{T['accent']};margin-bottom:4px">
            🔒 Bảo mật dữ liệu</div>
        <div style="font-size:11px;color:{T['muted']};line-height:1.5">
            Mọi dữ liệu xử lý <strong>100% tại local</strong>.<br>Không gửi lên server.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:18px 0"></div>',
                unsafe_allow_html=True)

    debug_mode = st.checkbox("🛠 Debug pdfplumber", value=False, key="debug_pdf")

    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:18px 0"></div>',
                unsafe_allow_html=True)

    st.page_link("app.py", label="🏠  Trang chủ")

    st.markdown(f"""
    <div style="margin-top:24px;padding-top:14px;border-top:1px solid {T['border']};text-align:center">
        <div style="font-size:11px;color:{T['muted']}">
            © 2026 <strong style="color:{T['accent']}">YenLT31</strong></div>
    </div>""", unsafe_allow_html=True)


# ============================================================
#  HEADER
# ============================================================
st.markdown(f"""
<div style="margin-bottom:28px">
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:6px">
        <div style="width:44px;height:44px;border-radius:14px;
                    background:linear-gradient(135deg,{T['accent']},{T['accent_dim']});
                    display:flex;align-items:center;justify-content:center;font-size:22px">🔍</div>
        <div>
            <h1 style="font-size:26px;font-weight:800;color:{T['text']};margin:0;line-height:1.2">
                Decision Lookup</h1>
            <p style="font-size:13px;color:{T['muted']};margin:0">
                Tra cứu MSSV trong các Quyết định PDF</p>
        </div>
    </div>
</div>""", unsafe_allow_html=True)


# ============================================================
#  TABS
# ============================================================
tabs = st.tabs(["⚙️  Cấu hình", "📊  Kết quả"])

# ── TAB 1: CẤU HÌNH ──────────────────────────────────────────
with tabs[0]:
    step_badge(1, "Tải lên file", "Upload file danh sách MSSV và các file PDF")

    col_excel, col_pdf = st.columns(2)
    with col_excel:
        st.markdown(f"<p style='font-size:11px;color:{T['muted']};font-weight:700;"
                    f"text-transform:uppercase;margin-bottom:8px'>📋 File Excel — MSSV</p>",
                    unsafe_allow_html=True)
        excel_file = st.file_uploader("Upload Excel", type=["xlsx", "xls"],
                                      key="excel_upload", label_visibility="collapsed")
    with col_pdf:
        st.markdown(f"<p style='font-size:11px;color:{T['muted']};font-weight:700;"
                    f"text-transform:uppercase;margin-bottom:8px'>📄 File PDF Quyết định</p>",
                    unsafe_allow_html=True)
        pdf_files = st.file_uploader("Upload PDF", type=["pdf"],
                                     accept_multiple_files=True,
                                     key="pdf_upload", label_visibility="collapsed")

    mssv_list = []
    mssv_col_name = ""

    if excel_file:
        try:
            df_mssv = pd.read_excel(excel_file)
            mssv_col_idx = logic.detect_mssv_col(list(df_mssv.columns))
            mssv_col_name = df_mssv.columns[mssv_col_idx] if mssv_col_idx >= 0 else df_mssv.columns[0]
            mssv_list = df_mssv[mssv_col_name].dropna().astype(str).str.strip().tolist()
        except Exception as e:
            st.error(f"Lỗi đọc Excel: {e}")

    if excel_file or pdf_files:
        divider()
        step_badge(2, "Xác nhận dữ liệu")
        mc1, mc2, mc3 = st.columns(3)

        with mc1:
            if mssv_list:
                st.markdown(f"""<div style="background:{T['card']};border:1px solid {T['border']};
                    border-radius:12px;padding:18px">
                    <div style="font-size:10px;color:{T['muted']};font-weight:700;
                        text-transform:uppercase;margin-bottom:6px">MSSV tìm thấy</div>
                    <div style="font-size:30px;font-weight:800;color:{T['accent']}">{len(mssv_list)}</div>
                    <div style="font-size:11px;color:{T['muted']};margin-top:3px">
                        Cột: <strong style="color:{T['text']}">{mssv_col_name}</strong></div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style="background:{T['card']};border:2px dashed {T['border']};
                    border-radius:12px;padding:18px;text-align:center">
                    <div style="font-size:20px;margin-bottom:4px">📋</div>
                    <div style="font-size:12px;color:{T['muted']}">Chưa upload file MSSV</div>
                </div>""", unsafe_allow_html=True)

        with mc2:
            pdf_count = len(pdf_files) if pdf_files else 0
            if pdf_count > 0:
                st.markdown(f"""<div style="background:{T['card']};border:1px solid {T['border']};
                    border-radius:12px;padding:18px">
                    <div style="font-size:10px;color:{T['muted']};font-weight:700;
                        text-transform:uppercase;margin-bottom:6px">File PDF</div>
                    <div style="font-size:30px;font-weight:800;color:{T['blue']}">{pdf_count}</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style="background:{T['card']};border:2px dashed {T['border']};
                    border-radius:12px;padding:18px;text-align:center">
                    <div style="font-size:20px;margin-bottom:4px">📄</div>
                    <div style="font-size:12px;color:{T['muted']}">Chưa upload file PDF</div>
                </div>""", unsafe_allow_html=True)

        with mc3:
            ready = bool(mssv_list and pdf_files)
            st.markdown(f"""<div style="background:{T['card']};border:1px solid {T['border']};
                border-radius:12px;padding:18px">
                <div style="font-size:10px;color:{T['muted']};font-weight:700;
                    text-transform:uppercase;margin-bottom:6px">Trạng thái</div>
                <div style="font-size:30px;margin-bottom:2px">{"✅" if ready else "⏳"}</div>
                <div style="font-size:11px;color:{T['green'] if ready else T['yellow']};font-weight:600">
                    {"Sẵn sàng tra cứu" if ready else "Đang chờ dữ liệu"}</div>
            </div>""", unsafe_allow_html=True)

    divider()
    step_badge(3, "Bắt đầu tra cứu")

    can_search = bool(mssv_list and pdf_files)
    if not can_search:
        st.markdown(f"""<div style="background:{T['ybg']};border:1px solid {T['yellow']}33;
            border-radius:10px;padding:12px 16px">
            <span style="font-size:13px;color:{T['ytxt']}">
                ⚠️ Cần upload: file Excel MSSV và file PDF Quyết định</span>
        </div>""", unsafe_allow_html=True)

    if st.button("🔍  Bắt đầu tra cứu", use_container_width=True,
                 disabled=not can_search, key="btn_search"):
        pdf_data = [{"name": f.name, "bytes": f.read()} for f in pdf_files]

        progress = st.progress(0, text="Đang chuẩn bị...")
        progress.progress(0.1, text="Đang đọc PDF...")

        results = logic.search_mssv_in_pdfs(mssv_list, pdf_data)
        progress.progress(0.7, text="Đang tạo báo cáo...")

        errors = results.pop("_errors", [])
        df_summary, df_detail = logic.build_export_data(mssv_list, results)

        found_count = sum(1 for m in mssv_list if results.get(m.strip(), {}).get("found"))

        st.session_state.dl_results = results
        st.session_state.dl_summary = df_summary
        st.session_state.dl_detail = df_detail
        st.session_state.dl_mssv_list = mssv_list
        st.session_state.dl_errors = errors
        st.session_state.dl_done = True
        st.session_state.dl_stats = {
            "total": len(mssv_list), "found": found_count,
            "not_found": len(mssv_list) - found_count,
            "pdf_count": len(pdf_data), "error_count": len(errors),
        }
        progress.progress(1.0, text="✅ Hoàn tất!")
        st.rerun()

    # Debug
    if debug_mode and pdf_files:
        divider()
        st.markdown(f"<div style='font-size:14px;font-weight:700;color:{T['orange']};"
                    f"margin-bottom:12px'>🛠 Debug pdfplumber</div>", unsafe_allow_html=True)
        debug_pdf = st.selectbox("Chọn file PDF", [f.name for f in pdf_files], key="debug_select")
        debug_page = st.number_input("Trang", min_value=1, value=1, key="debug_page")
        selected_pdf = next((f for f in pdf_files if f.name == debug_pdf), None)
        if selected_pdf:
            import pdfplumber as pdfp
            try:
                selected_pdf.seek(0)
                with pdfp.open(selected_pdf) as pdf:
                    if debug_page <= len(pdf.pages):
                        page = pdf.pages[debug_page - 1]
                        with st.expander("📝 Text", expanded=False):
                            st.code(page.extract_text() or "(trống)")
                        with st.expander("📊 Tables", expanded=True):
                            tables = page.extract_tables()
                            if tables:
                                for i, table in enumerate(tables):
                                    st.markdown(f"**Table {i+1}** ({len(table)} rows)")
                                    if table:
                                        st.dataframe(pd.DataFrame(table[1:],
                                            columns=table[0] if table[0] else None),
                                            use_container_width=True, hide_index=True)
                            else:
                                st.info("Không tìm thấy bảng.")
                    else:
                        st.warning(f"PDF chỉ có {len(pdf.pages)} trang.")
            except Exception as e:
                st.error(f"Lỗi: {e}")

# ── TAB 2: KẾT QUẢ ───────────────────────────────────────────
with tabs[1]:
    if not st.session_state.dl_done:
        st.markdown(f"""<div style="text-align:center;padding:80px 20px">
            <div style="font-size:52px;margin-bottom:16px">📭</div>
            <h3 style="font-size:18px;font-weight:700;color:{T['text']};margin-bottom:8px">
                Chưa có kết quả</h3>
            <p style="font-size:13px;color:{T['muted']}">
                Quay lại tab Cấu hình để upload file và bắt đầu tra cứu</p>
        </div>""", unsafe_allow_html=True)
    else:
        stats = st.session_state.dl_stats
        df_summary = st.session_state.dl_summary
        df_detail = st.session_state.dl_detail
        errors = st.session_state.dl_errors

        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:28px">
            {card_metric("Tổng MSSV", stats['total'], T['text'], T['card'])}
            {card_metric("Tìm thấy", stats['found'], T['green'], T['gbg'])}
            {card_metric("Không tìm thấy", stats['not_found'], T['red'], T['rbg'])}
            {card_metric("PDF đã quét", stats['pdf_count'], T['blue'], T['bbg'])}
        </div>""", unsafe_allow_html=True)

        if errors:
            st.markdown(f"""<div style="background:{T['rbg']};border:1px solid {T['red']}33;
                border-radius:10px;padding:12px 16px;margin-bottom:20px">
                <div style="font-size:12px;font-weight:700;color:{T['rtxt']};margin-bottom:6px">
                    ⚠️ {len(errors)} lỗi khi đọc PDF</div>
                <div style="font-size:11px;color:{T['muted']}">
                    {"<br>".join(f"• <strong>{e['file']}</strong>: {e['error']}" for e in errors)}
                </div>
            </div>""", unsafe_allow_html=True)

        result_tab1, result_tab2 = st.tabs(["📋 Tổng hợp", "📑 Chi tiết"])

        with result_tab1:
            fc1, fc2, fc3 = st.columns([2, 2, 1])
            with fc1:
                search_s = st.text_input("🔍 Tìm MSSV", key="search_summary")
            with fc2:
                filter_s = st.selectbox("Trạng thái", ["Tất cả", "Có", "Không"], key="filter_summary")
            with fc3:
                st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
                excel_bytes = logic.to_excel_bytes(df_summary, df_detail)
                st.download_button("📥 Tải Excel", data=excel_bytes,
                                   file_name="decision_lookup_result.xlsx",
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                   use_container_width=True)

            filtered = df_summary.copy()
            if search_s:
                filtered = filtered[filtered["MSSV"].str.contains(search_s, case=False, na=False)]
            if filter_s != "Tất cả":
                filtered = filtered[filtered["Tìm thấy"] == filter_s]

            st.markdown(f"<div style='font-size:12px;color:{T['muted']};margin-bottom:8px'>"
                        f"Hiển thị <strong style='color:{T['text']}'>{len(filtered)}</strong>"
                        f" / {len(df_summary)} kết quả</div>", unsafe_allow_html=True)
            st.dataframe(filtered, use_container_width=True, height=500, hide_index=True)

        with result_tab2:
            fc1d, fc2d, fc3d = st.columns([2, 2, 1])
            with fc1d:
                search_d = st.text_input("🔍 Tìm MSSV", key="search_detail")
            with fc2d:
                qd_options = ["Tất cả"]
                if "Tên QĐ" in df_detail.columns:
                    qd_options += sorted(df_detail["Tên QĐ"].dropna().unique().tolist())
                filter_qd = st.selectbox("Quyết định", qd_options, key="filter_qd")
            with fc3d:
                st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
                st.download_button("📥 Tải Excel", data=excel_bytes,
                                   file_name="decision_lookup_detail.xlsx",
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                   use_container_width=True, key="dl_detail_excel")

            filtered_d = df_detail.copy()
            if search_d:
                filtered_d = filtered_d[filtered_d["MSSV"].str.contains(search_d, case=False, na=False)]
            if filter_qd != "Tất cả":
                filtered_d = filtered_d[filtered_d["Tên QĐ"] == filter_qd]

            st.markdown(f"<div style='font-size:12px;color:{T['muted']};margin-bottom:8px'>"
                        f"Hiển thị <strong style='color:{T['text']}'>{len(filtered_d)}</strong>"
                        f" / {len(df_detail)} dòng</div>", unsafe_allow_html=True)
            st.dataframe(filtered_d, use_container_width=True, height=500, hide_index=True)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        if st.button("🔄  Làm lại tra cứu mới", key="btn_reset"):
            for k in defaults:
                st.session_state[k] = defaults[k]
            st.rerun()
