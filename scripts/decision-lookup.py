"""
scripts/decision-lookup.py
Logic thuần túy — không import streamlit
"""

import pdfplumber
import pandas as pd
import re
import io
from pathlib import Path

# ---------------------------------------------------------------------------
# Từ khoá nhận diện cột MSSV / RollNumber
# ---------------------------------------------------------------------------
MSSV_KEYWORDS = [
    'mssv', 'rollnumber', 'roll number', 'roll', 'mã sv',
    'mã sinh viên', 'mã số sv', 'mã số sinh viên',
    'student id', 'studentid', 'mã hs', 'mã học sinh',
    'mã số hs', 'mã', 'id'
]

STT_KEYWORDS = ['stt', 'tt', 'số tt', 'số thứ tự', 'no', 'no.', 'tт']


# ---------------------------------------------------------------------------
# Nhận diện tên QĐ
# ---------------------------------------------------------------------------
def get_qd_name(filename: str, pdf_bytes: bytes = None) -> str:
    """
    Lấy tên QĐ: ưu tiên tên file → fallback đọc nội dung trang 1.
    """
    stem = Path(filename).stem

    # Pattern từ tên file
    file_patterns = [
        r'[Qq][Đđd][-_\s]?(\d{2,4})',
        r'[Qq]uyet[-_\s]?[Dd]inh[-_\s]?(\d{2,4})',
        r'[-_](\d{2,4})[-_]',
        r'(\d{2,4})',
    ]
    for pat in file_patterns:
        m = re.search(pat, stem)
        if m:
            return f"QĐ {m.group(1)}"

    # Fallback: quét trang 1 của PDF
    if pdf_bytes:
        try:
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                if pdf.pages:
                    text = pdf.pages[0].extract_text() or ''
                    content_patterns = [
                        r'[Qq]uyết\s+[Đđ]ịnh\s+[Ss]ố[:\s]+(\d+[/\w-]*)',
                        r'[Qq][Đđ]\s*[Ss]ố[:\s]+(\d+[/\w-]*)',
                        r'[Ss]ố[:\s]+(\d{2,4}/[Qq][Đđ]-\w+)',
                    ]
                    for pat in content_patterns:
                        m = re.search(pat, text)
                        if m:
                            return f"QĐ {m.group(1)}"
        except Exception:
            pass

    return stem  # fallback cuối cùng


# ---------------------------------------------------------------------------
# Detect cột MSSV
# ---------------------------------------------------------------------------
def _normalize(s: str) -> str:
    s = str(s).lower().strip()
    s = s.replace('đ', 'd').replace('ắ', 'a').replace('ă', 'a')
    s = s.replace('ê', 'e').replace('ố', 'o').replace('ố', 'o')
    s = re.sub(r'\s+', '', s)
    return s


def detect_mssv_col(headers: list) -> int:
    """Trả về index cột MSSV, -1 nếu không tìm thấy."""
    if not headers:
        return -1
    for i, h in enumerate(headers):
        if h is None:
            continue
        h_norm = _normalize(str(h))
        for kw in MSSV_KEYWORDS:
            kw_norm = _normalize(kw)
            if kw_norm == h_norm or (len(kw_norm) > 3 and kw_norm in h_norm):
                return i
    return -1


def detect_stt_col(headers: list) -> int:
    """Trả về index cột STT, -1 nếu không tìm thấy."""
    if not headers:
        return -1
    for i, h in enumerate(headers):
        if h is None:
            continue
        h_norm = _normalize(str(h))
        for kw in STT_KEYWORDS:
            if _normalize(kw) == h_norm:
                return i
    return -1


# ---------------------------------------------------------------------------
# Gộp ô xuống dòng
# ---------------------------------------------------------------------------
def merge_wrapped_rows(rows: list, mssv_col: int) -> list:
    """
    Dòng bị xuống hàng trong PDF thường có ô MSSV trống.
    Hàm này gộp các dòng đó vào dòng trước.
    """
    if not rows or mssv_col < 0:
        return rows

    merged = []
    for raw_row in rows:
        if not raw_row:
            continue
        row = [str(c).strip() if c is not None else '' for c in raw_row]

        mssv_val = row[mssv_col] if mssv_col < len(row) else ''

        # Dòng tiếp nối: MSSV trống và có dòng trước
        if not mssv_val and merged:
            prev = merged[-1]
            for i in range(max(len(prev), len(row))):
                if i < len(row) and i < len(prev):
                    addon = row[i]
                    if addon:
                        prev[i] = (prev[i] + ' ' + addon).strip()
                elif i < len(row):
                    prev.append(row[i])
        else:
            merged.append(list(row))

    return merged


# ---------------------------------------------------------------------------
# Kiểm tra MSSV có hợp lệ không (chuỗi chữ + số liền nhau)
# ---------------------------------------------------------------------------
MSSV_PATTERN = re.compile(r'^[A-Za-z]{1,4}\d{4,10}$')


def looks_like_mssv(val: str) -> bool:
    return bool(MSSV_PATTERN.match(val.strip()))


# ---------------------------------------------------------------------------
# Hàm tìm kiếm chính
# ---------------------------------------------------------------------------
def search_mssv_in_pdfs(mssv_list: list, pdf_files: list) -> dict:
    """
    Tìm kiếm MSSV trong danh sách PDF.

    Args:
        mssv_list : list[str] — danh sách MSSV cần tra
        pdf_files : list[dict] — [{'name': str, 'bytes': bytes}]

    Returns:
        dict {
            mssv: {
                'found': bool,
                'results': [{
                    'qd_name': str,
                    'page'   : int,
                    'stt'    : str,
                    'headers': list[str],
                    'row'    : list[str],
                    'row_dict': dict
                }]
            },
            '_errors': [{'file': str, 'error': str}]
        }
    """
    results = {m.strip(): {'found': False, 'results': []} for m in mssv_list}
    mssv_upper_map = {m.strip().upper(): m.strip() for m in mssv_list}
    errors = []

    for pdf_file in pdf_files:
        fname   = pdf_file['name']
        fbytes  = pdf_file['bytes']
        qd_name = get_qd_name(fname, fbytes)

        try:
            with pdfplumber.open(io.BytesIO(fbytes)) as pdf:
                # Lưu headers hợp lệ từ trang trước để dùng lại
                last_valid_headers  = None
                last_valid_mssv_col = -1
                last_valid_stt_col  = -1

                for page_num, page in enumerate(pdf.pages, start=1):
                    tables = page.extract_tables()
                    if not tables:
                        continue

                    for table in tables:
                        if not table or len(table) < 1:
                            continue

                        # --- Thử detect header từ hàng đầu ---
                        raw_first = table[0] or []
                        candidate_headers = [str(h).strip() if h else '' for h in raw_first]
                        candidate_mssv_col = detect_mssv_col(candidate_headers)

                        if candidate_mssv_col >= 0:
                            # Hàng đầu là header hợp lệ
                            headers  = candidate_headers
                            mssv_col = candidate_mssv_col
                            stt_col  = detect_stt_col(headers)
                            data_rows = table[1:] if len(table) > 1 else []

                            # Lưu lại để dùng cho trang không có header
                            last_valid_headers  = headers
                            last_valid_mssv_col = mssv_col
                            last_valid_stt_col  = stt_col

                        elif last_valid_headers is not None:
                            # Trang này không có header → dùng lại headers trang trước
                            headers  = last_valid_headers
                            mssv_col = last_valid_mssv_col
                            stt_col  = last_valid_stt_col
                            # Toàn bộ table (kể cả hàng đầu) là data
                            data_rows = table

                        else:
                            # Chưa có headers nào hợp lệ, bỏ qua
                            continue

                        if mssv_col < 0:
                            continue

                        data_rows = merge_wrapped_rows(data_rows, mssv_col)

                        for row in data_rows:
                            if not row or mssv_col >= len(row):
                                continue

                            cell = str(row[mssv_col]).strip()
                            cell_upper = cell.upper()

                            if cell_upper not in mssv_upper_map:
                                continue

                            original = mssv_upper_map[cell_upper]

                            # STT
                            stt = ''
                            if stt_col >= 0 and stt_col < len(row):
                                stt = str(row[stt_col]).strip()
                            elif row:
                                stt = str(row[0]).strip()

                            # Pad row về đủ số cột header
                            padded_row = row + [''] * max(0, len(headers) - len(row))
                            row_dict = {
                                headers[i]: padded_row[i]
                                for i in range(len(headers))
                            }

                            results[original]['found'] = True
                            results[original]['results'].append({
                                'qd_name' : qd_name,
                                'page'    : page_num,
                                'stt'     : stt,
                                'headers' : headers,
                                'row'     : padded_row[:len(headers)],
                                'row_dict': row_dict,
                            })

        except Exception as e:
            errors.append({'file': fname, 'error': str(e)})

    results['_errors'] = errors
    return results


# ---------------------------------------------------------------------------
# Build export DataFrames
# ---------------------------------------------------------------------------
def build_export_data(mssv_list: list, results: dict):
    """
    Trả về (df_summary, df_detail) để xuất Excel.
    """
    # Sheet 1 — Tổng hợp
    summary_rows = []
    for mssv in mssv_list:
        r = results.get(mssv.strip(), {'found': False, 'results': []})
        qd_names = list(dict.fromkeys(x['qd_name'] for x in r['results']))
        summary_rows.append({
            'MSSV'        : mssv.strip(),
            'Tìm thấy'    : 'Có' if r['found'] else 'Không',
            'Số QĐ'       : len(qd_names),
            'Danh sách QĐ': ', '.join(qd_names),
            'Số vị trí'   : len(r['results']),
        })
    df_summary = pd.DataFrame(summary_rows)

    # Sheet 2 — Chi tiết
    detail_rows = []
    for mssv in mssv_list:
        r = results.get(mssv.strip(), {'found': False, 'results': []})
        if not r['results']:
            detail_rows.append({
                'MSSV'   : mssv.strip(),
                'Tên QĐ' : 'Không tìm thấy',
                'Trang'  : '',
                'STT'    : '',
            })
        else:
            for hit in r['results']:
                row = {
                    'MSSV'   : mssv.strip(),
                    'Tên QĐ' : hit['qd_name'],
                    'Trang'  : f"Trang {hit['page']}",
                    'STT'    : hit['stt'],
                }
                row.update(hit['row_dict'])
                detail_rows.append(row)
    df_detail = pd.DataFrame(detail_rows)

    return df_summary, df_detail


def to_excel_bytes(df_summary: pd.DataFrame, df_detail: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_summary.to_excel(writer, sheet_name='Tổng hợp', index=False)
        df_detail.to_excel(writer, sheet_name='Chi tiết', index=False)
    return output.getvalue()
