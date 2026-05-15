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
    'dl_active_tab'  : 'upload',   # 'upload' | 'results'
    'dl_sv_file_name': '',
    'dl_qd_names'    : [],
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

is_dark = st.session_state['dl_theme'] == 'dark'

# Color tokens
bg      = '#0f172a' if is_dark else '#f8fafc'
surface = '#1e293b' if is_dark else '#ffffff'
border  = '#334155' if is_dark else '#e2e8f0'
text    = '#f1f5f9' if is_dark else '#0f172a'
muted   = '#94a3b8' if is_dark else '#64748b'
green   = '#10b981'
red     = '#ef4444'
blue    = '#3b82f6'

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
st.markdown(f"""
<style>
/* Base */
.stApp {{ background-color: {bg} !important; }}
.block-container {{ padding: 0 !important; max-width: 100% !important; }}

/* Top bar */
.top-bar {{
    background: {surface};
    border-bottom: 1px solid {border};
    padding: 0 32px;
    display: flex; align-items: center;
    height: 56px; gap: 16px;
    position: sticky; top: 0; z-index: 100;
}}
.top-back {{
    font-size: 13px; color: {muted}; text-decoration: none;
    display: flex; align-items: center; gap: 6px; cursor: pointer;
    border: none; background: none; padding: 0;
}}
.top-back:hover {{ color: {text}; }}
.top-title {{
    font-size: 15px; font-weight: 800; color: {text};
    display: flex; align-items: center; gap: 10px; flex: 1;
}}
.live-badge {{
    font-size: 10px; font-weight: 700;
    background: {'#14532d' if is_dark else '#dcfce7'};
    color: {'#4ade80' if is_dark else '#166534'};
    border: 1px solid {'#166534' if is_dark else '#bbf7d0'};
    padding: 2px 8px; border-radius: 20px; letter-spacing: .3px;
}}
.theme-btns {{ display: flex; gap: 6px; }}
.tbtn {{
    width: 36px; height: 32px; border-radius: 8px;
    border: 1px solid {border}; background: {surface};
    color: {text}; font-size: 14px; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    transition: all .15s;
}}
.tbtn.active {{ background: {green}; border-color: {green}; color: white; }}

/* Tab nav */
.tab-nav {{
    background: {surface}; border-bottom: 1px solid {border};
    padding: 0 32px; display: flex; gap: 0;
}}
.tnav {{
    padding: 14px 20px; font-size: 13px; font-weight: 600;
    color: {muted}; border-bottom: 2px solid transparent;
    cursor: pointer; transition: all .15s;
    display: flex; align-items: center; gap: 6px;
}}
.tnav.active {{ color: {green}; border-bottom-color: {green}; }}
.tnav:hover {{ color: {text}; }}

/* Content */
.content {{ padding: 28px 32px; }}

/* Step */
.step-badge {{
    display:inline-flex;align-items:center;justify-content:center;
    width:32px;height:32px;background:{green};color:white;
    font-size:12px;font-weight:700;border-radius:8px;
    margin-right:10px;flex-shrink:0;
}}
.step-hdr {{ display:flex;align-items:center;margin-bottom:3px;margin-top:20px; }}
.step-hdr h3 {{ margin:0;font-size:16px;font-weight:700;color:{text}; }}
.step-sub {{ font-size:12px;color:{muted};margin-left:42px;margin-bottom:14px; }}
.divider {{ border:none;border-top:1px solid {border};margin:20px 0; }}

/* Stat cards */
.stat-row {{ display:flex;gap:14px;margin:20px 0;flex-wrap:wrap; }}
.stat-card {{
    background:{surface};border:1px solid {border};
    border-radius:12px;padding:18px 22px;flex:1;min-width:140px;
    border-left: 3px solid {green};
}}
.stat-card.red {{ border-left-color:{red}; }}
.stat-card.blue {{ border-left-color:{blue}; }}
.stat-card.gray {{ border-left-color:{muted}; }}
.stat-val {{ font-size:30px;font-weight:800;color:{green};line-height:1; }}
.stat-val.red  {{ color:{red}; }}
.stat-val.gray {{ color:{muted}; }}
.stat-lbl {{ font-size:11px;color:{muted};margin-top:5px;text-transform:uppercase;letter-spacing:.5px; }}

/* Search bar */
.search-bar {{
    display:flex;gap:10px;align-items:center;margin-bottom:14px;flex-wrap:wrap;
}}

/* Col label */
.col-lbl {{
    font-size:10px;font-weight:700;letter-spacing:.7px;
    text-transform:uppercase;color:{muted};margin-bottom:5px;
}}

/* Streamlit overrides */
div[data-testid="stButton"] > button {{
    border-radius:8px !important; font-weight:600 !important;
}}
div[data-testid="stButton"] > button[kind="primary"] {{
    background-color:{green} !important; border:none !important; color:white !important;
}}
div[data-testid="stFileUploader"] {{
    background:{surface} !important;
    border:1.5px dashed {border} !important;
    border-radius:10px !important; padding:6px !important;
}}
.stTextInput > div > div > input {{
    background:{surface} !important;
    border-color:{border} !important;
    color:{text} !important; border-radius:8px !important;
}}
.stSelectbox > div > div {{
    background:{surface} !important;
    border-color:{border} !important; color:{text} !important;
}}
.stRadio > div {{ gap:6px; }}
.stDataFrame {{ border-radius:10px !important; overflow:hidden; }}
div[data-testid="stMetric"] label {{ color:{muted} !important; font-size:11px !important; }}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# TOP BAR
# ---------------------------------------------------------------------------
st.markdown(f"""
<div class="top-bar">
    <span style="font-size:13px;color:{muted}">← Trang chủ</span>
    <div class="top-title">
        🔍 Decision Lookup
        <span class="live-badge">● LIVE</span>
    </div>
    <div class="theme-btns">
        <button class="tbtn {'active' if not is_dark else ''}" title="Sáng">☀️</button>
        <button class="tbtn {'active' if is_dark else ''}" title="Tối">🌙</button>
    </div>
</div>
""", unsafe_allow_html=True)

# Theme toggle (dùng Streamlit buttons ẩn để bắt click)
_c1, _c2, _c3 = st.columns([8, 1, 1])
with _c2:
    if st.button('☀️', key='btn_light', help='Giao diện sáng'):
        st.session_state['dl_theme'] = 'light'
        st.rerun()
with _c3:
    if st.button('🌙', key='btn_dark', help='Giao diện tối'):
        st.session_state['dl_theme'] = 'dark'
        st.rerun()

# ---------------------------------------------------------------------------
# TAB NAV
# ---------------------------------------------------------------------------
active_tab = st.session_state['dl_active_tab']
has_results = bool(st.session_state.get('dl_results'))

st.markdown(f"""
<div class="tab-nav">
    <div class="tnav {'active' if active_tab == 'upload' else ''}">📂 Cấu hình</div>
    <div class="tnav {'active' if active_tab == 'results' else ''}" style="{'opacity:.4;cursor:default;' if not has_results else ''}">
        📊 Kết quả {'(' + str(len(st.session_state.get('dl_mssv_list') or [])) + ')' if has_results else ''}
    </div>
</div>
""", unsafe_allow_html=True)

tab_cols = st.columns([1, 1, 8])
with tab_cols[0]:
    if st.button('📂 Cấu hình', key='nav_upload', use_container_width=True):
        st.session_state['dl_active_tab'] = 'upload'
        st.rerun()
with tab_cols[1]:
    if st.button('📊 Kết quả', key='nav_results',
                 disabled=not has_results, use_container_width=True):
        st.session_state['dl_active_tab'] = 'results'
        st.rerun()

st.markdown('<div class="content">', unsafe_allow_html=True)

# ===========================================================================
# TAB: CẤU HÌNH
# ===========================================================================
if active_tab == 'upload':

    # Bước 01
    st.markdown(f"""
    <div class="step-hdr"><span class="step-badge">01</span><h3>Tải lên file</h3></div>
    <div class="step-sub">Upload file danh sách MSSV và các file Quyết định PDF</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.4])
    with col1:
        st.markdown('<div class="col-lbl">📄 FILE EXCEL — DANH SÁCH MSSV</div>', unsafe_allow_html=True)
        sv_file = st.file_uploader('sv', type=['xlsx','xls'], key='sv_upload', label_visibility='collapsed')
    with col2:
        st.markdown('<div class="col-lbl">📁 FILE PDF QUYẾT ĐỊNH</div>', unsafe_allow_html=True)
        qd_files = st.file_uploader('qd', type=['pdf'], accept_multiple_files=True,
                                    key='qd_upload', label_visibility='collapsed')

    # Bước 02
    mssv_list   = []
    mssv_col_ok = False
    sel_col     = None

    if sv_file:
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="step-hdr"><span class="step-badge">02</span><h3>Xác nhận cột MSSV</h3></div>
        <div class="step-sub">Chọn đúng cột chứa MSSV / RollNumber trong file Excel</div>
        """, unsafe_allow_html=True)

        try:
            df_sv = pd.read_excel(sv_file, dtype=str)
            df_sv.columns = [str(c).strip() for c in df_sv.columns]
            cols = df_sv.columns.tolist()
            auto_idx = dl.detect_mssv_col(cols)

            c_sel, c_info = st.columns([1, 2])
            with c_sel:
                sel_col = st.selectbox('Cột MSSV', cols,
                                       index=auto_idx if auto_idx >= 0 else 0,
                                       key='mssv_col_sel')
            with c_info:
                raw = df_sv[sel_col].dropna().astype(str).str.strip().tolist()
                mssv_list = [m for m in raw if m and m.lower() != 'nan']
                if auto_idx >= 0:
                    st.success(f'✅ Tự động phát hiện cột **{sel_col}** — {len(mssv_list)} MSSV')
                else:
                    st.warning(f'⚠️ Đã chọn cột **{sel_col}** — {len(mssv_list)} MSSV')

            mssv_col_ok = bool(mssv_list)
        except Exception as e:
            st.error(f'Lỗi đọc file Excel: {e}')

    # Bước 03
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="step-hdr"><span class="step-badge">03</span><h3>Bắt đầu tra cứu</h3></div>
    <div class="step-sub">Hệ thống đọc từng PDF, tìm MSSV trong bảng dữ liệu rồi chuyển sang tab Kết quả</div>
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
    run_btn = st.button('🔍 Bắt đầu tra cứu', type='primary',
                        use_container_width=True, disabled=not btn_ready)
    if not btn_ready:
        parts = []
        if not (sv_file and mssv_col_ok): parts.append('file Excel MSSV')
        if not qd_files:                  parts.append('file PDF Quyết định')
        st.caption(f'⚠️ Cần upload: {" và ".join(parts)}')

    if run_btn and btn_ready:
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
        st.session_state['dl_results']    = all_results
        st.session_state['dl_mssv_list']  = mssv_list
        st.session_state['dl_qd_names']   = [f['name'] for f in pdf_file_list]
        st.session_state['dl_active_tab'] = 'results'
        st.rerun()


# ===========================================================================
# TAB: KẾT QUẢ
# ===========================================================================
elif active_tab == 'results' and has_results:
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
            <div class="stat-val" style="color:{blue}">{len(st.session_state.get('dl_qd_names', []))}</div>
            <div class="stat-lbl">File QĐ đã tra</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    for e in errors:
        st.warning(f'⚠️ Lỗi đọc **{e["file"]}**: {e["error"]}')

    # Build detail dataframe
    def build_detail_df(subset):
        rows = []
        stt  = 1
        for m in subset:
            r = results.get(m, {'found': False, 'results': []})
            if not r['found']:
                rows.append({'STT': stt, 'MSSV': m, 'Trạng thái': '❌ Không tìm thấy',
                             'Tên QĐ': '—', 'Trang': '—', 'STT trong QĐ': '—'})
                stt += 1
            else:
                for hit in r['results']:
                    row = {'STT': stt, 'MSSV': m, 'Trạng thái': '✅ Có',
                           'Tên QĐ': hit['qd_name'],
                           'Trang': f'Trang {hit["page"]}',
                           'STT trong QĐ': hit['stt'] or '—'}
                    for k, v in hit['row_dict'].items():
                        col_norm = str(k).strip()
                        if col_norm and col_norm not in row and col_norm.upper() not in ['MSSV','ROLLNUMBER','ROLL NUMBER','MÃ SV','MÃ SINH VIÊN','STT','TT']:
                            row[col_norm] = v
                    rows.append(row)
                    stt += 1
        return pd.DataFrame(rows) if rows else pd.DataFrame()

    # Filter tabs (dùng radio ẩn label)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    filter_col, search_col = st.columns([2, 5])
    with filter_col:
        filter_mode = st.radio(
            'filter', ['📋 Tất cả', '✅ Tìm thấy', '❌ Không có'],
            horizontal=True, key='dl_filter', label_visibility='collapsed'
        )
    with search_col:
        search_q = st.text_input(
            'search', placeholder='🔍 Tìm MSSV, Họ tên, Tên QĐ...',
            key='dl_search', label_visibility='collapsed'
        )

    # Subset
    if 'Tìm thấy' in filter_mode:
        subset = found_list
    elif 'Không có' in filter_mode:
        subset = miss_list
    else:
        subset = mssv_list

    df = build_detail_df(subset)

    # Apply search
    if search_q.strip() and not df.empty:
        q = search_q.strip().lower()
        mask = df.apply(lambda col: col.astype(str).str.lower().str.contains(q, na=False)).any(axis=1)
        df = df[mask]

    # Summary bar
    total_disp = len(df)
    st.markdown(
        f'<div style="background:{"#1e3a2e" if is_dark else "#f0fdf4"};border:1px solid {"#166534" if is_dark else "#bbf7d0"};border-radius:8px;padding:10px 16px;font-size:13px;font-weight:600;color:{"#4ade80" if is_dark else "#166534"};margin-bottom:12px">'
        f'Tổng: {len(mssv_list)} MSSV | ✅ Tìm thấy: {len(found_list)} | ❌ Không có: {len(miss_list)} | Đang hiển thị: {total_disp} dòng'
        f'</div>',
        unsafe_allow_html=True
    )

    # Table
    if df.empty:
        st.info('Không có kết quả phù hợp.')
    else:
        st.dataframe(df, use_container_width=True, hide_index=True, height=520)

    # Export
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    df_summary, df_detail_exp = dl.build_export_data(mssv_list, results)
    excel_bytes = dl.to_excel_bytes(df_summary, df_detail_exp)
    st.download_button(
        label='⬇️ Xuất file Excel kết quả',
        data=excel_bytes,
        file_name='decision_lookup_result.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        use_container_width=True,
    )

st.markdown('</div>', unsafe_allow_html=True)
