import streamlit as st
import importlib.util
import pandas as pd
import os
import io

# ============================================================
#  LOAD LOGIC
#  ⚠️ Nếu file script của bạn tên khác 'decision_lookup.py',
#     đổi tên file ở dòng dưới cho khớp.
# ============================================================
SCRIPT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'scripts', 'decision_lookup.py')
)
_load_error = None
logic = None
try:
    spec = importlib.util.spec_from_file_location("decision_lookup", SCRIPT_PATH)
    logic = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(logic)
except Exception as e:
    _load_error = e

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
    "dl_summary": None, "dl_detail": None, "dl_errors": [],
    "dl_done": False, "dl_stats": {},
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
.stTextInput input, .stTextArea textarea {{
    background: {T['card2']} !important; color: {T['text']} !important;
    border: 1px solid {T['border']} !important; border-radius: 10px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}}
.stTextInput input:focus, .stTextArea textarea:focus {{
    border-color: {T['accent']} !important; box-shadow: none !important;
}}
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
</style>""", unsafe_allow_html=True)


# ============================================================
#  UI HELPERS
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
                            text-transform:uppercase">Tra cứu MSSV trong Quyết định</div>
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
        <div>① Upload file Quyết định (PDF)</div>
        <div>② Nhập (các) MSSV cần tra cứu</div>
        <div>③ Bấm "Tra cứu"</div>
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
                Tra cứu MSSV trong các file Quyết định PDF — tìm nhanh sinh viên thuộc Quyết định nào</p>
        </div>
    </div>
</div>""", unsafe_allow_html=True)


# ============================================================
#  KIỂM TRA NẠP SCRIPT
# ============================================================
if _load_error is not None:
    st.markdown(f"""<div style="background:{T['rbg']};border:1px solid {T['red']}33;
        border-radius:10px;padding:14px 18px">
        <span style="font-size:13px;color:{T['rtxt']}">
            ❌ Không nạp được <code>scripts/decision_lookup.py</code>: {_load_error}</span>
    </div>""", unsafe_allow_html=True)
    st.stop()


# ============================================================
#  TABS
# ============================================================
tabs = st.tabs(["🔍  Tra cứu", "📊  Kết quả"])

# ── TAB 1: TRA CỨU ───────────────────────────────────────────
with tabs[0]:
    step_badge(1, "Tải lên Quyết định", "Upload một hoặc nhiều file Quyết định (.pdf)")
    pdf_files = st.file_uploader(
        "Upload Quyết định", type=["pdf"], accept_multiple_files=True,
        key="dl_pdf_upload", label_visibility="collapsed",
    )

    divider()
    step_badge(2, "Nhập MSSV", "Mỗi MSSV một dòng, hoặc cách nhau bằng dấu phẩy / khoảng trắng")
    mssv_raw = st.text_area(
        "MSSV", key="dl_mssv_input", height=120, label_visibility="collapsed",
        placeholder="VD:\nHE160001\nSE150234, DE170045",
    )
    # tách MSSV theo xuống dòng / phẩy / chấm phẩy / khoảng trắng, loại trùng & rỗng
    mssv_list = [m for m in dict.fromkeys(
        mssv_raw.replace(",", "\n").replace(";", "\n").split()
    ) if m]

    if pdf_files or mssv_list:
        divider()
        step_badge(3, "Xác nhận dữ liệu")
        mc1, mc2 = st.columns(2)
        with mc1:
            st.markdown(card_metric("File Quyết định", len(pdf_files) if pdf_files else 0,
                                    T['accent'], T['card']), unsafe_allow_html=True)
        with mc2:
            st.markdown(card_metric("MSSV cần tra cứu", len(mssv_list),
                                    T['blue'], T['bbg']), unsafe_allow_html=True)

    divider()
    step_badge(4, "Bắt đầu tra cứu")

    can_run = bool(pdf_files and mssv_list)
    if not can_run:
        st.markdown(f"""<div style="background:{T['ybg']};border:1px solid {T['yellow']}33;
            border-radius:10px;padding:12px 16px">
            <span style="font-size:13px;color:{T['ytxt']}">
                ⚠️ Cần upload ít nhất 1 file Quyết định và nhập ít nhất 1 MSSV</span>
        </div>""", unsafe_allow_html=True)

    if st.button("🔍  Tra cứu", use_container_width=True, disabled=not can_run, key="btn_run"):
        progress = st.progress(0, text="Đang chuẩn bị...")

        progress.progress(0.2, text="Đang đọc file PDF...")
        pdf_data_list = [{"name": f.name, "bytes": f.getvalue()} for f in pdf_files]

        progress.progress(0.4, text="Đang quét các Quyết định...")
        try:
            results = logic.search_mssv_in_pdfs(mssv_list, pdf_data_list)
        except Exception as e:
            st.error(f"❌ Lỗi khi tra cứu: {e}")
            st.stop()

        errors = results.get("_errors", [])

        progress.progress(0.8, text="Đang tổng hợp kết quả...")
        df_summary, df_detail = logic.build_export_data(mssv_list, results)

        # Đếm số QĐ (file) thực sự có hit
        hit_files = set()
        for mssv in mssv_list:
            info = results.get(mssv.strip(), {})
            for h in info.get("hits", []):
                hit_files.add(h["file"])

        found = int((df_summary["Tìm thấy"] == "Có").sum()) if not df_summary.empty else 0
        not_found = int((df_summary["Tìm thấy"] == "Không").sum()) if not df_summary.empty else 0

        st.session_state.dl_summary = df_summary
        st.session_state.dl_detail = df_detail
        st.session_state.dl_errors = errors
        st.session_state.dl_done = True
        st.session_state.dl_stats = {
            "found": found,
            "not_found": not_found,
            "decisions": len(hit_files),
            "files": len(pdf_files),
        }
        progress.progress(1.0, text="✅ Hoàn tất!")
        st.rerun()

# ── TAB 2: KẾT QUẢ ───────────────────────────────────────────
with tabs[1]:
    if not st.session_state.dl_done:
        st.markdown(f"""<div style="text-align:center;padding:80px 20px">
            <div style="font-size:52px;margin-bottom:16px">📭</div>
            <h3 style="font-size:18px;font-weight:700;color:{T['text']};margin-bottom:8px">
                Chưa có kết quả</h3>
            <p style="font-size:13px;color:{T['muted']}">
                Quay lại tab Tra cứu để upload Quyết định và nhập MSSV</p>
        </div>""", unsafe_allow_html=True)
    else:
        stats = st.session_state.dl_stats
        df_summary = st.session_state.dl_summary
        df_detail = st.session_state.dl_detail
        errors = st.session_state.dl_errors

        # Metric cards
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:28px">
            {card_metric("MSSV tìm thấy", stats['found'], T['green'], T['gbg'])}
            {card_metric("MSSV không thấy", stats['not_found'], T['orange'], T['obg'])}
            {card_metric("Số QĐ liên quan", stats['decisions'], T['blue'], T['bbg'])}
            {card_metric("File đã quét", stats['files'], T['accent'], T['card'])}
        </div>""", unsafe_allow_html=True)

        # Cảnh báo file đọc lỗi
        if errors:
            err_lines = "<br>".join(f"• {e['file']}: {e['error']}" for e in errors)
            st.markdown(f"""<div style="background:{T['rbg']};border:1px solid {T['red']}33;
                border-radius:10px;padding:14px 18px;margin-bottom:18px">
                <div style="font-size:12px;font-weight:700;color:{T['rtxt']};margin-bottom:6px">
                    ⚠️ {len(errors)} file không đọc được:</div>
                <div style="font-size:12px;color:{T['muted']};line-height:1.7">{err_lines}</div>
            </div>""", unsafe_allow_html=True)

        # Tabs chi tiết
        detail_tabs = st.tabs(["📋 Tổng hợp", "🔎 Chi tiết theo dòng"])

        with detail_tabs[0]:
            if df_summary is not None and not df_summary.empty:
                st.dataframe(df_summary, use_container_width=True, height=460, hide_index=True)
            else:
                st.info("Không có dữ liệu tổng hợp.")

        with detail_tabs[1]:
            if df_detail is not None and not df_detail.empty:
                st.dataframe(df_detail, use_container_width=True, height=460, hide_index=True)
            else:
                st.info("Không có dữ liệu chi tiết.")

        # Download
        divider()
        excel_bytes = logic.to_excel_bytes(df_summary, df_detail)
        st.download_button(
            label="📥  Tải kết quả tra cứu (.xlsx)",
            data=excel_bytes,
            file_name="KetQua_TraCuu_QuyetDinh.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        if st.button("🔄  Tra cứu mới", key="btn_reset"):
            for k in defaults:
                st.session_state[k] = defaults[k]
            st.rerun()
