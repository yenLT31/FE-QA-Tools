import pdfplumber
import pandas as pd
import re
import io
import os
import unicodedata


# ── Helpers ───────────────────────────────────────────────────────────────────

def is_valid_subject_code(s):
    """
    Kiem tra ma mon hop le.
    Hop le : IOT102, NWC303, SYB302c, PRU211m, AIL303m
    Khong hop le : "Thay the bang mon combo khac..."
    """
    s = s.strip()
    return bool(re.match(r'^[A-Za-z]{2,6}\d{2,4}[a-zA-Z]{0,2}$', s))


# Separator NHOM GOP (AND): '+', dau phay, chu "và".
# Cac ma noi voi nhau bang cac ky tu nay -> 1 to hop, giu chung 1 dong.
_COMBO_SEP = re.compile(r'\s*(?:\+|,|\bvà\b)\s*', re.IGNORECASE)


def _is_code_or_combo(s):
    """
    Hop le neu la 1 ma don (IOT102) HOAC 1 to hop ma moi phan deu la ma hop le.
    To hop co the noi bang '+', dau phay, chu "và", HOAC chi cach nhau bang dau cach
    (vd 'MAD111+MAD121', 'MAD101, MAD111', 'MAD101 và MAD111', 'CHI111 CHI121').
    Dung de KHONG bo qua cac o to hop, va giu nguyen ca cum (khong tach).
    """
    s = s.strip()
    if is_valid_subject_code(s):
        return True
    # tach theo separator gop ro rang HOAC dau cach
    parts = [p for p in re.split(r'\s*(?:\+|,|\bvà\b)\s*|\s+', s, flags=re.IGNORECASE) if p]
    return len(parts) >= 2 and all(is_valid_subject_code(p) for p in parts)


def _has_space_separated_codes(s):
    """
    True neu trong don vi co cac ma CHI cach nhau bang DAU CACH (khong co +, phay, "và").
    Day la truong hop MO HO: khong ro la gop hay chon -> can gan co canh bao.
    Vi du: 'CHI111 CHI121' -> True ; 'MAD101, MAD111' -> False ; 'MAD101+MAD111' -> False.
    """
    if not s:
        return False
    # Thay cac separator GOP ro rang bang '+' de loai chung ra, roi xem con dau cach khong
    norm = _COMBO_SEP.sub('+', s.strip())
    return bool(re.search(r'\S\s+\S', norm))


def _normalize(s):
    """
    Chuan hoa chuoi: lower + thay MOI loai khoang trang (xuong dong, tab,
    nhieu space) bang DUNG MOT space, roi strip.
    """
    if s is None:
        return ""
    return re.sub(r'\s+', ' ', str(s).lower()).strip()


def _extract_effective_date(pdf, so_qd=None):
    """
    Lay NGAY SOAN THAO VAN BAN (= ngay hieu luc) tu noi dung PDF.
    Tra ve "DD/MM/YYYY". Neu khong tim thay -> "".
    """
    pat = re.compile(
        r'ng[aà]y\s+(\S+?)\s+th[aá]ng\s+(\S+?)\s*n[aă]m\s+(\d{4})',
        re.IGNORECASE
    )
    for page in pdf.pages[:3]:
        txt = unicodedata.normalize('NFC', page.extract_text() or "")
        m = pat.search(txt)
        if m:
            d   = re.sub(r'\D', '', m.group(1))
            mth = re.sub(r'\D', '', m.group(2))
            y   = m.group(3)
            if d and mth and 1 <= int(d) <= 31 and 1 <= int(mth) <= 12:
                return f"{int(d):02d}/{int(mth):02d}/{y}"
    return ""


def _merge_continuation_rows(table):
    """
    Gop dong tiep noi (row[0] rong) vao dong chinh truoc do.
    """
    if not table:
        return []

    merged = []
    for row in table:
        if not row:
            continue

        cell_0 = str(row[0]).strip() if row[0] else ""

        if not cell_0 and merged:
            prev = merged[-1]
            while len(prev) < len(row):
                prev.append(None)
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
    Tim vi tri cot Hinh thuc (o chua 'tuong duong' hoac 'thay the').
    Mac dinh tra ve 4 neu khong tim thay.
    """
    for i in range(2, len(row)):
        val = _normalize(row[i])
        if "tương đương" in val or "thay thế" in val:
            return i
    return 4


# ── Lam sach o ma mon ─────────────────────────────────────────────────────────

def _clean_code_cell(v):
    """
    Lam sach o chua MA mon (SubjectCode / Replacecode), theo quy uoc:
      - Nhom CHON (OR)  : chu "hoặc" -> '/'  (se duoc TACH thanh nhieu dong sau).
      - Nhom GOP (AND)  : chu "và", dau phay ',', dau cong '+' -> GIU NGUYEN ky tu goc,
                          chi gon khoang trang (vd 'MAD101 và MAD111', 'MAD101, MAD111').
      - PDF cot hep ngat dong giua chuoi -> pdfplumber chen '\\n':
          (a) ngat GIUA mot token (manh vo)  -> NOI LIEN de han token bi cat;
          (b) ngat giua HAI ma hoan chinh     -> noi bang DAU CACH (se duoc gan co canh bao).
    """
    if v is None:
        return ""
    s = str(v)

    # Nhom CHON: "hoặc" -> '/' (cho phep ma sau dinh lien, vd "hoặcCPV301")
    s = re.sub(r'[\s\n]*\b(hoặc|hoăc)\s*(?=[A-Za-z0-9])', '/', s, flags=re.IGNORECASE)
    # Nhom GOP: giu chu "và", chuan hoa khoang trang/xuong dong quanh no thanh ' và '
    s = re.sub(r'[\s\n]*\bvà\b[\s\n]*(?=[A-Za-z0-9])', ' và ', s, flags=re.IGNORECASE)

    frags = [f.strip() for f in s.split('\n') if f.strip()]
    if not frags:
        return ""

    result = frags[0]
    for f in frags[1:]:
        prev_tail = re.split(r'[,/ ]', result)[-1]   # token cuoi cua phan da gop
        cur_head  = re.split(r'[,/ ]', f)[0]          # token dau cua manh moi
        if is_valid_subject_code(prev_tail) and is_valid_subject_code(cur_head):
            result = result + ' ' + f                 # hai ma hoan chinh -> noi bang dau cach
        else:
            result = result + f                       # noi lien (han token bi cat)

    # Gon khoang trang & cac separator GOP (GIU nguyen ky tu goc , va +)
    result = re.sub(r'\s*\+\s*', '+', result)     # gon quanh '+'
    result = re.sub(r'\s*,\s*', ', ', result)     # gon quanh ',' -> ', '
    result = re.sub(r'[ \t]{2,}', ' ', result).strip()

    return result


# ── Ham chinh ─────────────────────────────────────────────────────────────────

def extract_from_pdf(pdf_source, so_qd="Unknown"):
    """
    Trich xuat du lieu mon tuong duong tu PDF.

    Returns:
        (data_rows, skipped_rows)

    Moi dong data co them truong "effective_date" va "canh_bao".
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
        effective_date = _extract_effective_date(pdf, so_qd)

        for page_num, page in enumerate(pdf.pages, 1):
            raw_table = page.extract_table({
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines"
            })
            if not raw_table:
                continue

            table = _merge_continuation_rows(raw_table)
            table = [[unicodedata.normalize('NFC', str(c)) if c is not None else c
                      for c in row] for row in table]

            for row in table:
                if not row or len(row) < 5:
                    continue

                cell_0 = str(row[0]).strip() if row[0] else ""
                cell_1 = str(row[1]).strip() if row[1] else ""

                if any(kw in cell_0 for kw in ["TT", "STT"]):
                    continue
                if any(kw in cell_1 for kw in ["Mã", "học phần", "triển khai",
                                                "Ma", "hoc phan", "trien khai"]):
                    continue

                subject_raw = _clean_code_cell(row[1]) if row[1] else ""
                replace_raw = _clean_code_cell(row[2]) if len(row) > 2 and row[2] else ""

                if not subject_raw:
                    continue

                ht_idx = _find_hinh_thuc_idx(row)

                curriculum_parts = []
                for i in range(3, ht_idx):
                    if row[i] and str(row[i]).strip():
                        part = str(row[i]).strip().replace('\n', ' ')
                        curriculum_parts.append(part)
                curriculum = ", ".join(curriculum_parts)

                hinh_thuc = _normalize(row[ht_idx]) if len(row) > ht_idx else ""
                chu_y = ""
                if len(row) > ht_idx + 2 and row[ht_idx + 2]:
                    chu_y = str(row[ht_idx + 2]).strip().replace('\n', ' ')

                # Bo qua neu Replacecode la mo ta van ban (xet alternative dau tien)
                first_alt = replace_raw.split('/')[0].strip()
                if not replace_raw or not _is_code_or_combo(first_alt):
                    if subject_raw and replace_raw:
                        skipped_rows.append({
                            "page"           : page_num,
                            "SubjectCode"    : subject_raw,
                            "Replacecode_raw": replace_raw,
                            "ly_do"          : "Replacecode khong phai ma mon"
                        })
                    continue

                # Logic equivalent
                if "tương đương" in hinh_thuc:
                    equivalent = "TRUE"
                elif "thay thế" in hinh_thuc:
                    equivalent = "FALSE"
                else:
                    row_text = " ".join(_normalize(c) for c in row if c)
                    if "thay thế" in row_text:
                        equivalent = "FALSE"
                    elif "tương đương" in row_text:
                        equivalent = "TRUE"
                    else:
                        equivalent = "FALSE"
                note = f"{so_qd} {chu_y}".strip()

                # Co canh bao cho Replacecode (mo ho dau cach)?
                warn_rc = _has_space_separated_codes(replace_raw)

                # Tach SubjectCode: CHI tach theo '/' (OR) va xuong dong.
                # KHONG tach ',' '+' 'và' (nhom GOP) -> to hop giu nguyen 1 dong.
                for sc in re.split(r'[/\n]+', subject_raw):
                    sc = sc.strip()
                    if not sc or not _is_code_or_combo(sc):
                        continue
                    # Co canh bao neu SubjectCode HOAC Replacecode mo ho dau cach
                    warn = _has_space_separated_codes(sc) or warn_rc
                    canh_bao = "ma cach nhau bang dau cach - can kiem tra gop/chon" if warn else ""
                    data_rows.append({
                        "SubjectCode"   : sc,
                        "Replacecode"   : replace_raw,
                        "CurriculumCode": curriculum,
                        "Replace"       : "TRUE",
                        "Equivalent"    : equivalent,
                        "replace_status": "applied",
                        "note"          : note,
                        "no"            : so_qd,
                        "effective_date": effective_date,
                        "canh_bao"      : canh_bao
                    })

    return data_rows, skipped_rows


def _canon_curriculum(v):
    """
    Chuan hoa CurriculumCode de so khop on dinh.
    """
    s = "" if v is None else str(v).strip()
    if s.lower() in ("nan", ""):
        return ""
    s = s.lower().replace("\n", " ")
    toks = [t for t in re.split(r"[\s,/]+", s) if t]
    return ",".join(sorted(toks))


def _canon_equivalent(v):
    """Chuan hoa Equivalent: True -> 'T'; False -> 'F'; con lai -> ''."""
    s = str(v).strip().lower()
    if s in ("true", "1"):
        return "T"
    if s in ("false", "0"):
        return "F"
    return ""


def _record_key(sc, rc, cur, eq):
    """
    Khoa nhan dang 1 ban ghi = (SubjectCode, Replacecode, CurriculumCode, Equivalent).
    SubjectCode/Replacecode so theo CHUOI GOC (khong chuan hoa) theo yeu cau.
    """
    return (str(sc).strip(), str(rc).strip(),
            _canon_curriculum(cur), _canon_equivalent(eq))


def merge_database(existing_df, new_rows):
    """
    Gop du lieu nhieu QD vao DB, xac dinh lai moi dong thuoc QD nao.
    Mo hinh "giu tat ca lich su" (chi tiet xem ban goc).
    """
    COLS = ["SubjectCode", "Replacecode", "CurriculumCode",
            "Replace", "Equivalent", "replace_status", "note", "no",
            "effective_date", "canh_bao", "review"]

    if not new_rows:
        if existing_df is None:
            return pd.DataFrame(columns=COLS)
        out = existing_df.copy()
        for c in COLS:
            if c not in out.columns:
                out[c] = ""
        return out[COLS].reset_index(drop=True)

    new_df = pd.DataFrame(new_rows)

    fed_keys = set()
    fed_member_date = {}
    for r in new_rows:
        key = _record_key(r.get("SubjectCode"), r.get("Replacecode"),
                          r.get("CurriculumCode"), r.get("Equivalent"))
        no  = str(r.get("no", "")).strip()
        fed_keys.add(key)
        fed_member_date[(key, no)] = str(r.get("effective_date", "")).strip()

    if existing_df is None or existing_df.empty:
        for c in COLS:
            if c not in new_df.columns:
                new_df[c] = ""
        return new_df[COLS].reset_index(drop=True)

    existing_df = existing_df.copy()
    for c in COLS:
        if c not in existing_df.columns:
            existing_df[c] = ""

    existing_members = set()
    for idx, row in existing_df.iterrows():
        key = _record_key(row.get("SubjectCode"), row.get("Replacecode"),
                          row.get("CurriculumCode"), row.get("Equivalent"))
        no  = str(row.get("no", "")).strip()
        existing_members.add((key, no))

        if (key, no) in fed_member_date:
            existing_df.at[idx, "effective_date"] = fed_member_date[(key, no)]
            existing_df.at[idx, "review"] = ""
        elif key in fed_keys:
            existing_df.at[idx, "review"] = ""
        else:
            existing_df.at[idx, "review"] = "khong khop QD da nap"

    rows_to_add = []
    for _, nr in new_df.iterrows():
        key = _record_key(nr.get("SubjectCode"), nr.get("Replacecode"),
                          nr.get("CurriculumCode"), nr.get("Equivalent"))
        no  = str(nr.get("no", "")).strip()
        if (key, no) not in existing_members:
            row = nr.to_dict()
            row["review"] = ""
            rows_to_add.append(row)
            existing_members.add((key, no))

    if rows_to_add:
        add_df = pd.DataFrame(rows_to_add)
        result = pd.concat([existing_df, add_df], ignore_index=True)
    else:
        result = existing_df

    return result[COLS].reset_index(drop=True)


# ── Giao dien Streamlit ───────────────────────────────────────────────────────
if __name__ == "__main__":
    import streamlit as st

    st.set_page_config(page_title="Replacecode Manager", page_icon="📄", layout="wide")
    st.title("📄 Replacecode Manager")
    st.caption("Gộp các Quyết định (PDF) môn tương đương/thay thế vào DB, "
               "xác định mỗi dòng thuộc QĐ nào và ngày hiệu lực.")

    col1, col2 = st.columns(2)
    with col1:
        db_file = st.file_uploader(
            "DB Excel hiện có (.xlsx) — để trống nếu tạo mới", type=["xlsx"])
    with col2:
        pdf_files = st.file_uploader(
            "Các file PDF Quyết định (chọn nhiều cùng lúc)",
            type=["pdf"], accept_multiple_files=True)

    st.info("Mẹo: nạp **tất cả** các QĐ trong một lần để cột `review` "
            "(đánh dấu dòng không khớp QĐ nào) phản ánh đúng.")

    run = st.button("🔄 Gộp dữ liệu", type="primary",
                    disabled=not pdf_files)

    if run:
        existing = None
        if db_file is not None:
            try:
                existing = pd.read_excel(db_file)
            except Exception as e:
                st.error(f"Không đọc được file Excel: {e}")
                st.stop()

        all_rows, all_skipped, summaries = [], [], []
        with st.spinner("Đang đọc các file PDF..."):
            for pf in pdf_files:
                mt = re.search(r'\d+', pf.name)
                so_qd = mt.group() if mt else "Unknown"
                try:
                    rows, skipped = extract_from_pdf(pf.getvalue(), so_qd=so_qd)
                except Exception as e:
                    st.error(f"Lỗi đọc {pf.name}: {e}")
                    continue
                all_rows.extend(rows)
                all_skipped.extend(skipped)
                ngay = rows[0]["effective_date"] if rows else "?"
                warn_n = sum(1 for r in rows if r.get("canh_bao"))
                summaries.append({
                    "File": pf.name, "Số QĐ": so_qd, "Ngày hiệu lực": ngay,
                    "Dòng trích": len(rows), "Cảnh báo": warn_n, "Bỏ qua": len(skipped),
                })

        if not all_rows:
            st.warning("Không trích được dòng dữ liệu nào từ các PDF đã nạp.")
            st.stop()

        final = merge_database(existing, all_rows)

        before = 0 if existing is None else len(existing)
        st.success(f"Xong! DB: {before:,} → {len(final):,} dòng "
                   f"(thêm {len(final) - before:,}).")

        st.subheader("Tóm tắt từng QĐ")
        st.dataframe(pd.DataFrame(summaries), use_container_width=True, hide_index=True)

        if "canh_bao" in final.columns:
            warned = int((final["canh_bao"] != "").sum())
            if warned:
                st.warning(f"⚠️ {warned:,} dòng có **cảnh báo** (mã cách nhau bằng dấu cách "
                           f"— chưa rõ là gộp hay chọn). Hãy rà các dòng có cột `canh_bao`.")

        if "review" in final.columns:
            flagged = int((final["review"] == "khong khop QD da nap").sum())
            if flagged:
                st.warning(f"⚠️ {flagged:,} dòng được đánh dấu **review** "
                           f"(bản ghi không khớp QĐ nào đã nạp). Nạp thêm QĐ để giảm con số này.")

        st.subheader("Xem trước (50 dòng đầu)")
        st.dataframe(final.head(50), use_container_width=True, hide_index=True)

        buf = io.BytesIO()
        final.to_excel(buf, index=False)
        buf.seek(0)
        st.download_button(
            "⬇️ Tải DB đã cập nhật (.xlsx)", data=buf.getvalue(),
            file_name="Database_Tong_Hop_da_cap_nhat.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        if all_skipped:
            with st.expander(f"Các dòng bị bỏ qua khi đọc PDF ({len(all_skipped)})"):
                st.dataframe(pd.DataFrame(all_skipped), use_container_width=True,
                             hide_index=True)
