"""
pages/decision-lookup.py
Giao diện Streamlit — Decision Lookup 🔍
"""

import streamlit as st
import pandas as pd
import sys
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
st.set_page_config(
    page_title='Decision Lookup',
    page_icon='🔍',
    layout='wide',
)

# ---------------------------------------------------------------------------
# CSS — đồng nhất với hệ thống
# ---------------------------------------------------------------------------
st.markdown("""
<style>
/* ── Reset & base ── */
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1100px; }

/* ── Step badge ── */
.step-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px; height: 36px;
    background: #10b981;
    color: white;
    font-size: 13px;
    font-weight: 700;
    border-radius: 8px;
    margin-right: 12px;
    flex-shrink: 0;
}

/* ── Step header ── */
.step-header {
    display: flex;
    align-items: center;
    margin-bottom: 4px;
    margin-top: 8px;
}
.step-header h3 {
    margin: 0;
    font-size: 18px;
    font-weight: 700;
    color: #111827;
}
.step-sub {
    color: #6b7280;
    font-size: 13px;
    margin-left: 48px;
    margin-bottom: 16px;
}

/* ── Divider ── */
.step-divider {
    border: none;
    border-top: 1px solid #e5e7eb;
    margin: 24px 0;
}

/* ── Stat card ── */
.stat-row {
    display: flex;
    gap: 12px;
    margin: 16px 0;
    flex-wrap: wrap;
}
.stat-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 14px 20px;
    min-width: 130px;
    flex: 1;
}
.stat-card .val {
    font-size: 26px;
    font-weight: 800;
    color: #10b981;
    line-height: 1;
}
.stat-card .val.red  { color: #ef4444; }
.stat-card .val.gray { color: #6b7280; }
.stat-card .lbl {
    font-size: 12px;
    color: #6b7280;
    margin-top: 4px;
}

/* ── Result badge ── */
.badge-found {
    display: inline-block;
    background: #d1fae5;
    color: #065f46;
    font-size: 12px; font-weight: 700;
    padding: 2px 10px;
    border-radius: 20px;
}
.badge-miss {
    display: inline-block;
    background: #fee2e2;
    color: #991b1b;
    font-size: 12px; font-weight: 700;
    padding: 2px 10px;
    border-radius: 20px;
}

/* ── Lookup card ── */
.lookup-card {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.lookup-card .qd-label {
    font-weight: 700;
    font-size: 14px;
    color: #10b981;
    margin-bottom: 6px;
}
.lookup-card .loc-label {
    font-size: 12px;
    color: #6b7280;
    margin-bottom: 10px;
}

/* ── Error box ── */
.error-box {
    background: #fef2f2;
    border: 1px solid #fecaca;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 13px;
    color: #b91c1c;
    margin-top: 8px;
}

/* ── Sidebar section label ── */
.sidebar-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    color: #9ca3af;
    margin-bottom: 6px;
    margin-top: 16px;
}

/* Streamlit tweaks */
div[data-testid="stFileUploader"] label { font-size: 13px !important; }
div[data-testid="stButton"] > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
}
div[data-testid="stButton"] > button[kind="primary"] {
    background-color: #10b981 !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🔍 Decision Lookup")
    st.caption("Tra cứu MSSV trong các Quyết định PDF")
    st.divider()

    st.markdown('<div class="sidebar-label">CÔNG CỤ</div>', unsafe_allow_html=True)
    debug_mode = st.checkbox('🛠 Debug pdfplumber', value=False)
    show_all_tables = st.checkbox('📋 Hiện tất cả bảng tìm thấy', value=False)

    st.divider()
    st.markdown('<div class="sidebar-label">HƯỚNG DẪN</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:12px;color:#6b7280;line-height:1.8">
    1. Upload file Excel MSSV<br>
    2. Upload 1 hoặc nhiều file PDF QĐ<br>
    3. Nhấn <b>Bắt đầu tra cứu</b><br>
    4. Xem kết quả & xuất Excel
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------
st.markdown("## 🔍 Decision Lookup")
st.markdown(
    '<p style="color:#6b7280;margin-top:-8px;margin-bottom:24px">'
    'Kiểm tra MSSV có xuất hiện trong các Quyết định PDF và trả về vị trí chính xác</p>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------------------------
# BƯỚC 1 — Upload
# ---------------------------------------------------------------------------
st.markdown("""
<div class="step-header">
    <span class="step-badge">01</span>
    <h3>Tải lên file</h3>
</div>
<div class="step-sub">Upload file danh sách MSSV và các file Quyết định PDF</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.4])

with col1:
    st.markdown("**📄 FILE EXCEL — DANH SÁCH MSSV**")
    sv_file = st.file_uploader(
        'Excel chứa cột MSSV / RollNumber',
        type=['xlsx', 'xls'],
        key='sv_upload',
        label_visibility='collapsed'
    )

with col2:
    st.markdown("**📁 FILE PDF QUYẾT ĐỊNH**")
    qd_files = st.file_uploader(
        'Có thể chọn nhiều file cùng lúc',
        type=['pdf'],
        accept_multiple_files=True,
        key='qd_upload',
        label_visibility='collapsed'
    )

# ---------------------------------------------------------------------------
# BƯỚC 2 — Cấu hình cột MSSV
# ---------------------------------------------------------------------------
mssv_list = []
mssv_col_name = None

if sv_file:
    st.markdown('<hr class="step-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="step-header">
        <span class="step-badge">02</span>
        <h3>Xác nhận cột MSSV</h3>
    </div>
    <div class="step-sub">Kiểm tra và chọn đúng cột chứa MSSV / RollNumber</div>
    """, unsafe_allow_html=True)

    try:
        df_sv = pd.read_excel(sv_file, dtype=str)
        df_sv.columns = [str(c).strip() for c in df_sv.columns]

        # Auto-detect
        auto_idx = dl.detect_mssv_col(df_sv.columns.tolist())
        col_options = df_sv.columns.tolist()

        sel_col = st.selectbox(
            'Cột MSSV',
            options=col_options,
            index=auto_idx if auto_idx >= 0 else 0,
            key='mssv_col_sel'
        )
        mssv_col_name = sel_col

        raw_mssv = df_sv[sel_col].dropna().astype(str).str.strip().tolist()
        mssv_list = [m for m in raw_mssv if m and m.lower() != 'nan']

        # Preview
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(f'**Xem trước** — {len(mssv_list)} MSSV')
            st.dataframe(
                df_sv[[sel_col]].head(8),
                use_container_width=True,
                hide_index=True
            )
        with c2:
            st.metric('Tổng MSSV', len(mssv_list))
            if auto_idx >= 0:
                st.success(f'✅ Tự động phát hiện: **{sel_col}**')
            else:
                st.warning('⚠️ Vui lòng chọn đúng cột MSSV')

    except Exception as e:
        st.error(f'Lỗi đọc file Excel: {e}')

# ---------------------------------------------------------------------------
# BƯỚC 3 — Xử lý
# ---------------------------------------------------------------------------
if mssv_list and qd_files:
    st.markdown('<hr class="step-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="step-header">
        <span class="step-badge">03</span>
        <h3>Bắt đầu tra cứu</h3>
    </div>
    <div class="step-sub">Hệ thống sẽ đọc từng file PDF và tìm kiếm MSSV trong các bảng dữ liệu</div>
    """, unsafe_allow_html=True)

    # Hiển thị file QĐ đã chọn
    st.markdown(f'**{len(qd_files)} file QĐ đã chọn:**')
    for f in qd_files:
        st.markdown(
            f'<div style="font-size:13px;color:#374151;padding:2px 0">📄 {f.name}</div>',
            unsafe_allow_html=True
        )

    run_btn = st.button('🔍 Bắt đầu tra cứu', type='primary', use_container_width=True)

    if run_btn:
        # Chuẩn bị PDF files
        pdf_file_list = []
        for f in qd_files:
            pdf_file_list.append({'name': f.name, 'bytes': f.read()})

        # Debug mode
        if debug_mode:
            with st.expander('🛠 Debug — Bảng tìm thấy trong PDF', expanded=True):
                for pf in pdf_file_list:
                    import pdfplumber, io as _io
                    st.markdown(f'**{pf["name"]}**')
                    try:
                        with pdfplumber.open(_io.BytesIO(pf['bytes'])) as pdf:
                            for pi, page in enumerate(pdf.pages, 1):
                                tables = page.extract_tables()
                                if tables:
                                    st.markdown(f'Trang {pi}: {len(tables)} bảng')
                                    if show_all_tables:
                                        for ti, t in enumerate(tables):
                                            st.write(f'Bảng {ti+1}:', t[:5])
                    except Exception as e:
                        st.error(str(e))

        # Chạy tìm kiếm với progress
        progress_bar = st.progress(0, text='Đang khởi tạo...')
        results = {}

        for i, pf in enumerate(pdf_file_list):
            progress_bar.progress(
                int((i / len(pdf_file_list)) * 80),
                text=f'Đang đọc: {pf["name"]}'
            )
            partial = dl.search_mssv_in_pdfs(mssv_list, [pf])
            # Merge kết quả
            for mssv, data in partial.items():
                if mssv == '_errors':
                    results.setdefault('_errors', []).extend(data)
                    continue
                if mssv not in results:
                    results[mssv] = {'found': False, 'results': []}
                if data['found']:
                    results[mssv]['found'] = True
                    results[mssv]['results'].extend(data['results'])

        progress_bar.progress(100, text='✅ Hoàn thành!')

        # Lưu vào session
        st.session_state['dl_results']  = results
        st.session_state['dl_mssv_list'] = mssv_list


# ---------------------------------------------------------------------------
# BƯỚC 4 — Kết quả
# ---------------------------------------------------------------------------
if 'dl_results' in st.session_state and st.session_state['dl_results']:
    results   = st.session_state['dl_results']
    mssv_list = st.session_state['dl_mssv_list']

    st.markdown('<hr class="step-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="step-header">
        <span class="step-badge">04</span>
        <h3>Kết quả tra cứu</h3>
    </div>
    """, unsafe_allow_html=True)

    found_list = [m for m in mssv_list if results.get(m, {}).get('found')]
    miss_list  = [m for m in mssv_list if not results.get(m, {}).get('found')]
    errors     = results.get('_errors', [])

    # Stat cards
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card">
            <div class="val gray">{len(mssv_list)}</div>
            <div class="lbl">Tổng MSSV</div>
        </div>
        <div class="stat-card">
            <div class="val">{len(found_list)}</div>
            <div class="lbl">Tìm thấy trong QĐ</div>
        </div>
        <div class="stat-card">
            <div class="val red">{len(miss_list)}</div>
            <div class="lbl">Không có trong QĐ</div>
        </div>
        <div class="stat-card">
            <div class="val gray">{len(st.session_state.get('dl_pdf_files', []))}</div>
            <div class="lbl">File QĐ đã tra</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Lỗi parse
    if errors:
        for e in errors:
            st.markdown(
                f'<div class="error-box">❌ Lỗi đọc <b>{e["file"]}</b>: {e["error"]}</div>',
                unsafe_allow_html=True
            )

    # ── Tabs ──────────────────────────────────────────────────────────────
    tab_all, tab_found, tab_miss, tab_lookup = st.tabs([
        f'📋 Tất cả ({len(mssv_list)})',
        f'✅ Tìm thấy ({len(found_list)})',
        f'❌ Không có ({len(miss_list)})',
        '🔎 Tra cứu nhanh',
    ])

    def build_summary_df(mssv_subset):
        rows = []
        for m in mssv_subset:
            r = results.get(m, {'found': False, 'results': []})
            qd_names = list(dict.fromkeys(x['qd_name'] for x in r['results']))
            rows.append({
                'MSSV'        : m,
                'Trạng thái'  : '✅ Có' if r['found'] else '❌ Không',
                'Số QĐ'       : len(qd_names),
                'Danh sách QĐ': ', '.join(qd_names) if qd_names else '—',
                'Số vị trí'   : len(r['results']),
            })
        return pd.DataFrame(rows)

    with tab_all:
        df_show = build_summary_df(mssv_list)
        st.dataframe(df_show, use_container_width=True, hide_index=True, height=420)

    with tab_found:
        if found_list:
            df_show = build_summary_df(found_list)
            st.dataframe(df_show, use_container_width=True, hide_index=True, height=420)
        else:
            st.info('Không tìm thấy MSSV nào trong các QĐ.')

    with tab_miss:
        if miss_list:
            df_show = build_summary_df(miss_list)
            st.dataframe(df_show, use_container_width=True, hide_index=True, height=420)
        else:
            st.success('Tất cả MSSV đều có trong QĐ!')

    # ── Tra cứu nhanh ─────────────────────────────────────────────────────
    with tab_lookup:
        st.markdown('**Nhập MSSV để xem toàn bộ thông tin trong QĐ**')
        query = st.text_input(
            'MSSV', placeholder='VD: SE123456', key='lookup_input',
            label_visibility='collapsed'
        )

        if query:
            query_clean = query.strip().upper()
            matched_key = next(
                (m for m in mssv_list if m.upper() == query_clean), None
            )

            if not matched_key:
                st.warning(f'MSSV **{query}** không có trong danh sách tra cứu.')
            else:
                r = results.get(matched_key, {'found': False, 'results': []})
                if not r['found']:
                    st.markdown(
                        f'<span class="badge-miss">❌ Không tìm thấy</span> '
                        f'<span style="font-size:14px;margin-left:8px">'
                        f'<b>{matched_key}</b> không xuất hiện trong bất kỳ QĐ nào.</span>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<span class="badge-found">✅ Tìm thấy</span> '
                        f'<span style="font-size:14px;margin-left:8px">'
                        f'<b>{matched_key}</b> — {len(r["results"])} vị trí trong '
                        f'{len(set(x["qd_name"] for x in r["results"]))} QĐ</span>',
                        unsafe_allow_html=True
                    )
                    st.markdown('')
                    for hit in r['results']:
                        st.markdown(f"""
                        <div class="lookup-card">
                            <div class="qd-label">📄 {hit['qd_name']}</div>
                            <div class="loc-label">📍 Trang {hit['page']} &nbsp;·&nbsp; STT: {hit['stt'] or '—'}</div>
                        </div>
                        """, unsafe_allow_html=True)

                        # Hiển thị toàn bộ dòng dữ liệu
                        if hit['row_dict']:
                            df_row = pd.DataFrame([hit['row_dict']])
                            st.dataframe(df_row, use_container_width=True, hide_index=True)
                        st.markdown('')

    # ── Xuất Excel ────────────────────────────────────────────────────────
    st.markdown('<hr class="step-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="step-header">
        <span class="step-badge">05</span>
        <h3>Xuất kết quả</h3>
    </div>
    <div class="step-sub">Tải file Excel gồm 2 sheet: Tổng hợp và Chi tiết vị trí</div>
    """, unsafe_allow_html=True)

    df_summary, df_detail = dl.build_export_data(mssv_list, results)
    excel_bytes = dl.to_excel_bytes(df_summary, df_detail)

    st.download_button(
        label='⬇️ Tải file Excel kết quả',
        data=excel_bytes,
        file_name='decision_lookup_result.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        use_container_width=True,
    )
