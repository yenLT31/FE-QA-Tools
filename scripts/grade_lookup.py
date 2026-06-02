"""
Logic cho công cụ Grade Lookup (tra cứu điểm SV).
Thuần xử lý dữ liệu — không phụ thuộc Streamlit, có thể test riêng.

Public functions dùng cho page:
    load_and_clean(file_bytes) -> (DataFrame đã làm sạch, info: dict)
    lookup_grades(clean_df, mssv_list) -> (DataFrame kết quả, list MSSV không thấy)
    to_excel_bytes(result_df, not_found) -> bytes
    detect_mssv_col(columns) -> int   # để page đọc cột MSSV từ file upload
"""

import io
import re
import pandas as pd

# ============================================================
#  CHUẨN HÓA TÊN CỘT
# ============================================================
CANON = {
    "rollnumber": "RollNumber",
    "semestername": "SemesterName",
    "classname": "ClassName",
    "subjectcode": "SubjectCode",
    "averagemark": "AverageMark",
    "status": "Status",
    "startdate": "StartDate",
    "enddate": "EndDate",
    "credits": "Credits",
}

DISPLAY_COLS = ["RollNumber", "SubjectCode", "SemesterName", "ClassName",
                "AverageMark", "Status", "Credits", "StartDate", "EndDate"]


def _canon_columns(df):
    rename = {}
    for c in df.columns:
        key = re.sub(r"[\s_]+", "", str(c).strip().lower())
        if key in CANON:
            rename[c] = CANON[key]
    return df.rename(columns=rename)


# ============================================================
#  PHÁT HIỆN ĐỊNH DẠNG NGÀY (KHÔNG ĐOÁN)
# ============================================================
_DATE_RE = re.compile(r"^\s*(\d{1,2})\D+(\d{1,2})\D+(\d{2,4})")


def _date_parts(s):
    m = _DATE_RE.match(str(s))
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def _string_samples(*series_list):
    """Lấy giá trị dạng chữ từ các cột ngày (bỏ qua cột đã là datetime thật)."""
    samples, has_string = [], False
    for s in series_list:
        if s is None or pd.api.types.is_datetime64_any_dtype(s):
            continue
        has_string = True
        samples += s.dropna().astype(str).str.strip().tolist()
    return samples, has_string


def detect_dayfirst(start_series, end_series):
    """
    Quyết định định dạng ngày từ chính dữ liệu của 2 cột.
    True  -> dd/mm/yyyy (dayfirst)
    False -> mm/dd/yyyy
    None  -> không đủ bằng chứng từ giá trị (mọi phần đều <= 12)
    """
    samples, has_string = _string_samples(start_series, end_series)
    if not has_string:
        return True  # cột đã là ngày thật -> không mơ hồ
    day_ev = month_ev = 0
    for v in samples:
        p = _date_parts(v)
        if not p:
            continue
        a, b = p
        if a > 12 and b <= 12:
            day_ev += 1        # phần đầu > 12 -> ngày trước -> dd/mm
        elif b > 12 and a <= 12:
            month_ev += 1      # phần giữa > 12 -> tháng sau -> mm/dd
    if day_ev and not month_ev:
        return True
    if month_ev and not day_ev:
        return False
    if day_ev or month_ev:     # mâu thuẫn -> theo đa số
        return day_ev >= month_ev
    return None                # hoàn toàn mơ hồ


def _resolve_by_order(start_series, end_series):
    """
    Khi giá trị mơ hồ: dùng quan hệ StartDate <= EndDate để chọn định dạng.
    Thử cả 2 cách đọc, cách nào cho Start <= End ở nhiều dòng hơn thì chọn.
    """
    if start_series is None or end_series is None:
        return True
    best, best_score = True, -1
    for cand in (True, False):
        s = pd.to_datetime(start_series.astype(str), dayfirst=cand, errors="coerce")
        e = pd.to_datetime(end_series.astype(str), dayfirst=cand, errors="coerce")
        score = int(((s.notna()) & (e.notna()) & (s <= e)).sum())
        if score > best_score:
            best, best_score = cand, score
    return best


def _norm_date(series, dayfirst):
    if series is None:
        return series
    if pd.api.types.is_datetime64_any_dtype(series):
        return series
    return pd.to_datetime(series.astype(str).str.strip(),
                          dayfirst=dayfirst, errors="coerce")


# ============================================================
#  ĐỌC & LÀM SẠCH
# ============================================================
def load_and_clean(file_bytes):
    sheets = pd.read_excel(io.BytesIO(file_bytes), sheet_name=None)
    frames = []
    for _, sdf in sheets.items():
        if sdf is None or sdf.empty:
            continue
        frames.append(_canon_columns(sdf))
    if not frames:
        return pd.DataFrame(columns=list(CANON.values())), {"rows": 0}

    df = pd.concat(frames, ignore_index=True)

    # strip khoảng trắng ở mọi cột chữ
    for c in df.select_dtypes(include="object").columns:
        df[c] = (df[c].astype(str).str.strip()
                 .replace({"nan": "", "None": "", "NaT": ""}))

    # chuẩn hóa khóa tìm kiếm (viết hoa cho khớp khi tra cứu)
    if "RollNumber" in df:
        df["RollNumber"] = df["RollNumber"].str.upper()
    if "SubjectCode" in df:
        df["SubjectCode"] = df["SubjectCode"].str.upper()

    # số (chấp nhận cả dấu phẩy thập phân)
    if "AverageMark" in df:
        df["AverageMark"] = pd.to_numeric(
            df["AverageMark"].astype(str).str.replace(",", ".", regex=False),
            errors="coerce")
    if "Credits" in df:
        df["Credits"] = pd.to_numeric(df["Credits"], errors="coerce")

    # ngày: phát hiện định dạng từ dữ liệu
    start_raw = df["StartDate"] if "StartDate" in df else None
    end_raw = df["EndDate"] if "EndDate" in df else None
    dayfirst = detect_dayfirst(start_raw, end_raw)
    resolved_by = "giá trị ngày > 12" if dayfirst is not None else "thứ tự Start ≤ End"
    if dayfirst is None:
        dayfirst = _resolve_by_order(start_raw, end_raw)
    if "StartDate" in df:
        df["StartDate"] = _norm_date(df["StartDate"], dayfirst)
    if "EndDate" in df:
        df["EndDate"] = _norm_date(df["EndDate"], dayfirst)

    raw_rows = len(df)

    # giữ lần học gần nhất theo EndDate cho mỗi (RollNumber, SubjectCode)
    if {"RollNumber", "SubjectCode", "EndDate"} <= set(df.columns):
        df = df.sort_values("EndDate", na_position="first")
        df = df.drop_duplicates(subset=["RollNumber", "SubjectCode"], keep="last")

    df = df.reset_index(drop=True)
    info = {
        "rows": len(df),
        "raw_rows": raw_rows,
        "removed_dup": raw_rows - len(df),
        "date_format": "dd/mm/yyyy" if dayfirst else "mm/dd/yyyy",
        "date_resolved_by": resolved_by,
        "students": df["RollNumber"].nunique() if "RollNumber" in df else 0,
    }
    return df, info


# ============================================================
#  TRA CỨU
# ============================================================
def lookup_grades(clean_df, mssv_list):
    queries = list(dict.fromkeys(m.strip() for m in mssv_list if m and m.strip()))
    upper = {q.upper() for q in queries}

    if "RollNumber" not in clean_df.columns:
        return pd.DataFrame(columns=DISPLAY_COLS), queries

    res = clean_df[clean_df["RollNumber"].isin(upper)].copy()
    if "EndDate" in res.columns:
        res = res.sort_values(["RollNumber", "EndDate"],
                              ascending=[True, False], na_position="last")

    found = set(res["RollNumber"])
    not_found = [q for q in queries if q.upper() not in found]

    # định dạng ngày để hiển thị
    for c in ("StartDate", "EndDate"):
        if c in res.columns and pd.api.types.is_datetime64_any_dtype(res[c]):
            res[c] = res[c].dt.strftime("%d/%m/%Y").fillna("")

    cols = [c for c in DISPLAY_COLS if c in res.columns]
    if cols:
        res = res[cols]
    return res.reset_index(drop=True), not_found


# ============================================================
#  XUẤT EXCEL
# ============================================================
def to_excel_bytes(result_df, not_found):
    out = io.BytesIO()
    body = result_df if (result_df is not None and not result_df.empty) \
        else pd.DataFrame(columns=DISPLAY_COLS)
    with pd.ExcelWriter(out, engine="openpyxl") as w:
        body.to_excel(w, index=False, sheet_name="Điểm SV")
        pd.DataFrame({"MSSV không tìm thấy": not_found or [""]}).to_excel(
            w, index=False, sheet_name="Không tìm thấy")
    return out.getvalue()


# ============================================================
#  ĐỌC CỘT MSSV TỪ FILE (cho page khi upload file MSSV)
# ============================================================
def detect_mssv_col(columns):
    keywords = ["mssv", "rollnumber", "roll_number", "roll number", "ma_sv",
                "masv", "mã sv", "mã số sinh viên", "student_id", "studentid",
                "ma so sinh vien"]
    for i, col in enumerate(columns):
        col_lower = str(col).lower().strip()
        for kw in keywords:
            if kw in col_lower:
                return i
    return -1
