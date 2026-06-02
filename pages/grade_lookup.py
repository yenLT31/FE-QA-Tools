import streamlit as st
import importlib.util
import pandas as pd
import os
import io

# ============================================================
#  LOAD LOGIC
#  ⚠️ Nếu file script của bạn tên khác 'grade_lookup.py',
#     đổi tên file ở dòng dưới cho khớp.
# ============================================================
SCRIPT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'scripts', 'grade_lookup.py')
)
_load_error = None
logic = None
try:
    spec = importlib.util.spec_from_file_location("grade_lookup", SCRIPT_PATH)
    logic = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(logic)
except Exception as e:
    _load_error = e

# ============================================================
#  PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Grade Lookup | FE QA Tools",
    page_icon="📊",
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
    "gl_result": None, "gl_not_found": [], "gl_info": {},
    "gl_done": False, "gl_stats": {},
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


def extract_mssv_from_file(f):
    """Trích danh sách MSSV từ file .txt / .csv / .xlsx (loại trùng, giữ thứ tự)."""
    name = f.name.lower()
    if name.endswith(".txt"):
        text = f.getvalue().decode("utf-8", errors="ignore")
        tokens = text.replace(",", "\n").replace(";", "\n").split()
        return [t for t in dict.fromkeys(tokens) if t]
    try:
        if name.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(f.getvalue()), dtype=str)
        else:
            df = pd.read_excel(io.BytesIO(f.getvalue()), dtype=str)
    except Exception:
        return []
    if df.empty:
        return []
    col_idx = logic.detect_mssv_col(list(df.columns))
    series = df.iloc[:, col_idx] if col_idx >= 0 else df.iloc[:, 0]
    vals = [str(v).strip() for v in series.dropna().tolist()]
    return [v for v in dict.fromkeys(vals) if v and v.lower() != "nan"]


@st.cache_data(show_spinner=False)
def clean_cached(file_bytes, file_name):
    """Đọc + làm sạch file điểm (cache theo nội dung file để khỏi xử lý lại mỗi rerun)."""
    return logic.load_and_clean(file_bytes)


# ============================================================
#  SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(f"""
    <div style="padding:16px 0 20px;border-bottom:1px solid {T['border']};margin-bottom:20px">
        <div style="display:flex;align-items:center;gap:10px">
            <div style="width:36px;height:36px;border-radius:10px;
                        background:linear-gradient(135deg,{T['accent']},{T['accent_dim']});
                        display:flex;align-items:center;justify-content:center;font-size:18px">📊</div>
            <div>
                <div style="font-size:14px;font-weight:800;color:{T['accent']}">Grade Lookup</div>
                <div style="font-size:10px;color:{T['muted']};font-weight:600;letter-spacing:.8px;
                            text-transform:uppercase">Tra cứu điểm sinh viên</div>
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
        <div>① Upload file điểm (Excel)</div>
        <div>② Nhập / tải MSSV cần tra</div>
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
                    display:flex;align-items:center;justify-content:center;font-size:22px">📊</div>
        <div>
            <h1 style="font-size:26px;font-weight:800;color:{T['text']};margin:0;line-height:1.2">
                Grade Lookup</h1>
            <p style="font-size:13px;color:{T['muted']};margin:0">
                Tra cứu điểm sinh viên từ file điểm thô — tự làm sạch, chuẩn hóa ngày, giữ lần học gần nhất</p>
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
            ❌ Không nạp được <code>scripts/grade_lookup.py</code>: {_load_error}</span>
    </div>""", unsafe_allow_html=True)
    st.stop()


# ============================================================
#  TABS
# ============================================================
tabs = st.tabs(["🔍  Tra cứu", "📊  Kết quả"])

# ── TAB 1: TRA CỨU ───────────────────────────────────────────
with tabs[0]:
    step_badge(1, "Tải lên file điểm", "Upload file điểm thô (.xlsx / .xls) — có thể gồm nhiều sheet")
    grade_file = st.file_uploader(
        "Upload file điểm", type=["xlsx", "xls"], accept_multiple_files=False,
        key="gl_grade_file", label_visibility="collapsed",
    )

    divider()
    step_badge(2, "Nhập MSSV", "Nhập tay, hoặc tải file (.txt / .csv / .xlsx) chứa MSSV")

    input_mode = st.radio(
        "Cách nhập MSSV", ["✍️ Nhập tay", "📂 Tải file"],
        horizontal=True, key="gl_input_mode", label_visibility="collapsed",
    )

    mssv_list = []
    if input_mode == "✍️ Nhập tay":
        mssv_raw = st.text_area(
            "MSSV", key="gl_mssv_input", height=120, label_visibility="collapsed",
            placeholder="VD:\nSE190936\nSE173492, HE160001",
        )
        mssv_list = [m for m in dict.fromkeys(
            mssv_raw.replace(",", "\n").replace(";", "\n").split()
        ) if m]
    else:
        mssv_file = st.file_uploader(
            "File MSSV", type=["txt", "csv", "xlsx", "xls"],
            key="gl_mssv_file", label_visibility="collapsed",
        )
        if mssv_file is not None:
            mssv_list = extract_mssv_from_file(mssv_file)
            if mssv_list:
                st.markdown(f"""<div style="background:{T['gbg']};border:1px solid {T['green']}33;
                    border-radius:10px;padding:10px 14px;margin-top:8px">
                    <span style="font-size:12.5px;color:{T['gtxt']};font-weight:600">
                        ✅ Đã đọc {len(mssv_list)} MSSV từ file</span></div>""",
                    unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style="background:{T['ybg']};border:1px solid {T['yellow']}33;
                    border-radius:10px;padding:10px 14px;margin-top:8px">
                    <span style="font-size:12.5px;color:{T['ytxt']}">
                        ⚠️ Chưa đọc được MSSV nào. File .csv/.xlsx nên có cột tiêu đề "MSSV" /
                        "RollNumber", hoặc dùng .txt mỗi dòng 1 MSSV.</span></div>""",
                    unsafe_allow_html=True)

    if grade_file is not None or mssv_list:
        divider()
        step_badge(3, "Xác nhận dữ liệu")
        mc1, mc2 = st.columns(2)
        with mc1:
            st.markdown(card_metric("File điểm", "1" if grade_file is not None else "0",
                                    T['accent'], T['card']), unsafe_allow_html=True)
        with mc2:
            st.markdown(card_metric("MSSV cần tra cứu", len(mssv_list),
                                    T['blue'], T['bbg']), unsafe_allow_html=True)

    divider()
    step_badge(4, "Bắt đầu tra cứu")

    can_run = bool(grade_file is not None and mssv_list)
    if not can_run:
        st.markdown(f"""<div style="background:{T['ybg']};border:1px solid {T['yellow']}33;
            border-radius:10px;padding:12px 16px">
            <span style="font-size:13px;color:{T['ytxt']}">
                ⚠️ Cần upload file điểm và nhập ít nhất 1 MSSV</span>
        </div>""", unsafe_allow_html=True)

    if st.button("🔍  Tra cứu", use_container_width=True, disabled=not can_run, key="btn_run"):
        progress = st.progress(0, text="Đang chuẩn bị...")

        progress.progress(0.3, text="Đang đọc & làm sạch file điểm...")
        try:
            clean_df, info = clean_cached(grade_file.getvalue(), grade_file.name)
        except Exception as e:
            st.error(f"❌ Lỗi khi đọc file điểm: {e}")
            st.stop()

        if clean_df is None or clean_df.empty:
            st.error("❌ File điểm không có dữ liệu hợp lệ.")
            st.stop()

        progress.progress(0.7, text="Đang tra cứu MSSV...")
        distinct = list(dict.fromkeys(m.strip() for m in mssv_list if m and m.strip()))
        result, not_found = logic.lookup_grades(clean_df, distinct)

        total_credits = 0
        if "Credits" in result.columns:
            total_credits = int(pd.to_numeric(result["Credits"], errors="coerce")
                                 .fillna(0).sum())

        st.session_state.gl_result = result
        st.session_state.gl_not_found = not_found
        st.session_state.gl_info = info
        st.session_state.gl_done = True
        st.session_state.gl_stats = {
            "found": len(distinct) - len(not_found),
            "not_found": len(not_found),
            "subjects": len(result),
            "credits": total_credits,
        }
        progress.progress(1.0, text="✅ Hoàn tất!")
        st.rerun()

# ── TAB 2: KẾT QUẢ ───────────────────────────────────────────
with tabs[1]:
    if not st.session_state.gl_done:
        st.markdown(f"""<div style="text-align:center;padding:80px 20px">
            <div style="font-size:52px;margin-bottom:16px">📭</div>
            <h3 style="font-size:18px;font-weight:700;color:{T['text']};margin-bottom:8px">
                Chưa có kết quả</h3>
            <p style="font-size:13px;color:{T['muted']}">
                Quay lại tab Tra cứu để upload file điểm và nhập MSSV</p>
        </div>""", unsafe_allow_html=True)
    else:
        stats = st.session_state.gl_stats
        result = st.session_state.gl_result
        not_found = st.session_state.gl_not_found
        info = st.session_state.gl_info or {}

        # Banner thông tin xử lý dữ liệu (minh bạch định dạng ngày)
        st.markdown(f"""<div style="background:{T['bbg']};border:1px solid {T['blue']}33;
            border-radius:10px;padding:12px 16px;margin-bottom:20px">
            <span style="font-size:12.5px;color:{T['btxt']};line-height:1.7">
                🗓️ Định dạng ngày nhận diện: <strong>{info.get('date_format','?')}</strong>
                (căn cứ: {info.get('date_resolved_by','?')}) &nbsp;·&nbsp;
                Đã xử lý <strong>{info.get('raw_rows','?')}</strong> dòng →
                giữ <strong>{info.get('rows','?')}</strong> dòng
                (loại {info.get('removed_dup','?')} dòng trùng môn) &nbsp;·&nbsp;
                <strong>{info.get('students','?')}</strong> SV trong dữ liệu</span>
        </div>""", unsafe_allow_html=True)

        # Metric cards
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:28px">
            {card_metric("MSSV tìm thấy", stats['found'], T['green'], T['gbg'])}
            {card_metric("MSSV không thấy", stats['not_found'], T['orange'], T['obg'])}
            {card_metric("Tổng số môn", stats['subjects'], T['blue'], T['bbg'])}
            {card_metric("Tổng tín chỉ", stats['credits'], T['accent'], T['card'])}
        </div>""", unsafe_allow_html=True)

        if result is not None and not result.empty:
            st.dataframe(result, use_container_width=True, height=460, hide_index=True)
        else:
            st.markdown(f"""<div style="background:{T['obg']};border:1px solid {T['orange']}33;
                border-radius:10px;padding:16px;text-align:center">
                <span style="color:{T['otxt']};font-size:13px;font-weight:600">
                    Không tìm thấy điểm cho các MSSV đã nhập</span>
            </div>""", unsafe_allow_html=True)

        if not_found:
            st.markdown(f"""<div style="background:{T['ybg']};border:1px solid {T['yellow']}33;
                border-radius:10px;padding:14px 18px;margin-top:16px">
                <div style="font-size:12px;font-weight:700;color:{T['ytxt']};margin-bottom:6px">
                    ⚠️ {len(not_found)} MSSV không có trong file điểm:</div>
                <div style="font-size:12.5px;color:{T['muted']};line-height:1.7">
                    {", ".join(not_found)}</div>
            </div>""", unsafe_allow_html=True)

        # Download
        divider()
        excel_bytes = logic.to_excel_bytes(result, not_found)
        st.download_button(
            label="📥  Tải bảng điểm tra cứu (.xlsx)",
            data=excel_bytes,
            file_name="BangDiem_TraCuu.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        if st.button("🔄  Tra cứu mới", key="btn_reset"):
            for k in defaults:
                st.session_state[k] = defaults[k]
            st.rerun()
