import importlib.util
import io
import os

import pandas as pd
import streamlit as st


SCRIPT_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "scripts",
        "decision-lookup.py",
    )
)


def load_logic():
    spec = importlib.util.spec_from_file_location("decision_lookup", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Không thể nạp module Decision Lookup.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def extract_mssv_from_file(uploaded_file, logic):
    name = uploaded_file.name.lower()
    content = uploaded_file.getvalue()

    if name.endswith(".txt"):
        text = content.decode("utf-8", errors="ignore")
        values = text.replace(",", "\n").replace(";", "\n").split()
    else:
        try:
            if name.endswith(".csv"):
                dataframe = pd.read_csv(io.BytesIO(content), dtype=str)
            else:
                dataframe = pd.read_excel(io.BytesIO(content), dtype=str)
        except Exception:
            return []

        if dataframe.empty:
            return []
        column_index = logic.detect_mssv_col(list(dataframe.columns))
        column = dataframe.iloc[:, column_index if column_index >= 0 else 0]
        values = column.dropna().astype(str).tolist()

    return [
        value
        for value in dict.fromkeys(str(item).strip() for item in values)
        if value and value.lower() != "nan"
    ]


st.set_page_config(
    page_title="Decision Lookup | FE QA Tools",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

DARK = {
    "bg": "#080D18",
    "card": "#0F1628",
    "card2": "#162040",
    "border": "#1E2D4A",
    "text": "#E8EDF5",
    "muted": "#8892A4",
    "accent": "#00D4AA",
    "accent_dim": "#00A882",
    "green": "#22C55E",
    "green_bg": "#052E16",
    "red": "#F87171",
    "red_bg": "#1C1012",
}
LIGHT = {
    "bg": "#F0F4F8",
    "card": "#FFFFFF",
    "card2": "#F7F9FC",
    "border": "#E2E8F0",
    "text": "#1A2540",
    "muted": "#64748B",
    "accent": "#0A9E7F",
    "accent_dim": "#077A62",
    "green": "#15803D",
    "green_bg": "#DCFCE7",
    "red": "#DC2626",
    "red_bg": "#FEF2F2",
}
T = DARK if st.session_state.theme == "dark" else LIGHT

st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:
    wght@400;500;600;700;800&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True,
)
st.markdown(
    f"""
    <style>
    .stApp {{ background: {T["bg"]} !important; }}
    .block-container {{
        max-width: 1050px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
    }}
    [data-testid="stSidebar"] {{
        background: {T["card"]} !important;
        border-right: 1px solid {T["border"]} !important;
    }}
    [data-testid="stSidebarNav"] {{ display: none !important; }}
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown li, label {{
        font-family: "Plus Jakarta Sans", sans-serif !important;
        color: {T["text"]} !important;
    }}
    [data-testid="stFileUploader"] section {{
        background: {T["card2"]} !important;
        border: 2px dashed {T["border"]} !important;
        border-radius: 12px !important;
    }}
    .stTextArea textarea {{
        background: {T["card2"]} !important;
        color: {T["text"]} !important;
        border: 1px solid {T["border"]} !important;
        border-radius: 10px !important;
    }}
    .stButton > button {{
        background: {T["accent"]} !important;
        color: #080D18 !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        min-height: 44px;
    }}
    .stDownloadButton > button {{
        background: {T["accent"]} !important;
        color: #080D18 !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        min-height: 48px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

try:
    logic = load_logic()
except Exception as exc:
    st.error(f"Không nạp được `scripts/decision-lookup.py`: {exc}")
    st.stop()

if "decision_excel" not in st.session_state:
    st.session_state.decision_excel = None
if "decision_errors" not in st.session_state:
    st.session_state.decision_errors = []

with st.sidebar:
    st.markdown(
        f"""
        <div style="padding:16px 0 20px;border-bottom:1px solid {T["border"]};
                    margin-bottom:20px">
          <div style="display:flex;align-items:center;gap:10px">
            <div style="width:38px;height:38px;border-radius:11px;
                        background:linear-gradient(135deg,{T["accent"]},
                        {T["accent_dim"]});display:flex;align-items:center;
                        justify-content:center;font-size:20px">🔍</div>
            <div>
              <div style="font-size:14px;font-weight:800;color:{T["accent"]}">
                Decision Lookup
              </div>
              <div style="font-size:10px;color:{T["muted"]};font-weight:600">
                TRA CỨU MSSV TRONG QUYẾT ĐỊNH
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("GIAO DIỆN")
    light_column, dark_column = st.columns(2)
    with light_column:
        if st.button("☀ Sáng", use_container_width=True, key="decision_light"):
            st.session_state.theme = "light"
            st.rerun()
    with dark_column:
        if st.button("🌙 Tối", use_container_width=True, key="decision_dark"):
            st.session_state.theme = "dark"
            st.rerun()

    st.divider()
    st.markdown(
        f"""
        <div style="font-size:10px;color:{T["muted"]};font-weight:700;
                    letter-spacing:.9px;margin-bottom:10px">HƯỚNG DẪN NHANH</div>
        <div style="font-size:12px;color:{T["muted"]};line-height:2.1">
          <div>① Tải Quyết định PDF</div>
          <div>② Nhập hoặc tải danh sách MSSV</div>
          <div>③ Bấm “Chạy tra cứu”</div>
          <div>④ Tải file kết quả Excel</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown(
        f"""
        <div style="background:{T["accent"]}11;border:1px solid {T["accent"]}33;
                    border-radius:10px;padding:12px">
          <div style="font-size:12px;font-weight:700;color:{T["accent"]};
                      margin-bottom:4px">🔒 Bảo mật dữ liệu</div>
          <div style="font-size:11px;color:{T["muted"]};line-height:1.5">
            Dữ liệu chỉ được dùng trong phiên xử lý và không hiển thị chi tiết
            sinh viên trên giao diện.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.page_link("app.py", label="🏠 Trang chủ", use_container_width=True)
    st.markdown(
        f"""
        <div style="margin-top:24px;padding-top:14px;border-top:
                    1px solid {T["border"]};text-align:center;
                    font-size:11px;color:{T["muted"]}">
          © 2026 <strong style="color:{T["accent"]}">YenLT31</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    f"""
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:28px">
      <div style="width:48px;height:48px;border-radius:14px;
                  background:linear-gradient(135deg,{T["accent"]},
                  {T["accent_dim"]});display:flex;align-items:center;
                  justify-content:center;font-size:24px">🔍</div>
      <div>
        <h1 style="font-size:28px;font-weight:800;color:{T["text"]};
                   margin:0">Decision Lookup</h1>
        <p style="font-size:13px;color:{T["muted"]};margin:4px 0 0">
          Tra cứu MSSV trong các Quyết định PDF và tải kết quả Excel
        </p>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

form_column, info_column = st.columns([2.2, 1], gap="large")

with form_column:
    st.markdown("### 1. Tải Quyết định")
    pdf_files = st.file_uploader(
        "Quyết định PDF",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    st.markdown("### 2. Nhập MSSV")
    input_mode = st.radio(
        "Nguồn danh sách",
        ["Nhập trực tiếp", "Tải file"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if input_mode == "Nhập trực tiếp":
        raw_mssv = st.text_area(
            "MSSV",
            height=120,
            placeholder="Mỗi MSSV một dòng, hoặc ngăn cách bằng dấu phẩy.",
            label_visibility="collapsed",
        )
        mssv_list = [
            value
            for value in dict.fromkeys(
                raw_mssv.replace(",", "\n").replace(";", "\n").split()
            )
            if value
        ]
    else:
        mssv_file = st.file_uploader(
            "File MSSV",
            type=["txt", "csv", "xlsx", "xls"],
            label_visibility="collapsed",
        )
        mssv_list = (
            extract_mssv_from_file(mssv_file, logic)
            if mssv_file is not None
            else []
        )

    if st.button(
        "🔍 Chạy tra cứu",
        type="primary",
        use_container_width=True,
        disabled=not (pdf_files and mssv_list),
    ):
        st.session_state.decision_excel = None
        st.session_state.decision_errors = []
        pdf_data = [
            {"name": uploaded.name, "bytes": uploaded.getvalue()}
            for uploaded in pdf_files
        ]

        with st.spinner("Đang quét PDF và tạo file Excel..."):
            try:
                results = logic.search_mssv_in_pdfs(mssv_list, pdf_data)
                summary, detail = logic.build_export_data(mssv_list, results)
                st.session_state.decision_excel = logic.to_excel_bytes(
                    summary,
                    detail,
                )
                st.session_state.decision_errors = results.get("_errors", [])
            except Exception as exc:
                st.error(f"Không thể hoàn tất tra cứu: {exc}")

with info_column:
    st.markdown(
        f"""
        <div style="background:{T["card"]};border:1px solid {T["border"]};
                    border-radius:14px;padding:20px;margin-top:4px">
          <div style="font-size:13px;font-weight:800;color:{T["text"]};
                      margin-bottom:12px">Định dạng hỗ trợ</div>
          <div style="font-size:12px;color:{T["muted"]};line-height:1.9">
            <div>Quyết định: PDF</div>
            <div>Danh sách: TXT, CSV, XLSX, XLS</div>
            <div>Đầu ra: Excel (.xlsx)</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.decision_excel is not None:
        st.success("Đã hoàn tất tra cứu.")
        st.download_button(
            "⬇ Tải kết quả Excel",
            data=st.session_state.decision_excel,
            file_name="KetQua_TraCuu_QuyetDinh.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            use_container_width=True,
        )
        if st.session_state.decision_errors:
            st.warning(
                f"Có {len(st.session_state.decision_errors)} PDF không xử lý được."
            )
        if st.button("Tra cứu mới", use_container_width=True):
            st.session_state.decision_excel = None
            st.session_state.decision_errors = []
            st.rerun()
