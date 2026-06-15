import pandas as pd
from io import BytesIO
from datetime import datetime


# ============================================================
#  1. MERGE FILES
# ============================================================

def merge_gpa_files(uploaded_files):
    """Gộp tất cả sheets từ tất cả file GPA thành 1 DataFrame.
    Chỉ lấy sheet có chứa cột 'GV' và 'GPA'.

    Returns:
        (DataFrame, list[str]): Dữ liệu đã gộp và danh sách log các sheet bị bỏ qua.
    """
    all_data = []
    skipped_log = []

    for f in uploaded_files:
        try:
            xl = pd.ExcelFile(f)
            for sh in xl.sheet_names:
                try:
                    df = pd.read_excel(xl, sheet_name=sh)
                except Exception as e:
                    skipped_log.append(f"⚠️ {f.name} / sheet '{sh}': Không đọc được - {e}")
                    continue

                if df.empty:
                    skipped_log.append(f"⏭️ {f.name} / sheet '{sh}': Sheet trống")
                    continue

                # Chuẩn hóa tên cột (strip spaces)
                cols_stripped = [str(col).strip() for col in df.columns.tolist()]
                cols_upper = [col.upper() for col in cols_stripped]

                # Phải có cả 'GV' và 'GPA'
                has_gv = 'GV' in cols_upper
                has_gpa = 'GPA' in cols_upper

                if not (has_gv and has_gpa):
                    skipped_log.append(f"⏭️ {f.name} / sheet '{sh}': Thiếu cột "
                                       f"{'GV' if not has_gv else ''}"
                                       f"{' và ' if not has_gv and not has_gpa else ''}"
                                       f"{'GPA' if not has_gpa else ''}")
                    continue

                df.columns = cols_stripped
                df['Source_File'] = f.name
                df['Source_Sheet'] = sh
                all_data.append(df)
        except Exception as e:
            skipped_log.append(f"❌ {f.name}: Không mở được file - {e}")
            continue

    if not all_data:
        return pd.DataFrame(), skipped_log
    result = pd.concat(all_data, ignore_index=True)
    return result, skipped_log


def merge_schedule_files(uploaded_files):
    """Gộp tất cả sheets từ tất cả file lịch kỳ thành 1 DataFrame.
    Chỉ lấy sheet có chứa cột 'GroupName' và 'Lecturer'.

    Returns:
        (DataFrame, list[str]): Dữ liệu đã gộp và danh sách log các sheet bị bỏ qua.
    """
    all_data = []
    skipped_log = []

    for f in uploaded_files:
        try:
            xl = pd.ExcelFile(f)
            for sh in xl.sheet_names:
                try:
                    df = pd.read_excel(xl, sheet_name=sh)
                except Exception as e:
                    skipped_log.append(f"⚠️ {f.name} / sheet '{sh}': Không đọc được - {e}")
                    continue

                if df.empty:
                    skipped_log.append(f"⏭️ {f.name} / sheet '{sh}': Sheet trống")
                    continue

                cols_stripped = [str(col).strip() for col in df.columns.tolist()]

                has_group = 'GroupName' in cols_stripped
                has_lecturer = 'Lecturer' in cols_stripped

                if not (has_group and has_lecturer):
                    skipped_log.append(f"⏭️ {f.name} / sheet '{sh}': Thiếu cột "
                                       f"{'GroupName' if not has_group else ''}"
                                       f"{' và ' if not has_group and not has_lecturer else ''}"
                                       f"{'Lecturer' if not has_lecturer else ''}")
                    continue

                df.columns = cols_stripped
                df['Source_File'] = f.name
                df['Source_Sheet'] = sh
                all_data.append(df)
        except Exception as e:
            skipped_log.append(f"❌ {f.name}: Không mở được file - {e}")
            continue

    if not all_data:
        return pd.DataFrame(), skipped_log
    result = pd.concat(all_data, ignore_index=True)
    return result, skipped_log


# ============================================================
#  2. CALCULATE LECTURER PERCENTAGE (≥30%)
# ============================================================

def calculate_lecturer_percentage(schedule_df,
                                   group_col='GroupName',
                                   subject_col='SubjectCode',
                                   lecturer_col='Lecturer'):
    """
    Tính % số session mỗi GV dạy trong từng lớp/môn.
    Không phân biệt hoa/thường. Tất cả session đều được tính.
    """
    df = schedule_df.copy()

    # Chuẩn hóa: lowercase + strip
    df[group_col] = df[group_col].astype(str).str.strip().str.lower()
    df[subject_col] = df[subject_col].astype(str).str.strip().str.lower()
    df[lecturer_col] = df[lecturer_col].astype(str).str.strip().str.lower()

    # Tổng session theo lớp/môn
    total_sessions = df.groupby([group_col, subject_col]).size().reset_index(name='Total_Sessions')

    # Session theo GV/lớp/môn
    lecturer_sessions = df.groupby([group_col, subject_col, lecturer_col]).size().reset_index(name='GV_Sessions')

    # Merge
    merged = lecturer_sessions.merge(total_sessions, on=[group_col, subject_col], how='left')
    merged['Tỷ lệ (%)'] = round(merged['GV_Sessions'] / merged['Total_Sessions'] * 100, 1)
    merged['Đủ ĐK 30%'] = merged['Tỷ lệ (%)'] >= 30

    return merged


# ============================================================
#  3. CHECK RESPONSE RATE (≥60%) & SUCCESS RATE (≥95%)
# ============================================================

def check_response_rate(gpa_df):
    """
    Kiểm tra tỷ lệ phản hồi từng lớp và tính tỷ lệ lớp thành công.
    Thêm cột 'Tỷ lệ phản hồi (%)' và 'Đạt phản hồi 60%' vào DataFrame.
    """
    df = gpa_df.copy()

    # Tìm cột số SV đã feedback và số SV lớp
    sv_fb_col = None
    sv_total_col = None

    for col in df.columns:
        col_lower = col.lower().strip()
        if 'số sv đã feedback' in col_lower or 'sv đã feedback' in col_lower or 'số sv đã fb' in col_lower:
            sv_fb_col = col
        elif 'số sv lớp' in col_lower or 'sv lớp' in col_lower:
            sv_total_col = col

    # Tìm cột tỷ lệ có sẵn
    rate_col = None
    for col in df.columns:
        col_lower = col.lower().strip()
        if 'tỷ lệ' in col_lower and ('feedback' in col_lower or 'sv' in col_lower or 'phản hồi' in col_lower):
            rate_col = col
            break

    if sv_fb_col and sv_total_col:
        # Tính từ 2 cột số liệu
        fb = pd.to_numeric(df[sv_fb_col], errors='coerce')
        total = pd.to_numeric(df[sv_total_col], errors='coerce')
        df['Tỷ lệ phản hồi (%)'] = round(fb / total * 100, 1)
    elif rate_col:
        # Dùng cột tỷ lệ có sẵn
        df['Tỷ lệ phản hồi (%)'] = pd.to_numeric(
            df[rate_col].astype(str).str.replace('%', '').str.replace(',', '.'),
            errors='coerce'
        )
        # Nếu giá trị <= 1.5 thì đang ở dạng 0.xx → nhân 100
        if df['Tỷ lệ phản hồi (%)'].max() <= 1.5:
            df['Tỷ lệ phản hồi (%)'] = round(df['Tỷ lệ phản hồi (%)'] * 100, 1)
    else:
        # Không tìm được cột → trả về trống
        df['Tỷ lệ phản hồi (%)'] = None
        df['Đạt phản hồi 60%'] = None
        return df, pd.DataFrame(), {
            'total_classes': len(df),
            'classes_success': 0,
            'classes_fail': 0,
            'success_rate': 0
        }

    # Đánh dấu đạt / không đạt
    df['Đạt phản hồi 60%'] = df['Tỷ lệ phản hồi (%)'] >= 60

    # Lọc lớp không đạt
    low_response_df = df[df['Đạt phản hồi 60%'] == False].copy()

    # Tính tỷ lệ lớp thành công
    total_classes = len(df)
    classes_success = len(df[df['Đạt phản hồi 60%'] == True])
    classes_fail = total_classes - classes_success
    success_rate = round(classes_success / total_classes * 100, 1) if total_classes > 0 else 0

    summary_stats = {
        'total_classes': total_classes,
        'classes_success': classes_success,
        'classes_fail': classes_fail,
        'success_rate': success_rate,
    }

    return df, low_response_df, summary_stats


# ============================================================
#  4. GENERATE REPORTS
# ============================================================

def generate_reports(schedule_df, gpa_df):
    """
    Tạo 3 báo cáo chính:
    - report1: Lớp có GPA < 3.4
    - report2: GV đủ 30% nhưng chưa được lấy GPA
    - report3: GV dưới 30% nhưng bị lấy GPA (hiển thị theo cấu trúc lịch kỳ)

    Không phân biệt hoa/thường khi matching.
    Returns: (report1, report2, report3, error_message)
    """
    try:
        # Tính tỷ lệ GV (đã lowercase bên trong hàm)
        lecturer_pct = calculate_lecturer_percentage(schedule_df)

        # Tìm cột trong GPA
        gpa_cols = gpa_df.columns.tolist()

        gv_col = None
        for col in gpa_cols:
            if col.strip().upper() == 'GV':
                gv_col = col
                break
        if gv_col is None:
            for col in gpa_cols:
                if col.strip() == 'Lecturer':
                    gv_col = col
                    break

        lop_col = None
        for col in gpa_cols:
            if col.strip() == 'Lớp':
                lop_col = col
                break
        if lop_col is None:
            for col in gpa_cols:
                if col.strip() == 'GroupName':
                    lop_col = col
                    break

        mon_col = None
        for col in gpa_cols:
            if col.strip() == 'Môn':
                mon_col = col
                break
        if mon_col is None:
            for col in gpa_cols:
                if col.strip() == 'SubjectCode':
                    mon_col = col
                    break

        gpa_score_col = None
        for col in gpa_cols:
            if col.strip().upper() == 'GPA':
                gpa_score_col = col
                break

        if not all([gv_col, lop_col, mon_col, gpa_score_col]):
            missing = []
            if not gv_col: missing.append("GV")
            if not lop_col: missing.append("Lớp")
            if not mon_col: missing.append("Môn")
            if not gpa_score_col: missing.append("GPA")
            return None, None, None, f"Thiếu cột trong file GPA: {', '.join(missing)}"

        # ── REPORT 1: GPA < 3.4 ──
        gpa_df[gpa_score_col] = pd.to_numeric(gpa_df[gpa_score_col], errors='coerce')
        report1 = gpa_df[gpa_df[gpa_score_col] < 3.4].copy()

        # ── Tạo key matching (LOWERCASE để không phân biệt hoa/thường) ──
        eligible = lecturer_pct[lecturer_pct['Đủ ĐK 30%'] == True].copy()
        eligible['_key'] = (
            eligible['GroupName'].astype(str).str.strip().str.lower() + '|' +
            eligible['SubjectCode'].astype(str).str.strip().str.lower() + '|' +
            eligible['Lecturer'].astype(str).str.strip().str.lower()
        )

        gpa_df['_key'] = (
            gpa_df[lop_col].astype(str).str.strip().str.lower() + '|' +
            gpa_df[mon_col].astype(str).str.strip().str.lower() + '|' +
            gpa_df[gv_col].astype(str).str.strip().str.lower()
        )

        gpa_keys = set(gpa_df['_key'].tolist())

        # ── REPORT 2: GV đủ 30% nhưng chưa lấy GPA ──
        report2 = eligible[~eligible['_key'].isin(gpa_keys)].copy()
        report2 = report2.drop(columns=['_key'], errors='ignore')

        # ── REPORT 3: GV dưới 30% nhưng bị lấy GPA ──
        not_eligible = lecturer_pct[lecturer_pct['Đủ ĐK 30%'] == False].copy()
        not_eligible['_key'] = (
            not_eligible['GroupName'].astype(str).str.strip().str.lower() + '|' +
            not_eligible['SubjectCode'].astype(str).str.strip().str.lower() + '|' +
            not_eligible['Lecturer'].astype(str).str.strip().str.lower()
        )

        # Lọc: chỉ lấy GV dưới 30% mà CÓ xuất hiện trong file GPA
        gpa_keys_in_not_eligible = set(
            gpa_df[gpa_df['_key'].isin(set(not_eligible['_key'].tolist()))]['_key'].unique()
        )
        report3 = not_eligible[not_eligible['_key'].isin(gpa_keys_in_not_eligible)].copy()
        report3 = report3.drop(columns=['_key'], errors='ignore')

        # Clean up key tạm
        gpa_df.drop(columns=['_key'], errors='ignore', inplace=True)

        return report1, report2, report3, None

    except Exception as e:
        return None, None, None, str(e)


# ============================================================
#  5. GENERATE SUMMARY SHEET
# ============================================================

def generate_summary(gpa_stats, response_stats):
    """
    Tạo sheet tổng kết toàn bộ thông tin đã check.
    """
    today = datetime.now().strftime('%d/%m/%Y')

    summary_data = {
        'Chỉ số': [
            'Ngày kiểm tra',
            '---',
            'TỔNG QUAN GPA',
            'Tổng số lớp đã lấy GPA',
            'Số lớp GPA ≥ 3.4 (Đạt)',
            'Số lớp GPA < 3.4 (Không đạt)',
            '---',
            'KIỂM TRA ĐIỀU KIỆN 30%',
            'Số GV/lớp đủ 30% nhưng chưa lấy GPA',
            'Số GV/lớp dưới 30% nhưng bị lấy GPA (vi phạm)',
            '---',
            'TỶ LỆ PHẢN HỒI',
            'Tổng số lớp kiểm tra phản hồi',
            'Số lớp đạt tỷ lệ phản hồi ≥ 60%',
            'Số lớp KHÔNG đạt tỷ lệ phản hồi < 60%',
            'Tỷ lệ lớp lấy GPA thành công',
            'Ngưỡng yêu cầu',
            'Kết luận tỷ lệ thành công',
        ],
        'Giá trị': [
            today,
            '',
            '',
            gpa_stats.get('total_gpa_classes', 0),
            gpa_stats.get('gpa_pass', 0),
            gpa_stats.get('gpa_low', 0),
            '',
            '',
            gpa_stats.get('eligible_no_gpa', 0),
            gpa_stats.get('not_eligible_has_gpa', 0),
            '',
            '',
            response_stats.get('total_classes', 0),
            response_stats.get('classes_success', 0),
            response_stats.get('classes_fail', 0),
            f"{response_stats.get('success_rate', 0)}%",
            '≥ 95%',
            'ĐẠT' if response_stats.get('success_rate', 0) >= 95 else 'KHÔNG ĐẠT',
        ]
    }

    return pd.DataFrame(summary_data)


# ============================================================
#  6. GENERATE OUTPUT FILENAME
# ============================================================

def generate_output_filename():
    """Tạo tên file output theo cú pháp: yyyymmdd-GPA check.xlsx"""
    today = datetime.now().strftime('%Y%m%d')
    return f"{today}-GPA check.xlsx"


# ============================================================
#  7. EXPORT TO EXCEL
# ============================================================

def export_reports_to_excel(report1, report2, report3, gpa_merged, low_response_df, summary_df):
    """
    Xuất báo cáo ra file Excel với nhiều sheets:
    - Sheet 1: Tổng kết
    - Sheet 2: Tổng hợp GPA (có Source_File, Source_Sheet, Tỷ lệ phản hồi, Đạt phản hồi 60%)
    - Sheet 3: GPA dưới 3.4
    - Sheet 4: Đủ 30% chưa lấy GPA
    - Sheet 5: Dưới 30% bị lấy GPA
    - Sheet 6: Lớp có tỷ lệ phản hồi < 60%
    """
    output = BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Sheet 1: Tổng kết
        if summary_df is not None and not summary_df.empty:
            summary_df.to_excel(writer, sheet_name='Tổng kết', index=False)
        else:
            pd.DataFrame({'Thông báo': ['Không có dữ liệu tổng kết']}).to_excel(
                writer, sheet_name='Tổng kết', index=False)

        # Sheet 2: Tổng hợp GPA
        if gpa_merged is not None and not gpa_merged.empty:
            gpa_merged.to_excel(writer, sheet_name='Tổng hợp GPA', index=False)
        else:
            pd.DataFrame({'Thông báo': ['Không có dữ liệu GPA']}).to_excel(
                writer, sheet_name='Tổng hợp GPA', index=False)

        # Sheet 3: GPA dưới 3.4
        if report1 is not None and not report1.empty:
            report1.to_excel(writer, sheet_name='GPA dưới 3.4', index=False)
        else:
            pd.DataFrame({'Thông báo': ['Không có lớp nào GPA dưới 3.4']}).to_excel(
                writer, sheet_name='GPA dưới 3.4', index=False)

        # Sheet 4: Đủ 30% chưa lấy GPA
        if report2 is not None and not report2.empty:
            report2.to_excel(writer, sheet_name='Đủ 30% chưa lấy GPA', index=False)
        else:
            pd.DataFrame({'Thông báo': ['Tất cả GV đủ ĐK đã được lấy GPA']}).to_excel(
                writer, sheet_name='Đủ 30% chưa lấy GPA', index=False)

        # Sheet 5: Dưới 30% bị lấy GPA
        if report3 is not None and not report3.empty:
            report3.to_excel(writer, sheet_name='Dưới 30% bị lấy GPA', index=False)
        else:
            pd.DataFrame({'Thông báo': ['Không có lớp nào vi phạm']}).to_excel(
                writer, sheet_name='Dưới 30% bị lấy GPA', index=False)

        # Sheet 6: Lớp phản hồi dưới 60%
        if low_response_df is not None and not low_response_df.empty:
            low_response_df.to_excel(writer, sheet_name='Phản hồi dưới 60%', index=False)
        else:
            pd.DataFrame({'Thông báo': ['Tất cả lớp đều đạt tỷ lệ phản hồi ≥ 60%']}).to_excel(
                writer, sheet_name='Phản hồi dưới 60%', index=False)

    output.seek(0)
    return output.getvalue()
