import pdfplumber
import pandas as pd
import re
import io
import os


# ── Helpers ───────────────────────────────────────────────────────────────────

def is_valid_subject_code(s):
    """
    Kiem tra ma mon hop le.
    Hop le : IOT102, NWC303, SYB302c, PRU211m, AIL303m
    Khong hop le : "Thay the bang mon combo khac..."
    """
    s = s.strip()
    return bool(re.match(r'^[A-Za-z]{2,6}\d{2,4}[a-zA-Z]{0,2}$', s))


def _normalize(s):
    """
    Chuan hoa chuoi: lower + strip + thay newline bang space.
    De so sanh noi dung cell bat ke PDF co xuong dong hay khong.
    VD: "Thay\\nthe" -> "thay the" -> match duoc "thay the"
    """
    if s is None:
        return ""
    return str(s).lower().strip().replace('\n', ' ')


def _merge_continuation_rows(table):
    """
    Gop dong tiep noi vao dong chinh truoc do.

    Dong tiep noi: row[0] la None hoac rong (khong co so thu tu).
    pdfplumber thuong tach cell nhieu dong thanh nhieu row rieng biet.

    Vi du:
        Row 9:  ['4', 'AIP391', 'AIL303m', ..., 'BIT_AI', ..., 'Thay', ...]
        Row 10: [None, None, ..., None, ..., 'the', ...]
        -> Sau gop:
        Row 9:  ['4', 'AIP391', 'AIL303m', ..., 'BIT_AI', ..., 'Thay the', ...]
    """
    if not table:
        return []

    merged = []
    for row in table:
        if not row:
            continue

        cell_0 = str(row[0]).strip() if row[0] else ""

        # Dong tiep noi: row[0] rong va da co dong truoc
        if not cell_0 and merged:
            prev = merged[-1]
            # Dam bao prev du do dai
            while len(prev) < len(row):
                prev.append(None)
            # Gop tung cell: append noi dung moi vao cell cu
            for i, cell in enumerate(row):
                if cell and str(cell).strip():
                    val = str(cell).strip()
                    if prev[i]:
                        prev[i] = str(prev[i]).rstrip() + ' ' + val
                    else:
                        prev[i] = val
        else:
            merged.append(list(row))

    return merged


def _find_hinh_thuc_idx(row):
    """
    Tim vi tri cot Hinh thuc trong row (sau khi da gop continuation rows).
    Do o chua 'tuong duong' hoac 'thay the'.
    Mac dinh tra ve 4 neu khong tim thay.
    """
    for i in range(2, len(row)):
        val = _normalize(row[i])
        if "tương đương" in val or "thay thế" in val:
            return i
    return 4  # fallback


# ── Ham chinh ─────────────────────────────────────────────────────────────────

def extract_from_pdf(pdf_source, so_qd="Unknown"):
    """
    Trich xuat du lieu mon tuong duong tu PDF.

    Args:
        pdf_source : duong dan file (str) hoac bytes / BytesIO
        so_qd      : so quyet dinh

    Returns:
        (data_rows, skipped_rows)
    """
    data_rows    = []
    skipped_rows = []

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
            raw_table = page.extract_table({
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines"
            })
            if not raw_table:
                continue

            # ── BUOC 1: Gop dong tiep noi truoc khi parse ────────────────
            table = _merge_continuation_rows(raw_table)

            for row in table:
                if not row or len(row) < 5:
                    continue

                cell_0 = str(row[0]).strip() if row[0] else ""
                cell_1 = str(row[1]).strip() if row[1] else ""

                # Bo qua dong tieu de
                if any(kw in cell_0 for kw in ["TT", "STT"]):
                    continue
                if any(kw in cell_1 for kw in ["Mã", "học phần", "triển khai",
                                                "Ma", "hoc phan", "trien khai"]):
                    continue

                # Cot co dinh
                subject_raw = str(row[1]).strip() if row[1] else ""
                replace_raw = str(row[2]).strip() if len(row) > 2 and row[2] else ""

                if not subject_raw:
                    continue

                # ── BUOC 2: Tim vi tri cot Hinh thuc ─────────────────────
                # Sau khi gop row, "Thay the" da nam trong 1 cell
                # _find_hinh_thuc_idx bat dau tu col 2 (skip TT, SubjectCode)
                ht_idx = _find_hinh_thuc_idx(row)

                # ── BUOC 3: Lay curriculum ────────────────────────────────
                # Gom tat ca cell khong rong tu row[3] den truoc ht_idx
                # (bo qua row[2] vi do la Replacecode)
                curriculum_parts = []
                for i in range(3, ht_idx):
                    if row[i] and str(row[i]).strip():
                        part = str(row[i]).strip().replace('\n', ' ')
                        curriculum_parts.append(part)
                curriculum = ", ".join(curriculum_parts)

                # ── BUOC 4: Lay Hinh thuc va Chu y ───────────────────────
                hinh_thuc = _normalize(row[ht_idx]) if len(row) > ht_idx else ""
                chu_y = ""
                if len(row) > ht_idx + 2 and row[ht_idx + 2]:
                    chu_y = str(row[ht_idx + 2]).strip().replace('\n', ' ')

                # Bo qua neu Replacecode la mo ta van ban
                first_code = replace_raw.split(',')[0].split('/')[0].strip()
                if not replace_raw or not is_valid_subject_code(first_code):
                    if subject_raw and replace_raw:
                        skipped_rows.append({
                            "page"           : page_num,
                            "SubjectCode"    : subject_raw,
                            "Replacecode_raw": replace_raw,
                            "ly_do"          : "Replacecode khong phai ma mon"
                        })
                    continue

                # Logic equivalent
                equivalent = "TRUE" if "tương đương" in hinh_thuc else "FALSE"
                note       = f"{so_qd} {chu_y}".strip()

                # Xu ly nhieu SubjectCode trong 1 o
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

    - Cap da co + co trong QD moi  -> cap nhat no/note/curriculum, giu "applied"
    - Cap da co + KHONG trong QD   -> "expired"
    - Cap hoan toan moi             -> them moi "applied"
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
            matched               = new_df[(new_df["SubjectCode"] == sc) &
                                           (new_df["Replacecode"] == rc)].iloc[0]
            row                   = row.copy()
            row["no"]             = matched["no"]
            row["note"]           = matched["note"]
            row["curriculumcode"] = matched["curriculumcode"]
            row["replace_status"] = "applied"
        else:
            row                   = row.copy()
            row["replace_status"] = "expired"

        updated_rows.append(row)

    for _, new_row in new_df.iterrows():
        pair = (str(new_row["SubjectCode"]).strip(), str(new_row["Replacecode"]).strip())
        if pair not in existing_pairs:
            updated_rows.append(new_row)

    return pd.DataFrame(updated_rows)[COLS].reset_index(drop=True)


# ── Chay doc lap ──────────────────────────────────────────────────────────────
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
