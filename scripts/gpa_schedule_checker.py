import pandas as pd
import re
from io import BytesIO
from datetime import datetime


def merge_gpa_files(uploaded_files):
    """
    Gộp tất cả sheets từ tất cả files GPA thành 1 DataFrame.
    """
    all_data = []

    for file in uploaded_files:
        try:
            xl = pd.ExcelFile(file)
            for sheet_name in xl.sheet_names:
                try:
                    df = pd.read_excel(file, sheet_name=sheet_name)
                    if df.empty:
                        continue
                    df['Source_File'] = file.name
                    df['Source_Sheet'] = sheet_name
                    all_data.append(df)
                except Exception:
                    pass
        except Exception:
            pass

    if all_data:
        result = pd.concat(all_data, ignore_index=True)
        return result
    else:
        return pd.DataFrame()


def merge_schedule_files(uploaded_files):
    """
    Gộp tất cả sheets từ tất cả files lịch kỳ thành 1 DataFrame.
    """
    all_data = []

    for file in uploaded_files:
        try:
            xl = pd.ExcelFile(file)
            for sheet_name in xl.sheet_names:
                try:
                    df = pd.read_excel(file, sheet_name=sheet_name)
                    if df.empty:
                        continue
                    all_data.append(df)
                except Exception:
                    pass
        except Exception:
            pass

    if all_data:
        result = pd.concat(all_data, ignore_index=True)
        return result
    else:
        return pd.DataFrame()


def calculate_lecturer_percentage(schedule_df):
    """
    Tính tỷ lệ % session mỗi GV dạy trong từng lớp/môn.
    """
    total_sessions = schedule_df.groupby(
        ['GroupName', 'SubjectCode']
    ).size().reset_index(name='Tổng_Session_Lớp')

    gv_sessions = schedule_df.groupby(
        ['GroupName', 'SubjectCode', 'Lecturer']
    ).size().reset_index(name='Session_GV_Dạy')

    result = gv_sessions.merge(total_sessions, on=['GroupName', 'SubjectCode'], how='left')
    result['Tỷ_Lệ_%'] = round(result['Session_GV_Dạy'] / result['Tổng_Session_Lớp'] * 100, 1)
    result['Đủ_ĐK_30%'] = result['Tỷ_Lệ_%'] >= 30

    return result


def generate_reports(schedule_df, gpa_df):
    """
    Tạo 4 báo cáo:
    1. Lớp có GPA < 3.4
    2. Lớp đủ ĐK >=30% nhưng CHƯA lấy GPA
    3. Lớp dưới 30% nhưng BỊ lấy GPA
    4. Lớp có trong GPA nhưng KHÔNG có trong lịch kỳ
    """

    # --- Tính tỷ lệ GV ---
    lecturer_pct = calculate_lecturer_percentage(schedule_df)

    # Lấy danh sách GV đủ ĐK 30%
    eligible = lecturer_pct[lecturer_pct['Đủ_ĐK_30%'] == True][['GroupName', 'SubjectCode', 'Lecturer', 'Tỷ_Lệ_%']].copy()
    eligible.rename(columns={'GroupName': 'Lớp', 'Lecturer': 'GV'}, inplace=True)

    # Lấy danh sách GV không đủ ĐK 30%
    not_eligible = lecturer_pct[lecturer_pct['Đủ_ĐK_30%'] == False][['GroupName', 'SubjectCode', 'Lecturer', 'Tỷ_Lệ_%']].copy()
    not_eligible.rename(columns={'GroupName': 'Lớp', 'Lecturer': 'GV'}, inplace=True)

    # --- Chuẩn hóa cột trong GPA ---
    gpa_lop_col = None
    gpa_gv_col = None
    gpa_mon_col = None

    for col in gpa_df.columns:
        if col.strip().lower() in ['lớp', 'lop', 'groupname']:
            gpa_lop_col = col
        if col.strip().lower() in ['gv', 'lecturer']:
            gpa_gv_col = col
        if col.strip().lower() in ['môn', 'mon', 'subjectcode']:
            gpa_mon_col = col

    if not gpa_lop_col or not gpa_gv_col:
        return None, None, None, None, "Không tìm thấy cột Lớp hoặc GV trong file GPA"

    # Tạo key để match
    gpa_df['_key'] = gpa_df[gpa_lop_col].astype(str).str.strip() + '|' + gpa_df[gpa_gv_col].astype(str).str.strip()
    eligible['_key'] = eligible['Lớp'].astype(str).str.strip() + '|' + eligible['GV'].astype(str).str.strip()
    not_eligible['_key'] = not_eligible['Lớp'].astype(str).str.strip() + '|' + not_eligible['GV'].astype(str).str.strip()

    # Tạo key từ lịch kỳ (tất cả GV/Lớp)
    all_schedule_keys = set(
        lecturer_pct['GroupName'].astype(str).str.strip() + '|' + lecturer_pct['Lecturer'].astype(str).str.strip()
    )

    # --- BÁO CÁO 1: GPA < 3.4 ---
    gpa_col = None
    for col in gpa_df.columns:
        if col.strip().upper() == 'GPA':
            gpa_col = col
            break

    if gpa_col:
        gpa_df[gpa_col] = pd.to_numeric(gpa_df[gpa_col], errors='coerce')
        report1 = gpa_df[gpa_df[gpa_col] < 3.4].copy()
        report1 = report1.drop(columns=['_key'], errors='ignore')
    else:
        report1 = pd.DataFrame()

    # --- BÁO CÁO 2: Đủ ĐK >=30% nhưng CHƯA lấy GPA ---
    gpa_keys = set(gpa_df['_key'].tolist())
    eligible_not_surveyed = eligible[~eligible['_key'].isin(gpa_keys)].copy()
    eligible_not_surveyed = eligible_not_surveyed.drop(columns=['_key'], errors='ignore')

    # --- BÁO CÁO 3: Dưới 30% nhưng BỊ lấy GPA ---
    not_eligible_but_surveyed = gpa_df[gpa_df['_key'].isin(set(not_eligible['_key'].tolist()))].copy()
    not_eligible_but_surveyed = not_eligible_but_surveyed.drop(columns=['_key'], errors='ignore')

    # --- BÁO CÁO 4: Có trong GPA nhưng KHÔNG có trong lịch kỳ ---
    gpa_not_in_schedule = gpa_df[~gpa_df['_key'].isin(all_schedule_keys)].copy()
    gpa_not_in_schedule = gpa_not_in_schedule.drop(columns=['_key'], errors='ignore')

    # Cleanup
    gpa_df.drop(columns=['_key'], errors='ignore', inplace=True)

    return report1, eligible_not_surveyed, not_eligible_but_surveyed, gpa_not_in_schedule, None


def export_gpa_merged(gpa_df):
    """
    Xuất file tổng hợp GPA (có Source_File, Source_Sheet).
    Tên file: yyyymmdd Tổng hợp GPA.xlsx
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        gpa_df.to_excel(writer, index=False, sheet_name='Tổng hợp GPA')
    output.seek(0)
    return output


def get_merged_filename():
    """Trả về tên file tổng hợp GPA với ngày hiện tại."""
    today = datetime.now().strftime('%Y%m%d')
    return f"{today} Tổng hợp GPA.xlsx"


def export_reports_to_excel(report1, report2, report3, report4):
    """
    Xuất 4 báo cáo ra 1 file Excel với 4 sheets.
    Tên file: yyyymmdd Result check GPA.xlsx
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        if report1 is not None and not report1.empty:
            report1.to_excel(writer, index=False, sheet_name='GPA dưới 3.4')
        else:
            pd.DataFrame({'Thông báo': ['Không có lớp nào GPA dưới 3.4']}).to_excel(
                writer, index=False, sheet_name='GPA dưới 3.4')

        if report2 is not None and not report2.empty:
            report2.to_excel(writer, index=False, sheet_name='Đủ 30% chưa lấy GPA')
        else:
            pd.DataFrame({'Thông báo': ['Tất cả GV đủ ĐK đã được lấy GPA']}).to_excel(
                writer, index=False, sheet_name='Đủ 30% chưa lấy GPA')

        if report3 is not None and not report3.empty:
            report3.to_excel(writer, index=False, sheet_name='Dưới 30% bị lấy GPA')
        else:
            pd.DataFrame({'Thông báo': ['Không có lớp nào dưới 30% bị lấy GPA']}).to_excel(
                writer, index=False, sheet_name='Dưới 30% bị lấy GPA')

        if report4 is not None and not report4.empty:
            report4.to_excel(writer, index=False, sheet_name='GPA không có trong lịch kỳ')
        else:
            pd.DataFrame({'Thông báo': ['Tất cả lớp lấy GPA đều có trong lịch kỳ']}).to_excel(
                writer, index=False, sheet_name='GPA không có trong lịch kỳ')

    output.seek(0)
    return output


def get_report_filename():
    """Trả về tên file báo cáo với ngày hiện tại."""
    today = datetime.now().strftime('%Y%m%d')
    return f"{today} Result check GPA.xlsx"
