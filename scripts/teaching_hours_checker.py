import pandas as pd
import re
import io
from datetime import datetime
import unicodedata

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def normalize_str(s):
    """Chuẩn hóa chuỗi: trim, collapse whitespace, NFC unicode"""
    if pd.isna(s):
        return ''
    s = str(s).strip()
    s = unicodedata.normalize('NFC', s)
    s = re.sub(r'\s+', ' ', s)
    return s


def normalize_account(s):
    """Chuẩn hóa AccountFE: lowercase, strip all whitespace"""
    if pd.isna(s):
        return ''
    s = str(s).strip().lower()
    s = re.sub(r'\s+', '', s)
    if s == 'nan':
        return ''
    return s


def normalize_id(s):
    """Chuẩn hóa ID: bỏ .0, strip, giữ nguyên leading zeros"""
    if pd.isna(s):
        return ''
    s = str(s).strip()
    s = re.sub(r'\.0$', '', s)
    if s.lower() == 'nan':
        return ''
    return s


def parse_date_flexible(date_val):
    """
    Parse ngày linh hoạt: hỗ trợ nhiều format khác nhau.
    Trả về pd.Timestamp hoặc pd.NaT
    """
    if pd.isna(date_val):
        return pd.NaT
    
    # Nếu đã là datetime
    if isinstance(date_val, (datetime, pd.Timestamp)):
        return pd.Timestamp(date_val)
    
    date_str = str(date_val).strip()
    
    # Loại bỏ phần giờ nếu có
    date_str = re.sub(r'\s+\d{1,2}:\d{2}(:\d{2})?.*$', '', date_str)
    
    # Thử các format phổ biến
    formats = [
        '%d/%m/%Y',      # 16/03/2026
        '%d-%m-%Y',      # 16-03-2026
        '%d.%m.%Y',      # 16.03.2026
        '%Y-%m-%d',      # 2026-03-16
        '%Y/%m/%d',      # 2026/03/16
        '%m/%d/%Y',      # 03/16/2026
        '%d/%m/%y',      # 16/03/26
        '%d-%m-%y',      # 16-03-26
    ]
    
    for fmt in formats:
        try:
            return pd.Timestamp(datetime.strptime(date_str, fmt))
        except ValueError:
            continue
    
    # Fallback: pandas parser
    try:
        return pd.to_datetime(date_str, dayfirst=True)
    except:
        pass
    
    try:
        return pd.to_datetime(date_str)
    except:
        return pd.NaT


# ============================================================
# READ LỊCH KỲ FAP
# ============================================================

def read_lich_ky(files):
    """
    Đọc nhiều file Lịch kỳ FAP.
    Chuẩn hóa Date, Lecturer, TypeSlot, SlotTypeCode.
    """
    all_dfs = []
    
    for file in files:
        try:
            # Đọc tất cả sheet
            xl = pd.ExcelFile(file)
            for sheet_name in xl.sheet_names:
                df = pd.read_excel(file, sheet_name=sheet_name, dtype=str)
                if df.empty:
                    continue
                
                # Chuẩn hóa tên cột
                df.columns = df.columns.str.strip()
                
                # Kiểm tra các cột cần thiết
                required_cols = ['Date', 'Lecturer', 'TypeSlot']
                col_map = {}
                for col in df.columns:
                    col_lower = col.lower().strip()
                    if 'date' in col_lower and 'date' not in col_map:
                        col_map['Date'] = col
                    elif 'lecturer' in col_lower:
                        col_map['Lecturer'] = col
                    elif 'typeslot' in col_lower or 'type slot' in col_lower:
                        col_map['TypeSlot'] = col
                    elif 'slottypecode' in col_lower or 'slot type code' in col_lower:
                        col_map['SlotTypeCode'] = col
                    elif 'groupname' in col_lower or 'group name' in col_lower:
                        col_map['GroupName'] = col
                    elif 'subjectcode' in col_lower or 'subject code' in col_lower:
                        col_map['SubjectCode'] = col
                    elif col_lower == 'slot':
                        col_map['Slot'] = col
                
                # Đổi tên cột
                df = df.rename(columns={v: k for k, v in col_map.items()})
                
                if 'Date' not in df.columns or 'Lecturer' not in df.columns:
                    continue
                
                # Parse Date linh hoạt
                df['Date'] = df['Date'].apply(parse_date_flexible)
                
                # Bỏ dòng không parse được ngày
                before_count = len(df)
                df = df.dropna(subset=['Date'])
                
                # Chuẩn hóa các cột khác
                df['Lecturer'] = df['Lecturer'].apply(normalize_account)
                
                if 'SubjectCode' in df.columns:
                    df['SubjectCode'] = df['SubjectCode'].apply(lambda x: normalize_str(x).upper() if pd.notna(x) else '')
                
                if 'GroupName' in df.columns:
                    df['GroupName'] = df['GroupName'].apply(normalize_str)
                
                if 'TypeSlot' in df.columns:
                    df['TypeSlot'] = df['TypeSlot'].apply(lambda x: str(x).strip().upper() if pd.notna(x) else 'NEW SLOT')
                
                if 'SlotTypeCode' in df.columns:
                    df['SlotTypeCode'] = df['SlotTypeCode'].apply(lambda x: str(x).strip().upper() if pd.notna(x) else '')
                
                # Bỏ dòng không có Lecturer
                df = df[df['Lecturer'] != '']
                
                all_dfs.append(df)
        except Exception as e:
            print(f"Lỗi đọc file lịch kỳ: {e}")
            continue
    
    if not all_dfs:
        return pd.DataFrame()
    
    result = pd.concat(all_dfs, ignore_index=True)
    return result


# ============================================================
# READ TEACHING SUMMARIES
# ============================================================

def read_teaching_summaries(files):
    """
    Đọc file Teaching Summaries (1 file có thể nhiều sheets).
    Parse cấu trúc grouped: Teacher → các dòng Group/Subject.
    """
    all_data = []
    
    for file in files:
        try:
            xl = pd.ExcelFile(file)
            for sheet_name in xl.sheet_names:
                df = pd.read_excel(file, sheet_name=sheet_name, header=None)
                if df.empty:
                    continue
                
                # Tìm FromDate / ToDate
                from_date = None
                to_date = None
                for idx in range(min(20, len(df))):
                    row_vals = [str(v).strip().lower() for v in df.iloc[idx].values if pd.notna(v)]
                    row_text = ' '.join(row_vals)
                    
                    if 'from date' in row_text or 'from' in row_text:
                        # Tìm ngày trong dòng hiện tại và dòng tiếp theo
                        for search_idx in range(idx, min(idx + 3, len(df))):
                            search_row = df.iloc[search_idx]
                            for val in search_row.values:
                                if pd.notna(val):
                                    parsed = parse_date_flexible(val)
                                    if pd.notna(parsed):
                                        if from_date is None:
                                            from_date = parsed
                                        elif to_date is None and parsed > from_date:
                                            to_date = parsed
                                            break
                            if to_date:
                                break
                        if from_date:
                            break
                
                # Tìm header row - quét rộng hơn
                header_row_idx = None
                for idx in range(min(30, len(df))):
                    row_vals = [str(v).strip().lower() for v in df.iloc[idx].values if pd.notna(v)]
                    has_teacher = any('teacher' in v for v in row_vals)
                    has_group = any('group' in v for v in row_vals)
                    if has_teacher and has_group:
                        header_row_idx = idx
                        break
                
                if header_row_idx is None:
                    continue
                
                # Xử lý duplicate headers
                raw_headers = df.iloc[header_row_idx].values
                seen = {}
                clean_headers = []
                for h in raw_headers:
                    h_str = str(h).strip() if pd.notna(h) else 'unnamed'
                    if h_str in seen:
                        seen[h_str] += 1
                        clean_headers.append(f"{h_str}_{seen[h_str]}")
                    else:
                        seen[h_str] = 0
                        clean_headers.append(h_str)
                
                df_data = df.iloc[header_row_idx + 1:].copy()
                df_data.columns = clean_headers
                
                # Map columns
                teacher_col = group_col = subject_col = allplan_col = wasnot_col = None
                for col in df_data.columns:
                    lc = str(col).strip().lower()
                    if 'teacher' in lc and teacher_col is None:
                        teacher_col = col
                    elif 'group' in lc and group_col is None:
                        group_col = col
                    elif 'subject' in lc and subject_col is None:
                        subject_col = col
                    elif 'all plan' in lc or 'allplan' in lc:
                        if allplan_col is None:
                            allplan_col = col
                    elif ('wasnot' in lc or 'was not' in lc) and wasnot_col is None:
                        wasnot_col = col
                
                if not teacher_col or not group_col:
                    continue
                
                # Parse data
                current_teacher = None
                for _, row in df_data.iterrows():
                    teacher_val = normalize_str(row[teacher_col]) if teacher_col and pd.notna(row[teacher_col]) else ''
                    group_val = normalize_str(row[group_col]) if group_col and pd.notna(row[group_col]) else ''
                    subject_val = normalize_str(row[subject_col]) if subject_col and pd.notna(row[subject_col]) else ''
                    
                    if teacher_val.lower() == 'nan':
                        teacher_val = ''
                    if group_val.lower() == 'nan':
                        group_val = ''
                    if subject_val.lower() == 'nan':
                        subject_val = ''
                    
                    # Dòng chỉ có Teacher → tên GV mới
                    if teacher_val and not group_val and not subject_val:
                        current_teacher = normalize_account(teacher_val)
                    elif group_val or subject_val:
                        # Nếu dòng có cả teacher VÀ group → teacher mới + record
                        if teacher_val and group_val:
                            current_teacher = normalize_account(teacher_val)
                        
                        # Parse WasNotTaken
                        wasnot_count = 0
                        wasnot_raw = ''
                        if wasnot_col and pd.notna(row[wasnot_col]):
                            wasnot_raw = str(row[wasnot_col]).strip()
                            if wasnot_raw.lower() != 'nan':
                                m = re.search(r'(\d+)\s*slot', wasnot_raw, re.IGNORECASE)
                                if m:
                                    wasnot_count = int(m.group(1))
                        
                        # Parse AllPlan
                        allplan_count = 0
                        if allplan_col and pd.notna(row[allplan_col]):
                            try:
                                allplan_count = int(float(row[allplan_col]))
                            except (ValueError, TypeError):
                                allplan_count = 0
                        
                        if current_teacher:
                            all_data.append({
                                'Teacher': current_teacher,
                                'Group': group_val,
                                'Subject': subject_val.upper() if subject_val else '',
                                'AllPlan': allplan_count,
                                'WasNotTaken': wasnot_count,
                                'WasNotTakenRaw': wasnot_raw,
                                'FromDate': from_date,
                                'ToDate': to_date
                            })
        except Exception as e:
            print(f"Lỗi đọc Teaching Summaries: {e}")
            continue
    
    return pd.DataFrame(all_data) if all_data else pd.DataFrame()


# ============================================================
# READ CHẤM CÔNG ĐT
# ============================================================

def read_cham_cong(files):
    """
    Đọc nhiều file Phiếu chấm công ĐT.
    Parse tháng, khoảng ngày, giờ dạy (Hệ số 1 + Hệ số 1.3).
    """
    all_data = []
    
    for file in files:
        try:
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
            
            for idx in range(min(20, len(df))):
                row = df.iloc[idx]
                row_text = ' '.join([str(v).strip() for v in row.values if pd.notna(v)])
                
                # Tìm ô chứa "NĂM" hoặc "NAM"
                if 'NĂM' in row_text.upper() or 'NAM' in row_text.upper():
                    # Gộp toàn bộ text của dòng
                    all_text = row_text
                    
                    # Parse tháng (1-2 chữ số)
                    thang_match = re.search(r'(\d{1,2}/\d{4})', all_text)
                    if thang_match:
                        raw_thang = thang_match.group(1)
                        parts = raw_thang.split('/')
                        thang = f"{int(parts[0]):02d}/{parts[1]}"
                    
                    # Parse khoảng ngày (cho phép không có space)
                    date_match = re.search(
                        r'[Tt]ừ\s*(\d{1,2}/\d{1,2}/\d{4})\s*đến\s*(\d{1,2}/\d{1,2}/\d{4})',
                        all_text
                    )
                    if date_match:
                        from_date = pd.to_datetime(date_match.group(1), dayfirst=True, errors='coerce')
                        to_date = pd.to_datetime(date_match.group(2), dayfirst=True, errors='coerce')
                    
                    if thang:
                        break
            
            if thang is None:
                continue
            
            # Tìm dòng header chứa thông tin cột
            header_row_idx = None
            id_col = None
            name_col = None
            donvi_col = None
            bomon_col = None
            doituong_col = None
            hs1_col = None
            hs13_col = None
            
            for idx in range(min(30, len(df))):
                row = df.iloc[idx]
                row_vals = [str(v).strip().lower() for v in row.values if pd.notna(v)]
                row_text = ' '.join(row_vals)
                
                # Tìm dòng có "stt" hoặc "id" kết hợp với "họ tên" hoặc "ho ten"
                has_id = any(v in ['stt', 'id', 'mã', 'ma'] for v in row_vals)
                has_name = any('tên' in v or 'ten' in v or 'name' in v for v in row_vals)
                
                if has_id and has_name:
                    header_row_idx = idx
                    # Map vị trí cột
                    for col_idx, val in enumerate(row.values):
                        if pd.isna(val):
                            continue
                        val_lower = str(val).strip().lower()
                        
                        if val_lower in ['id', 'mã', 'ma', 'mã nv', 'ma nv']:
                            id_col = col_idx
                        elif 'stt' in val_lower and id_col is None:
                            # Skip STT, tìm ID ở cột tiếp theo
                            pass
                        elif ('họ' in val_lower and 'tên' in val_lower) or ('ho' in val_lower and 'ten' in val_lower) or val_lower == 'name':
                            name_col = col_idx
                        elif 'đơn vị' in val_lower or 'don vi' in val_lower or val_lower == 'campus':
                            donvi_col = col_idx
                        elif 'bộ môn' in val_lower or 'bo mon' in val_lower or 'khoa' in val_lower:
                            bomon_col = col_idx
                        elif 'đối tượng' in val_lower or 'doi tuong' in val_lower or 'object' in val_lower:
                            doituong_col = col_idx
                    break
            
            if header_row_idx is None:
                continue
            
            # Tìm cột Hệ số 1 và Hệ số 1.3
            # Quét thêm dòng header phụ (merged cells thường có header 2 dòng)
            for scan_idx in range(max(0, header_row_idx - 2), min(header_row_idx + 3, len(df))):
                row = df.iloc[scan_idx]
                for col_idx, val in enumerate(row.values):
                    if pd.isna(val):
                        continue
                    val_str = str(val).strip().lower()
                    
                    if ('hệ số 1.3' in val_str or 'he so 1.3' in val_str or 
                        'hs 1.3' in val_str or val_str == '1.3'):
                        hs13_col = col_idx
                    elif ('hệ số 1' in val_str or 'he so 1' in val_str or 
                          'hs 1' in val_str or val_str == '1') and 'hệ số 1.3' not in val_str:
                        if hs1_col is None:
                            hs1_col = col_idx
            
            # Nếu không tìm được cột ID riêng, thử dùng cột thứ 2 (sau STT)
            if id_col is None:
                # Giả sử cột 0 = STT, cột 1 = ID
                for col_idx, val in enumerate(df.iloc[header_row_idx].values):
                    if pd.isna(val):
                        continue
                    val_lower = str(val).strip().lower()
                    if 'stt' in val_lower:
                        id_col = col_idx + 1
                        break
            
            if id_col is None or hs1_col is None:
                continue
            
            # Đọc data từ dòng sau header
            for idx in range(header_row_idx + 1, len(df)):
                row = df.iloc[idx]
                
                # Lấy ID
                id_val = normalize_id(row.iloc[id_col]) if id_col < len(row) else ''
                if not id_val or not re.match(r'^\d+$', id_val):
                    continue
                
                # Lấy các thông tin khác
                ho_ten = normalize_str(row.iloc[name_col]) if name_col and name_col < len(row) else ''
                don_vi = normalize_str(row.iloc[donvi_col]) if donvi_col and donvi_col < len(row) else ''
                bo_mon = normalize_str(row.iloc[bomon_col]) if bomon_col and bomon_col < len(row) else ''
                doi_tuong = normalize_str(row.iloc[doituong_col]) if doituong_col and doituong_col < len(row) else ''
                
                # Lấy giờ dạy
                hs1 = 0
                hs13 = 0
                
                if hs1_col and hs1_col < len(row):
                    try:
                        val = row.iloc[hs1_col]
                        if pd.notna(val):
                            hs1 = float(val)
                    except (ValueError, TypeError):
                        hs1 = 0
                
                if hs13_col and hs13_col < len(row):
                    try:
                        val = row.iloc[hs13_col]
                        if pd.notna(val):
                            hs13 = float(val)
                    except (ValueError, TypeError):
                        hs13 = 0
                
                all_data.append({
                    'ID': id_val,
                    'HoTen': ho_ten,
                    'DonVi': don_vi,
                    'BoMon': bo_mon,
                    'DoiTuong': doi_tuong,
                    'HeSo1': hs1,
                    'HeSo13': hs13,
                    'GioDayDT': hs1 + hs13,
                    'Thang': thang,
                    'FromDate': from_date,
                    'ToDate': to_date
                })
        except Exception as e:
            print(f"Lỗi đọc chấm công: {e}")
            continue
    
    return pd.DataFrame(all_data) if all_data else pd.DataFrame()


# ============================================================
# READ DANH SÁCH GV
# ============================================================

def read_danh_sach_gv(file):
    """
    Đọc file danh sách GV mapping.
    Chuẩn hóa ID, AccountFE.
    """
    df = pd.read_excel(file)
    df.columns = df.columns.str.strip()
    
    # Tìm và map cột
    col_map = {}
    for col in df.columns:
        col_lower = col.lower().strip()
        if col_lower in ['no', 'no.', 'stt', 'số tt', 'so tt']:
            continue  # Bỏ qua cột STT
        elif 'id' in col_lower or 'mã' in col_lower or 'ma' in col_lower:
            if 'ID' not in col_map:
                col_map['ID'] = col
        elif 'account' in col_lower or 'accountfe' in col_lower:
            col_map['AccountFE'] = col
        elif 'fullname' in col_lower or 'full name' in col_lower or 'teacher' in col_lower or 'họ tên' in col_lower:
            col_map['TeacherFullname'] = col
        elif 'major' in col_lower or 'chuyên ngành' in col_lower:
            col_map['Major'] = col
        elif 'note' in col_lower or 'ghi chú' in col_lower:
            col_map['Note'] = col
    
    if 'ID' not in col_map or 'AccountFE' not in col_map:
        # Fallback: giả sử cột 1 = ID, cột 3 = AccountFE (dựa theo thứ tự No, ID, Name, Account)
        cols = df.columns.tolist()
        if len(cols) >= 4:
            col_map['ID'] = cols[1]
            col_map['TeacherFullname'] = cols[2]
            col_map['AccountFE'] = cols[3]
    
    # Rename
    df = df.rename(columns={v: k for k, v in col_map.items()})
    
    # Chuẩn hóa
    if 'ID' in df.columns:
        df['ID'] = df['ID'].apply(normalize_id)
    if 'AccountFE' in df.columns:
        df['AccountFE'] = df['AccountFE'].apply(normalize_account)
    
    # Loại bỏ dòng trống
    df = df[(df['ID'] != '') & (df['AccountFE'] != '')]
    
    return df


# ============================================================
# CALCULATION FUNCTIONS
# ============================================================

def get_type_slot_mapping(df_lich_ky):
    """
    Tạo mapping SubjectCode → TypeSlot từ lịch kỳ.
    Bỏ qua SlotTypeCode = 'G'.
    """
    if df_lich_ky.empty or 'SubjectCode' not in df_lich_ky.columns:
        return {}
    
    df_filtered = df_lich_ky.copy()
    if 'SlotTypeCode' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['SlotTypeCode'] != 'G']
    
    mapping = {}
    for _, row in df_filtered.iterrows():
        subject = row.get('SubjectCode', '')
        type_slot = row.get('TypeSlot', 'NEW SLOT')
        if subject and subject not in mapping:
            mapping[subject] = type_slot
    
    return mapping


def get_hours_per_slot(type_slot):
    """NEW SLOT = 2.25h, OLD SLOT = 1.5h"""
    if pd.isna(type_slot):
        return 2.25
    type_slot = str(type_slot).strip().upper()
    if 'OLD' in type_slot:
        return 1.5
    return 2.25


def calculate_gio_lich_ky(df_lich_ky, from_date, to_date):
    """
    Tính tổng giờ theo Lịch kỳ cho từng GV trong khoảng ngày.
    Bỏ qua SlotTypeCode = 'G'.
    """
    if df_lich_ky.empty:
        return pd.DataFrame(columns=['AccountFE', 'GioLichKy'])
    
    df = df_lich_ky.copy()
    
    # Lọc theo ngày
    mask = (df['Date'] >= pd.Timestamp(from_date)) & (df['Date'] <= pd.Timestamp(to_date))
    df = df[mask]
    
    # Bỏ SlotTypeCode = 'G'
    if 'SlotTypeCode' in df.columns:
        df = df[df['SlotTypeCode'] != 'G']
    
    if df.empty:
        return pd.DataFrame(columns=['AccountFE', 'GioLichKy'])
    
    # Tính giờ cho từng buổi
    df['Hours'] = df['TypeSlot'].apply(get_hours_per_slot)
    
    # Group by Lecturer (= AccountFE)
    result = df.groupby('Lecturer')['Hours'].sum().reset_index()
    result.columns = ['AccountFE', 'GioLichKy']
    
    return result


def calculate_gio_fap(df_teaching_summaries, df_lich_ky, from_date, to_date):
    """
    Tính tổng giờ FAP = (AllPlan - WasNotTaken) × giờ/slot.
    Match TypeSlot theo SubjectCode từ lịch kỳ.
    """
    if df_teaching_summaries.empty:
        return pd.DataFrame(columns=['AccountFE', 'GioFAP'])
    
    # Lọc Teaching Summaries theo khoảng ngày
    df = df_teaching_summaries.copy()
    
    if 'FromDate' in df.columns and 'ToDate' in df.columns:
        mask = pd.notna(df['FromDate']) & pd.notna(df['ToDate'])
        if mask.any():
            df_dated = df[mask]
            # Lọc records trùng khoảng ngày
            date_mask = (
                (df_dated['FromDate'] >= pd.Timestamp(from_date) - pd.Timedelta(days=5)) & 
                (df_dated['ToDate'] <= pd.Timestamp(to_date) + pd.Timedelta(days=5))
            )
            if date_mask.any():
                df = df_dated[date_mask]
    
    # Lấy mapping SubjectCode → TypeSlot
    type_slot_mapping = get_type_slot_mapping(df_lich_ky)
    
    # Tính giờ cho từng record
    records = []
    for _, row in df.iterrows():
        teacher = row.get('Teacher', '')
        subject = str(row.get('Subject', '')).strip().upper()
        all_plan = row.get('AllPlan', 0)
        was_not_taken = row.get('WasNotTaken', 0)
        
        actual_slots = max(0, all_plan - was_not_taken)
        
        # Lấy TypeSlot từ mapping
        type_slot = type_slot_mapping.get(subject, 'NEW SLOT')
        hours = actual_slots * get_hours_per_slot(type_slot)
        
        records.append({
            'AccountFE': teacher,
            'GioFAP': hours
        })
    
    if not records:
        return pd.DataFrame(columns=['AccountFE', 'GioFAP'])
    
    df_result = pd.DataFrame(records)
    result = df_result.groupby('AccountFE')['GioFAP'].sum().reset_index()
    
    return result


def calculate_gio_dt(df_cham_cong, thang):
    """
    Lấy giờ dạy ĐT cho 1 tháng cụ thể.
    """
    if df_cham_cong.empty:
        return pd.DataFrame(columns=['ID', 'HoTen', 'DonVi', 'BoMon', 'DoiTuong', 'GioDayDT'])
    
    df = df_cham_cong[df_cham_cong['Thang'] == thang].copy()
    
    if df.empty:
        return pd.DataFrame(columns=['ID', 'HoTen', 'DonVi', 'BoMon', 'DoiTuong', 'GioDayDT'])
    
    # Group by ID (phòng trường hợp trùng)
    result = df.groupby('ID').agg({
        'HoTen': 'first',
        'DonVi': 'first',
        'BoMon': 'first',
        'DoiTuong': 'first',
        'GioDayDT': 'sum'
    }).reset_index()
    
    return result


# ============================================================
# ĐỐI SÁNH GIỜ DẠY
# ============================================================

def doi_sanh_gio_day(df_lich_ky, df_teaching_summaries, df_cham_cong, df_gv_mapping):
    """
    Đối sánh giờ dạy: Lịch kỳ vs FAP vs Chấm công ĐT.
    Trả về DataFrame kết quả gộp nhiều tháng.
    """
    results = []
    
    if df_cham_cong.empty or df_gv_mapping.empty:
        return pd.DataFrame()
    
    # Lấy danh sách tháng unique
    months = df_cham_cong[['Thang', 'FromDate', 'ToDate']].drop_duplicates()
    
    for _, month_row in months.iterrows():
        thang = month_row['Thang']
        from_date = month_row['FromDate']
        to_date = month_row['ToDate']
        
        if pd.isna(from_date) or pd.isna(to_date):
            continue
        
        # Tính giờ từ 3 nguồn
        gio_lich_ky = calculate_gio_lich_ky(df_lich_ky, from_date, to_date)
        gio_fap = calculate_gio_fap(df_teaching_summaries, df_lich_ky, from_date, to_date)
        gio_dt = calculate_gio_dt(df_cham_cong, thang)
        
        # Master: lấy từ danh sách GV
        master = df_gv_mapping[['ID', 'AccountFE']].copy()
        master = master[(master['ID'] != '') & (master['AccountFE'] != '')]
        
        # Merge với chấm công (inner join - chỉ GV có trong chấm công)
        master = master.merge(
            gio_dt[['ID', 'HoTen', 'DonVi', 'BoMon', 'DoiTuong', 'GioDayDT']], 
            on='ID', 
            how='inner'
        )
        
        # Merge giờ lịch kỳ
        if not gio_lich_ky.empty:
            master = master.merge(gio_lich_ky, on='AccountFE', how='left')
        else:
            master['GioLichKy'] = 0
        
        # Merge giờ FAP
        if not gio_fap.empty:
            master = master.merge(gio_fap, on='AccountFE', how='left')
        else:
            master['GioFAP'] = 0
        
        # Fill NaN
        master['GioLichKy'] = master['GioLichKy'].fillna(0)
        master['GioFAP'] = master['GioFAP'].fillna(0)
        master['GioDayDT'] = master['GioDayDT'].fillna(0)
        
        # Tính chênh lệch và kết quả
        master['ChenhLech_LichKy_DT'] = master['GioLichKy'] - master['GioDayDT']
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
    cols_order = ['Thang', 'ID', 'HoTen', 'AccountFE', 'DonVi', 'BoMon', 
                  'DoiTuong', 'GioLichKy', 'GioFAP', 'GioDayDT', 
                  'ChenhLech_LichKy_DT', 'KetQua']
    final = final[[c for c in cols_order if c in final.columns]]
    final = final.sort_values(['Thang', 'HoTen']).reset_index(drop=True)
    
    return final


# ============================================================
# WASNOT TAKEN DETAIL
# ============================================================

def get_wasnot_taken_detail(df_teaching_summaries):
    """
    Chi tiết các buổi WasNot Taken.
    """
    if df_teaching_summaries.empty:
        return pd.DataFrame()
    
    df = df_teaching_summaries[df_teaching_summaries['WasNotTaken'] > 0].copy()
    
    if df.empty:
        return pd.DataFrame()
    
    result = df[['Teacher', 'Group', 'Subject', 'WasNotTaken', 'WasNotTakenRaw', 'FromDate', 'ToDate']].copy()
    result.columns = ['AccountFE', 'Group', 'Subject', 'SoBuoiNghi', 'ChiTiet', 'FromDate', 'ToDate']
    
    return result.reset_index(drop=True)


# ============================================================
# GIỜ DẠY CƠ HỮU
# ============================================================

def is_co_huu(doi_tuong):
    """
    Kiểm tra đối tượng có phải cơ hữu không.
    Cơ hữu: CBNV, CBQL, CH, CHdn, CHNN1, GVNCV, GVQL hoặc bắt đầu bằng 'CH'
    """
    if pd.isna(doi_tuong) or str(doi_tuong).strip() == '':
        return False
    
    dt = str(doi_tuong).strip().upper()
    
    co_huu_list = ['CBNV', 'CBQL', 'CH', 'CHDN', 'CHNN1', 'GVNCV', 'GVQL']
    
    if dt in co_huu_list:
        return True
    if dt.startswith('CH'):
        return True
    
    return False


def calculate_gio_co_huu(df_lich_ky_full, df_cham_cong, df_gv_mapping):
    """
    Tính giờ dạy cơ hữu từ lịch kỳ toàn kỳ.
    KHÔNG bỏ qua SlotTypeCode = 'G'.
    """
    if df_lich_ky_full.empty:
        return pd.DataFrame(), 0, 0
    
    df = df_lich_ky_full.copy()
    
    # Tính giờ từng buổi (KHÔNG loại G)
    df['Hours'] = df['TypeSlot'].apply(get_hours_per_slot)
    
    # Group by Lecturer
    gio_per_gv = df.groupby('Lecturer')['Hours'].sum().reset_index()
    gio_per_gv.columns = ['AccountFE', 'TongGio']
    
    # Merge với danh sách GV để lấy ID
    result = gio_per_gv.merge(
        df_gv_mapping[['ID', 'AccountFE']], 
        on='AccountFE', 
        how='left'
    )
    
    # Lấy đối tượng từ chấm công
    if not df_cham_cong.empty:
        doi_tuong_map = df_cham_cong.groupby('ID')['DoiTuong'].first().reset_index()
        result = result.merge(doi_tuong_map, on='ID', how='left')
    else:
        result['DoiTuong'] = ''
    
    # Xác định cơ hữu
    result['LaCoHuu'] = result['DoiTuong'].apply(is_co_huu)
    
    # Tính tổng
    tong_gio_all = result['TongGio'].sum()
    tong_gio_co_huu = result[result['LaCoHuu'] == True]['TongGio'].sum()
    
    return result, tong_gio_co_huu, tong_gio_all


# ============================================================
# EXPORT TO EXCEL
# ============================================================

def export_to_excel(df_doi_sanh, df_wasnot_taken, df_co_huu=None):
    """
    Xuất kết quả ra file Excel với formatting.
    """
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Sheet 1: Đối sánh giờ dạy
        if not df_doi_sanh.empty:
            df_doi_sanh.to_excel(writer, sheet_name='Đối sánh giờ dạy', index=False)
        
        # Sheet 2: WasNot Taken
        if not df_wasnot_taken.empty:
            df_wasnot_taken.to_excel(writer, sheet_name='WasNot Taken', index=False)
        
        # Sheet 3: Giờ dạy cơ hữu
        if df_co_huu is not None and not df_co_huu.empty:
            df_co_huu.to_excel(writer, sheet_name='Giờ dạy cơ hữu', index=False)
        
        # Formatting
        workbook = writer.book
        
        header_font = Font(bold=True, color='FFFFFF', size=11)
        header_fill = PatternFill(start_color='10B981', end_color='10B981', fill_type='solid')
        header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        
        false_fill = PatternFill(start_color='FFE0E0', end_color='FFE0E0', fill_type='solid')
        
        thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        for sheet_name in workbook.sheetnames:
            ws = workbook[sheet_name]
            
            # Format header
            for cell in ws[1]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
                cell.border = thin_border
            
            # Auto-fit column width
            for col_idx, col in enumerate(ws.columns, 1):
                max_length = 0
                col_letter = get_column_letter(col_idx)
                
                for cell in col:
                    try:
                        if cell.value:
                            max_length = max(max_length, len(str(cell.value)))
                    except:
                        pass
                
                adjusted_width = min(max_length + 3, 40)
                ws.column_dimensions[col_letter].width = adjusted_width
            
            # Format data rows
            for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
                for cell in row:
                    cell.border = thin_border
                    cell.alignment = Alignment(vertical='center')
                    
                    # Format số
                    if isinstance(cell.value, (int, float)):
                        cell.number_format = '#,##0.00'
            
            # Highlight FALSE rows (Sheet Đối sánh)
            if sheet_name == 'Đối sánh giờ dạy':
                # Tìm cột KetQua
                ketqua_col = None
                for cell in ws[1]:
                    if cell.value == 'KetQua':
                        ketqua_col = cell.column
                        break
                
                if ketqua_col:
                    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
                        ketqua_cell = row[ketqua_col - 1]
                        if ketqua_cell.value == False or str(ketqua_cell.value).upper() == 'FALSE':
                            for cell in row:
                                cell.fill = false_fill
    
    output.seek(0)
    return output
