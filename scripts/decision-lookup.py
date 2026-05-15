"""
pages/decision-lookup.py
Giao diện Streamlit — Decision Lookup 🔍
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import importlib.util

# ---------------------------------------------------------------------------
# Import script logic
# ---------------------------------------------------------------------------
def load_script():
    script_path = Path(__file__).parent.parent / 'scripts' / 'decision-lookup.py'
    spec = importlib.util.spec_from_file_location('decision_lookup', script_path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

dl = load_script()

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(page_title='Decision Lookup', page_icon='🔍', layout='wide')

# ---------------------------------------------------------------------------
# Session defaults
# ---------------------------------------------------------------------------
for key, val in {
    'dl_theme'      : 'light',
    'dl_results'    : None,
    'dl_mssv_list'  : None,
    'dl_show_results': False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

is_dark = st.session_state['dl_theme'] == 'dark'

# Color tokens
bg      = '#0f172a' if is_dark else '#f8fafc'
surface = '#1e293b' if is_dark else '#ffffff'
border  = '#334155' if is_dark else '#e2e8f0'
text    = '#f1f5f9' if is_dark else '#0f172a'
muted   = '#94a3b8' if is_dark else '#64748b'

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
st.markdown(f"""
<style>
.stApp {{ background-color: {bg} !important; }}
.block-container {{ padding-top: 2rem; padding-bottom: 3rem; max-width: 1100px; }}
section[data-testid="stSidebar"] > div {{
    background-color: {surface} !important;
    border-right: 1px solid {border};
}}

.step-badge {{
    display:inline-flex;align-items:center;justify-content:center;
    width:36px;height:36px;background:#10b981;color:white;
    font-size:13px;font-weight:700;border-radius:8px;
    margin-right:12px;flex-shrink:0;
}}
.step-header {{ display:flex;align-items:center;margin-bottom:4px;margin-top:8px; }}
.step-header h3 {{ margin:0;font-size:18px;font-weight:700; }}
.step-sub {{ color:{muted};font-size:13px;margin-left:48px;margin-bottom:16px; }}
.step-divider {{ border:none;border-top:1px solid {border};margin:24px 0; }}

.stat-row {{ display:flex;gap:12px;margin:16px 0;flex-wrap:wrap; }}
.stat-card {{
    background:{surface};border:1px solid {border};
    border-radius:10px;padding:14px 20px;min-width:130px;flex:1;
}}
.stat-card .val {{ font-size:28px;font-weight:800;color:#10b981;line-height:1; }}
.stat-card .val.red  {{ color:#ef4444; }}
.stat-card .val.gray {{ color:{muted}; }}
.stat-card .lbl {{ font-size:12px;color:{muted};margin-top:4px; }}

.sb-label {{
    font-size:11px;font-weight:700;letter-spacing:.8px;
    text-transform:uppercase;color:{muted};margin-bottom:6px;margin-top:16px;
}}
.col-label {{
    font-size:11px;font-weight:700;letter-spacing:.6px;
    text-transform:uppercase;color:{muted};margin-bottom:6px;
}}

div[data-testid="stButton"] > button {{ border-radius:8px !important;font-weight:600 !important; }}
div[data-testid="stButton"] > button[kind="primary"] {{
    background-color:#10b981 !important;border:none !important;color:white !important;
}}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div style="font-size:18px;font-weight:800">🔍 Decision Lookup</div>', unsafe_allow_html=True)
    st.caption('Tra cứu MSSV trong các Quyết định PDF')
    st.divider()

    st.markdown('<div class="sb-label">GIAO DIỆN</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button('☀️ Sáng', use_container_width=True,
                     type='primary' if not is_dark else 'secondary'):
            st.session_state['dl_theme'] = 'light'
            st.rerun()
    with c2:
        if st.button('🌙 Tối', use_container_width=True,
                     type='primary' if is_dark else 'secondary'):
            st.session_state['dl_theme'] = 'dark'
            st.rerun()

    st.divider()
    st.markdown('<div class="sb-label">CÔNG CỤ</div>', unsafe_allow_html=True)
    debug_mode      = st.checkbox('🛠 Debug pdfplumber', value=False)
    show_all_tables = st.checkbox('📋 Hiện tất cả bảng', value=False)

    # Nút quay lại (chỉ hiện khi đang xem kết quả)
    if st.session_state['dl_show_results']:
        st.divider()
        if st.button('← Tra cứu mới', use_container_width=True):
            st.session_state['dl_show_results'] = False
            st.rerun()

    st.divider()
    st.markdown('<div class="sb-label">HƯỚNG DẪN</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:12px;color:{muted};line-height:2">1. Upload file Excel MSSV<br>2. Upload file PDF QĐ<br>3. Nhấn <b>Bắt đầu tra cứu</b><br>4. Xem bảng kết quả & xuất Excel</div>', unsafe_allow_html=True)


# ===========================================================================
# MÀN 1 — UPLOAD & CẤU HÌNH
# ===========================================================================
if not st.session_state['dl_show_results']:

    st.markdown('<h2 style="margin-bottom:4px">🔍 Decision Lookup</h2>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:{muted};margin-top:0;margin-bottom:28px">Kiểm tra MSSV có xuất hiện trong các Quyết định PDF và trả về vị trí chính xác</p>', unsafe_allow_html=True)

    # ── Bước 01 — Upload ──
    st.markdown("""
    <div class="step-header"><span class="step-badge">01</span><h3>Tải lên file</h3></div>
    <div class="step-sub">Upload file danh sách MSSV và các file Quyết định PDF</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.4])
    with col1:
        st.markdown('<div class="col-label">📄 FILE EXCEL — DANH SÁCH MSSV</div>', unsafe_allow_html=True)
        sv_file = st.file_uploader('sv', type=['xlsx', 'xls'], key='sv_upload', label_visibility='collapsed')
    with col2:
        st.markdown('<div class="col-label">📁 FILE PDF QUYẾT ĐỊNH</div>', unsafe_allow_html=True)
        qd_files = st.file_uploader('qd', type=['pdf'], accept_multiple_files=True,
                                    key='qd_upload', label_visibility='collapsed')

    # ── Bước 02 — Chọn cột MSSV ──
    mssv_list   = []
    mssv_col_ok = False

    if sv_file:
        st.markdown('<hr class="step-divider">', unsafe_allow_html=True)
        st.markdown("""
        <div class="step-header"><span class="step-badge">02</span><h3>Xác nhận cột MSSV</h3></div>
        <div class="step-sub">Chọn đúng cột chứa MSSV / RollNumber trong file Excel</div>
        """, unsafe_allow_html=True)

        try:
            df_sv = pd.read_excel(sv_file, dtype=str)
            df_sv.columns = [str(c).strip() for c in df_sv.columns]
            cols = df_sv.columns.tolist()
            auto_idx = dl.detect_mssv_col(cols)

            ca, cb = st.columns([1, 2])
            with ca:
                sel_col = st.selectbox('Cột MSSV', cols,
                                       index=auto_idx if auto_idx >= 0 else 0,
                                       key='mssv_col_sel')
                if auto_idx >= 0:
                    st.success(f'✅ Tự động phát hiện: **{sel_col}**')
                else:
                    st.warning('⚠️ Vui lòng chọn đúng cột MSSV')
            with cb:
                raw = df_sv[sel_col].dropna().astype(str).str.strip().tolist()
                mssv_list = [m for m in raw if m and m.lower() != 'nan']
                st.markdown(f'**Xem trước** — {len(mssv_list)} MSSV')
                st.dataframe(df_sv[[sel_col]].head(6), use_container_width=True, hide_index=True)
            mssv_col_ok = bool(mssv_list)
        except Exception as e:
            st.error(f'Lỗi đọc file Excel: {e}')

    # ── Bước 03 — Bắt đầu ──
    st.markdown('<hr class="step-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="step-header"><span class="step-badge">03</span><h3>Bắt đầu tra cứu</h3></div>
    <div class="step-sub">Hệ thống đọc từng file PDF, tìm MSSV trong bảng dữ liệu rồi chuyển sang màn kết quả</div>
    """, unsafe_allow_html=True)

    cs, cq = st.columns(2)
    with cs:
        if sv_file and mssv_col_ok:
            st.success(f'✅ {len(mssv_list)} MSSV sẵn sàng')
        elif sv_file:
            st.warning('⚠️ Chưa xác nhận cột MSSV')
        else:
            st.info('📄 Chưa upload file MSSV')
    with cq:
        if qd_files:
            st.success(f'✅ {len(qd_files)} file PDF')
            for f in qd_files:
                st.markdown(f'<div style="font-size:12px;color:{muted}">📄 {f.name}</div>', unsafe_allow_html=True)
        else:
            st.info('📁 Chưa upload file PDF')

    btn_ready = mssv_col_ok and bool(qd_files)
    run_btn = st.button('🔍 Bắt đầu tra cứu', type='primary',
                        use_container_width=True, disabled=not btn_ready)
    if not btn_ready:
        parts = []
        if not (sv_file and mssv_col_ok): parts.append('file Excel MSSV')
        if not qd_files:                  parts.append('file PDF Quyết định')
        st.caption(f'⚠️ Cần upload: {" và ".join(parts)}')

    # ── Xử lý ──
    if run_btn and btn_ready:
        if debug_mode:
            with st.expander('🛠 Debug pdfplumber', expanded=True):
                import pdfplumber, io as _io
                for f in qd_files:
                    f.seek(0)
                    st.markdown(f'**{f.name}**')
                    try:
                        with pdfplumber.open(_io.BytesIO(f.read())) as pdf:
                            for pi, page in enumerate(pdf.pages, 1):
                                tables = page.extract_tables()
                                if tables:
                                    st.markdown(f'Trang {pi}: {len(tables)} bảng')
                                    if show_all_tables:
                                        for ti, t in enumerate(tables):
                                            st.write(f'Bảng {ti+1}:', t[:5])
                    except Exception as e:
                        st.error(str(e))

        pdf_file_list = []
        for f in qd_files:
            f.seek(0)
            pdf_file_list.append({'name': f.name, 'bytes': f.read()})

        prog = st.progress(0, text='Đang khởi tạo...')
        all_results = {}

        for i, pf in enumerate(pdf_file_list):
            prog.progress(int((i / len(pdf_file_list)) * 90),
                          text=f'Đang đọc ({i+1}/{len(pdf_file_list)}): {pf["name"]}')
            partial = dl.search_mssv_in_pdfs(mssv_list, [pf])
            for mssv, data in partial.items():
                if mssv == '_errors':
                    all_results.setdefault('_errors', []).extend(data)
                    continue
                if mssv not in all_results:
                    all_results[mssv] = {'found': False, 'results': []}
                if data['found']:
                    all_results[mssv]['found'] = True
                    all_results[mssv]['results'].extend(data['results'])

        prog.progress(100, text='✅ Hoàn thành!')

        st.session_state['dl_results']     = all_results
        st.session_state['dl_mssv_list']   = mssv_list
        st.session_state['dl_show_results'] = True
        st.rerun()


# ===========================================================================
# MÀN 2 — KẾT QUẢ
# ===========================================================================
else:
    results   = st.session_state['dl_results']   or {}
    mssv_list = st.session_state['dl_mssv_list'] or []

    found_list = [m for m in mssv_list if results.get(m, {}).get('found')]
    miss_list  = [m for m in mssv_list if not results.get(m, {}).get('found')]
    errors     = results.get('_errors', [])

    # ── Header ──
    col_h, col_btn = st.columns([3, 1])
    with col_h:
        st.markdown('<h2 style="margin-bottom:4px">📊 Kết quả tra cứu</h2>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:{muted};margin-top:0">Kết quả tìm kiếm MSSV trong các Quyết định PDF</p>', unsafe_allow_html=True)
    with col_btn:
        if st.button('← Tra cứu mới', use_container_width=True):
            st.session_state['dl_show_results'] = False
            st.rerun()

    # ── Stat cards ──
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card"><div class="val gray">{len(mssv_list)}</div><div class="lbl">Tổng MSSV</div></div>
        <div class="stat-card"><div class="val">{len(found_list)}</div><div class="lbl">Tìm thấy trong QĐ</div></div>
        <div class="stat-card"><div class="val red">{len(miss_list)}</div><div class="lbl">Không có trong QĐ</div></div>
    </div>
    """, unsafe_allow_html=True)

    for e in errors:
        st.warning(f'⚠️ Lỗi đọc **{e["file"]}**: {e["error"]}')

    st.markdown('<hr class="step-divider">', unsafe_allow_html=True)

    # ── Build bảng chi tiết (full row data) ──
    def build_detail_df(subset):
        rows = []
        for m in subset:
            r = results.get(m, {'found': False, 'results': []})
            if not r['found']:
                rows.append({
                    'MSSV'       : m,
                    'Trạng thái' : '❌ Không tìm thấy',
                    'Tên QĐ'     : '—',
                    'Trang'      : '—',
                    'STT'        : '—',
                })
            else:
                for hit in r['results']:
                    row = {
                        'MSSV'       : m,
                        'Trạng thái' : '✅ Có',
                        'Tên QĐ'     : hit['qd_name'],
                        'Trang'      : f'Trang {hit["page"]}',
                        'STT'        : hit['stt'] or '—',
                    }
                    # Thêm toàn bộ dữ liệu từ bảng QĐ (bỏ cột MSSV vì đã có)
                    for k, v in hit['row_dict'].items():
                        if k and k.strip() and k not in row:
                            row[k] = v
                    rows.append(row)
        return pd.DataFrame(rows) if rows else pd.DataFrame()

    # ── Filter bar ──
    fc, fq = st.columns([1, 3])
    with fc:
        filter_mode = st.radio('Lọc', ['Tất cả', '✅ Tìm thấy', '❌ Không có'],
                               horizontal=False, key='filter_mode', label_visibility='collapsed')
    with fq:
        search_q = st.text_input('🔍 Tìm kiếm MSSV, Họ tên, QĐ...',
                                 placeholder='Nhập để lọc bảng...', key='search_q',
                                 label_visibility='collapsed')

    # Chọn subset theo filter
    if filter_mode == '✅ Tìm thấy':
        subset = found_list
    elif filter_mode == '❌ Không có':
        subset = miss_list
    else:
        subset = mssv_list

    df_detail = build_detail_df(subset)

    # Lọc theo từ khoá
    if search_q and not df_detail.empty:
        q = search_q.lower()
        mask = df_detail.apply(
            lambda col: col.astype(str).str.lower().str.contains(q, na=False)
        ).any(axis=1)
        df_detail = df_detail[mask]

    # Hiển thị bảng
    if df_detail.empty:
        st.info('Không có kết quả phù hợp.')
    else:
        st.markdown(f'<div style="font-size:12px;color:{muted};margin-bottom:6px">{len(df_detail)} dòng</div>', unsafe_allow_html=True)
        st.dataframe(df_detail, use_container_width=True, hide_index=True, height=500)

    # ── Xuất Excel ──
    st.markdown('<hr class="step-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="step-header"><span class="step-badge">05</span><h3>Xuất kết quả</h3></div>
    <div class="step-sub">File Excel gồm 2 sheet: Tổng hợp và Chi tiết đầy đủ thông tin từ QĐ</div>
    """, unsafe_allow_html=True)

    df_summary, df_exp_detail = dl.build_export_data(mssv_list, results)
    excel_bytes = dl.to_excel_bytes(df_summary, df_exp_detail)
    st.download_button(
        label='⬇️ Tải file Excel kết quả',
        data=excel_bytes,
        file_name='decision_lookup_result.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        use_container_width=True,
    )
