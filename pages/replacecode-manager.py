import streamlit as st
import pandas as pd
import io
import base64
import re
import requests
import pdfplumber
import importlib.util
import os

# ── Load logic module ─────────────────────────────────────────────────────────
def load_script_module():
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "replacecode-manager.py")
    script_path = os.path.abspath(script_path)
    spec   = importlib.util.spec_from_file_location("replacecode_manager", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

try:
    rm = load_script_module()
    extract_from_pdf = rm.extract_from_pdf
    merge_database   = rm.merge_database
except Exception as e:
    st.error(f"Không load được scripts/replacecode-manager.py: {e}")
    st.stop()

# ── Helpers ───────────────────────────────────────────────────────────────────
def to_excel_bytes(df):
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    buf.seek(0)
    return buf.getvalue()

def fetch_db_from_github(token, repo):
    url     = f"https://api.github.com/repos/{repo}/contents/output/Database_Tong_Hop.xlsx"
    headers = {"Authorization": f"token {token}"}
    resp    = requests.get(url, headers=headers)
    if resp.status_code == 200:
        content = base64.b64decode(resp.json()["content"])
        sha     = resp.json()["sha"]
        return pd.read_excel(io.BytesIO(content)), sha
    return None, None

def commit_to_github(token, repo, excel_bytes, so_qd, sha=None):
    url     = f"https://api.github.com/repos/{repo}/contents/output/Database_Tong_Hop.xlsx"
    headers = {"Authorization": f"token {token}", "Content-Type": "application/json"}
    payload = {"message": f"chore: update Database_Tong_Hop — QĐ {so_qd}", "content": base64.b64encode(excel_bytes).decode()}
    if sha:
        payload["sha"] = sha
    resp = requests.put(url, json=payload, headers=headers)
    return resp.status_code in [200, 201], resp.json().get("message", "")

def read_raw_rows(pdf_bytes, max_rows=80):
    raw_rows = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for pg_num, page in enumerate(pdf.pages, 1):
            tbl = page.extract_table({"vertical_strategy": "lines", "horizontal_strategy": "lines"})
            if tbl:
                for r_idx, row in enumerate(tbl):
                    raw_rows.append({"page": pg_num, "row_idx": r_idx, "cells": row})
                    if len(raw_rows) >= max_rows:
                        return raw_rows
    return raw_rows

# ── Theme state ───────────────────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ReplaceCode Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
DARK = {
    "bg":       "#0D1117",
    "surface":  "#161B22",
    "surface2": "#21262D",
    "border":   "#30363D",
    "text":     "#E6EDF3",
    "muted":    "#7D8590",
    "accent":   "#00D4AA",
    "accent2":  "#0A9E7F",
    "green":    "#3FB950",
    "red":      "#F85149",
    "blue":     "#58A6FF",
    "badge_applied_bg":  "#1A3A2A",
    "badge_applied_txt": "#3FB950",
    "badge_expired_bg":  "#3A1A1A",
    "badge_expired_txt": "#F85149",
}
LIGHT = {
    "bg":       "#F6F8FA",
    "surface":  "#FFFFFF",
    "surface2": "#F0F2F5",
    "border":   "#D0D7DE",
    "text":     "#1F2328",
    "muted":    "#636C76",
    "accent":   "#0A9E7F",
    "accent2":  "#007A65",
    "green":    "#1A7F37",
    "red":      "#CF222E",
    "blue":     "#0969DA",
    "badge_applied_bg":  "#DAFBE1",
    "badge_applied_txt": "#116329",
    "badge_expired_bg":  "#FFEBE9",
    "badge_expired_txt": "#82071E",
}

T = DARK if st.session_state.theme == "dark" else LIGHT

st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
/* ── Reset & Base ── */
*, *::before, *::after {{ box-sizing: border-box; }}

.stApp {{
    background-color: {T['bg']} !important;
    font-family: 'Outfit', sans-serif !important;
}}

/* Sidebar */
[data-testid="stSidebar"] {{
    background-color: {T['surface']} !important;
    border-right: 1px solid {T['border']} !important;
}}
[data-testid="stSidebar"] * {{
    color: {T['text']} !important;
    font-family: 'Outfit', sans-serif !important;
}}

/* Main text */
.stApp, .stMarkdown, p, span, label, div {{
    color: {T['text']} !important;
    font-family: 'Outfit', sans-serif !important;
}}

/* Hide default Streamlit header */
header[data-testid="stHeader"] {{ display: none !important; }}
.block-container {{ padding-top: 1.5rem !important; max-width: 1400px !important; }}

/* Inputs */
.stTextInput input, .stSelectbox select {{
    background: {T['surface2']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 8px !important;
    color: {T['text']} !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 14px !important;
}}
.stTextInput input:focus {{
    border-color: {T['accent']} !important;
    box-shadow: 0 0 0 3px {T['accent']}22 !important;
}}

/* File uploader */
[data-testid="stFileUploader"] {{
    background: {T['surface2']} !important;
    border: 1.5px dashed {T['border']} !important;
    border-radius: 12px !important;
    transition: border-color 0.2s;
}}
[data-testid="stFileUploader"]:hover {{
    border-color: {T['accent']} !important;
}}

/* Buttons */
.stButton > button {{
    background: {T['accent']} !important;
    color: #0D1117 !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.3px;
}}
.stButton > button:hover {{
    background: {T['accent2']} !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px {T['accent']}44 !important;
}}

/* Download button */
[data-testid="stDownloadButton"] > button {{
    background: {T['surface2']} !important;
    color: {T['text']} !important;
    border: 1px solid {T['border']} !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    transition: all 0.2s ease !important;
}}
[data-testid="stDownloadButton"] > button:hover {{
    border-color: {T['accent']} !important;
    color: {T['accent']} !important;
}}

/* Dataframe */
[data-testid="stDataFrame"] {{
    border: 1px solid {T['border']} !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}}
.dvn-scroller {{ background: {T['surface']} !important; }}

/* Metrics */
[data-testid="stMetric"] {{
    background: {T['surface']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
}}
[data-testid="stMetricLabel"] {{ color: {T['muted']} !important; font-size: 12px !important; font-weight: 500 !important; text-transform: uppercase; letter-spacing: 0.8px; }}
[data-testid="stMetricValue"] {{ color: {T['text']} !important; font-size: 28px !important; font-weight: 700 !important; }}

/* Selectbox */
[data-testid="stSelectbox"] > div > div {{
    background: {T['surface2']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 8px !important;
    color: {T['text']} !important;
}}

/* Alerts */
.stSuccess {{ background: {T['badge_applied_bg']} !important; border-left: 3px solid {T['green']} !important; border-radius: 8px !important; }}
.stError   {{ background: {T['badge_expired_bg']} !important; border-left: 3px solid {T['red']}   !important; border-radius: 8px !important; }}
.stInfo    {{ background: {T['surface2']} !important; border-left: 3px solid {T['blue']} !important; border-radius: 8px !important; }}
.stWarning {{ background: {T['surface2']} !important; border-left: 3px solid #D29922 !important; border-radius: 8px !important; }}

/* Checkbox */
.stCheckbox label {{ color: {T['text']} !important; font-size: 14px !important; }}

/* Spinner */
.stSpinner > div {{ border-top-color: {T['accent']} !important; }}

/* Expander */
[data-testid="stExpander"] {{
    background: {T['surface']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 10px !important;
}}

/* Custom scrollbar */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: {T['surface']}; }}
::-webkit-scrollbar-thumb {{ background: {T['border']}; border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: {T['muted']}; }}
</style>
""", unsafe_allow_html=True)

# ── Custom components ─────────────────────────────────────────────────────────
def card(content_fn, padding="24px"):
    st.markdown(f"""
    <div style="background:{T['surface']};border:1px solid {T['border']};
                border-radius:14px;padding:{padding};margin-bottom:16px;">
    """, unsafe_allow_html=True)
    content_fn()
    st.markdown("</div>", unsafe_allow_html=True)

def section_header(icon, title, subtitle=""):
    sub = f'<p style="color:{T["muted"]};font-size:13px;margin:4px 0 0 0;font-weight:400;">{subtitle}</p>' if subtitle else ""
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;margin:28px 0 16px 0;">
        <span style="font-size:22px;line-height:1">{icon}</span>
        <div>
            <h3 style="margin:0;color:{T['text']};font-size:18px;font-weight:600;letter-spacing:-0.3px">{title}</h3>
            {sub}
        </div>
    </div>
    """, unsafe_allow_html=True)

def badge(text, color_bg, color_txt):
    st.markdown(f"""
    <span style="background:{color_bg};color:{color_txt};padding:3px 10px;
                 border-radius:20px;font-size:12px;font-weight:600;
                 letter-spacing:0.3px;font-family:'Outfit',sans-serif">
        {text}
    </span>
    """, unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo & title
    st.markdown(f"""
    <div style="padding:8px 0 20px 0;border-bottom:1px solid {T['border']};margin-bottom:20px">
        <div style="display:flex;align-items:center;gap:10px">
            <span style="font-size:28px">📚</span>
            <div>
                <div style="font-size:16px;font-weight:700;color:{T['text']};letter-spacing:-0.3px">ReplaceCode</div>
                <div style="font-size:11px;color:{T['muted']};font-weight:500;letter-spacing:0.5px;text-transform:uppercase">Manager</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Theme toggle
    st.markdown(f'<p style="font-size:12px;color:{T["muted"]};font-weight:600;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px">Giao diện</p>', unsafe_allow_html=True)
    col_theme1, col_theme2 = st.columns(2)
    with col_theme1:
        if st.button("☀️ Sáng", use_container_width=True):
            st.session_state.theme = "light"
            st.rerun()
    with col_theme2:
        if st.button("🌙 Tối", use_container_width=True):
            st.session_state.theme = "dark"
            st.rerun()

    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:20px 0"></div>', unsafe_allow_html=True)

    # GitHub config
    st.markdown(f'<p style="font-size:12px;color:{T["muted"]};font-weight:600;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:12px">GitHub</p>', unsafe_allow_html=True)
    try:
        github_token = st.secrets["github"]["token"]
        github_repo  = st.secrets["github"].get("repo", "yenLT31/FE-QA-Tools")
        st.markdown(f"""
        <div style="background:{T['badge_applied_bg']};border:1px solid {T['green']}44;
                    border-radius:8px;padding:10px 14px;margin-bottom:12px">
            <span style="color:{T['green']};font-size:13px;font-weight:600">✓ Token đã cấu hình</span>
        </div>
        """, unsafe_allow_html=True)
    except Exception:
        github_token = ""
        github_repo  = "yenLT31/FE-QA-Tools"
        st.markdown(f"""
        <div style="background:{T['badge_expired_bg']};border:1px solid {T['red']}44;
                    border-radius:8px;padding:10px 14px;margin-bottom:12px">
            <span style="color:{T['red']};font-size:13px;font-weight:600">⚠ Chưa có token</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f'<code style="font-size:11px;color:{T["muted"]};font-family:\'JetBrains Mono\',monospace">{github_repo}</code>', unsafe_allow_html=True)

    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:20px 0"></div>', unsafe_allow_html=True)

    # Debug toggle
    st.markdown(f'<p style="font-size:12px;color:{T["muted"]};font-weight:600;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px">Công cụ</p>', unsafe_allow_html=True)
    debug_mode = st.checkbox("🔍 Debug pdfplumber", value=False)

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="margin-bottom:32px">
    <h1 style="font-size:32px;font-weight:700;color:{T['text']};letter-spacing:-0.8px;margin:0 0 6px 0">
        Quản lý môn tương đương
    </h1>
    <p style="color:{T['muted']};font-size:15px;margin:0;font-weight:400">
        Cập nhật và theo dõi danh sách môn thay thế / tương đương từ Quyết định PDF
    </p>
</div>
""", unsafe_allow_html=True)

# ── Step 1: Upload ────────────────────────────────────────────────────────────
section_header("01", "Tải lên file", "Upload PDF Quyết định và database hiện có")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(f'<p style="font-size:13px;font-weight:600;color:{T["muted"]};text-transform:uppercase;letter-spacing:0.6px;margin-bottom:8px">📄 File PDF Quyết định</p>', unsafe_allow_html=True)
    uploaded_pdf = st.file_uploader("", type=["pdf"], key="pdf_upload", label_visibility="collapsed")
    so_qd_input  = st.text_input("Số Quyết định", value="", placeholder="Tự detect từ tên file nếu để trống")

with col2:
    st.markdown(f'<p style="font-size:13px;font-weight:600;color:{T["muted"]};text-transform:uppercase;letter-spacing:0.6px;margin-bottom:8px">📊 Database hiện có <span style="font-weight:400;font-size:11px">(tùy chọn)</span></p>', unsafe_allow_html=True)
    uploaded_excel = st.file_uploader("", type=["xlsx"], key="excel_upload", label_visibility="collapsed")
    if not uploaded_excel:
        status_txt = "✓ Sẽ tự fetch từ GitHub" if github_token else "⚠ Sẽ tạo database mới"
        status_clr = T['green'] if github_token else "#D29922"
        st.markdown(f'<p style="color:{status_clr};font-size:13px;font-weight:500;margin-top:8px">{status_txt}</p>', unsafe_allow_html=True)

# Debug panel
if debug_mode and uploaded_pdf is not None:
    pdf_bytes_dbg = uploaded_pdf.read()
    uploaded_pdf.seek(0)
    raw_rows = read_raw_rows(pdf_bytes_dbg, max_rows=80)
    with st.expander(f"🔍 Raw pdfplumber — {len(raw_rows)} rows đầu tiên"):
        for item in raw_rows:
            st.markdown(f'<code style="font-size:11px;color:{T["muted"]};font-family:\'JetBrains Mono\',monospace">Trang {item["page"]} | Row {item["row_idx"]}: {item["cells"]}</code>', unsafe_allow_html=True)

# ── Step 2: Process ───────────────────────────────────────────────────────────
section_header("02", "Xử lý dữ liệu", "Trích xuất và merge với database hiện có")

btn_disabled = uploaded_pdf is None
st.markdown(f'<div style="margin-bottom:8px">', unsafe_allow_html=True)
btn_process = st.button(
    "▶  Bắt đầu xử lý" if not btn_disabled else "⬆  Upload PDF trước",
    type="primary",
    disabled=btn_disabled,
    use_container_width=False
)
st.markdown('</div>', unsafe_allow_html=True)

if btn_process:
    with st.spinner("Đang xử lý..."):
        so_qd = so_qd_input.strip()
        if not so_qd:
            match = re.search(r'\d+', uploaded_pdf.name)
            so_qd = match.group() if match else "Unknown"

        pdf_bytes         = uploaded_pdf.read()
        new_rows, skipped = extract_from_pdf(pdf_bytes, so_qd=so_qd)

        existing_df = None
        github_sha  = None

        if uploaded_excel:
            existing_df = pd.read_excel(uploaded_excel)
            st.info(f"Database từ file upload: **{len(existing_df)} dòng**")
        elif github_token:
            existing_df, github_sha = fetch_db_from_github(github_token, github_repo)
            if existing_df is not None:
                st.info(f"Database từ GitHub: **{len(existing_df)} dòng**")
            else:
                st.warning("Chưa có database trên GitHub — sẽ tạo mới")
        else:
            st.warning("Không có database cũ — sẽ tạo mới từ QĐ này")

        final_df = merge_database(existing_df, new_rows)

        st.session_state.update({
            "final_df"   : final_df,
            "existing_df": existing_df,
            "new_rows"   : new_rows,
            "skipped"    : skipped,
            "so_qd"      : so_qd,
            "github_sha" : github_sha,
        })

        st.success(f"✓ Hoàn tất — trích xuất **{len(new_rows)} dòng** từ QĐ {so_qd}")
        if skipped:
            with st.expander(f"⚠  {len(skipped)} dòng bị bỏ qua"):
                st.dataframe(pd.DataFrame(skipped), use_container_width=True)

# ── Step 3: Results ───────────────────────────────────────────────────────────
if "final_df" in st.session_state:
    final_df    = st.session_state["final_df"]
    existing_df = st.session_state["existing_df"]
    new_rows    = st.session_state["new_rows"]
    so_qd       = st.session_state["so_qd"]
    github_sha  = st.session_state["github_sha"]

    section_header("03", "Kết quả", f"QĐ {so_qd} — {len(final_df)} bản ghi tổng")

    # Metrics
    old_pairs  = set(zip(existing_df["SubjectCode"], existing_df["Replacecode"])) if existing_df is not None else set()
    n_applied  = int((final_df["replace_status"] == "applied").sum())
    n_expired  = int((final_df["replace_status"] == "expired").sum())
    n_new      = sum(1 for r in new_rows if (r["SubjectCode"], r["Replacecode"]) not in old_pairs)
    n_updated  = len(new_rows) - n_new

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Tổng bản ghi",     len(final_df))
    m2.metric("Đang hiệu lực",    n_applied)
    m3.metric("Hết hiệu lực",     n_expired)
    m4.metric("Thêm mới",         n_new)
    m5.metric("Cập nhật",         n_updated)

    st.markdown(f'<div style="height:20px"></div>', unsafe_allow_html=True)

    # Filters
    col_f1, col_f2, col_f3 = st.columns([1, 1, 2])
    with col_f1:
        filter_status = st.selectbox("Trạng thái", ["Tất cả", "applied", "expired"], label_visibility="visible")
    with col_f2:
        filter_equiv = st.selectbox("Hình thức", ["Tất cả", "Tương đương", "Thay thế"])
    with col_f3:
        search_code = st.text_input("Tìm mã môn", placeholder="VD: IOT102, NWC303...")

    display_df = final_df.copy()
    if filter_status != "Tất cả":
        display_df = display_df[display_df["replace_status"] == filter_status]
    if filter_equiv == "Tương đương":
        display_df = display_df[display_df["equivalent"] == "TRUE"]
    elif filter_equiv == "Thay thế":
        display_df = display_df[display_df["equivalent"] == "FALSE"]
    if search_code.strip():
        kw = search_code.strip().upper()
        display_df = display_df[
            display_df["SubjectCode"].str.upper().str.contains(kw, na=False) |
            display_df["Replacecode"].str.upper().str.contains(kw, na=False)
        ]

    st.markdown(f'<p style="color:{T["muted"]};font-size:12px;margin-bottom:8px">Hiển thị <b style="color:{T["text"]}">{len(display_df)}</b> / {len(final_df)} bản ghi</p>', unsafe_allow_html=True)
    st.dataframe(display_df, use_container_width=True, height=380)

    # ── Step 4: Save ──────────────────────────────────────────────────────────
    section_header("04", "Lưu dữ liệu", "Tải về máy hoặc đồng bộ lên GitHub")

    excel_bytes = to_excel_bytes(final_df)
    col_dl, col_gh, col_empty = st.columns([1, 1, 2])

    with col_dl:
        st.download_button(
            label     = "⬇  Tải về máy (.xlsx)",
            data      = excel_bytes,
            file_name = "Database_Tong_Hop.xlsx",
            mime      = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with col_gh:
        if st.button("☁  Commit lên GitHub", type="primary", use_container_width=True):
            if not github_token:
                st.error("Chưa cấu hình GitHub Token")
            else:
                with st.spinner("Đang commit..."):
                    ok, msg = commit_to_github(github_token, github_repo, excel_bytes, so_qd, sha=github_sha)
                if ok:
                    st.success(f"✓ Commit thành công — QĐ {so_qd}")
                    _, new_sha = fetch_db_from_github(github_token, github_repo)
                    st.session_state["github_sha"] = new_sha
                else:
                    st.error(f"Lỗi: {msg}")
