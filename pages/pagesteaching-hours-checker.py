"""
Teaching Hours Checker - Giao diện Streamlit.
Kiểm soát giờ dạy GV: đối chiếu Lịch kỳ FAP, Teaching Summaries và Phiếu chấm công ĐT.
FPT Education QA Department
© 2026 YenLT31
"""

import os
import sys

import pandas as pd
import streamlit as st

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
try:
    from Script.scriptsteaching_hours_checker import (
        build_lich_ky_kiem_tra,
        calculate_gio_co_huu,
        doi_sanh_gio_day,
        export_to_excel,
        get_wasnot_taken_detail,
        read_cham_cong,
        read_danh_sach_gv,
        read_lich_ky,
        read_teaching_summaries,
    )
except ModuleNotFoundError:
    from Script.scriptsteaching_hours_checker import (
        build_lich_ky_kiem_tra,
        calculate_gio_co_huu,
        doi_sanh_gio_day,
        export_to_excel,
        get_wasnot_taken_detail,
        read_cham_cong,
        read_danh_sach_gv,
        read_lich_ky,
        read_teaching_summaries,
    )


st.set_page_config(
    page_title="Teaching Hours Checker",
    page_icon="⏱️",
    layout="wide",
)


def load_css():
    st.markdown(
        """
        <style>
            :root {
                --qa-green: #0f8f66;
                --qa-green-dark: #08704e;
                --qa-ink: #111827;
                --qa-muted: #64748b;
                --qa-line: #d8dee8;
                --qa-soft: #f7f9fc;
                --qa-warn-bg: #fff7db;
                --qa-warn-line: #e7b84d;
                --qa-ok-bg: #e8f8ef;
                --qa-ok-line: #63c58d;
            }

            .block-container {
                padding-top: 1.35rem;
                padding-bottom: 2rem;
                max-width: 1240px;
            }

            h1, h2, h3, p {
                letter-spacing: 0;
            }

            [data-testid="stSidebar"] {
                border-right: 1px solid var(--qa-line);
            }

            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
                margin-bottom: 0.35rem;
            }

            .app-kicker {
                color: var(--qa-green-dark);
                font-size: 0.78rem;
                font-weight: 800;
                letter-spacing: 0;
                text-transform: uppercase;
                margin-bottom: 0.25rem;
            }

            .main-title {
                color: var(--qa-ink);
                font-size: 2rem;
                font-weight: 800;
                line-height: 1.15;
                margin: 0 0 0.35rem;
            }

            .main-description {
                color: var(--qa-muted);
                font-size: 0.98rem;
                margin: 0 0 1.2rem;
                max-width: 860px;
            }

            .section-head {
                display: flex;
                align-items: center;
                gap: 0.65rem;
                margin: 1rem 0 0.2rem;
            }

            .step-number {
                align-items: center;
                background: var(--qa-green);
                border-radius: 999px;
                color: #ffffff;
                display: inline-flex;
                font-size: 0.82rem;
                font-weight: 800;
                height: 2rem;
                justify-content: center;
                min-width: 2rem;
            }

            .step-title {
                color: var(--qa-ink);
                font-size: 1.08rem;
                font-weight: 750;
            }

            .step-desc {
                color: var(--qa-muted);
                font-size: 0.9rem;
                margin: 0 0 0.9rem 2.65rem;
            }

            .upload-label {
                color: #334155;
                font-size: 0.78rem;
                font-weight: 800;
                letter-spacing: 0;
                margin: 0.35rem 0 0.25rem;
                text-transform: uppercase;
            }

            [data-testid="stFileUploader"] {
                background: var(--qa-soft);
                border: 1px solid var(--qa-line);
                border-radius: 8px;
                padding: 0.55rem 0.75rem 0.15rem;
            }

            [data-testid="stFileUploaderDropzone"] {
                border: 1px dashed #aab6c6;
                border-radius: 8px;
                min-height: 88px;
            }

            .status-box {
                border-radius: 8px;
                font-size: 0.92rem;
                margin: 0.7rem 0 0.9rem;
                padding: 0.8rem 0.95rem;
            }

            .status-box.warn {
                background: var(--qa-warn-bg);
                border: 1px solid var(--qa-warn-line);
                color: #7a4b00;
            }

            .status-box.ok {
                background: var(--qa-ok-bg);
                border: 1px solid var(--qa-ok-line);
                color: #075b37;
            }

            .stButton > button,
            .stDownloadButton > button {
                border-radius: 8px;
                font-weight: 750;
                min-height: 2.85rem;
            }

            .stButton > button {
                background: var(--qa-green);
                border: 1px solid var(--qa-green);
                color: #ffffff;
            }

            .stButton > button:hover {
                background: var(--qa-green-dark);
                border-color: var(--qa-green-dark);
                color: #ffffff;
            }

            .stButton > button:disabled {
                background: #e5e9f0;
                border-color: #d7dde7;
                color: #8793a3;
            }

            .stTabs [data-baseweb="tab-list"] {
                border-bottom: 1px solid var(--qa-line);
                gap: 0.25rem;
            }

            .stTabs [data-baseweb="tab"] {
                border-radius: 8px 8px 0 0;
                font-weight: 700;
                padding: 0.65rem 1.1rem;
            }

            [data-testid="stMetric"] {
                background: #ffffff;
                border: 1px solid var(--qa-line);
                border-radius: 8px;
                padding: 0.8rem 0.95rem;
            }

            .sidebar-title {
                color: var(--qa-ink);
                font-size: 1.05rem;
                font-weight: 800;
                line-height: 1.25;
                margin-bottom: 0.15rem;
            }

            .sidebar-subtitle {
                color: var(--qa-muted);
                font-size: 0.74rem;
                font-weight: 800;
                letter-spacing: 0;
                text-transform: uppercase;
            }

            .side-panel {
                background: #ffffff;
                border: 1px solid var(--qa-line);
                border-radius: 8px;
                margin: 0.65rem 0;
                padding: 0.75rem;
            }

            .side-panel p {
                color: #475569;
                font-size: 0.82rem;
                line-height: 1.42;
                margin: 0.25rem 0;
            }

            .side-panel strong {
                color: var(--qa-ink);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def mask_pii(df, mask_enabled):
    if not mask_enabled or df is None or df.empty:
        return df

    df_masked = df.copy()

    if "HoTen" in df_masked.columns:
        def mask_name(name):
            if not name or pd.isna(name):
                return name
            parts = str(name).strip().split()
            if len(parts) >= 3:
                return f"{parts[0]} * {parts[-1]}"
            if len(parts) == 2:
                return f"{parts[0]} *"
            name_str = str(name).strip()
            return name_str[0] + "*" * (len(name_str) - 1) if name_str else ""

        df_masked["HoTen"] = df_masked["HoTen"].apply(mask_name)

    if "ID" in df_masked.columns:
        def mask_id(id_val):
            if not id_val or pd.isna(id_val):
                return id_val
            id_str = str(id_val).strip()
            if len(id_str) > 5:
                return id_str[:3] + "*" * (len(id_str) - 5) + id_str[-2:]
            if len(id_str) > 2:
                return id_str[0] + "*" * (len(id_str) - 2) + id_str[-1]
            return "*" * len(id_str)

        df_masked["ID"] = df_masked["ID"].apply(mask_id)

    if "AccountFE" in df_masked.columns:
        def mask_account(acc):
            if not acc or pd.isna(acc):
                return acc
            acc_str = str(acc).strip()
            if len(acc_str) > 4:
                mask_len = min(5, len(acc_str) - 4)
                return acc_str[:3] + "*" * mask_len + acc_str[-1]
            if len(acc_str) > 2:
                return acc_str[0] + "*" * (len(acc_str) - 2) + acc_str[-1]
            return "*" * len(acc_str)

        df_masked["AccountFE"] = df_masked["AccountFE"].apply(mask_account)

    return df_masked


def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-title">⏱️ Teaching Hours Checker</div>
            <div class="sidebar-subtitle">Kiểm soát giờ dạy GV</div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        st.markdown("**Bảo mật dữ liệu**")
        mask_enabled = st.checkbox(
            "Ẩn danh thông tin giảng viên",
            value=False,
            help="Ẩn Họ tên, ID và AccountFE trên giao diện khi cần chia sẻ màn hình.",
        )
        st.session_state["mask_enabled"] = mask_enabled

        st.markdown(
            """
            <div class="side-panel">
                <p><strong>Quy trình</strong></p>
                <p>1. Tải lên Lịch kỳ, Teaching Summaries, Chấm công ĐT và Danh sách GV.</p>
                <p>2. Tải thêm Lịch kỳ toàn kỳ nếu cần tính giờ cơ hữu.</p>
                <p>3. Chạy kiểm tra, xem kết quả và tải báo cáo Excel.</p>
            </div>
            <div class="side-panel">
                <p><strong>Dữ liệu local</strong></p>
                <p>File được xử lý tại máy đang chạy Streamlit, không gửi ra dịch vụ bên ngoài.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()
        st.markdown(
            '<p style="font-size:0.76rem; color:#64748b; margin-top:1rem;">© 2026 YenLT31<br>FPT Education QA Department</p>',
            unsafe_allow_html=True,
        )


def render_main():
    st.markdown(
        """
        <div class="app-kicker">FPT Education QA Department</div>
        <h1 class="main-title">Teaching Hours Checker</h1>
        <p class="main-description">
            Đối chiếu giờ dạy giữa Lịch kỳ FAP, Teaching Summaries và Phiếu chấm công ĐT.
            Giao diện tập trung vào thao tác upload, kiểm tra nhanh sai lệch và xuất báo cáo.
        </p>
        """,
        unsafe_allow_html=True,
    )

    tab_config, tab_result = st.tabs(["Cấu hình", "Kết quả"])

    with tab_config:
        render_config_tab()

    with tab_result:
        render_result_tab()


def render_config_tab():
    st.markdown(
        """
        <div class="section-head">
            <span class="step-number">01</span>
            <span class="step-title">File kiểm soát giờ dạy</span>
        </div>
        <p class="step-desc">Tải lên đủ 4 nhóm file để chạy đối chiếu theo tháng.</p>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<p class="upload-label">Lịch kỳ FAP</p>', unsafe_allow_html=True)
        files_lich_ky = st.file_uploader(
            "Upload file(s) Lịch kỳ",
            type=["xlsx", "xls"],
            accept_multiple_files=True,
            key="lich_ky",
            label_visibility="collapsed",
        )

    with col2:
        st.markdown('<p class="upload-label">Teaching Summaries</p>', unsafe_allow_html=True)
        files_teaching = st.file_uploader(
            "Upload file(s) Teaching Summaries",
            type=["xlsx", "xls"],
            accept_multiple_files=True,
            key="teaching_summaries",
            label_visibility="collapsed",
        )

    col3, col4 = st.columns(2, gap="large")

    with col3:
        st.markdown('<p class="upload-label">Phiếu chấm công ĐT</p>', unsafe_allow_html=True)
        files_cham_cong = st.file_uploader(
            "Upload file(s) Chấm công ĐT",
            type=["xlsx", "xls"],
            accept_multiple_files=True,
            key="cham_cong",
            label_visibility="collapsed",
        )

    with col4:
        st.markdown('<p class="upload-label">Danh sách GV</p>', unsafe_allow_html=True)
        file_gv = st.file_uploader(
            "Upload file Danh sách GV",
            type=["xlsx", "xls"],
            accept_multiple_files=False,
            key="danh_sach_gv",
            label_visibility="collapsed",
        )

    st.markdown(
        """
        <div class="section-head">
            <span class="step-number">02</span>
            <span class="step-title">File tính giờ cơ hữu HK</span>
        </div>
        <p class="step-desc">Không bắt buộc. Dùng khi cần tổng hợp giờ cơ hữu toàn học kỳ.</p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<p class="upload-label">Lịch kỳ toàn kỳ</p>', unsafe_allow_html=True)
    files_co_huu = st.file_uploader(
        "Upload file Lịch kỳ toàn kỳ",
        type=["xlsx", "xls"],
        accept_multiple_files=True,
        key="lich_ky_co_huu",
        label_visibility="collapsed",
    )

    can_run = files_lich_ky and files_teaching and files_cham_cong and file_gv
    missing_labels = []
    if not files_lich_ky:
        missing_labels.append("Lịch kỳ FAP")
    if not files_teaching:
        missing_labels.append("Teaching Summaries")
    if not files_cham_cong:
        missing_labels.append("Chấm công ĐT")
    if not file_gv:
        missing_labels.append("Danh sách GV")

    st.markdown(
        """
        <div class="section-head">
            <span class="step-number">03</span>
            <span class="step-title">Chạy kiểm tra</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if missing_labels:
        st.markdown(
            f'<div class="status-box warn">Cần tải thêm: {", ".join(missing_labels)}.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="status-box ok">Đã đủ file bắt buộc. Có thể bắt đầu kiểm tra.</div>',
            unsafe_allow_html=True,
        )

    if st.button("Bắt đầu kiểm tra", disabled=not can_run, use_container_width=True):
        run_check(files_lich_ky, files_teaching, files_cham_cong, file_gv, files_co_huu)


def run_check(files_lich_ky, files_teaching, files_cham_cong, file_gv, files_co_huu):
    with st.spinner("Đang xử lý dữ liệu..."):
        try:
            progress = st.progress(0, text="Đọc file Lịch kỳ...")
            df_lich_ky = read_lich_ky(files_lich_ky)

            progress.progress(20, text="Đọc file Teaching Summaries...")
            df_teaching = read_teaching_summaries(files_teaching)

            progress.progress(40, text="Đọc file Chấm công ĐT...")
            df_cham_cong = read_cham_cong(files_cham_cong)

            progress.progress(60, text="Đọc file Danh sách GV...")
            df_gv = read_danh_sach_gv(file_gv)

            if df_lich_ky.empty:
                st.error("Không đọc được dữ liệu từ file Lịch kỳ.")
                return
            if df_teaching.empty:
                st.error("Không đọc được dữ liệu từ file Teaching Summaries.")
                return
            if df_cham_cong.empty:
                st.error("Không đọc được dữ liệu từ file Chấm công.")
                return

            progress.progress(70, text="Đối chiếu giờ dạy...")
            df_doi_sanh = doi_sanh_gio_day(df_lich_ky, df_teaching, df_cham_cong, df_gv)

            progress.progress(80, text="Tổng hợp WasNot Taken...")
            df_wasnot = get_wasnot_taken_detail(df_teaching)

            df_co_huu = None
            df_lich_ky_kiem_tra = None
            if files_co_huu:
                progress.progress(90, text="Tính giờ dạy cơ hữu...")
                df_lich_ky_full = read_lich_ky(files_co_huu)
                if not df_lich_ky_full.empty:
                    df_co_huu, _tong_co_huu, _tong_all = calculate_gio_co_huu(
                        df_lich_ky_full,
                        df_cham_cong,
                        df_gv,
                    )
                    df_lich_ky_kiem_tra = build_lich_ky_kiem_tra(
                        df_lich_ky_full,
                        df_cham_cong,
                        df_gv,
                    )

            progress.progress(100, text="Hoàn tất.")

            st.session_state["doi_sanh"] = df_doi_sanh
            st.session_state["wasnot_taken"] = df_wasnot
            st.session_state["co_huu"] = df_co_huu
            st.session_state["lich_ky_kiem_tra"] = df_lich_ky_kiem_tra
            st.session_state["check_done"] = True

            st.markdown(
                '<div class="status-box ok">Kiểm tra hoàn tất. Mở tab Kết quả để xem chi tiết.</div>',
                unsafe_allow_html=True,
            )

        except Exception as e:
            st.error(f"Lỗi xử lý: {str(e)}")
            import traceback

            st.code(traceback.format_exc())


def render_result_tab():
    if not st.session_state.get("check_done", False):
        st.info("Chưa có kết quả. Vui lòng tải file và bấm Bắt đầu kiểm tra ở tab Cấu hình.")
        return

    df_doi_sanh = st.session_state.get("doi_sanh", None)
    df_wasnot = st.session_state.get("wasnot_taken", None)
    df_co_huu = st.session_state.get("co_huu", None)
    df_lich_ky_kiem_tra = st.session_state.get("lich_ky_kiem_tra", None)
    mask_enabled = st.session_state.get("mask_enabled", False)

    excel_file = export_to_excel(
        df_doi_sanh if df_doi_sanh is not None else pd.DataFrame(),
        df_wasnot if df_wasnot is not None else pd.DataFrame(),
        df_co_huu,
        df_lich_ky_kiem_tra,
    )

    _action_left, _action_spacer, _action_right = st.columns([1.2, 4.2, 1.4], gap="medium")
    with _action_left:
        if st.button("Xóa kết quả", use_container_width=True):
            for key in ("doi_sanh", "wasnot_taken", "co_huu", "lich_ky_kiem_tra", "check_done"):
                st.session_state.pop(key, None)
            st.rerun()
    with _action_right:
        st.download_button(
            label="Tải Excel",
            data=excel_file,
            file_name="Teaching_Hours_Check_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    if df_doi_sanh is not None and not df_doi_sanh.empty:
        total_gv = len(df_doi_sanh)
        total_true = len(df_doi_sanh[df_doi_sanh["KetQua"] == True])
        total_false = len(df_doi_sanh[df_doi_sanh["KetQua"] == False])

        col1, col2, col3 = st.columns(3, gap="large")
        col1.metric("Tổng GV kiểm tra", total_gv)
        col2.metric("Khớp", total_true)
        col3.metric("Lệch", total_false)
        st.divider()

    st.markdown("### Đối sánh giờ dạy")
    if df_doi_sanh is not None and not df_doi_sanh.empty:
        def highlight_false(row):
            if row.get("KetQua") == False:
                return ["background-color: #fee2e2"] * len(row)
            return [""] * len(row)

        df_display = mask_pii(df_doi_sanh, mask_enabled)
        st.dataframe(
            df_display.style.apply(highlight_false, axis=1),
            use_container_width=True,
            height=410,
        )
    else:
        st.warning("Không có dữ liệu đối sánh.")

    st.divider()

    st.markdown("### Chi tiết WasNot Taken")
    if df_wasnot is not None and not df_wasnot.empty:
        df_wasnot_display = mask_pii(df_wasnot, mask_enabled)
        st.dataframe(df_wasnot_display, use_container_width=True, height=300)
    else:
        st.info("Không có GV nào bị WasNot Taken.")

    st.divider()

    if df_co_huu is not None and not df_co_huu.empty:
        st.markdown("### Giờ dạy cơ hữu HK")

        tong_all = df_co_huu["TongGio"].sum()
        total_acc = len(df_co_huu)
        total_acc_has_hours = len(df_co_huu[df_co_huu["TongGio"] > 0])

        col1, col2, col3 = st.columns(3, gap="large")
        col1.metric("Tổng AccountFE", total_acc)
        col2.metric("Có giờ lịch kỳ", total_acc_has_hours)
        col3.metric("Tổng giờ", f"{tong_all:,.1f}h")

        df_co_huu_display = mask_pii(df_co_huu, mask_enabled)
        st.dataframe(df_co_huu_display, use_container_width=True, height=300)
        st.divider()

load_css()
render_sidebar()
render_main()
