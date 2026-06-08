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
    Chuan hoa chuoi: lower + thay MOI loai khoang trang (xuong dong, tab,
    nhieu space) bang DUNG MOT space, roi strip.
    Dam bao "Tương \\nđương", "Tương  đương", "Tương\\nđương" deu thanh
    "tương đương" -> phep kiem 'tương đương' in ... khong bi truot.
    """
    if s is None:
        return ""
    return re.sub(r'\s+', ' ', str(s).lower()).strip()


def _extract_effective_date(pdf):
    """
    Lay NGAY SOAN THAO VAN BAN (= ngay hieu luc) tu noi dung PDF.

    Trong van ban QD cua DHFPT, ngay nay nam o header trang dau,
    mau: "Ha Noi, ngay 16 thang 12 nam 2025"
    (va lap lai o header moi phu luc).

    Tra ve chuoi "DD/MM/YYYY", vd "16/12/2025". Neu khong tim thay -> "".
    Chi quet vai trang dau cho nhanh, lay lan khop dau tien.
    """
    pat = re.compile(
        r'ng[aà]y\s+(\d{1,2})\s+th[aá]ng\s+(\d{1,2})\s+n[aă]m\s+(\d{4})',
        re.IGNORECASE
    )
    for page in pdf.pages[:3]:
        txt = page.extract_text() or ""
        m = pat.search(txt)
        if m:
            d, mth, y = m.groups()
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
    # "hoặc"/"và" (kem khoang trang/xuong dong xung quanh) -> '/'
    s = re.sub(r'[\s\n]*\b(hoặc|và)\b[\s\n]*', '/', s, flags=re.IGNORECASE)

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

    return re.sub(r'[ \t]{2,}', ' ', result).strip()


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
        effective_date = _extract_effective_date(pdf)

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

                # Xu ly nhieu SubjectCode trong 1 o
                for sc in re.split(r'[,/\n]+', subject_raw):
                    sc = sc.strip()
                    if sc and is_valid_subject_code(sc):
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
            ngay = rows[0]["effective_date"] if rows else "?"
            print(f"   Trich xuat: {len(rows)} dong | Ngay hieu luc: {ngay}")
            if skipped:
                print(f"   Bo qua   : {len(skipped)} dong")

    if all_new_data:
        existing = pd.read_excel(OUTPUT_FILE) if os.path.exists(OUTPUT_FILE) else None
        final    = merge_database(existing, all_new_data)
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        final.to_excel(OUTPUT_FILE, index=False)
        print(f"\nDa luu {len(final)} dong vao {OUTPUT_FILE}")

    if all_skipped:
        print("\nCac dong bi bo qua:")
        for s in all_skipped:
            print(f"   Trang {s['page']}: {s['SubjectCode']} -> \"{s['Replacecode_raw']}\"")
