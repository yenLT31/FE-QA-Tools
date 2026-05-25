import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.gpa_schedule_checker import (
    merge_gpa_files,
    merge_schedule_files,
    calculate_lecturer_percentage,
    generate_reports,
    export_reports_to_excel
)

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="GPA Schedule Checker", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;'>
        <span style='font-size:2.5em;'>📋</span>
        <h3>GPA Schedule Checker</h3>
        <p style='font-size:0.85em; color:gray;'>KIỂM TRA GPA & LỊCH KỲ</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**GIAO DIỆN**")
    col1, col2 = st.columns(2)
    with col1:
        light = st.button("☀ Sáng")
    with col2:
        dark = st.button("🌙 Tối")

    st.markdown("---")
    st.markdown("**HƯỚNG DẪN NHANH**")
    st.markdown("""
    ① Upload file Lịch kỳ (.xlsx)  
    ② Upload file(s) GPA Feedback (.xlsx)  
    ③ Bấm "Bắt đầu đối sánh"  
    ④ Xem kết quả & tải báo cáo
    """)

    st.markdown("---")
    st.info("🔒 **Bảo mật dữ liệu**\n\nMọi dữ liệu xử lý 100% tại local.\nKhông gửi lên server.")

# --- HEADER ---
st.markdown("""
<h1>📋 GPA Schedule Checker</h1>
<p>Đối sánh lịch kỳ và GPA – kiểm tra GV đủ 30%, phát hiện lớp GPA dưới 3.4</p>
""", unsafe_allow_html=True)

# --- TABS ---
tab_config, tab_result = st.tabs(["⚙ Cấu hình", "📊 Kết quả"])

with tab_config:

    # --- BƯỚC 1: TẢI LÊN FILE ---
    st.markdown("### 01 &nbsp; Tải lên file")
    st.markdown("Upload file Lịch kỳ và các file GPA Feedback")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("**📁 FILE LỊCH KỲ**")
        schedule_files = st.file_uploader(
            "Chọn file(s) lịch kỳ (chứa cột: GroupName, SubjectCode, Lecturer...)",
            type=['xlsx', 'xls'],
            accept_multiple_files=True,
            key='schedule',
            label_visibility='collapsed'
        )
        if schedule_files:
            st.success(f"✅ Đã nạp {len(schedule_files)} file lịch kỳ")

    with col_right:
        st.markdown("**📁 FILE GPA FEEDBACK**")
        gpa_files = st.file_uploader(
            "Chọn file(s) GPA (chứa cột: GV, Lớp, Môn, GPA, Comments...)",
            type=['xlsx', 'xls'],
            accept_multiple_files=True,
            key='gpa',
            label_visibility='collapsed'
        )
        if gpa_files:
            st.success(f"✅ Đã nạp {len(gpa_files)} file GPA")

    st.markdown("---")

    # --- BƯỚC 2: CHẠY ĐỐI SÁNH ---
    st.markdown("### 02 &nbsp; Bắt đầu đối sánh")

    if not schedule_files or not gpa_files:
        st.warning("⚠ Cần upload: file Lịch kỳ và file(s) GPA Feedback")

    run_button = st.button(
        "🔍 Bắt đầu đối sánh",
        use_container_width=True,
        type="primary",
        disabled=(not schedule_files or not gpa_files)
    )

    if run_button:
        with st.spinner("Đang xử lý..."):
            # Gộp files
            schedule_df = merge_schedule_files(schedule_files)
            gpa_df = merge_gpa_files(gpa_files)

            if schedule_df.empty:
                st.error("❌ File lịch kỳ không có dữ liệu.")
                st.stop()
            if gpa_df.empty:
                st.error("❌ File GPA không có dữ liệu.")
                st.stop()

            # Tính tỷ lệ GV
            lecturer_pct = calculate_lecturer_percentage(schedule_df)
            st.session_state['lecturer_pct'] = lecturer_pct

            # Tạo báo cáo
            report1, report2, report3, error = generate_reports(schedule_df, gpa_df)

            if error:
                st.error(f"❌ {error}")
                st.stop()

            st.session_state['report1'] = report1
            st.session_state['report2'] = report2
            st.session_state['report3'] = report3
            st.session_state['processed'] = True

        st.success("✅ Đối sánh hoàn tất! Chuyển sang tab Kết quả để xem.")

with tab_result:

    if 'processed' not in st.session_state:
        st.info("Chưa có kết quả. Vui lòng cấu hình và chạy đối sánh trước.")
    else:
        # --- KẾT QUẢ ---
        report1 = st.session_state['report1']
        report2 = st.session_state['report2']
        report3 = st.session_state['report3']
        lecturer_pct = st.session_state['lecturer_pct']

        # Thống kê nhanh
        col1, col2, col3 = st.columns(3)
        with col1:
            count1 = len(report1) if report1 is not None and not report1.empty else 0
            st.metric("🔴 GPA dưới 3.4", f"{count1} lớp")
        with col2:
            count2 = len(report2) if report2 is not None and not report2.empty else 0
            st.metric("🟡 Đủ 30% chưa lấy GPA", f"{count2} GV")
        with col3:
            count3 = len(report3) if report3 is not None and not report3.empty else 0
            st.metric("🟠 Dưới 30% bị lấy GPA", f"{count3} lớp")

        st.markdown("---")

        # Chi tiết
        detail_tab1, detail_tab2, detail_tab3, detail_tab4 = st.tabs([
            f"🔴 GPA dưới 3.4 ({count1})",
            f"🟡 Đủ 30% chưa lấy GPA ({count2})",
            f"🟠 Dưới 30% bị lấy GPA ({count3})",
            "📊 Tỷ lệ % GV theo lớp"
        ])

        with detail_tab1:
            if count1 > 0:
                st.dataframe(report1, use_container_width=True)
            else:
                st.success("Không có lớp nào GPA dưới 3.4")

        with detail_tab2:
            if count2 > 0:
                st.dataframe(report2, use_container_width=True)
            else:
                st.success("Tất cả GV đủ ĐK đã được lấy GPA")

        with detail_tab3:
            if count3 > 0:
                st.dataframe(report3, use_container_width=True)
            else:
                st.success("Không có lớp nào vi phạm")

        with detail_tab4:
            st.dataframe(lecturer_pct, use_container_width=True)

        # --- TẢI BÁO CÁO ---
        st.markdown("---")
        excel_report = export_reports_to_excel(report1, report2, report3)
        st.download_button(
            label="⬇️ Tải báo cáo đối sánh (.xlsx)",
            data=excel_report,
            file_name="BaoCao_DoiSanh_GPA.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            type="primary"
        )
