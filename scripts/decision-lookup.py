# scripts/decision-lookup.py
# ============================================================
#  LOGIC THUẦN — KHÔNG IMPORT STREAMLIT
# ============================================================
import pdfplumber
import pandas as pd
import re
import io


def detect_mssv_col(columns):
    """Trả về index cột MSSV, -1 nếu không tìm thấy."""
    keywords = ["mssv", "ma_sv", "masv", "mã sv", "mã số sinh viên",
                "student_id", "studentid", "ma so sinh vien"]
    for i, col in enumerate(columns):
        col_lower = str(col).lower().strip()
        for kw in keywords:
            if kw in col_lower:
                return i
    return -1


def search_mssv_in_pdfs(mssv_list, pdf_data_list):
    """
    mssv_list : list[str]
    pdf_data_list : list[dict]  — mỗi dict có {"name": str, "bytes": bytes}
    Returns : dict keyed by mssv  +  "_errors" key
    """
    results = {}
    errors = []

    for mssv in mssv_list:
        results[mssv.strip()] = {"found": False, "hits": []}

    for pdf_item in pdf_data_list:
        fname = pdf_item["name"]
        try:
            with pdfplumber.open(io.BytesIO(pdf_item["bytes"])) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    tables = page.extract_tables()
                    for table in tables:
                        if not table:
                            continue
                        header = table[0] if table[0] else []
                        for row in table[1:]:
                            row_text = " ".join(str(cell) for cell in row if cell)
                            for mssv in mssv_list:
                                ms = mssv.strip()
                                if ms and ms in row_text:
                                    row_dict = {}
                                    for ci, cell in enumerate(row):
                                        col_name = (header[ci]
                                                    if ci < len(header) and header[ci]
                                                    else f"Col_{ci}")
                                        row_dict[str(col_name)] = cell
                                    results[ms]["found"] = True
                                    results[ms]["hits"].append({
                                        "file": fname,
                                        "page": page_num,
                                        "row_dict": row_dict,
                                    })
        except Exception as e:
            errors.append({"file": fname, "error": str(e)})

    results["_errors"] = errors
    return results


def build_export_data(mssv_list, results):
    """
    Tạo 2 DataFrame: df_summary và df_detail.
    df_detail chứa TẤT CẢ cột từ PDF (row_dict).
    """
    summary_rows = []
    detail_rows = []

    for mssv in mssv_list:
        ms = mssv.strip()
        info = results.get(ms, {"found": False, "hits": []})

        if info["found"]:
            files = list(set(h["file"] for h in info["hits"]))
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
                # Thêm tất cả cột từ PDF
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

    df_summary = pd.DataFrame(summary_rows)
    df_detail = pd.DataFrame(detail_rows)
    return df_summary, df_detail


def to_excel_bytes(df_summary, df_detail):
    """Xuất 2 sheet ra bytes Excel."""
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine="openpyxl") as w:
        df_summary.to_excel(w, index=False, sheet_name="Tổng hợp")
        df_detail.to_excel(w, index=False, sheet_name="Chi tiết")
    return out.getvalue()
