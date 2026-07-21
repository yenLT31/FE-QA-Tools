import io
import re

import numpy as np
import pandas as pd
import pdfplumber

try:
    import cv2
except ImportError:
    cv2 = None


OCR_RESOLUTION = 180
OCR_HEADERS = ["STT", "Mã SV", "Họ và tên", "Ngành học", "Lý do", "Cơ sở"]
_ocr_engine = None


def require_opencv():
    if cv2 is None:
        raise RuntimeError(
            "PDF dạng ảnh cần OpenCV. Hãy cài dependencies bằng: "
            "pip install -r requirements.txt"
        )


def normalize_mssv(value):
    return re.sub(r"[^A-Z0-9]", "", str(value).upper())


def get_ocr_engine():
    global _ocr_engine
    require_opencv()
    if _ocr_engine is None:
        try:
            from rapidocr import RapidOCR
        except ImportError as exc:
            raise RuntimeError(
                "PDF dạng ảnh cần OCR. Hãy cài: "
                "pip install rapidocr onnxruntime opencv-python"
            ) from exc
        _ocr_engine = RapidOCR()
    return _ocr_engine


def group_line_positions(indices):
    groups = []
    for value in indices:
        value = int(value)
        if not groups or value > groups[-1][-1] + 1:
            groups.append([value])
        else:
            groups[-1].append(value)
    return [round(sum(group) / len(group)) for group in groups]


def detect_table_grid(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    binary = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )[1]
    height, width = binary.shape

    horizontal = cv2.morphologyEx(
        binary,
        cv2.MORPH_OPEN,
        cv2.getStructuringElement(cv2.MORPH_RECT, (max(60, width // 15), 1)),
    )
    vertical = cv2.morphologyEx(
        binary,
        cv2.MORPH_OPEN,
        cv2.getStructuringElement(cv2.MORPH_RECT, (1, max(25, height // 60))),
    )

    y_indices = np.where((horizontal > 0).sum(axis=1) > width * 0.25)[0]
    x_indices = np.where((vertical > 0).sum(axis=0) > height * 0.03)[0]
    x_lines = group_line_positions(x_indices)
    x_lines = [x for x in x_lines if width * 0.03 < x < width * 0.97]
    return x_lines, group_line_positions(y_indices)


def detect_mssv_row_bounds(image, x1, x2):
    column = image[:, x1 + 3:x2 - 3]
    gray = cv2.cvtColor(column, cv2.COLOR_RGB2GRAY)
    binary = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )[1]

    horizontal_lines = cv2.morphologyEx(
        binary,
        cv2.MORPH_OPEN,
        cv2.getStructuringElement(
            cv2.MORPH_RECT, (max(30, binary.shape[1] // 2), 1)
        ),
    )
    text_only = cv2.subtract(binary, horizontal_lines)
    row_indices = np.where(
        (text_only > 0).sum(axis=1) > max(2, binary.shape[1] * 0.02)
    )[0]

    groups = []
    for value in row_indices:
        value = int(value)
        if not groups or value > groups[-1][-1] + 2:
            groups.append([value])
        else:
            groups[-1].append(value)

    bands = [
        (group[0], group[-1])
        for group in groups
        if 5 <= group[-1] - group[0] + 1 <= 40
    ]
    if len(bands) < 2:
        return []

    centers = [(start + end) // 2 for start, end in bands]
    typical_gap = int(np.median(np.diff(centers)))
    half_height = max(12, min(35, int(typical_gap * 0.45)))
    image_height = image.shape[0]
    return [
        (max(0, center - half_height), min(image_height, center + half_height))
        for center in centers
    ]


def find_matching_target(recognized, targets):
    normalized = normalize_mssv(recognized)
    if normalized in targets:
        return targets[normalized]

    # Chỉ sửa các lỗi OCR đã biết ở KÝ TỰ CHỮ (không đụng tới phần số),
    # ví dụ "1I"/"II" bị đọc nhầm từ "H".
    variants = {normalized}
    if normalized.startswith(("1I", "II")):
        variants.add("H" + normalized[2:])
    if (
        len(normalized) >= 3
        and normalized[0] == "H"
        and normalized[1] == "I"
        and normalized[2].isalpha()
    ):
        variants.add("H" + normalized[2:])

    for variant in variants:
        if variant in targets:
            return targets[variant]

    # KHÔNG dùng fuzzy edit-distance: HS163275 và HS163285 chỉ khác 1 ký tự
    # nhưng là hai MSSV khác nhau, không phải lỗi OCR. Chỉ chấp nhận khớp
    # chính xác để tránh gán nhầm sinh viên khác.
    return None


def recognize_cell(image, x1, y1, x2, y2):
    margin = 3
    cell = image[y1 + margin:y2 - margin, x1 + margin:x2 - margin]
    if cell.size == 0:
        return ""

    cell = cv2.copyMakeBorder(
        cell, 8, 8, 8, 8, cv2.BORDER_CONSTANT, value=(255, 255, 255)
    )
    cell = cv2.resize(cell, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    result = get_ocr_engine()(
        cell, use_det=False, use_cls=False, use_rec=True
    )
    return result.txts[0].strip() if result.txts else ""


def search_mssv_in_scanned_page(page, targets):
    require_opencv()
    pil_image = page.to_image(resolution=OCR_RESOLUTION).original.convert("RGB")
    image = np.asarray(pil_image)
    x_lines, _ = detect_table_grid(image)

    # Mẫu quyết định có cột STT đứng ngay trước cột Mã SV.
    if len(x_lines) < 3:
        return []

    hits = []
    row_bounds = detect_mssv_row_bounds(image, x_lines[1], x_lines[2])
    for y1, y2 in row_bounds:
        recognized_mssv = recognize_cell(
            image, x_lines[1], y1, x_lines[2], y2
        )
        matched_mssv = find_matching_target(recognized_mssv, targets)
        if matched_mssv is None:
            continue

        row_dict = {}
        for index, (x1, x2) in enumerate(zip(x_lines, x_lines[1:])):
            header = (
                OCR_HEADERS[index]
                if index < len(OCR_HEADERS)
                else f"Col_{index}"
            )
            value = (
                matched_mssv
                if index == 1
                else recognize_cell(image, x1, y1, x2, y2)
            )
            row_dict[header] = value

        hits.append({
            "mssv": matched_mssv,
            "row_dict": row_dict,
        })
    return hits


def detect_mssv_col(columns):
    keywords = [
        "mssv", "ma_sv", "masv", "mã sv", "mã số sinh viên",
        "student_id", "studentid", "ma so sinh vien",
    ]
    for index, column in enumerate(columns):
        column_lower = str(column).lower().strip()
        for keyword in keywords:
            if keyword in column_lower:
                return index
    return -1


def search_mssv_in_pdfs(mssv_list, pdf_data_list):
    results = {}
    errors = []
    targets = {}

    for mssv in mssv_list:
        ms = mssv.strip()
        results[ms] = {"found": False, "hits": []}
        if ms:
            targets[normalize_mssv(ms)] = ms

    for pdf_item in pdf_data_list:
        fname = pdf_item["name"]
        try:
            with pdfplumber.open(io.BytesIO(pdf_item["bytes"])) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    tables = page.extract_tables()
                    has_searchable_text = bool(
                        (page.extract_text() or "").strip()
                    )

                    for table in tables:
                        if not table:
                            continue
                        header = table[0] if table[0] else []
                        for row in table[1:]:
                            row_text = " ".join(
                                str(cell) for cell in row if cell
                            )
                            normalized_row = normalize_mssv(row_text)
                            for normalized, ms in targets.items():
                                if normalized and normalized in normalized_row:
                                    row_dict = {}
                                    for column_index, cell in enumerate(row):
                                        column_name = (
                                            header[column_index]
                                            if (
                                                column_index < len(header)
                                                and header[column_index]
                                            )
                                            else f"Col_{column_index}"
                                        )
                                        row_dict[str(column_name)] = cell
                                    results[ms]["found"] = True
                                    results[ms]["hits"].append({
                                        "file": fname,
                                        "page": page_num,
                                        "row_dict": row_dict,
                                    })

                    if not has_searchable_text:
                        for hit in search_mssv_in_scanned_page(page, targets):
                            ms = hit["mssv"]
                            results[ms]["found"] = True
                            results[ms]["hits"].append({
                                "file": fname,
                                "page": page_num,
                                "row_dict": hit["row_dict"],
                            })
        except Exception as exc:
            errors.append({"file": fname, "error": str(exc)})

    results["_errors"] = errors
    return results


def build_export_data(mssv_list, results):
    summary_rows = []
    detail_rows = []

    for mssv in mssv_list:
        ms = mssv.strip()
        info = results.get(ms, {"found": False, "hits": []})

        if info["found"]:
            files = sorted(set(hit["file"] for hit in info["hits"]))
            summary_rows.append({
                "MSSV": ms,
                "Tìm thấy": "Có",
                "Số QĐ": len(files),
                "Danh sách QĐ": ", ".join(files),
            })
            for hit in info["hits"]:
                row = {
                    "MSSV": ms,
                    "Tên QĐ": hit["file"],
                    "Trang": hit["page"],
                }
                row.update(hit.get("row_dict", {}))
                detail_rows.append(row)
        else:
            summary_rows.append({
                "MSSV": ms,
                "Tìm thấy": "Không",
                "Số QĐ": 0,
                "Danh sách QĐ": "",
            })
            detail_rows.append({
                "MSSV": ms,
                "Tên QĐ": "Không tìm thấy",
                "Trang": "",
            })

    return pd.DataFrame(summary_rows), pd.DataFrame(detail_rows)


def to_excel_bytes(df_summary, df_detail):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_summary.to_excel(writer, index=False, sheet_name="Tổng hợp")
        df_detail.to_excel(writer, index=False, sheet_name="Chi tiết")
    return output.getvalue()
