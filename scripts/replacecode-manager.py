import pdfplumber
import pandas as pd
import re
import io
import os


def is_valid_subject_code(s):
    """
    Kiểm tra mã môn hợp lệ.
    Hợp lệ : IOT102, NWC303, SYB302c, PRU211m, AIL303m
    Không hợp lệ : "Thay thế bằng môn combo khác..."
    """
    s = s.strip()
    return bool(re.match(r'^[A-Za-z]{2,6}\d{2,4}[a-zA-Z]{0,2}$', s))


def _find_hinh_thuc_idx(row):
    """
    Tìm vị trí cột Hình thức trong row bằng cách dò ô chứa
    'tương đương' hoặc 'thay thế'. Mặc định trả về 4 nếu không tìm thấy.

    Lý do cần hàm này: cell curriculumcode nhiều dòng đôi khi bị
    pdfplumber tách thành nhiều cell → các cột sau bị lệch sang phải.
    """
    for i in range(3, len(row)):
        val = str(row[i]).lower().strip() if row[i] else ""
        if "tương đương" in val or "thay thế" in val:
            return i
    return 4  # fallback mặc định


def extract_from_pdf(pdf_source, so_qd="Unknown"):
    """
    Trích xuất dữ liệu môn tương đương từ PDF.

    Args:
        pdf_source : đường dẫn file (str) hoặc bytes / BytesIO (từ Streamlit upload)
        so_qd      : số quyết định, tự động lấy từ tên file nếu pdf_source là str

    Returns:
        (data_rows, skipped_rows)
    """
    data_rows    = []
    skipped_rows = []

    # Xác định nguồn mở
    if isinstance(pdf_source, str):
        file_name     = os.path.basename(pdf_source)
        match         = re.search(r'\d+', file_name)
        so_qd         = match.group() if match else so_qd
        open_target   = pdf_source
    elif isinstance(pdf_source, bytes):
        open_target   = io.BytesIO(pdf_source)
    else:
        open_target   = pdf_source  # BytesIO đã sẵn sàng

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

                # Bỏ qua dòng tiêu đề
                if any(kw in cell_0 for kw in ["TT", "STT"]):
                    continue
                if any(kw in cell_1 for kw in ["Mã", "học phần", "triển khai"]):
                    continue

                # ── Đọc cột cố định (không bao giờ lệch) ─────────────────
                subject_raw = str(row[1]).strip() if row[1] else ""
                replace_raw = str(row[2]).strip() if len(row) > 2 and row[2] else ""

                if not subject_raw:
                    continue

                # ── Tìm động vị trí cột Hình thức ────────────────────────
                # Cell curriculumcode nhiều dòng có thể bị tách thành nhiều
                # cell → dò ô chứa "Tương đương"/"Thay thế" thay vì dùng index cố định
                ht_idx = _find_hinh_thuc_idx(row)

                # curriculum = gộp tất cả cell từ row[3] đến trước ht_idx
                curriculum_parts = [
                    str(row[i]).strip()
                    for i in range(3, ht_idx)
                    if row[i] and str(row[i]).strip()
                ]
                curriculum = ", ".join(curriculum_parts)

                hinh_thuc  = str(row[ht_idx]).strip()                                    if len(row) > ht_idx     else ""
                chu_y      = str(row[ht_idx + 2]).strip()                                \
                             if len(row) > ht_idx + 2 and row[ht_idx + 2] else ""

                if not subject_raw:
                    continue

                # Bỏ qua nếu Replacecode là mô tả văn bản (không phải mã môn)
                first_code = replace_raw.split(',')[0].split('/')[0].strip()
                if not replace_raw or not is_valid_subject_code(first_code):
                    if subject_raw and replace_raw:
                        skipped_rows.append({
                            "page"           : page_num,
                            "SubjectCode"    : subject_raw,
                            "Replacecode_raw": replace_raw,
                            "ly_do"          : "Replacecode không phải mã môn hợp lệ"
                        })
                    continue

                # ── Logic equivalent / replace ────────────────────────────
                # "Tương đương" → 2 chiều : replace=TRUE, equivalent=TRUE
                # "Thay thế"   → 1 chiều : replace=TRUE, equivalent=FALSE
                equivalent = "TRUE" if "tương đương" in hinh_thuc.lower() else "FALSE"

                # Note = "{so_qd} {chu_y}"
                note = f"{so_qd} {chu_y}".strip()

                # Xử lý nhiều SubjectCode trong 1 ô: "LAB101, PRU211m, PRU212"
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
    Gộp dữ liệu QĐ mới vào database hiện có.

    Logic:
        - Cặp (SubjectCode, Replacecode) đã có + có trong QĐ mới
          → cập nhật no / note / curriculumcode, giữ "applied"
        - Cặp đã có + KHÔNG có trong QĐ mới
          → đánh dấu "expired"
        - Cặp hoàn toàn mới
          → thêm mới với "applied"

    Returns:
        DataFrame đã cập nhật, cột chuẩn 8 trường
    """
    COLS = ["SubjectCode", "Replacecode", "curriculumcode",
            "replace", "equivalent", "replace_status", "note", "no"]

    if not new_rows:
        return existing_df if existing_df is not None else pd.DataFrame(columns=COLS)

    new_df    = pd.DataFrame(new_rows)
    new_pairs = set(zip(new_df["SubjectCode"], new_df["Replacecode"]))

    if existing_df is None or existing_df.empty:
        return new_df[COLS].reset_index(drop=True)

    existing_df = existing_df.copy()
    updated_rows  = []
    existing_pairs = set()

    for _, row in existing_df.iterrows():
        sc   = str(row.get("SubjectCode", "")).strip()
        rc   = str(row.get("Replacecode", "")).strip()
        pair = (sc, rc)
        existing_pairs.add(pair)

        if pair in new_pairs:
            # Cập nhật theo QĐ mới
            matched              = new_df[(new_df["SubjectCode"] == sc) & (new_df["Replacecode"] == rc)].iloc[0]
            row                  = row.copy()
            row["no"]            = matched["no"]
            row["note"]          = matched["note"]
            row["curriculumcode"]= matched["curriculumcode"]
            row["replace_status"]= "applied"
        else:
            # Không có trong QĐ mới → hết hiệu lực
            row                  = row.copy()
            row["replace_status"]= "expired"

        updated_rows.append(row)

    # Thêm cặp hoàn toàn mới
    for _, new_row in new_df.iterrows():
        pair = (str(new_row["SubjectCode"]).strip(), str(new_row["Replacecode"]).strip())
        if pair not in existing_pairs:
            updated_rows.append(new_row)

    result_df = pd.DataFrame(updated_rows)[COLS].reset_index(drop=True)
    return result_df


# ── Chạy độc lập (không dùng Streamlit) ──────────────────────────────────────
if __name__ == "__main__":
    INPUT_DIR   = "input/"
    OUTPUT_FILE = "output/Database_Tong_Hop.xlsx"

    all_new_data = []
    all_skipped  = []

    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".pdf")]

    if not pdf_files:
        print("❌ Không tìm thấy file PDF nào trong input/")
    else:
        for file in pdf_files:
            path = os.path.join(INPUT_DIR, file)
            print(f"\n📄 Đang xử lý: {file}")
            rows, skipped = extract_from_pdf(path)
            all_new_data.extend(rows)
            all_skipped.extend(skipped)
            print(f"   ✅ Trích xuất: {len(rows)} dòng")
            if skipped:
                print(f"   ⚠️  Bỏ qua   : {len(skipped)} dòng")

    if all_new_data:
        existing = pd.read_excel(OUTPUT_FILE) if os.path.exists(OUTPUT_FILE) else None
        final    = merge_database(existing, all_new_data)
        final.to_excel(OUTPUT_FILE, index=False)
        print(f"\n✅ Đã lưu {len(final)} dòng → {OUTPUT_FILE}")

    if all_skipped:
        print(f"\n⚠️  Các dòng bị bỏ qua:")
        for s in all_skipped:
            print(f"   Trang {s['page']}: {s['SubjectCode']} → \"{s['Replacecode_raw']}\"")
