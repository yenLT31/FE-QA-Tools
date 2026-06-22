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
    layout="centered",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 820px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    [data-testid="stSidebarNav"] {
        display: none;
    }
    [data-testid="stFileUploader"] section {
        border-radius: 12px;
    }
    .stButton > button,
    .stDownloadButton > button {
        border-radius: 10px;
        font-weight: 700;
        min-height: 46px;
    }
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

st.title("🔍 Decision Lookup")
st.caption("Tải Quyết định PDF và danh sách MSSV để tạo file kết quả Excel.")

pdf_files = st.file_uploader(
    "Quyết định PDF",
    type=["pdf"],
    accept_multiple_files=True,
)

input_mode = st.radio(
    "Nguồn danh sách MSSV",
    ["Nhập trực tiếp", "Tải file"],
    horizontal=True,
)

if input_mode == "Nhập trực tiếp":
    raw_mssv = st.text_area(
        "MSSV",
        height=120,
        placeholder="Mỗi MSSV một dòng, hoặc ngăn cách bằng dấu phẩy.",
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
    )
    mssv_list = (
        extract_mssv_from_file(mssv_file, logic)
        if mssv_file is not None
        else []
    )

can_run = bool(pdf_files and mssv_list)

if st.button(
    "Chạy tra cứu",
    type="primary",
    use_container_width=True,
    disabled=not can_run,
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

if st.session_state.decision_excel is not None:
    st.success("Đã hoàn tất. Nhấn nút bên dưới để tải kết quả.")
    st.download_button(
        "Tải kết quả Excel",
        data=st.session_state.decision_excel,
        file_name="KetQua_TraCuu_QuyetDinh.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

    if st.session_state.decision_errors:
        st.warning(
            f"Có {len(st.session_state.decision_errors)} file PDF không xử lý được."
        )

    if st.button("Tra cứu mới", use_container_width=True):
        st.session_state.decision_excel = None
        st.session_state.decision_errors = []
        st.rerun()

st.page_link("app.py", label="← Về trang chủ")
