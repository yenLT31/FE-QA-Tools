import streamlit as st
import pandas as pd
from scripts.gpa-schedule-checker import (
    merge_gpa_files,
    merge_schedule_files,
    calculate_lecturer_percentage,
    generate_reports,
    export_reports_to_excel
)

st.set_page_config(page_title="GPA Schedule Checker", layout="wide")
st.title("📋 Đối sánh GPA & Lịch kỳ")

st.markdown("---")

# --- BƯỚC 1: Nạp file lịch kỳ ---
st.header("1. Nạp file Lịch kỳ")
schedule_files = st.file_uploader(
    "Chọn file(s) lịch kỳ (chứa cột: GroupName, SubjectCode, Lecturer...)",
    type=['xlsx', 'xls'],
    accept_multiple_files=True,
    key='schedule'
)

# --- BƯỚC 2: Nạp file GPA ---
st.header("2. Nạp file(s) GPA Feedback")
gpa_files = st.file_uploader(
    "Chọn file(s) GPA (chứa cột: GV, Lớp, Môn, GPA, Comments...)",
    type=['xlsx', 'xls'],
    accept_multiple_files=True,
    key='gpa'
)

st.markdown("---")

# --- BƯỚC 3: Chạy đối sánh ---
if schedule_files and gpa_files:
    st.header("3. Kết quả đối sánh")

    if st.button("🔍 Chạy đối sánh"):
        with st.spinner("Đang xử lý..."):

            # Gộp files
            schedule_df = merge_schedule_files(schedule_files)
            gpa_df = merge_gpa_files(gpa_files)

            if schedule_df.empty:
                st.error("File lịch kỳ không có dữ liệu.")
                st.stop()
            if gpa_df.empty:
                st.error("File GPA không có dữ liệu.")
                st.stop()

            # Tính tỷ lệ GV
            lecturer_pct = calculate_lecturer_percentage(schedule_df)
            st.session_state['lecturer_pct'] = lecturer_pct

            # Tạo báo cáo
            report1, report2, report3, error = generate_reports(schedule_df, gpa_df)

            if error:
                st.error(error)
                st.stop()

            st.session_state['report1'] = report1
            st.session_state['report2'] = report2
            st.session_state['report3'] = report3

        st.success("Đối sánh hoàn tất!")

    # --- Hiển thị kết quả ---
    if 'report1' in st.session_state:

        # Tab hiển thị
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔴 GPA dưới 3.4",
            "🟡 Đủ 30% chưa lấy GPA",
            "🟠 Dưới 30% bị lấy GPA",
            "📊 Tỷ lệ % GV theo lớp"
        ])

        with tab1:
            report1 = st.session_state['report1']
            if not report1.empty:
                st.warning(f"Có {len(report1)} lớp GPA dưới 3.4")
                st.dataframe(report1, use_container_width=True)
            else:
                st.success("Không có lớp nào GPA dưới 3.4")

        with tab2:
            report2 = st.session_state['report2']
            if not report2.empty:
                st.warning(f"Có {len(report2)} GV đủ ĐK nhưng chưa lấy GPA")
                st.dataframe(report2, use_container_width=True)
            else:
                st.success("Tất cả GV đủ ĐK đã được lấy GPA")

        with tab3:
            report3 = st.session_state['report3']
            if not report3.empty:
                st.error(f"Có {len(report3)} lớp dưới 30% nhưng bị lấy GPA (sai quy định)")
                st.dataframe(report3, use_container_width=True)
            else:
                st.success("Không có lớp nào vi phạm")

        with tab4:
            lecturer_pct = st.session_state['lecturer_pct']
            st.dataframe(lecturer_pct, use_container_width=True)

        # --- Tải báo cáo ---
        st.markdown("---")
        excel_report = export_reports_to_excel(
            st.session_state['report1'],
            st.session_state['report2'],
            st.session_state['report3']
        )
        st.download_button(
            label="⬇️ Tải báo cáo đối sánh (.xlsx)",
            data=excel_report,
            file_name="BaoCao_DoiSanh_GPA.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:
    st.info("Vui lòng nạp cả file lịch kỳ và file GPA để bắt đầu đối sánh.")
