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


def _is_code_or_combo(s):
    """
    Hop le neu la 1 ma don (IOT102) HOAC 1 to hop 'A+B[+...]' ma moi phan
    deu la ma hop le (vd 'MAD111+MAD121', 'MAD101+AIH301m').
    Dung de KHONG bo qua cac o to hop, va giu nguyen ca cum (khong tach).
    """
    s = s.strip()
    if is_valid_subject_code(s):
        return True
    parts = [p.strip() for p in s.split('+')]
    return len(parts) >= 2 and all(is_valid_subject_code(p) for p in parts)


def _normalize(s):
    """
    Chuan hoa chuoi: lower + thay MOI loai khoang trang (xuong dong, tab,
    nhieu space) bang DUNG MOT space, roi strip.
    Dam bao "Tương \\nđương", "Tương  đương", "Tương\\nđương" deu thanh
    "tương đương" -> phep kiem 'tương đương' in ... khong bi truot.
    """
    if s is None:
        return ""
    return re.sub(r'\s+', ' ', str(s).lower()).strip()


def _extract_effective_date(pdf, so_qd=None):
    """
    Lay NGAY SOAN THAO VAN BAN (= ngay hieu luc) tu noi dung PDF.

    Truong hop thuong: "Ha Noi, ngay 16 thang 12 nam 2025".

    Truong hop mau ky so co PLACEHOLDER: cong cu ky CHEN cac chu so XEN KE
    vao placeholder, vd "ngay k0e3yd thang k5eymnam 2024" (k0e3yd = keyd + "03",
    k5eym = keym + "5"). => Lay token ngay/thang roi RUT CHU SO ra khoi token.
    Cach nay dung cho ca file thuong lan file placeholder.

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
            d   = re.sub(r'\D', '', m.group(1))   # rut chu so tu token ngay
            mth = re.sub(r'\D', '', m.group(2))   # rut chu so tu token thang
            y   = m.group(3)
            if d and mth and 1 <= int(d) <= 31 and 1 <= int(mth) <= 12:
                return f"{int(d):02d}/{int(mth):02d}/{y}"
    return ""


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

def _clean_code_cell(v):
    """
    Lam sach o chua MA mon (SubjectCode / Replacecode).

    PDF cot hep ngat dong giua chuoi -> pdfplumber chen '\\n'. Co 2 kieu:
      (a) Ngat GIUA mot token  : 'C\\nSI102'->'CSI102', 'ITA203\\nc'->'ITA203c'
      (b) Liet ke NHIEU ma     : 'SAL301/\\nIBC201/\\nIBI101', 'A\\nhoặc\\nB'

    Xu ly:
      - "hoặc"/"và" -> '/' (thanh dau tach de tach thanh nhieu ma o buoc sau).
      - Voi moi '\\n': NOI LIEN neu mot ben la manh vo (token khong phai ma hop le)
        -> han gan token bi cat; nguoc lai (hai ben deu la ma hop le) -> dung '/'.
    """
    if v is None:
        return ""
    s = str(v)
    # "hoặc"/"và" -> '/'. Cho phep ma sau DINH LIEN (vd "hoặcCPV301"):
    # bat dau bang word-boundary truoc, theo sau la 1 chu/so (lookahead) thay vi \b sau.
    s = re.sub(r'[\s\n]*\b(hoặc|hoăc|và)\s*(?=[A-Za-z0-9])', '/', s, flags=re.IGNORECASE)

    frags = [f.strip() for f in s.split('\n') if f.strip()]
    if not frags:
        return ""

    result = frags[0]
    for f in frags[1:]:
        prev_tail = re.split(r'[,/ ]', result)[-1]   # token cuoi cua phan da gop
        cur_head  = re.split(r'[,/ ]', f)[0]          # token dau cua manh moi
        if is_valid_subject_code(prev_tail) and is_valid_subject_code(cur_head):
            result = result + '/' + f                 # hai ma hoan chinh -> tach
        else:
            result = result + f                       # noi lien (han token bi cat)

    result = re.sub(r'[ \t]{2,}', ' ', result).strip()
    # Tho gon khoang trang quanh '+' (giu to hop dang "A+B")
    result = re.sub(r'\s*\+\s*', '+', result)

    # Tach ma ngan nhau bang DAU CACH: neu tat ca token deu la ma hop le -> noi '/'
    # (vd "CHI111 CHI121" -> "CHI111/CHI121"). Cell mo ta (co tu thuong/khong phai
    # ma) se khong thoa -> giu nguyen.
    parts = result.split(' ')
    if len(parts) >= 2 and all(is_valid_subject_code(p) for p in parts):
        result = '/'.join(parts)

    return result


def extract_from_pdf(pdf_source, so_qd="Unknown"):
    """
    Trich xuat du lieu mon tuong duong tu PDF.

    Args:
        pdf_source : duong dan file (str) hoac bytes / BytesIO
        so_qd      : so quyet dinh

    Returns:
        (data_rows, skipped_rows)

    Moi dong data co them truong "effective_date" = ngay soan thao VB.
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
        # ── Lay ngay hieu luc (1 lan cho ca van ban) ────────────────────
        effective_date = _extract_effective_date(pdf, so_qd)

        for page_num, page in enumerate(pdf.pages, 1):
            raw_table = page.extract_table({
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines"
            })
            if not raw_table:
                continue

            # ── BUOC 1: Gop dong tiep noi truoc khi parse ────────────────
            table = _merge_continuation_rows(raw_table)

            # Chuan hoa Unicode NFC: PDF co the ma hoa tieng Viet kieu to hop
            # (vd "ặ" = ă + dau nang roi U+0323). NFC dua ve dang dung san de
            # moi phep so chuoi tieng Viet ("hoặc", "tương đương"...) khop dung.
            table = [[unicodedata.normalize('NFC', str(c)) if c is not None else c
                      for c in row] for row in table]

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

                # Cot co dinh (lam sach \n ngat dong giua ma)
                subject_raw = _clean_code_cell(row[1]) if row[1] else ""
                replace_raw = _clean_code_cell(row[2]) if len(row) > 2 and row[2] else ""

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

                # Bo qua neu Replacecode la mo ta van ban (chap nhan ca to hop A+B)
                first_code = replace_raw.split(',')[0].split('/')[0].strip()
                if not replace_raw or not _is_code_or_combo(first_code):
                    if subject_raw and replace_raw:
                        skipped_rows.append({
                            "page"           : page_num,
                            "SubjectCode"    : subject_raw,
                            "Replacecode_raw": replace_raw,
                            "ly_do"          : "Replacecode khong phai ma mon"
                        })
                    continue

                # Logic equivalent:
                #  - Uu tien o Hinh thuc: co "tương đương" -> TRUE; co "thay thế" -> FALSE.
                #  - Neu o Hinh thuc KHONG co chu nao (nhan dien hut), quet ca dong;
                #    uu tien "thay thế" de tranh bat nham "tương đương" trong ghi chu.
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
                        equivalent = "FALSE"   # khong xac dinh duoc -> mac dinh FALSE
                note = f"{so_qd} {chu_y}".strip()

                # Xu ly nhieu SubjectCode trong 1 o (tach , / xuong dong,
                # NHUNG khong tach '+': giu nguyen ca to hop "A+B")
                for sc in re.split(r'[,/\n]+', subject_raw):
                    sc = sc.strip()
                    if sc and _is_code_or_combo(sc):
                        data_rows.append({
                            "SubjectCode"   : sc,
                            "Replacecode"   : replace_raw,
                            "CurriculumCode": curriculum,
                            "Replace"       : "TRUE",
                            "Equivalent"    : equivalent,
                            "replace_status": "applied",
                            "note"          : note,
                            "no"            : so_qd,
                            "effective_date": effective_date
                        })

    return data_rows, skipped_rows


def _canon_curriculum(v):
    """
    Chuan hoa CurriculumCode de so khop on dinh.
    Bo NaN/rong, lower, gop khoang trang, tach theo , / va khoang trang,
    sap xep roi ghep lai bang ','.
    => "BCS, BIA, BSE, BIT" == "bcs bia bse bit" == "bia,bcs,bit,bse".
    """
    s = "" if v is None else str(v).strip()
    if s.lower() in ("nan", ""):
        return ""
    s = s.lower().replace("\n", " ")
    toks = [t for t in re.split(r"[\s,/]+", s) if t]
    return ",".join(sorted(toks))


def _canon_equivalent(v):
    """Chuan hoa Equivalent: True/'TRUE'/1 -> 'T'; False/'FALSE'/0 -> 'F'; con lai -> ''."""
    s = str(v).strip().lower()
    if s in ("true", "1"):
        return "T"
    if s in ("false", "0"):
        return "F"
    return ""


def _record_key(sc, rc, cur, eq):
    """
    Khoa nhan dang 1 ban ghi = (SubjectCode, Replacecode, CurriculumCode, Equivalent),
    da chuan hoa CurriculumCode va Equivalent.
    """
    return (str(sc).strip(), str(rc).strip(),
            _canon_curriculum(cur), _canon_equivalent(eq))


def merge_database(existing_df, new_rows):
    """
    Gop du lieu nhieu QD vao DB, dung de XAC DINH lai moi dong thuoc QD nao.

    Mo hinh "giu tat ca lich su":
      - Dinh danh 1 dong = (ban ghi 4 truong) + so QD ('no').
        => Mot ban ghi xuat hien o N QD se co N dong, moi QD 1 dong.
      - Voi moi QD nap vao: dam bao moi (ban ghi, QD) deu co dong; THIEU thi THEM,
        kem 'effective_date' cua QD do. Neu dong da ton tai (cung ban ghi + cung
        no) thi GHI DE lai effective_date theo PDF (PDF la nguon chuan).
      - Dong cu trong DB ma BAN GHI khong xuat hien o BAT KY QD nao da nap:
        GIU NGUYEN, va danh dau o cot 'review' = "khong khop QD da nap" de ra tay.

    Luu y: nen nap TAT CA cac QD trong cung mot lan chay de cot 'review' chinh xac
    (vi 'review' tinh theo tap QD cua lan chay nay).
    """
    COLS = ["SubjectCode", "Replacecode", "CurriculumCode",
            "Replace", "Equivalent", "replace_status", "note", "no",
            "effective_date", "review"]

    if not new_rows:
        if existing_df is None:
            return pd.DataFrame(columns=COLS)
        out = existing_df.copy()
        for c in COLS:
            if c not in out.columns:
                out[c] = ""
        return out[COLS].reset_index(drop=True)

    new_df = pd.DataFrame(new_rows)

    # Tap ban ghi (khoa 4 truong) co trong CAC QD nap vao
    fed_keys = set()
    # Membership (khoa 4 truong, no) -> effective_date (PDF la nguon chuan)
    fed_member_date = {}
    for r in new_rows:
        key = _record_key(r.get("SubjectCode"), r.get("Replacecode"),
                          r.get("CurriculumCode"), r.get("Equivalent"))
        no  = str(r.get("no", "")).strip()
        fed_keys.add(key)
        fed_member_date[(key, no)] = str(r.get("effective_date", "")).strip()

    # DB rong -> tra thang new_df (review rong)
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
            # Dong khop dung QD trong PDF -> xac nhan, ghi de ngay theo PDF
            existing_df.at[idx, "effective_date"] = fed_member_date[(key, no)]
            existing_df.at[idx, "review"] = ""
        elif key in fed_keys:
            # Ban ghi co trong QD nao do, nhung 'no' cua dong nay khong phai QD do
            # -> giu nguyen, khong danh dau (ban ghi van duoc nhan dien)
            existing_df.at[idx, "review"] = ""
        else:
            # Ban ghi KHONG co o bat ky QD nao da nap -> giu nguyen + danh dau
            existing_df.at[idx, "review"] = "khong khop QD da nap"

    # Them cac (ban ghi, QD) con THIEU
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
# Tren Streamlit Cloud, page chay nhu __main__. KHONG doc thu muc input/ tren dia
# (gay FileNotFoundError); thay vao do nhan file qua st.file_uploader va xu ly
# trong bo nho. Cac ham loi o tren van import duoc ma khong can streamlit.
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
        # 1) Doc DB hien co (neu co)
        existing = None
        if db_file is not None:
            try:
                existing = pd.read_excel(db_file)
            except Exception as e:
                st.error(f"Không đọc được file Excel: {e}")
                st.stop()

        # 2) Trich xuat tung PDF (so QD lay tu ten file)
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
                summaries.append({
                    "File": pf.name, "Số QĐ": so_qd, "Ngày hiệu lực": ngay,
                    "Dòng trích": len(rows), "Bỏ qua": len(skipped),
                })

        if not all_rows:
            st.warning("Không trích được dòng dữ liệu nào từ các PDF đã nạp.")
            st.stop()

        # 3) Gop
        final = merge_database(existing, all_rows)

        before = 0 if existing is None else len(existing)
        st.success(f"Xong! DB: {before:,} → {len(final):,} dòng "
                   f"(thêm {len(final) - before:,}).")

        st.subheader("Tóm tắt từng QĐ")
        st.dataframe(pd.DataFrame(summaries), use_container_width=True, hide_index=True)

        if "review" in final.columns:
            flagged = int((final["review"] == "khong khop QD da nap").sum())
            if flagged:
                st.warning(f"⚠️ {flagged:,} dòng được đánh dấu **review** "
                           f"(bản ghi không khớp QĐ nào đã nạp). Nạp thêm QĐ để giảm con số này.")

        st.subheader("Xem trước (50 dòng đầu)")
        st.dataframe(final.head(50), use_container_width=True, hide_index=True)

        # 4) Tai ve
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
