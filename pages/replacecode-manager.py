import streamlit as st
import pandas as pd
import io
import base64
import re
import requests
import importlib.util
import sys
import os

# ── Import logic từ scripts/replacecode-manager.py ───────────────────────────
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
    st.error(f"❌ Không load được scripts/replacecode-manager.py: {e}")
    st.stop()

# ── Helpers ───────────────────────────────────────────────────────────────────
def to_excel_bytes(df):
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    buf.seek(0)
    return buf.getvalue()


def fetch_db_from_github(token, repo):
    """Lấy Database_Tong_Hop.xlsx từ GitHub repo."""
    url     = f"https://api.github.com/repos/{repo}/contents/output/Database_Tong_Hop.xlsx"
    headers = {"Authorization": f"token {token}"}
    resp    = requests.get(url, headers=headers)
    if resp.status_code == 200:
        content = base64.b64decode(resp.json()["content"])
        sha     = resp.json()["sha"]
        return pd.read_excel(io.BytesIO(content)), sha
    return None, None


def commit_to_github(token, repo, excel_bytes, so_qd, sha=None):
    """Commit file Excel lên GitHub output/Database_Tong_Hop.xlsx."""
    url     = f"https://api.github.com/repos/{repo}/contents/output/Database_Tong_Hop.xlsx"
    headers = {"Authorization": f"token {token}", "Content-Type": "application/json"}
    payload = {
        "message": f"Update Database_Tong_Hop.xlsx — QĐ {so_qd}",
        "content": base64.b64encode(excel_bytes).decode()
    }
    if sha:
        payload["sha"] = sha
    resp = requests.put(url, json=payload, headers=headers)
    return resp.status_code in [200, 201], resp.json().get("message", "")


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="ReplaceCode Manager", page_icon="📚", layout="wide")

st.title("📚 ReplaceCode Manager")
st.caption("Cập nhật danh sách môn tương đương / thay thế từ Quyết định PDF")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ GitHub")
    try:
        github_token = st.secrets["github"]["token"]
        github_repo  = st.secrets["github"].get("repo", "yenLT31/FE-QA-Tools")
        st.success("✅ Token đã cấu hình")
    except Exception:
        github_token = ""
        github_repo  = "yenLT31/FE-QA-Tools"
        st.warning("⚠️ Chưa có GitHub Token trong secrets")

    st.caption(f"Repo: `{github_repo}`")
    st.markdown("---")
    st.markdown(
        "**Cách thêm Token:**\n"
        "Vào App Settings → Secrets → thêm:\n"
        "```toml\n[github]\ntoken = \"ghp_...\"\nrepo  = \"yenLT31/FE-QA-Tools\"\n```"
    )

# ── Step 1: Upload ────────────────────────────────────────────────────────────
st.header("1️⃣  Tải lên file")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 File PDF Quyết định mới")
    uploaded_pdf = st.file_uploader("Chọn file PDF", type=["pdf"], key="pdf_upload")
    so_qd_input  = st.text_input(
        "Số QĐ",
        value="",
        placeholder="Để trống → tự lấy số từ tên file",
        help="VD: 498  |  Nếu để trống, hệ thống tự tìm số trong tên file PDF"
    )

with col2:
    st.subheader("📊 Database hiện có")
    uploaded_excel = st.file_uploader(
        "Upload Database_Tong_Hop.xlsx  (tùy chọn)",
        type=["xlsx"],
        key="excel_upload",
        help="Nếu không upload, hệ thống tự lấy từ GitHub output/"
    )
    if not uploaded_excel and github_token:
        st.caption("✅ Sẽ tự fetch từ GitHub nếu không upload")
    elif not uploaded_excel and not github_token:
        st.caption("⚠️ Không có database → sẽ tạo mới từ QĐ này")

# ── Step 2: Process ───────────────────────────────────────────────────────────
st.header("2️⃣  Xử lý")

btn_process = st.button("▶️  Bắt đầu xử lý", type="primary", disabled=(uploaded_pdf is None))

if btn_process:
    with st.spinner("Đang trích xuất và xử lý..."):

        # Xác định số QĐ
        so_qd = so_qd_input.strip()
        if not so_qd:
            match = re.search(r'\d+', uploaded_pdf.name)
            so_qd = match.group() if match else "Unknown"

        # Trích xuất từ PDF
        pdf_bytes          = uploaded_pdf.read()
        new_rows, skipped  = extract_from_pdf(pdf_bytes, so_qd=so_qd)

        # Lấy database cũ
        existing_df = None
        github_sha  = None

        if uploaded_excel:
            existing_df = pd.read_excel(uploaded_excel)
            st.info(f"📂 Database từ file upload: **{len(existing_df)} dòng**")
        elif github_token:
            existing_df, github_sha = fetch_db_from_github(github_token, github_repo)
            if existing_df is not None:
                st.info(f"📂 Database từ GitHub: **{len(existing_df)} dòng**")
            else:
                st.warning("⚠️ Chưa có database trên GitHub, sẽ tạo mới")
        else:
            st.warning("⚠️ Không có database cũ, sẽ tạo mới từ QĐ này")

        # Merge
        final_df = merge_database(existing_df, new_rows)

        # Lưu vào session
        st.session_state["final_df"]    = final_df
        st.session_state["existing_df"] = existing_df
        st.session_state["new_rows"]    = new_rows
        st.session_state["skipped"]     = skipped
        st.session_state["so_qd"]       = so_qd
        st.session_state["github_sha"]  = github_sha

        st.success(f"✅ Hoàn tất! Trích xuất **{len(new_rows)} dòng** từ QĐ {so_qd}")

        if skipped:
            with st.expander(f"⚠️  {len(skipped)} dòng bị bỏ qua (Replacecode không phải mã môn)"):
                st.dataframe(pd.DataFrame(skipped), use_container_width=True)

# ── Step 3: Preview ───────────────────────────────────────────────────────────
if "final_df" in st.session_state:
    final_df    = st.session_state["final_df"]
    existing_df = st.session_state["existing_df"]
    new_rows    = st.session_state["new_rows"]
    so_qd       = st.session_state["so_qd"]
    github_sha  = st.session_state["github_sha"]

    st.header("3️⃣  Kết quả")

    # Thống kê
    old_pairs   = set(zip(existing_df["SubjectCode"], existing_df["Replacecode"])) \
                  if existing_df is not None else set()
    n_applied   = int((final_df["replace_status"] == "applied").sum())
    n_expired   = int((final_df["replace_status"] == "expired").sum())
    n_new       = sum(1 for r in new_rows if (r["SubjectCode"], r["Replacecode"]) not in old_pairs)
    n_updated   = len(new_rows) - n_new

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("📋 Tổng dòng",        len(final_df))
    c2.metric("✅ Đang hiệu lực",     n_applied)
    c3.metric("❌ Hết hiệu lực",      n_expired)
    c4.metric("🆕 Thêm mới từ QĐ",   n_new)
    c5.metric("🔄 Cập nhật từ QĐ",   n_updated)

    # Bộ lọc
    col_f1, col_f2 = st.columns([1, 3])
    with col_f1:
        filter_status = st.selectbox("Lọc trạng thái", ["Tất cả", "applied", "expired"])
    with col_f2:
        search_code = st.text_input("🔍 Tìm mã môn", placeholder="VD: IOT102")

    display_df = final_df.copy()
    if filter_status != "Tất cả":
        display_df = display_df[display_df["replace_status"] == filter_status]
    if search_code.strip():
        kw = search_code.strip().upper()
        display_df = display_df[
            display_df["SubjectCode"].str.upper().str.contains(kw, na=False) |
            display_df["Replacecode"].str.upper().str.contains(kw, na=False)
        ]

    st.dataframe(display_df, use_container_width=True, height=400)

    # ── Step 4: Save ──────────────────────────────────────────────────────────
    st.header("4️⃣  Lưu dữ liệu")

    excel_bytes = to_excel_bytes(final_df)
    col_dl, col_gh = st.columns(2)

    with col_dl:
        st.download_button(
            label    = "⬇️  Tải về máy (.xlsx)",
            data     = excel_bytes,
            file_name= "Database_Tong_Hop.xlsx",
            mime     = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help     = "Download file Excel về máy tính"
        )

    with col_gh:
        if st.button("☁️  Commit lên GitHub", type="primary"):
            if not github_token:
                st.error("❌ Chưa cấu hình GitHub Token trong Streamlit secrets")
            else:
                with st.spinner("Đang commit lên GitHub..."):
                    success, msg = commit_to_github(
                        github_token, github_repo, excel_bytes, so_qd, sha=github_sha
                    )
                if success:
                    st.success(f"✅ Commit thành công lên `output/Database_Tong_Hop.xlsx`")
                    st.caption(f"Message: Update Database_Tong_Hop.xlsx — QĐ {so_qd}")
                    # Reset SHA sau khi commit
                    _, new_sha = fetch_db_from_github(github_token, github_repo)
                    st.session_state["github_sha"] = new_sha
                else:
                    st.error(f"❌ Lỗi khi commit: {msg}")
