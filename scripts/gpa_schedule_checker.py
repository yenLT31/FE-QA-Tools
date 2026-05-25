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


def check_response_rate(gpa_df):
    """
    Kiểm tra tỷ lệ phản hồi >= 60%.
    Trả về DataFrame các lớp chưa đạt tỷ lệ phản hồi.
    """
    # Tìm cột tỷ lệ phản hồi
    rate_col = None
    for col in gpa_df.columns:
        col_lower = col.strip().lower()
        if 'tỷ lệ' in col_lower or 'ti le' in col_lower or 'tỉ lệ' in col_lower or 'rate' in col_lower:
            rate_col = col
            break

    if not rate_col:
        # Thử tính từ Số SV đã feedback / Số SV lớp
        sv_fb_col = None
        sv_lop_col = None
        for col in gpa_df.columns:
            col_lower = col.strip().lower()
            if 'số sv đã' in col_lower or 'so sv da' in col_lower or 'feedback' in col_lower.replace(' ', ''):
                sv_fb_col = col
            if 'số sv lớp' in col_lower or 'so sv lop' in col_lower or col_lower == 'số sv lớp':
                sv_lop_col = col

        if sv_fb_col and sv_lop_col:
            gpa_df['_Tỷ_lệ_phản_hồi'] = pd.to_numeric(gpa_df[sv_fb_col], errors='coerce') / pd.to_numeric(gpa_df[sv_lop_col], errors='coerce')
            rate_col = '_Tỷ_lệ_phản_hồi'
        else:
            return pd.DataFrame(), None

    # Chuyển đổi tỷ lệ
    gpa_df['_rate_numeric'] = pd.to_numeric(gpa_df[rate_col], errors='coerce')

    # Nếu giá trị > 1 thì đang ở dạng % (vd: 63%), cần chia 100
    # Nếu giá trị <= 1 thì đang ở dạng thập phân (vd: 0.63)
    if gpa_df['_rate_numeric'].max() > 1:
        gpa_df['_rate_decimal'] = gpa_df['_rate_numeric'] / 100
    else:
        gpa_df['_rate_decimal'] = gpa_df['_rate_numeric']

    # Lọc lớp có tỷ lệ phản hồi < 60%
    low_response = gpa_df[gpa_df['_rate_decimal'] < 0.6].copy()
    low_response = low_response.drop(columns=['_rate_numeric', '_rate_decimal', '_Tỷ_lệ_phản_hồi'], errors='ignore')

    # Cleanup
    gpa_df.drop(columns=['_rate_numeric', '_rate_decimal', '_Tỷ_lệ_phản_hồi'], errors='ignore', inplace=True)

    return low_response, rate_col


def generate_summary(gpa_df, report1, report2, report3, report4, low_response, lecturer_pct):
    """
    Tạo sheet tổng kết thông tin chung.
    """
    # Tổng số lớp trong GPA
    gpa_lop_col = None
    for col in gpa_df.columns:
        if col.strip().lower() in ['lớp', 'lop', 'groupname']:
            gpa_lop_col = col
            break

    total_classes_gpa = len(gpa_df) if not gpa_df.empty else 0

    # Tổng số lớp/GV trong lịch kỳ đủ ĐK 30%
    total_eligible = len(lecturer_pct[lecturer_pct['Đủ_ĐK_30%'] == True]) if not lecturer_pct.empty else 0

    # Tỷ lệ lớp lấy GPA thành công
    # = Số lớp đã lấy GPA có tỷ lệ phản hồi >= 60% / Tổng lớp đã lấy GPA
    low_response_count = len(low_response) if low_response is not None and not low_response.empty else 0
    classes_success = total_classes_gpa - low_response_count
    success_rate = round(classes_success / total_classes_gpa * 100, 1) if total_classes_gpa > 0 else 0

    summary_data = {
        'Chỉ số': [
            'Tổng số lớp đã lấy GPA',
            'Tổng GV/Lớp đủ ĐK 30% (theo lịch kỳ)',
            'Số lớp GPA dưới 3.4',
            'Số GV đủ 30% chưa lấy GPA',
            'Số lớp dưới 30% bị lấy GPA',
            'Số lớp GPA không có trong lịch kỳ',
            'Số lớp tỷ lệ phản hồi < 60%',
            'Số lớp tỷ lệ phản hồi >= 60%',
            'Tỷ lệ lớp lấy GPA thành công (phản hồi >= 60%)',
            'Đạt chuẩn tỷ lệ lớp thành công >= 95%'
        ],
        'Giá trị': [
            total_classes_gpa,
            total_eligible,
            len(report1) if report1 is not None and not report1.empty else 0,
            len(report2) if report2 is not None and not report2.empty else 0,
            len(report3) if report3 is not None and not report3.empty else 0,
            len(report4) if report4 is not None and not report4.empty else 0,
            low_response_count,
            classes_success,
            f"{success_rate}%",
            "✅ ĐẠT" if success_rate >= 95 else "❌ CHƯA ĐẠT"
        ]
    }

    return pd.DataFrame(summary_data)


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

    for col in gpa_df.columns:
        if col.strip().lower() in ['lớp', 'lop', 'groupname']:
            gpa_lop_col = col
        if col.strip().lower() in ['gv', 'lecturer']:
            gpa_gv_col = col

    if not gpa_lop_col or not gpa_gv_col:
        return None, None, None, None, None, None, "Không tìm thấy cột Lớp hoặc GV trong file GPA"

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

    # --- Kiểm tra tỷ lệ phản hồi ---
    low_response, rate_col = check_response_rate(gpa_df)

    # --- Tổng kết ---
    summary = generate_summary(gpa_df, report1, report2, report3, report4, low_response, lecturer_pct)

    # Cleanup
    gpa_df.drop(columns=['_key'], errors='ignore', inplace=True)

    return report1, eligible_not_surveyed, not_eligible_but_surveyed, gpa_not_in_schedule, low_response, summary, None


def export_gpa_merged(gpa_df):
    """
    Xuất file tổng hợp GPA (có Source_File, Source_Sheet).
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


def export_reports_to_excel(report1, report2, report3, report4, low_response, summary):
    """
    Xuất báo cáo ra 1 file Excel với nhiều sheets.
    Sheet đầu tiên là Tổng kết.
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Sheet 1: Tổng kết
        if summary is not None and not summary.empty:
            summary.to_excel(writer, index=False, sheet_name='Tổng kết')
        else:
            pd.DataFrame({'Thông báo': ['Không có dữ liệu tổng kết']}).to_excel(
                writer, index=False, sheet_name='Tổng kết')

        # Sheet 2: GPA dưới 3.4
        if report1 is not None and not report1.empty:
            report1.to_excel(writer, index=False, sheet_name='GPA dưới 3.4')
        else:
            pd.DataFrame({'Thông báo': ['Không có lớp nào GPA dưới 3.4']}).to_excel(
                writer, index=False, sheet_name='GPA dưới 3.4')

        # Sheet 3: Đủ 30% chưa lấy GPA
        if report2 is not None and not report2.empty:
            report2.to_excel(writer, index=False, sheet_name='Đủ 30% chưa lấy GPA')
        else:
            pd.DataFrame({'Thông báo': ['Tất cả GV đủ ĐK đã được lấy GPA']}).to_excel(
                writer, index=False, sheet_name='Đủ 30% chưa lấy GPA')

        # Sheet 4: Dưới 30% bị lấy GPA
        if report3 is not None and not report3.empty:
            report3.to_excel(writer, index=False, sheet_name='Dưới 30% bị lấy GPA')
        else:
            pd.DataFrame({'Thông báo': ['Không có lớp nào dưới 30% bị lấy GPA']}).to_excel(
                writer, index=False, sheet_name='Dưới 30% bị lấy GPA')

        # Sheet 5: GPA không có trong lịch kỳ
        if report4 is not None and not report4.empty:
            report4.to_excel(writer, index=False, sheet_name='GPA không có trong lịch kỳ')
        else:
            pd.DataFrame({'Thông báo': ['Tất cả lớp lấy GPA đều có trong lịch kỳ']}).to_excel(
                writer, index=False, sheet_name='GPA không có trong lịch kỳ')

        # Sheet 6: Lớp tỷ lệ phản hồi < 60%
        if low_response is not None and not low_response.empty:
            low_response.to_excel(writer, index=False, sheet_name='Phản hồi dưới 60%')
        else:
            pd.DataFrame({'Thông báo': ['Tất cả lớp đều đạt tỷ lệ phản hồi >= 60%']}).to_excel(
                writer, index=False, sheet_name='Phản hồi dưới 60%')

    output.seek(0)
    return output


def get_report_filename():
    """Trả về tên file báo cáo với ngày hiện tại."""
    today = datetime.now().strftime('%Y%m%d')
    return f"{today} Result check GPA.xlsx"
