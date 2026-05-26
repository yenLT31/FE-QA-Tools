"""
Teaching Hours Checker - Logic xử lý
Kiểm soát giờ dạy GV: đối chiếu Lịch kỳ FAP, Teaching Summaries, Phiếu chấm công ĐT
FPT Education QA Department
© 2026 YenLT31
"""

import pandas as pd
import numpy as np
import re
from io import BytesIO
from datetime import datetime


# ============================================================
# 1. ĐỌC VÀ CHUẨN HÓA DỮ LIỆU
# ============================================================

def read_lich_ky(files):
    """
    Đọc và gộp nhiều file Lịch kỳ FAP.
    Chuẩn hóa cột Date về datetime.
    """
    all_data = []
    for file in files:
        try:
            df = pd.read_excel(file, dtype=str)
            # Chuẩn hóa tên cột (strip whitespace)
            df.columns = df.columns.str.strip()
            all_data.append(df)
        except Exception as e:
            print(f"Lỗi đọc file lịch kỳ: {e}")
            continue
    
    if not all_data:
        return pd.DataFrame()
    
    df = pd.concat(all_data, ignore_index=True)
    
    # Chuẩn hóa cột Date
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    
    # Chuẩn hóa cột Lecturer: lowercase, strip
    df['Lecturer'] = df['Lecturer'].astype(str).str.strip().str.lower()
    
    # Chuẩn hóa SubjectCode: strip
    df['SubjectCode'] = df['SubjectCode'].astype(str).str.strip()
    
    # Chuẩn hóa GroupName: strip
    df['GroupName'] = df['GroupName'].astype(str).str.strip()
    
    # Chuẩn hóa TypeSlot: strip, uppercase
    df['TypeSlot'] = df['TypeSlot'].astype(str).str.strip().str.upper()
    
    # Chuẩn hóa SlotTypeCode: strip, uppercase
    df['SlotTypeCode'] = df['SlotTypeCode'].astype(str).str.strip().str.upper()
    
    return df


def read_teaching_summaries(files):
    """
    Đọc nhiều file Teaching Summaries FAP.
    Mỗi file có thể có nhiều sheets (mỗi sheet là 1 tháng).
    Parse cấu trúc grouped (GV ở dòng riêng).
    Trả về DataFrame: Teacher, Group, Subject, AllPlan, WasNotTaken, FromDate, ToDate
    """
    all_data = []
    
    for file in files:
        try:
            # Đọc tất cả sheets trong file
            xl = pd.ExcelFile(file)
            
            for sheet_name in xl.sheet_names:
                df = pd.read_excel(file, sheet_name=sheet_name, header=None)
                
                # Bỏ qua sheet trống
                if df.empty or len(df) < 5:
                    continue
                
                # Tìm From Date và To Date
                from_date = None
                to_date = None
                
                for idx in range(min(10, len(df))):
                    row = df.iloc[idx]
                    row_str = [str(v).strip() for v in row.values if pd.notna(v)]
                    row_str_lower = [s.lower() for s in row_str]
                    
                    if 'from date' in row_str_lower:
                        # Dòng tiếp theo là giá trị
                        if idx + 1 < len(df):
                            next_row = df.iloc[idx + 1]
                            from_date = pd.to_datetime(next_row.iloc[0], dayfirst=True, errors='coerce')
                            to_date = pd.to_datetime(next_row.iloc[1], dayfirst=True, errors='coerce')
                        break
                
                # Tìm header row (Teacher, Group, Subject, All Plan, WasNot Taken)
                header_row_idx = None
                for idx in range(min(15, len(df))):
                    row = df.iloc[idx]
                    row_str = [str(v).strip().lower() for v in row.values if pd.notna(v)]
                    if 'teacher' in row_str and ('group' in row_str or 'class' in row_str):
                        header_row_idx = idx
                        break
                
                if header_row_idx is None:
                    continue
                
                # Đọc lại với header đúng
                df_data = df.iloc[header_row_idx + 1:].copy()
                headers = df.iloc[header_row_idx].values
                
                # Xử lý duplicate column names
                seen = {}
                clean_headers = []
                for h in headers:
                    h_str = str(h).strip() if pd.notna(h) else 'unnamed'
                    if h_str in seen:
                        seen[h_str] += 1
                        clean_headers.append(f"{h_str}_{seen[h_str]}")
                    else:
                        seen[h_str] = 0
                        clean_headers.append(h_str)
                
                df_data.columns = clean_headers
                
                # Tìm cột tương ứng (lấy cột đầu tiên match)
                teacher_col = None
                group_col = None
                subject_col = None
                allplan_col = None
                wasnot_col = None
                
                for col in df_data.columns:
                    col_lower = str(col).strip().lower()
                    if 'teacher' in col_lower and teacher_col is None:
                        teacher_col = col
                    elif 'group' in col_lower and group_col is None:
                        group_col = col
                    elif 'subject' in col_lower and subject_col is None:
                        subject_col = col
                    elif 'all plan' in col_lower and allplan_col is None:
                        allplan_col = col
                    elif ('wasnot' in col_lower or 'was not' in col_lower) and wasnot_col is None:
                        wasnot_col = col
                
                # Parse grouped structure
                current_teacher = None
                records = []
                
                for idx, row in df_data.iterrows():
                    teacher_val = str(row[teacher_col]).strip() if teacher_col and pd.notna(row[teacher_col]) else ''
                    group_val = str(row[group_col]).strip() if group_col and pd.notna(row[group_col]) else ''
                    subject_val = str(row[subject_col]).strip() if subject_col and pd.notna(row[subject_col]) else ''
                    allplan_val = row[allplan_col] if allplan_col else None
                    wasnot_val = str(row[wasnot_col]).strip() if wasnot_col and pd.notna(row[wasnot_col]) else ''
                    
                    # Loại bỏ giá trị 'nan'
                    if teacher_val.lower() == 'nan':
                        teacher_val = ''
                    if group_val.lower() == 'nan':
                        group_val = ''
                    if subject_val.lower() == 'nan':
                        subject_val = ''
                    if wasnot_val.lower() == 'nan':
                        wasnot_val = ''
                    
                    # Nếu có Teacher và không có Group → đây là dòng tên GV
                    if teacher_val and not group_val:
                        current_teacher = teacher_val.lower()
                    # Nếu có Group và Subject → đây là dòng dữ liệu
                    elif group_val and subject_val:
                        # Parse số WasNotTaken từ text
                        wasnot_count = 0
                        if wasnot_val:
                            match = re.search(r'(\d+)\s*slot', wasnot_val, re.IGNORECASE)
                            if match:
                                wasnot_count = int(match.group(1))
                        
                        # Parse AllPlan
                        try:
                            allplan_count = int(float(allplan_val)) if pd.notna(allplan_val) else 0
                        except (ValueError, TypeError):
                            allplan_count = 0
                        
                        records.append({
                            'Teacher': current_teacher if current_teacher else '',
                            'Group': group_val,
                            'Subject': subject_val,
                            'AllPlan': allplan_count,
                            'WasNotTaken': wasnot_count,
                            'WasNotTakenRaw': wasnot_val,
                            'FromDate': from_date,
                            'ToDate': to_date
                        })
                
                if records:
                    all_data.extend(records)
        
        except Exception as e:
            print(f"Lỗi đọc file Teaching Summaries: {e}")
            continue
    
    if not all_data:
        return pd.DataFrame()
    
    result = pd.DataFrame(all_data)
    return result


def read_cham_cong(files):
    """
    Đọc nhiều file Phiếu chấm công ĐT (sheet "Gio day cua thang").
    Parse thông tin tháng, khoảng ngày, giờ dạy.
    Xử lý merged cells.
    """
    all_data = []
    
    for file in files:
        try:
            # Tìm sheet phù hợp
            xl = pd.ExcelFile(file)
            target_sheet = None
            
            for s in xl.sheet_names:
                s_lower = s.lower().replace(' ', '').replace('_', '')
                if 'giodaycuathang' in s_lower or 'giờdạycủatháng' in s_lower:
                    target_sheet = s
                    break
                elif 'gioday' in s_lower or 'giờdạy' in s_lower:
                    target_sheet = s
                    break
            
            if target_sheet is None:
                target_sheet = xl.sheet_names[0]
            
            df = pd.read_excel(file, sheet_name=target_sheet, header=None)
            
            # Parse thông tin tháng và khoảng ngày
            thang = None
            from_date = None
            to_date = None
            
            for idx in range(min(10, len(df))):
                row = df.iloc[idx]
                for col_idx, val in enumerate(row.values):
                    if pd.notna(val):
                        val_str = str(val).strip()
                        if 'NĂM' in val_str.upper() or 'NAM' in val_str.upper():
                            for next_col in range(col_idx + 1, len(row.values)):
                                next_val = row.values[next_col]
                                if pd.notna(next_val):
                                    next_str = str(next_val).strip()
                                    thang_match = re.match(r'(\d{2}/\d{4})', next_str)
                                    if thang_match:
                                        thang = thang_match.group(1)
                                    
                                    date_match = re.search(
                                        r'[Tt]ừ\s+(\d{1,2}/\d{1,2}/\d{4})\s+đến\s+(\d{1,2}/\d{1,2}/\d{4})',
                                        next_str
                                    )
                                    if date_match:
                                        from_date = pd.to_datetime(date_match.group(1), dayfirst=True, errors='coerce')
                                        to_date = pd.to_datetime(date_match.group(2), dayfirst=True, errors='coerce')
                                    break
            
            if thang is None:
                continue
            
            # Tìm vị trí các cột quan trọng
            id_col = None
            ho_ten_col = None
            don_vi_col = None
            bo_mon_col = None
            doi_tuong_col = None
            hs1_col = None
            hs13_col = None
            header_end_row = None
            
            for idx in range(min(20, len(df))):
                row = df.iloc[idx]
                for col_idx, val in enumerate(row.values):
                    if pd.notna(val):
                        val_str = str(val).strip().lower()
                        if val_str == 'id':
                            id_col = col_idx
                            header_end_row = idx
                        elif 'họ tên' in val_str or 'ho ten' in val_str or val_str == 'hỌ tÊn':
                            ho_ten_col = col_idx
                        elif 'đơn vị' in val_str or 'don vi' in val_str or val_str == 'đơn vị':
                            don_vi_col = col_idx
                        elif 'bộ môn' in val_str or 'bo mon' in val_str:
                            bo_mon_col = col_idx
                        elif 'đối tượng' in val_str or 'doi tuong' in val_str:
                            doi_tuong_col = col_idx
                        elif 'hệ số 1.3' in val_str or 'he so 1.3' in val_str:
                            hs13_col = col_idx
                        elif ('hệ số 1' in val_str or 'he so 1' in val_str) and '1.3' not in val_str:
                            hs1_col = col_idx
            
            if id_col is None or hs1_col is None:
                continue
            
            # Tìm dòng bắt đầu dữ liệu (sau header, có ID là số)
            data_start = (header_end_row + 1) if header_end_row else 0
            for idx in range(data_start, min(data_start + 10, len(df))):
                val = df.iloc[idx, id_col]
                if pd.notna(val):
                    val_clean = re.sub(r'\.0$', '', str(val).strip())
                    if re.match(r'^\d+$', val_clean):
                        data_start = idx
                        break
            
            # Đọc từng dòng dữ liệu
            for idx in range(data_start, len(df)):
                row = df.iloc[idx]
                
                id_val = str(row.iloc[id_col]).strip() if pd.notna(row.iloc[id_col]) else ''
                # Loại bỏ .0 nếu pandas đọc số thành float
                id_val = re.sub(r'\.0$', '', id_val)
                
                # Bỏ qua dòng trống hoặc không phải ID số
                if not id_val or id_val == 'nan' or not re.match(r'^\d+$', id_val):
                    continue
                
                ho_ten = str(row.iloc[ho_ten_col]).strip() if ho_ten_col is not None and pd.notna(row.iloc[ho_ten_col]) else ''
                don_vi = str(row.iloc[don_vi_col]).strip() if don_vi_col is not None and pd.notna(row.iloc[don_vi_col]) else ''
                bo_mon = str(row.iloc[bo_mon_col]).strip() if bo_mon_col is not None and pd.notna(row.iloc[bo_mon_col]) else ''
                doi_tuong = str(row.iloc[doi_tuong_col]).strip() if doi_tuong_col is not None and pd.notna(row.iloc[doi_tuong_col]) else ''
                
                # Loại bỏ 'nan'
                if ho_ten.lower() == 'nan':
                    ho_ten = ''
                if don_vi.lower() == 'nan':
                    don_vi = ''
                if bo_mon.lower() == 'nan':
                    bo_mon = ''
                if doi_tuong.lower() == 'nan':
                    doi_tuong = ''
                
                # Giờ dạy
                hs1 = 0
                hs13 = 0
                try:
                    hs1 = float(row.iloc[hs1_col]) if pd.notna(row.iloc[hs1_col]) else 0
                except (ValueError, TypeError):
                    hs1 = 0
                try:
                    if hs13_col is not None:
                        hs13 = float(row.iloc[hs13_col]) if pd.notna(row.iloc[hs13_col]) else 0
                except (ValueError, TypeError):
                    hs13 = 0
                
                gio_day_dt = hs1 + hs13
                
                all_data.append({
                    'Thang': thang,
                    'FromDate': from_date,
                    'ToDate': to_date,
                    'ID': id_val,
                    'HoTen': ho_ten,
                    'DonVi': don_vi,
                    'BoMon': bo_mon,
                    'DoiTuong': doi_tuong,
                    'HeSo1': hs1,
                    'HeSo13': hs13,
                    'GioDayDT': gio_day_dt
                })
        
        except Exception as e:
            print(f"Lỗi đọc file chấm công: {e}")
            continue
    
    if not all_data:
        return pd.DataFrame()
    
    result = pd.DataFrame(all_data)
    return result


def read_danh_sach_gv(file):
    """
    Đọc file Danh sách GV (mapping).
    Trả về DataFrame: ID, TeacherFullname, AccountFE, Major, Note
    """
    df = pd.read_excel(file, dtype=str)
    df.columns = df.columns.str.strip()
    
    # Chuẩn hóa tên cột
    col_mapping = {}
    drop_cols = []
    for col in df.columns:
        col_lower = col.strip().lower()
        if col_lower in ['no.', 'no', 'stt']:
            drop_cols.append(col)
        elif col_lower == 'id':
            col_mapping[col] = 'ID'
        elif 'fullname' in col_lower or 'full name' in col_lower or "teacher" in col_lower:
            col_mapping[col] = 'TeacherFullname'
        elif 'accountfe' in col_lower or 'account' in col_lower:
            col_mapping[col] = 'AccountFE'
        elif 'major' in col_lower:
            col_mapping[col] = 'Major'
        elif 'note' in col_lower:
            col_mapping[col] = 'Note'
    
    # Xóa cột STT
    if drop_cols:
        df = df.drop(columns=drop_cols)
    
    df = df.rename(columns=col_mapping)
    
    # Chuẩn hóa
    if 'ID' in df.columns:
        df['ID'] = df['ID'].astype(str).str.strip()
        # Loại bỏ .0 nếu pandas đọc thành float
        df['ID'] = df['ID'].str.replace(r'\.0$', '', regex=True)
        # Loại bỏ dòng ID trống hoặc nan
        df = df[df['ID'].notna() & (df['ID'] != '') & (df['ID'] != 'nan')]
    
    if 'AccountFE' in df.columns:
        df['AccountFE'] = df['AccountFE'].astype(str).str.strip().str.lower()
        # Loại bỏ dòng AccountFE trống
        df = df[df['AccountFE'].notna() & (df['AccountFE'] != '') & (df['AccountFE'] != 'nan')]
    
    return df


# ============================================================
# 2. LOGIC TÍNH TOÁN
# ============================================================

def get_type_slot_mapping(df_lich_ky):
    """
    Tạo mapping SubjectCode → TypeSlot từ lịch kỳ.
    Mỗi SubjectCode chỉ có 1 TypeSlot duy nhất.
    Bỏ qua SlotTypeCode = 'G' khi tạo mapping.
    """
    df_filtered = df_lich_ky[df_lich_ky['SlotTypeCode'] != 'G'].copy()
    
    mapping = {}
    for _, row in df_filtered.drop_duplicates(subset=['SubjectCode']).iterrows():
        subject = str(row['SubjectCode']).strip()
        type_slot = str(row['TypeSlot']).strip().upper()
        mapping[subject] = type_slot
    
    return mapping


def get_hours_per_slot(type_slot):
    """
    Trả về số giờ cho mỗi buổi dựa vào TypeSlot.
    NEW SLOT = 2.25h, OLD SLOT = 1.5h
    """
    type_slot_upper = str(type_slot).upper()
    if 'NEW' in type_slot_upper:
        return 2.25
    elif 'OLD' in type_slot_upper:
        return 1.5
    else:
        return 2.25  # Default NEW SLOT


def calculate_gio_lich_ky(df_lich_ky, from_date, to_date):
    """
    Tính tổng giờ Lịch kỳ mỗi GV trong khoảng ngày.
    Lọc bỏ SlotTypeCode = 'G'.
    Chưa trừ WasNot Taken.
    """
    # Lọc theo khoảng ngày
    mask = (df_lich_ky['Date'] >= from_date) & (df_lich_ky['Date'] <= to_date)
    df_filtered = df_lich_ky[mask].copy()
    
    # Lọc bỏ SlotTypeCode = 'G'
    df_filtered = df_filtered[df_filtered['SlotTypeCode'] != 'G']
    
    if df_filtered.empty:
        return pd.DataFrame(columns=['AccountFE', 'GioLichKy'])
    
    # Tính giờ cho mỗi buổi
    df_filtered['Hours'] = df_filtered['TypeSlot'].apply(get_hours_per_slot)
    
    # Tổng giờ theo GV (Lecturer = AccountFE lowercase)
    result = df_filtered.groupby('Lecturer')['Hours'].sum().reset_index()
    result.columns = ['AccountFE', 'GioLichKy']
    
    return result


def calculate_gio_fap(df_teaching_summaries, df_lich_ky, from_date, to_date):
    """
    Tính tổng giờ FAP mỗi GV.
    Giờ FAP = Σ từng lớp: (AllPlan - WasNotTaken) × giờ/buổi (theo TypeSlot của SubjectCode)
    Match TypeSlot qua SubjectCode từ lịch kỳ.
    """
    if df_teaching_summaries.empty:
        return pd.DataFrame(columns=['AccountFE', 'GioFAP'])
    
    # Lọc Teaching Summaries theo khoảng ngày
    mask = (df_teaching_summaries['FromDate'] == from_date) & (df_teaching_summaries['ToDate'] == to_date)
    df_filtered = df_teaching_summaries[mask].copy()
    
    if df_filtered.empty:
        return pd.DataFrame(columns=['AccountFE', 'GioFAP'])
    
    # Lấy mapping SubjectCode → TypeSlot từ lịch kỳ (bỏ qua G)
    type_slot_mapping = get_type_slot_mapping(df_lich_ky)
    
    # Tính giờ từng dòng
    def calc_hours(row):
        actual_slots = row['AllPlan'] - row['WasNotTaken']
        if actual_slots < 0:
            actual_slots = 0
        subject = str(row['Subject']).strip()
        type_slot = type_slot_mapping.get(subject, 'NEW SLOT')
        hours = actual_slots * get_hours_per_slot(type_slot)
        return hours
    
    df_filtered = df_filtered.copy()
    df_filtered['Hours'] = df_filtered.apply(calc_hours, axis=1)
    
    # Tổng theo GV
    result = df_filtered.groupby('Teacher')['Hours'].sum().reset_index()
    result.columns = ['AccountFE', 'GioFAP']
    
    return result


def calculate_gio_dt(df_cham_cong, thang):
    """
    Lấy tổng giờ ĐT mỗi GV từ phiếu chấm công cho tháng cụ thể.
    Giờ ĐT = Hệ số 1 + Hệ số 1.3
    """
    df_filtered = df_cham_cong[df_cham_cong['Thang'] == thang].copy()
    
    if df_filtered.empty:
        return pd.DataFrame(columns=['ID', 'HoTen', 'DonVi', 'BoMon', 'DoiTuong', 'GioDayDT'])
    
    result = df_filtered[['ID', 'HoTen', 'DonVi', 'BoMon', 'DoiTuong', 'GioDayDT']].copy()
    return result


# ============================================================
# 3. ĐỐI SÁNH VÀ TẠO BÁO CÁO
# ============================================================

def doi_sanh_gio_day(df_lich_ky, df_teaching_summaries, df_cham_cong, df_gv_mapping):
    """
    Đối sánh giờ dạy: Lịch kỳ vs FAP vs ĐT.
    Trả về DataFrame kết quả gộp nhiều tháng.
    """
    results = []
    
    # Chuẩn hóa ID (loại bỏ .0, strip)
    df_gv_mapping = df_gv_mapping.copy()
    if 'ID' in df_gv_mapping.columns:
        df_gv_mapping['ID'] = df_gv_mapping['ID'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
    
    df_cham_cong = df_cham_cong.copy()
    df_cham_cong['ID'] = df_cham_cong['ID'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
    
    # Lấy danh sách tháng từ chấm công
    months = df_cham_cong[['Thang', 'FromDate', 'ToDate']].drop_duplicates()
    
    for _, month_row in months.iterrows():
        thang = month_row['Thang']
        from_date = month_row['FromDate']
        to_date = month_row['ToDate']
        
        if pd.isna(from_date) or pd.isna(to_date):
            continue
        
        # Tính giờ Lịch kỳ
        gio_lich_ky = calculate_gio_lich_ky(df_lich_ky, from_date, to_date)
        
        # Tính giờ FAP
        gio_fap = calculate_gio_fap(df_teaching_summaries, df_lich_ky, from_date, to_date)
        
        # Lấy giờ ĐT
        gio_dt = calculate_gio_dt(df_cham_cong, thang)
        
        # === Tạo bảng master từ Danh sách GV ===
        if 'ID' in df_gv_mapping.columns and 'AccountFE' in df_gv_mapping.columns:
            master = df_gv_mapping[['ID', 'AccountFE']].copy()
            master = master.dropna(subset=['AccountFE'])
            master['AccountFE'] = master['AccountFE'].astype(str).str.strip().str.lower()
            # Loại bỏ AccountFE = 'nan'
            master = master[master['AccountFE'] != 'nan']
        else:
            continue
        
        # Merge giờ ĐT vào master qua ID (chỉ lấy GV có trong chấm công)
        master = master.merge(
            gio_dt[['ID', 'HoTen', 'DonVi', 'BoMon', 'DoiTuong', 'GioDayDT']],
            on='ID',
            how='inner'
        )
        
        # Merge giờ Lịch kỳ vào master qua AccountFE
        master = master.merge(gio_lich_ky, on='AccountFE', how='left')
        
        # Merge giờ FAP vào master qua AccountFE
        master = master.merge(gio_fap, on='AccountFE', how='left')
        
        # Fill NaN = 0 cho cột giờ
        master['GioLichKy'] = master['GioLichKy'].fillna(0)
        master['GioFAP'] = master['GioFAP'].fillna(0)
        master['GioDayDT'] = master['GioDayDT'].fillna(0)
        
        # Tính chênh lệch
        master['ChenhLech_LichKy_DT'] = master['GioLichKy'] - master['GioDayDT']
        
        # Kết quả TRUE/FALSE
        master['KetQua'] = (
            (master['GioLichKy'] == master['GioFAP']) &
            (master['GioFAP'] == master['GioDayDT'])
        )
        
        master['Thang'] = thang
        results.append(master)
    
    if not results:
        return pd.DataFrame()
    
    final = pd.concat(results, ignore_index=True)
    
    # Sắp xếp cột
    cols_order = ['Thang', 'ID', 'HoTen', 'AccountFE', 'DonVi', 'BoMon', 'DoiTuong',
                  'GioLichKy', 'GioFAP', 'GioDayDT', 'ChenhLech_LichKy_DT', 'KetQua']
    existing_cols = [c for c in cols_order if c in final.columns]
    final = final[existing_cols]
    
    # Sắp xếp theo Tháng, HoTen
    final = final.sort_values(['Thang', 'HoTen']).reset_index(drop=True)
    
    return final


def get_wasnot_taken_detail(df_teaching_summaries):
    """
    Trả về chi tiết các buổi WasNot Taken.
    """
    if df_teaching_summaries.empty:
        return pd.DataFrame()
    
    df_filtered = df_teaching_summaries[df_teaching_summaries['WasNotTaken'] > 0].copy()
    
    if df_filtered.empty:
        return pd.DataFrame()
    
    result = df_filtered[['Teacher', 'Group', 'Subject', 'WasNotTaken', 'WasNotTakenRaw', 'FromDate', 'ToDate']].copy()
    result.columns = ['AccountFE', 'Group', 'Subject', 'SoBuoiNghi', 'ChiTiet', 'FromDate', 'ToDate']
    
    return result


# ============================================================
# 4. TÍNH GIỜ DẠY CƠ HỮU
# ============================================================

def is_co_huu(doi_tuong):
    """
    Kiểm tra đối tượng có phải cơ hữu không.
    Cơ hữu: CBNV, CBQL, CH, CHdn, CHNN1, GVNCV, GVQL hoặc bắt đầu bằng 'CH'
    """
    if not doi_tuong or str(doi_tuong).strip() == '' or str(doi_tuong).strip().lower() == 'nan':
        return False
    
    doi_tuong = str(doi_tuong).strip().upper()
    co_huu_list = ['CBNV', 'CBQL', 'CH', 'CHDN', 'CHNN1', 'GVNCV', 'GVQL']
    
    if doi_tuong in co_huu_list:
        return True
    if doi_tuong.startswith('CH'):
        return True
    
    return False


def calculate_gio_co_huu(df_lich_ky_full, df_cham_cong, df_gv_mapping):
    """
    Tính giờ dạy cơ hữu HK.
    Nguồn giờ: Lịch kỳ FAP toàn kỳ (KHÔNG bỏ SlotTypeCode = 'G')
    Đối tượng: Từ chấm công ĐT
    """
    # Tính giờ mỗi GV từ lịch kỳ (KHÔNG lọc SlotTypeCode G)
    df_calc = df_lich_ky_full.copy()
    df_calc['Hours'] = df_calc['TypeSlot'].apply(get_hours_per_slot)
    
    gio_per_gv = df_calc.groupby('Lecturer')['Hours'].sum().reset_index()
    gio_per_gv.columns = ['AccountFE', 'TongGio']
    
    # Chuẩn hóa ID
    df_gv_mapping = df_gv_mapping.copy()
    if 'ID' in df_gv_mapping.columns:
        df_gv_mapping['ID'] = df_gv_mapping['ID'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
    
    df_cham_cong = df_cham_cong.copy()
    df_cham_cong['ID'] = df_cham_cong['ID'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
    
    # Lấy đối tượng từ chấm công (lấy unique theo ID)
    doi_tuong_mapping = df_cham_cong[['ID', 'DoiTuong', 'DonVi', 'BoMon']].drop_duplicates(subset=['ID'])
    
    # Merge với danh sách GV để có AccountFE
    if 'ID' in df_gv_mapping.columns and 'AccountFE' in df_gv_mapping.columns:
        doi_tuong_mapping = doi_tuong_mapping.merge(
            df_gv_mapping[['ID', 'AccountFE']],
            on='ID',
            how='left'
        )
    
    if 'AccountFE' not in doi_tuong_mapping.columns:
        return pd.DataFrame(), 0, 0
    
    # Chuẩn hóa AccountFE
    doi_tuong_mapping['AccountFE'] = doi_tuong_mapping['AccountFE'].astype(str).str.strip().str.lower()
    doi_tuong_mapping = doi_tuong_mapping[doi_tuong_mapping['AccountFE'] != 'nan']
    
    # Merge giờ với đối tượng
    result = gio_per_gv.merge(
        doi_tuong_mapping[['AccountFE', 'DoiTuong', 'DonVi', 'BoMon']],
        on='AccountFE',
        how='left'
    )
    
    # Xác định cơ hữu
    result['LaCoHuu'] = result['DoiTuong'].apply(is_co_huu)
    
    # Tính tổng
    tong_gio_all = result['TongGio'].sum()
    tong_gio_co_huu = result[result['LaCoHuu'] == True]['TongGio'].sum()
    
    return result, tong_gio_co_huu, tong_gio_all


# ============================================================
# 5. XUẤT FILE EXCEL
# ============================================================

def export_to_excel(df_doi_sanh, df_wasnot_taken, df_co_huu=None):
    """
    Xuất kết quả ra file Excel với nhiều sheet.
    """
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Sheet 1: Đối sánh chi tiết
        if df_doi_sanh is not None and not df_doi_sanh.empty:
            df_export = df_doi_sanh.copy()
            df_export.to_excel(writer, sheet_name='Đối sánh giờ dạy', index=False)
        
        # Sheet 2: WasNot Taken
        if df_wasnot_taken is not None and not df_wasnot_taken.empty:
            df_wasnot_taken.to_excel(writer, sheet_name='WasNot Taken', index=False)
        
        # Sheet 3: Giờ cơ hữu (nếu có)
        if df_co_huu is not None and not df_co_huu.empty:
            df_co_huu.to_excel(writer, sheet_name='Giờ dạy cơ hữu', index=False)
    
    output.seek(0)
    return output
