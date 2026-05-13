import pdfplumber
import pandas as pd
import re
import io
import os


# ── Helpers ───────────────────────────────────────────────────────────────────

def is_valid_subject_code(s):
    """
    Kiểm tra mã môn hợp lệ.
    Hợp lệ : IOT102, NWC303, SYB302c, PRU211m, AIL303m
    Không hợp lệ : "Thay thế bằng môn combo khác..."
    """
    s = s.strip()
    return bool(re.match(r'^[A-Za-z]{2,6}\d{2,4}[a-zA-Z]{0,2}$', s))


def _normalize(s):
    """
    Chuẩn hóa chuỗi: lower + strip + thay newline bằng space.
    Dùng để so sánh nội dung cell bất kể PDF có xuống dòng hay không.
    VD: "Thay\nthe" -> "thay the" -> match duoc "thay the"
    """
    if s is None:
        return ""
    return str(s).lower().strip().replace('\n', ' ')


def _find_hinh_thuc_idx(row):
    """
    Tim vi tri cot Hinh thuc trong row bang cach do o chua
    'tuong duong' hoac 'thay the'. Mac dinh tra ve 4 neu khong tim thay.

    Ly do can ham nay:
    1. Cell curriculumcode dai bi pdfplumber tach thanh nhieu cell
       -> cac cot sau lech sang phai.
    2. Cell "Thay the" doi khi chua ky tu xuong dong "Thay\nthe"
       -> can chuan hoa truoc khi so sanh.
    """
    for i in range(3, len(row)):
        val = _normalize(row[i])
        if "tuong duong" in val or "thay the" in val or "tương đương" in val or "thay thế" in val:
            return i
    return 4  # fallback mac dinh


# ── Ham chinh ─────────────────────────────────────────────────────────────────

def extract_from_pdf(pdf_source, so_qd="Unknown"):
    """
    Trich xuat du lieu mon tuong duong tu PDF.

    Args:
        pdf_source : duong dan file (str) hoac bytes / BytesIO (tu Streamlit upload)
        so_qd      : so quyet dinh, tu dong lay tu ten file neu pdf_source la str

    Returns:
        (data_rows, skipped_rows)
    """
    data_rows    = []
    skipped_rows = []

    # Xac dinh nguon mo
    if isinstance(pdf_source, str):
        file_name   = os.path.basename(pdf_source)
        match       = re.search(r'\d+', file_name)
        so_qd       = match.group() if match else so_qd
        open_target = pdf_source
    elif isinstance(pdf_source, bytes):
        open_target = io.BytesIO(pdf_source)
    else:
        open_target = pdf_source

    with pdfplumber.open(open_target) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            table = page.extract_table({
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines"
            })
            if not table:
                continue

            for row in table:
                if not row or len(row) < 5:
                    continue

                cell_0 = str(row[0]).strip() if row[0] else ""
                cell_1 = str(row[1]).strip() if row[1] else ""

                # Bo qua dong tieu de
                if any(kw in cell_0 for kw in ["TT", "STT"]):
                    continue
                if any(kw in cell_1 for kw in ["M\u00e3", "h\u1ecdc ph\u1ea7n", "tri\u1ec3n khai"]):
                    continue

                # Cot co dinh
                subject_raw = str(row[1]).strip() if row[1] else ""
                replace_raw = str(row[2]).strip() if len(row) > 2 and row[2] else ""

                if not subject_raw:
                    continue

                # Tim dong vi tri cot Hinh thuc
                ht_idx = _find_hinh_thuc_idx(row)

                # curriculum: gop tat ca cell tu row[3] den truoc ht_idx
                # Chuan hoa: thay \n bang space trong tung part
                curriculum_parts = []
                for i in range(3, ht_idx):
                    if row[i] and str(row[i]).strip():
                        part = str(row[i]).strip().replace('\n', ' ')
                        curriculum_parts.append(part)
                curriculum = ", ".join(curriculum_parts)

                # hinh_thuc: chuan hoa (lower + replace \n -> space)
                hinh_thuc = _normalize(row[ht_idx]) if len(row) > ht_idx else ""

                # chu_y: o ht_idx + 2
                chu_y = ""
                if len(row) > ht_idx + 2 and row[ht_idx + 2]:
                    chu_y = str(row[ht_idx + 2]).strip().replace('\n', ' ')

                # Bo qua neu Replacecode la mo ta van ban (khong phai ma mon)
                first_code = replace_raw.split(',')[0].split('/')[0].strip()
                if not replace_raw or not is_valid_subject_code(first_code):
                    if subject_raw and replace_raw:
                        skipped_rows.append({
                            "page"           : page_num,
                            "SubjectCode"    : subject_raw,
                            "Replacecode_raw": replace_raw,
                            "ly_do"          : "Replacecode khong phai ma mon hop le"
                        })
                    continue

                # Logic equivalent / replace
                # "Tuong duong" -> 2 chieu : replace=TRUE, equivalent=TRUE
                # "Thay the"   -> 1 chieu : replace=TRUE, equivalent=FALSE
                equivalent = "TRUE" if ("tương đương" in hinh_thuc or "tuong duong" in hinh_thuc) else "FALSE"

                # Note = "{so_qd} {chu_y}"
                note = f"{so_qd} {chu_y}".strip()

                # Xu ly nhieu SubjectCode trong 1 o: "LAB101, PRU211m, PRU212"
                for sc in re.split(r'[,/\n]+', subject_raw):
                    sc = sc.strip()
                    if sc and is_valid_subject_code(sc):
                        data_rows.append({
                            "SubjectCode"   : sc,
                            "Replacecode"   : replace_raw,
                            "curriculumcode": curriculum,
                            "replace"       : "TRUE",
                            "equivalent"    : equivalent,
                            "replace_status": "applied",
                            "note"          : note,
                            "no"            : so_qd
                        })

    return data_rows, skipped_rows


def merge_database(existing_df, new_rows):
    """
    Gop du lieu QD moi vao database hien co.

    Logic:
        - Cap (SubjectCode, Replacecode) da co + co trong QD moi
          -> cap nhat no / note / curriculumcode, giu "applied"
        - Cap da co + KHONG co trong QD moi
          -> danh dau "expired"
        - Cap hoan toan moi
          -> them moi voi "applied"

    Returns:
        DataFrame da cap nhat, cot chuan 8 truong
    """
    COLS = ["SubjectCode", "Replacecode", "curriculumcode",
            "replace", "equivalent", "replace_status", "note", "no"]

    if not new_rows:
        return existing_df if existing_df is not None else pd.DataFrame(columns=COLS)

    new_df    = pd.DataFrame(new_rows)
    new_pairs = set(zip(new_df["SubjectCode"], new_df["Replacecode"]))

    if existing_df is None or existing_df.empty:
        return new_df[COLS].reset_index(drop=True)

    existing_df    = existing_df.copy()
    updated_rows   = []
    existing_pairs = set()

    for _, row in existing_df.iterrows():
        sc   = str(row.get("SubjectCode", "")).strip()
        rc   = str(row.get("Replacecode", "")).strip()
        pair = (sc, rc)
        existing_pairs.add(pair)

        if pair in new_pairs:
            matched               = new_df[(new_df["SubjectCode"] == sc) & (new_df["Replacecode"] == rc)].iloc[0]
            row                   = row.copy()
            row["no"]             = matched["no"]
            row["note"]           = matched["note"]
            row["curriculumcode"] = matched["curriculumcode"]
            row["replace_status"] = "applied"
        else:
            row                   = row.copy()
            row["replace_status"] = "expired"

        updated_rows.append(row)

    # Them cap hoan toan moi
    for _, new_row in new_df.iterrows():
        pair = (str(new_row["SubjectCode"]).strip(), str(new_row["Replacecode"]).strip())
        if pair not in existing_pairs:
            updated_rows.append(new_row)

    result_df = pd.DataFrame(updated_rows)[COLS].reset_index(drop=True)
    return result_df


# ── Chay doc lap (khong dung Streamlit) ──────────────────────────────────────
if __name__ == "__main__":
    INPUT_DIR   = "input/"
    OUTPUT_FILE = "output/Database_Tong_Hop.xlsx"

    all_new_data = []
    all_skipped  = []

    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".pdf")]

    if not pdf_files:
        print("Khong tim thay file PDF nao trong input/")
    else:
        for file in pdf_files:
            path = os.path.join(INPUT_DIR, file)
            print(f"\nDang xu ly: {file}")
            rows, skipped = extract_from_pdf(path)
            all_new_data.extend(rows)
            all_skipped.extend(skipped)
            print(f"   Trich xuat: {len(rows)} dong")
            if skipped:
                print(f"   Bo qua   : {len(skipped)} dong")

    if all_new_data:
        existing = pd.read_excel(OUTPUT_FILE) if os.path.exists(OUTPUT_FILE) else None
        final    = merge_database(existing, all_new_data)
        final.to_excel(OUTPUT_FILE, index=False)
        print(f"\nDa luu {len(final)} dong vao {OUTPUT_FILE}")

    if all_skipped:
        print("\nCac dong bi bo qua:")
        for s in all_skipped:
            print(f"   Trang {s['page']}: {s['SubjectCode']} -> \"{s['Replacecode_raw']}\"")
