import streamlit as st
import pandas as pd
import io, base64, re, requests, os
import pdfplumber
import importlib.util

# ── Load logic ────────────────────────────────────────────────────────────────
def load_script_module():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "replacecode-manager.py"))
    spec = importlib.util.spec_from_file_location("rm", path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

try:
    rm               = load_script_module()
    extract_from_pdf = rm.extract_from_pdf
    merge_database   = rm.merge_database
except Exception as e:
    st.error(f"Không load được scripts/replacecode-manager.py: {e}")
    st.stop()

# ── Helpers ───────────────────────────────────────────────────────────────────
def to_excel_bytes(df):
    buf = io.BytesIO(); df.to_excel(buf, index=False); buf.seek(0); return buf.getvalue()

def fetch_db_from_github(token, repo):
    resp = requests.get(
        f"https://api.github.com/repos/{repo}/contents/output/Database_Tong_Hop.xlsx",
        headers={"Authorization": f"token {token}"}
    )
    if resp.status_code == 200:
        d = resp.json()
        return pd.read_excel(io.BytesIO(base64.b64decode(d["content"]))), d["sha"]
    return None, None

def commit_to_github(token, repo, excel_bytes, so_qd, sha=None):
    payload = {
        "message": f"chore: update database QD {so_qd}",
        "content": base64.b64encode(excel_bytes).decode()
    }
    if sha: payload["sha"] = sha
    resp = requests.put(
        f"https://api.github.com/repos/{repo}/contents/output/Database_Tong_Hop.xlsx",
        json=payload,
        headers={"Authorization": f"token {token}", "Content-Type": "application/json"}
    )
    return resp.status_code in [200, 201], resp.json().get("message", "")

def read_raw_rows(pdf_bytes, max_rows=80):
    rows = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for pg, page in enumerate(pdf.pages, 1):
            tbl = page.extract_table({"vertical_strategy": "lines", "horizontal_strategy": "lines"})
            if tbl:
                for i, row in enumerate(tbl):
                    rows.append({"page": pg, "row": i, "cells": row})
                    if len(rows) >= max_rows: return rows
    return rows

# ── Theme ─────────────────────────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

DARK = dict(
    bg="#080D18", card="#0F1628", card2="#162040", border="#1E2D4A",
    text="#E8EDF5", muted="#8892A4", accent="#00D4AA", accent_dim="#00A882",
    green="#22C55E", red="#EF4444", blue="#60A5FA",
    gbg="#052E16", gtxt="#22C55E", rbg="#2D0A0A", rtxt="#EF4444",
)
LIGHT = dict(
    bg="#F0F4F8", card="#FFFFFF", card2="#F7F9FC", border="#E2E8F0",
    text="#1A2540", muted="#64748B", accent="#0A9E7F", accent_dim="#077A62",
    green="#16A34A", red="#DC2626", blue="#2563EB",
    gbg="#DCFCE7", gtxt="#15803D", rbg="#FEE2E2", rtxt="#991B1B",
)
T = DARK if st.session_state.theme == "dark" else LIGHT

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="ReplaceCode Manager", page_icon="📋", layout="wide")

# ── Fonts ─────────────────────────────────────────────────────────────────────
st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">',
    unsafe_allow_html=True
)

# ── CSS vars ──────────────────────────────────────────────────────────────────
st.markdown(f"""<style>:root{{
--bg:{T['bg']};--card:{T['card']};--card2:{T['card2']};--border:{T['border']};
--text:{T['text']};--muted:{T['muted']};--accent:{T['accent']};--adim:{T['accent_dim']};
--green:{T['green']};--red:{T['red']};--blue:{T['blue']};
--gbg:{T['gbg']};--gtxt:{T['gtxt']};--rbg:{T['rbg']};--rtxt:{T['rtxt']};
}}</style>""", unsafe_allow_html=True)

# ── CSS rules — KHÔNG override font toàn cục (giữ Material Icons của Streamlit) ──
st.markdown("""<style>
/* App background */
.stApp { background: var(--bg) !important; }
header[data-testid="stHeader"] { display: none !important; }
.block-container { padding-top: 0 !important; max-width: 1300px !important; }

/* Sidebar */
[data-testid="stSidebar"] { background: var(--card) !important; border-right: 1px solid var(--border) !important; }

/* Typography — CHỈ target text elements, không phải icon */
.stMarkdown p, .stMarkdown span, .stMarkdown div,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
[data-testid="stMetricLabel"] span,
.stTextInput label {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: var(--text) !important;
}

/* Text input */
.stTextInput input {
    background: var(--card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
    transition: border-color .2s, box-shadow .2s;
}
.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,212,170,.12) !important;
}
.stTextInput input::placeholder { color: var(--muted) !important; }

/* File uploader — ẩn label bị duplicate */
[data-testid="stFileUploader"] {
    background: var(--card2) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: 14px !important;
    transition: border-color .2s !important;
}
[data-testid="stFileUploader"]:hover { border-color: var(--accent) !important; }
[data-testid="stFileUploaderDropzone"] { background: transparent !important; }
/* Ẩn label text thừa của file uploader */
[data-testid="stFileUploader"] > label { display: none !important; }

/* Buttons */
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
.stButton > button:disabled {
    background: var(--card2) !important;
    color: var(--muted) !important;
    transform: none !important;
    box-shadow: none !important;
}

/* Download button */
[data-testid="stDownloadButton"] > button {
    background: var(--card2) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    padding: 10px 22px !important;
    transition: all .2s;
}
[data-testid="stDownloadButton"] > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 18px 20px !important;
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 11px !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: .8px; }
[data-testid="stMetricValue"] { color: var(--text) !important; font-size: 28px !important; font-weight: 800 !important; }

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
    background: var(--card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

/* Dataframe */
[data-testid="stDataFrame"] { border: 1px solid var(--border) !important; border-radius: 14px !important; overflow: hidden !important; }

/* Alerts */
.stSuccess { background: var(--gbg) !important; border-left: 3px solid var(--green) !important; border-radius: 10px !important; }
.stError   { background: var(--rbg) !important; border-left: 3px solid var(--red)   !important; border-radius: 10px !important; }
.stInfo    { background: var(--card2) !important; border-left: 3px solid var(--blue) !important; border-radius: 10px !important; }
.stWarning { background: var(--card2) !important; border-left: 3px solid #D97706    !important; border-radius: 10px !important; }

/* Expander */
[data-testid="stExpander"] { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; }

/* Checkbox */
.stCheckbox span { color: var(--text) !important; font-size: 13px !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--card); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted); }
</style>""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:16px 0 20px;border-bottom:1px solid {T['border']};margin-bottom:20px">
        <div style="font-size:15px;font-weight:800;color:{T['accent']};letter-spacing:-.3px">📋 ReplaceCode</div>
        <div style="font-size:10px;color:{T['muted']};font-weight:600;letter-spacing:.9px;text-transform:uppercase;margin-top:2px">Manager</div>
    </div>
    <p style="font-size:10px;color:{T['muted']};font-weight:700;letter-spacing:.9px;text-transform:uppercase;margin-bottom:8px">Giao diện</p>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("☀ Sáng", use_container_width=True, key="btn_light"):
            st.session_state.theme = "light"; st.rerun()
    with c2:
        if st.button("🌙 Tối", use_container_width=True, key="btn_dark"):
            st.session_state.theme = "dark"; st.rerun()

    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:18px 0"></div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:10px;color:{T["muted"]};font-weight:700;letter-spacing:.9px;text-transform:uppercase;margin-bottom:10px">GitHub</p>', unsafe_allow_html=True)

    try:
        github_token = st.secrets["github"]["token"]
        github_repo  = st.secrets["github"].get("repo", "yenLT31/FE-QA-Tools")
        st.markdown(f'<div style="background:{T["gbg"]};border:1px solid {T["green"]}33;border-radius:10px;padding:9px 13px;margin-bottom:10px"><span style="color:{T["green"]};font-size:13px;font-weight:600">● Token đã cấu hình</span></div>', unsafe_allow_html=True)
    except Exception:
        github_token, github_repo = "", "yenLT31/FE-QA-Tools"
        st.markdown(f'<div style="background:{T["rbg"]};border:1px solid {T["red"]}33;border-radius:10px;padding:9px 13px;margin-bottom:10px"><span style="color:{T["red"]};font-size:13px;font-weight:600">⚠ Chưa có token</span></div>', unsafe_allow_html=True)

    st.markdown(f'<code style="font-size:11px;color:{T["muted"]}">{github_repo}</code>', unsafe_allow_html=True)
    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:18px 0"></div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:10px;color:{T["muted"]};font-weight:700;letter-spacing:.9px;text-transform:uppercase;margin-bottom:8px">Công cụ</p>', unsafe_allow_html=True)
    debug_mode = st.checkbox("🔍 Debug pdfplumber", value=False)

# ── Helpers UI ────────────────────────────────────────────────────────────────
def divider():
    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:24px 0"></div>', unsafe_allow_html=True)

def step_label(num, title, sub=""):
    sub_html = f'<div style="font-size:12px;color:{T["muted"]};margin-top:2px">{sub}</div>' if sub else ""
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:18px">
        <div style="background:linear-gradient(135deg,{T['accent']},{T['accent_dim']});color:#080D18;
                    font-size:11px;font-weight:800;border-radius:8px;padding:5px 10px;
                    letter-spacing:.5px;flex-shrink:0;font-family:'Plus Jakarta Sans',sans-serif">{num}</div>
        <div>
            <div style="font-size:16px;font-weight:700;color:{T['text']};letter-spacing:-.3px;
                        font-family:'Plus Jakarta Sans',sans-serif">{title}</div>
            {sub_html}
        </div>
    </div>""", unsafe_allow_html=True)

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:{T['card']};border-bottom:1px solid {T['border']};
            padding:28px 0 24px;margin:-1rem 0 0">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
        <span style="color:{T['accent']};font-size:12px;font-weight:700;letter-spacing:.9px;
                     text-transform:uppercase;font-family:'Plus Jakarta Sans',sans-serif">ReplaceCode Manager</span>
        <span style="background:{T['gbg']};color:{T['gtxt']};font-size:11px;font-weight:700;
                     padding:2px 9px;border-radius:20px;font-family:'Plus Jakarta Sans',sans-serif">● LIVE</span>
    </div>
    <h1 style="font-size:26px;font-weight:800;color:{T['text']};letter-spacing:-.5px;margin:0 0 6px;
               font-family:'Plus Jakarta Sans',sans-serif">Quản lý môn tương đương</h1>
    <p style="color:{T['muted']};font-size:14px;margin:0;font-family:'Plus Jakarta Sans',sans-serif">
        Cập nhật danh sách môn thay thế / tương đương từ Quyết định PDF
    </p>
</div>
<div style="height:28px"></div>
""", unsafe_allow_html=True)

# ── 01 Upload ─────────────────────────────────────────────────────────────────
step_label("01", "Tải lên file", "Upload PDF Quyết định và database hiện có")

col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown(f'<p style="font-size:11px;font-weight:700;color:{T["muted"]};text-transform:uppercase;letter-spacing:.7px;margin-bottom:6px;font-family:\'Plus Jakarta Sans\',sans-serif">📄 File PDF Quyết định</p>', unsafe_allow_html=True)
    uploaded_pdf  = st.file_uploader("PDF Quyết định", type=["pdf"], key="pdf_upload")
    so_qd_input   = st.text_input("Số Quyết định", placeholder="Tự detect từ tên file nếu để trống")

with col2:
    st.markdown(f'<p style="font-size:11px;font-weight:700;color:{T["muted"]};text-transform:uppercase;letter-spacing:.7px;margin-bottom:6px;font-family:\'Plus Jakarta Sans\',sans-serif">📊 Database hiện có (tùy chọn)</p>', unsafe_allow_html=True)
    uploaded_excel = st.file_uploader("Database Excel", type=["xlsx"], key="excel_upload")
    if not uploaded_excel:
        clr = T['green'] if github_token else "#D97706"
        txt = "● Tự fetch từ GitHub" if github_token else "⚠ Sẽ tạo database mới"
        st.markdown(f'<p style="color:{clr};font-size:13px;font-weight:500;margin-top:6px;font-family:\'Plus Jakarta Sans\',sans-serif">{txt}</p>', unsafe_allow_html=True)

if debug_mode and uploaded_pdf:
    b = uploaded_pdf.read(); uploaded_pdf.seek(0)
    rows = read_raw_rows(b)
    with st.expander(f"🔍 Raw pdfplumber — {len(rows)} rows"):
        for r in rows:
            st.code(f"T{r['page']} R{r['row']}: {r['cells']}", language=None)

divider()

# ── 02 Process ────────────────────────────────────────────────────────────────
step_label("02", "Xử lý dữ liệu", "Trích xuất và merge với database hiện có")

btn_process = st.button(
    "▶  Bắt đầu xử lý" if uploaded_pdf else "⬆  Upload PDF trước",
    type="primary", disabled=not uploaded_pdf
)

if btn_process:
    with st.spinner("Đang xử lý..."):
        so_qd = so_qd_input.strip()
        if not so_qd:
            m = re.search(r'\d+', uploaded_pdf.name)
            so_qd = m.group() if m else "Unknown"

        pdf_bytes          = uploaded_pdf.read()
        new_rows, skipped  = extract_from_pdf(pdf_bytes, so_qd=so_qd)
        existing_df, github_sha = None, None

        if uploaded_excel:
            existing_df = pd.read_excel(uploaded_excel)
            st.info(f"Database từ file upload: **{len(existing_df)} dòng**")
        elif github_token:
            existing_df, github_sha = fetch_db_from_github(github_token, github_repo)
            if existing_df is not None:
                st.info(f"Database từ GitHub: **{len(existing_df)} dòng**")
            else:
                st.warning("Chưa có database — sẽ tạo mới")
        else:
            st.warning("Không có database cũ — sẽ tạo mới từ QĐ này")

        final_df = merge_database(existing_df, new_rows)
        st.session_state.update(dict(
            final_df=final_df, existing_df=existing_df,
            new_rows=new_rows, skipped=skipped,
            so_qd=so_qd, github_sha=github_sha
        ))
        st.success(f"✓ Hoàn tất — trích xuất **{len(new_rows)} dòng** từ QĐ {so_qd}")
        if skipped:
            with st.expander(f"⚠  {len(skipped)} dòng bị bỏ qua"):
                st.dataframe(pd.DataFrame(skipped), use_container_width=True)

# ── 03 Results ────────────────────────────────────────────────────────────────
if "final_df" in st.session_state:
    fd  = st.session_state["final_df"]
    ed  = st.session_state["existing_df"]
    nr  = st.session_state["new_rows"]
    qd  = st.session_state["so_qd"]
    sha = st.session_state["github_sha"]

    divider()
    step_label("03", "Kết quả", f"QĐ {qd} — tổng {len(fd)} bản ghi")

    old_pairs = set(zip(ed["SubjectCode"], ed["Replacecode"])) if ed is not None else set()
    n_app = int((fd["replace_status"] == "applied").sum())
    n_exp = int((fd["replace_status"] == "expired").sum())
    n_new = sum(1 for r in nr if (r["SubjectCode"], r["Replacecode"]) not in old_pairs)

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Tổng bản ghi",  len(fd))
    m2.metric("Đang hiệu lực", n_app)
    m3.metric("Hết hiệu lực",  n_exp)
    m4.metric("Thêm mới",      n_new)
    m5.metric("Cập nhật",      len(nr) - n_new)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    f1, f2, f3 = st.columns([1, 1, 2])
    with f1: fs = st.selectbox("Trạng thái", ["Tất cả", "applied", "expired"])
    with f2: fe = st.selectbox("Hình thức",  ["Tất cả", "Tương đương", "Thay thế"])
    with f3: fk = st.text_input("Tìm mã môn", placeholder="VD: IOT102, NWC303...")

    df = fd.copy()
    if fs != "Tất cả": df = df[df["replace_status"] == fs]
    if fe == "Tương đương": df = df[df["equivalent"] == "TRUE"]
    elif fe == "Thay thế":  df = df[df["equivalent"] == "FALSE"]
    if fk.strip():
        k = fk.strip().upper()
        df = df[
            df["SubjectCode"].str.upper().str.contains(k, na=False) |
            df["Replacecode"].str.upper().str.contains(k, na=False)
        ]

    st.markdown(f'<p style="color:{T["muted"]};font-size:12px;margin-bottom:8px">Hiển thị <b style="color:{T["text"]}">{len(df)}</b> / {len(fd)} bản ghi</p>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, height=380)

    divider()

    # ── 04 Save ───────────────────────────────────────────────────────────────
    step_label("04", "Lưu dữ liệu", "Tải về máy hoặc đồng bộ lên GitHub")

    xb = to_excel_bytes(fd)
    cl, cg, _ = st.columns([1, 1, 2])
    with cl:
        st.download_button(
            "⬇  Tải về máy (.xlsx)", data=xb,
            file_name="Database_Tong_Hop.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    with cg:
        if st.button("☁  Commit lên GitHub", type="primary", use_container_width=True):
            if not github_token:
                st.error("Chưa cấu hình GitHub Token")
            else:
                with st.spinner("Đang commit..."):
                    ok, msg = commit_to_github(github_token, github_repo, xb, qd, sha=sha)
                if ok:
                    st.success(f"✓ Commit thành công — QĐ {qd}")
                    _, new_sha = fetch_db_from_github(github_token, github_repo)
                    st.session_state["github_sha"] = new_sha
                else:
                    st.error(f"Lỗi: {msg}")

    st.markdown(f'<div style="text-align:center;padding:32px 0 8px"><span style="color:{T["muted"]};font-size:12px">© 2026 YenLT31 — FPT Education QA Department</span></div>', unsafe_allow_html=True)
