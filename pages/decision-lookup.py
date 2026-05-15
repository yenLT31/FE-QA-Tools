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
for k, v in {
    'dl_theme'       : 'light',
    'dl_results'     : None,
    'dl_mssv_list'   : None,
    'dl_qd_names'    : [],
    'dl_goto_results': False,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

is_dark = st.session_state['dl_theme'] == 'dark'

# Color tokens
bg      = '#0f172a' if is_dark else '#f8fafc'
surface = '#1e293b' if is_dark else '#ffffff'
border  = '#334155' if is_dark else '#e5e7eb'
text    = '#f1f5f9' if is_dark else '#111827'
muted   = '#94a3b8' if is_dark else '#6b7280'
green   = '#10b981'
red     = '#ef4444'
blue    = '#3b82f6'

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
st.markdown(f"""
<style>
.stApp {{ background: {bg} !important; }}
.block-container {{ padding: 0 !important; max-width: 100% !important; }}

/* Sidebar */
section[data-testid="stSidebar"] > div {{
    background: {surface} !important;
    border-right: 1px solid {border};
}}

/* Top bar */
.top-bar {{
    background: {'#1e293b' if is_dark else '#111827'};
    height: 52px;
    display: flex; align-items: center; justify-content: center;
    padding: 0 28px; gap: 12px;
    position: sticky; top: 0; z-index: 999;
    border-bottom: 1px solid {'#334155' if is_dark else '#374151'};
}}
.tb-back {{
    position: absolute; left: 28px;
    font-size: 12px; color: #9ca3af;
    display: flex; align-items: center; gap: 4px;
}}
.tb-title {{ font-size: 15px; font-weight: 800; color: #fff; }}
.tb-live {{
    font-size: 10px; font-weight: 700;
    background: #14532d; color: #4ade80;
    border: 1px solid #166534;
    padding: 2px 8px; border-radius: 20px;
}}

/* Tabs */
div[data-baseweb="tab-list"] {{
    background: {surface} !important;
    border-bottom: 1px solid {border} !important;
    gap: 0 !important; padding: 0 !important;
}}
div[data-baseweb="tab"] {{
    background: transparent !important;
    color: {muted} !important;
    font-size: 13px !important; font-weight: 600 !important;
    padding: 14px 24px !important;
    border-bottom: 2px solid transparent !important;
}}
div[data-baseweb="tab"]:hover {{ color: {text} !important; }}
div[data-baseweb="tab"][aria-selected="true"] {{
    color: {green} !important;
    border-bottom: 2px solid {green} !important;
}}
div[data-baseweb="tab-highlight"],
div[data-baseweb="tab-border"] {{ display: none !important; }}
div[data-testid="stTabsContent"] {{
    padding: 24px 28px !important;
    background: {bg} !important;
}}

/* Stat cards */
.stat-row {{ display:flex; gap:14px; flex-wrap:wrap; margin-bottom:24px; }}
.stat-card {{
    background: {surface}; border: 1px solid {border};
    border-left: 4px solid {green};
    border-radius: 10px; padding: 16px 20px;
    flex: 1; min-width: 130px;
}}
.stat-card.red  {{ border-left-color: {red}; }}
.stat-card.blue {{ border-left-color: {blue}; }}
.stat-card.gray {{ border-left-color: {muted}; }}
.stat-val {{ font-size: 32px; font-weight: 900; color: {green}; line-height: 1; }}
.stat-val.red  {{ color: {red}; }}
.stat-val.blue {{ color: {blue}; }}
.stat-val.gray {{ color: {muted}; }}
.stat-lbl {{
    font-size: 10px; font-weight: 700; letter-spacing: .7px;
    text-transform: uppercase; color: {muted}; margin-top: 6px;
}}

/* Summary bar */
.summary-bar {{
    background: {'#14532d' if is_dark else '#f0fdf4'};
    border: 1px solid {'#166534' if is_dark else '#bbf7d0'};
    border-radius: 8px; padding: 10px 16px;
    font-size: 13px; font-weight: 600;
    color: {'#4ade80' if is_dark else '#166534'};
    margin-bottom: 12px;
}}

/* Step */
.step-badge {{
    display:inline-flex; align-items:center; justify-content:center;
    width:32px; height:32px; background:{green}; color:white;
    font-size:12px; font-weight:800; border-radius:8px;
    margin-right:10px; flex-shrink:0;
}}
.step-hdr {{ display:flex; align-items:center; margin-bottom:3px; margin-top:20px; }}
.step-hdr h3 {{ margin:0; font-size:16px; font-weight:700; color:{text}; }}
.step-sub {{ font-size:12px; color:{muted}; margin-left:42px; margin-bottom:14px; }}
.divider {{ border:none; border-top:1px solid {border}; margin:20px 0; }}
.col-lbl {{
    font-size:10px; font-weight:700; letter-spacing:.7px;
    text-transform:uppercase; color:{muted}; margin-bottom:5px;
}}
.sb-label {{
    font-size:11px; font-weight:700; letter-spacing:.8px;
    text-transform:uppercase; color:{muted};
    margin-top:16px; margin-bottom:6px;
}}

/* Streamlit buttons */
div[data-testid="stButton"] > button {{
    border-radius: 8px !important; font-weight: 600 !important;
}}
div[data-testid="stButton"] > button[kind="primary"] {{
    background: {green} !important; border: none !important; color: white !important;
}}
div[data-testid="stFileUploader"] {{
    background: {surface} !important;
    border: 1.5px dashed {border} !important;
    border-radius: 10px !important;
}}
.stTextInput input {{
    background: {surface} !important;
    border-color: {border} !important; color: {text} !important;
    border-radius: 8px !important;
}}
.stSelectbox > div > div {{
    background: {surface} !important;
    border-color: {border} !important; color: {text} !important;
}}
div[data-testid="stAppViewContainer"] > section {{ padding-top: 0 !important; }}
div[data-testid="stRadio"] > div {{ flex-direction: row !important; gap: 12px !important; flex-wrap: wrap; }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div style="font-size:18px;font-weight:800">🔍 Decision Lookup</div>',
                unsafe_allow_html=True)
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
    debug_mode = st.checkbox('🛠 Debug pdfplumber', value=False)

    st.divider()
    st.markdown('<div class="sb-label">HƯỚNG DẪN</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:12px;color:{muted};line-height:2">
    1. Upload file Excel MSSV<br>
    2. Upload file PDF QĐ<br>
    3. Nhấn <b>Bắt đầu tra cứu</b><br>
    4. Xem bảng & xuất Excel
    </div>""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# TOP BAR
# ---------------------------------------------------------------------------
st.markdown(f"""
<div class="top-bar">
    <span class="tb-back">← Trang chủ</span>
    <span class="tb-title">🔍 Decision Lookup</span>
    <span class="tb-live">● LIVE</span>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# TABS
# ---------------------------------------------------------------------------
has_results = bool(st.session_state.get('dl_results'))

tab_cfg, tab_res = st.tabs(['📂 Cấu hình', '📊 Kết quả'])

# Auto-switch sang tab Kết quả sau khi xử lý
if st.session_state.get('dl_goto_results'):
    st.session_state['dl_goto_results'] = False
    st.markdown("""
    <script>
    setTimeout(function() {
        const tabs = window.parent.document.querySelectorAll('[data-baseweb="tab"]');
        if (tabs.length >= 2) tabs[1].click();
    }, 400);
    </script>
    """, unsafe_allow_html=True)

# ===========================================================================
# TAB 1 — CẤU HÌNH
# ===========================================================================
with tab_cfg:

    st.markdown("""
    <div class="step-hdr"><span class="step-badge">01</span><h3>Tải lên file</h3></div>
    <div class="step-sub">Upload file danh sách MSSV và các file Quyết định PDF</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.4])
    with col1:
        st.markdown('<div class="col-lbl">📄 FILE EXCEL — DANH SÁCH MSSV</div>', unsafe_allow_html=True)
        sv_file = st.file_uploader('sv', type=['xlsx', 'xls'],
                                   key='sv_upload', label_visibility='collapsed')
    with col2:
        st.markdown('<div class="col-lbl">📁 FILE PDF QUYẾT ĐỊNH</div>', unsafe_allow_html=True)
        qd_files = st.file_uploader('qd', type=['pdf'], accept_multiple_files=True,
                                    key='qd_upload', label_visibility='collapsed')

    # Bước 02 — Cột MSSV
    mssv_list   = []
    mssv_col_ok = False

    if sv_file:
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("""
        <div class="step-hdr"><span class="step-badge">02</span><h3>Xác nhận cột MSSV</h3></div>
        <div class="step-sub">Chọn đúng cột chứa MSSV / RollNumber trong file Excel</div>
        """, unsafe_allow_html=True)

        try:
            df_sv    = pd.read_excel(sv_file, dtype=str)
            df_sv.columns = [str(c).strip() for c in df_sv.columns]
            cols     = df_sv.columns.tolist()
            auto_idx = dl.detect_mssv_col(cols)

            ca, cb = st.columns([1, 2])
            with ca:
                sel_col = st.selectbox('Cột MSSV', cols,
                                       index=auto_idx if auto_idx >= 0 else 0,
                                       key='mssv_col_sel')
            with cb:
                raw       = df_sv[sel_col].dropna().astype(str).str.strip().tolist()
                mssv_list = [m for m in raw if m and m.lower() != 'nan']
                if auto_idx >= 0:
                    st.success(f'✅ Tự động phát hiện cột **{sel_col}** — {len(mssv_list)} MSSV')
                else:
                    st.warning(f'⚠️ Đã chọn cột **{sel_col}** — {len(mssv_list)} MSSV')
            mssv_col_ok = bool(mssv_list)
        except Exception as e:
            st.error(f'Lỗi đọc file Excel: {e}')

    # Bước 03 — Chạy
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="step-hdr"><span class="step-badge">03</span><h3>Bắt đầu tra cứu</h3></div>
    <div class="step-sub">Hệ thống đọc từng PDF, tìm MSSV trong bảng rồi chuyển sang tab Kết quả</div>
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
                st.markdown(f'<div style="font-size:12px;color:{muted}">📄 {f.name}</div>',
                            unsafe_allow_html=True)
        else:
            st.info('📁 Chưa upload file PDF')

    btn_ready = mssv_col_ok and bool(qd_files)
    run_btn   = st.button('🔍 Bắt đầu tra cứu', type='primary',
                          use_container_width=True, disabled=not btn_ready)
    if not btn_ready:
        parts = []
        if not (sv_file and mssv_col_ok): parts.append('file Excel MSSV')
        if not qd_files:                  parts.append('file PDF Quyết định')
        st.caption(f'⚠️ Cần upload: {" và ".join(parts)}')

    if run_btn and btn_ready:
        if debug_mode:
            with st.expander('🛠 Debug pdfplumber', expanded=True):
                import pdfplumber as _plumber, io as _io
                for f in qd_files:
                    f.seek(0)
                    st.markdown(f'**{f.name}**')
                    try:
                        with _plumber.open(_io.BytesIO(f.read())) as pdf:
                            for pi, page in enumerate(pdf.pages, 1):
                                tables = page.extract_tables()
                                if tables:
                                    st.markdown(f'Trang {pi}: {len(tables)} bảng')
                                    for ti, t in enumerate(tables):
                                        st.write(f'Bảng {ti+1} (3 dòng đầu):', t[:3])
                    except Exception as e:
                        st.error(str(e))

        pdf_file_list = []
        for f in qd_files:
            f.seek(0)
            pdf_file_list.append({'name': f.name, 'bytes': f.read()})

        prog        = st.progress(0, text='Đang khởi tạo...')
        all_results = {}

        for i, pf in enumerate(pdf_file_list):
            prog.progress(
                int((i / len(pdf_file_list)) * 90),
                text=f'Đang đọc ({i+1}/{len(pdf_file_list)}): {pf["name"]}'
            )
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
        st.session_state['dl_qd_names']    = [f['name'] for f in pdf_file_list]
        st.session_state['dl_goto_results'] = True
        st.rerun()


# ===========================================================================
# TAB 2 — KẾT QUẢ
# ===========================================================================
with tab_res:
    if not has_results:
        st.markdown(f"""
        <div style="text-align:center;padding:80px 20px;color:{muted}">
            <div style="font-size:48px;margin-bottom:14px">🔍</div>
            <div style="font-size:16px;font-weight:700;color:{text}">Chưa có kết quả</div>
            <div style="font-size:13px;margin-top:8px">
                Vui lòng upload file và chạy tra cứu ở tab <b>Cấu hình</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        results   = st.session_state['dl_results']
        mssv_list = st.session_state['dl_mssv_list'] or []

        found_list = [m for m in mssv_list if results.get(m, {}).get('found')]
        miss_list  = [m for m in mssv_list if not results.get(m, {}).get('found')]
        errors     = results.get('_errors', [])

        # Stat cards
        st.markdown(f"""
        <div class="stat-row">
            <div class="stat-card gray">
                <div class="stat-val gray">{len(mssv_list)}</div>
                <div class="stat-lbl">Tổng MSSV</div>
            </div>
            <div class="stat-card">
                <div class="stat-val">{len(found_list)}</div>
                <div class="stat-lbl">Tìm thấy trong QĐ</div>
            </div>
            <div class="stat-card red">
                <div class="stat-val red">{len(miss_list)}</div>
                <div class="stat-lbl">Không có trong QĐ</div>
            </div>
            <div class="stat-card blue">
                <div class="stat-val blue">{len(st.session_state.get('dl_qd_names', []))}</div>
                <div class="stat-lbl">File QĐ đã tra</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        for e in errors:
            st.warning(f'⚠️ Lỗi đọc **{e["file"]}**: {e["error"]}')

        # Build dataframe
        def build_df(subset):
            rows = []
            stt  = 1
            skip_cols = {'mssv','rollnumber','roll number','mã sv',
                         'mã sinh viên','stt','tt','số tt'}
            for m in subset:
                r = results.get(m, {'found': False, 'results': []})
                if not r['found']:
                    rows.append({'STT': stt, 'MSSV': m,
                                 'Trạng thái': '❌ Không tìm thấy',
                                 'Tên QĐ': '—', 'Trang': '—', 'STT trong QĐ': '—'})
                    stt += 1
                else:
                    for hit in r['results']:
                        row = {
                            'STT': stt, 'MSSV': m,
                            'Trạng thái': '✅ Có',
                            'Tên QĐ': hit['qd_name'],
                            'Trang': f'Trang {hit["page"]}',
                            'STT trong QĐ': hit['stt'] or '—',
                        }
                        for k, v in hit['row_dict'].items():
                            kn = str(k).strip()
                            if kn and kn.lower() not in skip_cols and kn not in row:
                                row[kn] = v
                        rows.append(row)
                        stt += 1
            return pd.DataFrame(rows) if rows else pd.DataFrame()

        # Filter + Search
        fc, fs = st.columns([3, 5])
        with fc:
            filter_mode = st.radio(
                'f', ['📋 Tất cả', '✅ Tìm thấy', '❌ Không có'],
                horizontal=True, key='dl_filter', label_visibility='collapsed'
            )
        with fs:
            search_q = st.text_input(
                's', placeholder='🔍  Tìm MSSV, Họ tên, Tên QĐ...',
                key='dl_search', label_visibility='collapsed'
            )

        subset = (found_list if 'Tìm thấy' in filter_mode
                  else miss_list if 'Không có' in filter_mode
                  else mssv_list)

        df = build_df(subset)

        if search_q.strip() and not df.empty:
            q    = search_q.strip().lower()
            mask = df.apply(
                lambda col: col.astype(str).str.lower().str.contains(q, na=False)
            ).any(axis=1)
            df = df[mask]

        # Summary bar
        st.markdown(f"""
        <div class="summary-bar">
            Tổng: {len(mssv_list)} MSSV &nbsp;|&nbsp;
            ✅ Tìm thấy: {len(found_list)} &nbsp;|&nbsp;
            ❌ Không có: {len(miss_list)} &nbsp;|&nbsp;
            Đang hiển thị: {len(df)} dòng
        </div>
        """, unsafe_allow_html=True)

        # Bảng — height động theo số dòng, có thanh cuộn
        if df.empty:
            st.info('Không có kết quả phù hợp.')
        else:
            row_h  = 35
            header = 38
            max_h  = 600
            tbl_h  = min(header + len(df) * row_h, max_h)
            st.dataframe(df, use_container_width=True, hide_index=True, height=tbl_h)

        # Export
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        df_sum, df_det = dl.build_export_data(mssv_list, results)
        excel_bytes    = dl.to_excel_bytes(df_sum, df_det)
        st.download_button(
            label='⬇️ Xuất file Excel kết quả',
            data=excel_bytes,
            file_name='decision_lookup_result.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            use_container_width=True,
        )
