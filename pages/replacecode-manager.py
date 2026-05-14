import streamlit as st
import pandas as pd
import io
import base64
import re
import requests
import pdfplumber
import importlib.util
import sys
import os

# ── Import logic tu scripts/replacecode-manager.py ───────────────────────────
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
    st.error(f"Khong load duoc scripts/replacecode-manager.py: {e}")
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
    payload = {
        "message": f"Update Database_Tong_Hop.xlsx - QD {so_qd}",
        "content": base64.b64encode(excel_bytes).decode()
    }
    if sha:
        payload["sha"] = sha
    resp = requests.put(url, json=payload, headers=headers)
    return resp.status_code in [200, 201], resp.json().get("message", "")


def read_raw_rows(pdf_bytes, max_rows=60):
    """Doc raw rows tu pdfplumber de debug."""
    raw_rows = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for pg_num, page in enumerate(pdf.pages, 1):
            tbl = page.extract_table({
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines"
            })
            if tbl:
                for r_idx, row in enumerate(tbl):
                    raw_rows.append({
                        "page"   : pg_num,
                        "row_idx": r_idx,
                        "cells"  : row
                    })
                    if len(raw_rows) >= max_rows:
                        return raw_rows
    return raw_rows


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="ReplaceCode Manager", page_icon="📚", layout="wide")

st.title("📚 ReplaceCode Manager")
st.caption("Cap nhat danh sach mon tuong duong / thay the tu Quyet dinh PDF")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("GitHub")
    try:
        github_token = st.secrets["github"]["token"]
        github_repo  = st.secrets["github"].get("repo", "yenLT31/FE-QA-Tools")
        st.success("Token da cau hinh")
    except Exception:
        github_token = ""
        github_repo  = "yenLT31/FE-QA-Tools"
        st.warning("Chua co GitHub Token trong secrets")

    st.caption(f"Repo: `{github_repo}`")
    st.markdown("---")
    st.markdown(
        "**Cach them Token:**\n"
        "Vao App Settings > Secrets > them:\n"
        "```toml\n[github]\ntoken = \"ghp_...\"\nrepo  = \"yenLT31/FE-QA-Tools\"\n```"
    )

# ── Step 1: Upload ────────────────────────────────────────────────────────────
st.header("1. Tai len file")

col1, col2 = st.columns(2)

with col1:
    st.subheader("File PDF Quyet dinh moi")
    uploaded_pdf = st.file_uploader("Chon file PDF", type=["pdf"], key="pdf_upload")
    so_qd_input  = st.text_input(
        "So QD",
        value="",
        placeholder="De trong -> tu lay so tu ten file",
        help="VD: 498"
    )

with col2:
    st.subheader("Database hien co (tuy chon)")
    uploaded_excel = st.file_uploader(
        "Upload Database_Tong_Hop.xlsx",
        type=["xlsx"],
        key="excel_upload",
        help="Neu khong upload, he thong tu lay tu GitHub output/"
    )
    if not uploaded_excel and github_token:
        st.caption("Se tu fetch tu GitHub neu khong upload")
    elif not uploaded_excel and not github_token:
        st.caption("Khong co database -> se tao moi tu QD nay")

# ── Step 2: Process ───────────────────────────────────────────────────────────
st.header("2. Xu ly")

col_btn, col_dbg = st.columns([2, 1])
with col_btn:
    btn_process = st.button("Bat dau xu ly", type="primary", disabled=(uploaded_pdf is None))
with col_dbg:
    debug_mode = st.checkbox(
        "Debug - xem raw pdfplumber",
        value=False,
        help="Hien thi du lieu tho tung row pdfplumber doc duoc"
    )

# ── Debug section ─────────────────────────────────────────────────────────────
if debug_mode and uploaded_pdf is not None:
    pdf_bytes_dbg = uploaded_pdf.read()
    uploaded_pdf.seek(0)  # reset de btn_process van doc duoc
    raw_rows = read_raw_rows(pdf_bytes_dbg, max_rows=60)
    with st.expander(f"Raw pdfplumber - {len(raw_rows)} rows dau tien", expanded=True):
        for item in raw_rows:
            st.write(f"**Trang {item['page']} | Row {item['row_idx']}:** `{item['cells']}`")

# ── Xu ly chinh ───────────────────────────────────────────────────────────────
if btn_process:
    with st.spinner("Dang trich xuat va xu ly..."):

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
            st.info(f"Database tu file upload: **{len(existing_df)} dong**")
        elif github_token:
            existing_df, github_sha = fetch_db_from_github(github_token, github_repo)
            if existing_df is not None:
                st.info(f"Database tu GitHub: **{len(existing_df)} dong**")
            else:
                st.warning("Chua co database tren GitHub, se tao moi")
        else:
            st.warning("Khong co database cu, se tao moi tu QD nay")

        final_df = merge_database(existing_df, new_rows)

        st.session_state["final_df"]    = final_df
        st.session_state["existing_df"] = existing_df
        st.session_state["new_rows"]    = new_rows
        st.session_state["skipped"]     = skipped
        st.session_state["so_qd"]       = so_qd
        st.session_state["github_sha"]  = github_sha

        st.success(f"Hoan tat! Trich xuat **{len(new_rows)} dong** tu QD {so_qd}")

        if skipped:
            with st.expander(f"{len(skipped)} dong bi bo qua (Replacecode khong phai ma mon)"):
                st.dataframe(pd.DataFrame(skipped), use_container_width=True)

# ── Step 3: Preview ───────────────────────────────────────────────────────────
if "final_df" in st.session_state:
    final_df    = st.session_state["final_df"]
    existing_df = st.session_state["existing_df"]
    new_rows    = st.session_state["new_rows"]
    so_qd       = st.session_state["so_qd"]
    github_sha  = st.session_state["github_sha"]

    st.header("3. Ket qua")

    old_pairs = set(zip(existing_df["SubjectCode"], existing_df["Replacecode"])) \
                if existing_df is not None else set()
    n_applied  = int((final_df["replace_status"] == "applied").sum())
    n_expired  = int((final_df["replace_status"] == "expired").sum())
    n_new      = sum(1 for r in new_rows if (r["SubjectCode"], r["Replacecode"]) not in old_pairs)
    n_updated  = len(new_rows) - n_new

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Tong dong",        len(final_df))
    c2.metric("Dang hieu luc",    n_applied)
    c3.metric("Het hieu luc",     n_expired)
    c4.metric("Them moi tu QD",   n_new)
    c5.metric("Cap nhat tu QD",   n_updated)

    col_f1, col_f2 = st.columns([1, 3])
    with col_f1:
        filter_status = st.selectbox("Loc trang thai", ["Tat ca", "applied", "expired"])
    with col_f2:
        search_code = st.text_input("Tim ma mon", placeholder="VD: IOT102")

    display_df = final_df.copy()
    if filter_status != "Tat ca":
        display_df = display_df[display_df["replace_status"] == filter_status]
    if search_code.strip():
        kw = search_code.strip().upper()
        display_df = display_df[
            display_df["SubjectCode"].str.upper().str.contains(kw, na=False) |
            display_df["Replacecode"].str.upper().str.contains(kw, na=False)
        ]

    st.dataframe(display_df, use_container_width=True, height=400)

    # ── Step 4: Save ──────────────────────────────────────────────────────────
    st.header("4. Luu du lieu")

    excel_bytes = to_excel_bytes(final_df)
    col_dl, col_gh = st.columns(2)

    with col_dl:
        st.download_button(
            label    = "Tai ve may (.xlsx)",
            data     = excel_bytes,
            file_name= "Database_Tong_Hop.xlsx",
            mime     = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with col_gh:
        if st.button("Commit len GitHub", type="primary"):
            if not github_token:
                st.error("Chua cau hinh GitHub Token trong Streamlit secrets")
            else:
                with st.spinner("Dang commit len GitHub..."):
                    success, msg = commit_to_github(
                        github_token, github_repo, excel_bytes, so_qd, sha=github_sha
                    )
                if success:
                    st.success("Commit thanh cong len output/Database_Tong_Hop.xlsx")
                    _, new_sha = fetch_db_from_github(github_token, github_repo)
                    st.session_state["github_sha"] = new_sha
                else:
                    st.error(f"Loi khi commit: {msg}")
