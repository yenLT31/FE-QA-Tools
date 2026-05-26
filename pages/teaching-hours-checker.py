"""
Teaching Hours Checker - Giao diện Streamlit
Kiểm soát giờ dạy GV: đối chiếu Lịch kỳ FAP, Teaching Summaries, Phiếu chấm công ĐT
FPT Education QA Department
© 2026 YenLT31
"""

import streamlit as st
import sys
import os

# Thêm path để import scripts
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts.teaching_hours_checker import (
    read_lich_ky,
    read_teaching_summaries,
    read_cham_cong,
    read_danh_sach_gv,
    doi_sanh_gio_day,
    get_wasnot_taken_detail,
    calculate_gio_co_huu,
    export_to_excel
)

# ============================================================
# CẤU HÌNH TRANG
# ============================================================
st.set_page_config(
    page_title="Teaching Hours Checker",
    page_icon="⏱️",
    layout="wide"
)

# ============================================================
# CUSTOM CSS
# ============================================================
def load_css():
    st.markdown("""
    <style>
        /* Header */
        .main-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 4px;
        }
        .main-header h1 {
            font-size: 1.8rem;
            margin: 0;
        }
        .main-description {
            color: #6b7280;
            font-size: 0.95rem;
            margin-bottom: 20px;
        }
        
        /* Step sections */
        .step-section {
            background: var(--background-color, #f8fafc);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            border: 1px solid var(--border-color, #e2e8f0);
        }
        .step-number {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: #10b981;
            color: white;
            font-weight: 700;
            font-size: 0.85rem;
            margin-right: 10px;
        }
        .step-title {
            font-size: 1.1rem;
            font-weight: 600;
            display: inline;
        }
        .step-desc {
            color: #6b7280;
            font-size: 0.85rem;
            margin-top: 4px;
            margin-bottom: 16px;
        }
        
        /* Upload area */
        .upload-label {
            font-weight: 600;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }
        
        /* Button */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #059669, #047857);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        }
        
        /* Warning */
        .warning-box {
            background: #fef3c7;
            border: 1px solid #f59e0b;
            border-radius: 8px;
            padding: 12px 16px;
            color: #92400e;
            font-size: 0.9rem;
            margin-bottom: 12px;
        }
        
        /* Success */
        .success-box {
            background: #d1fae5;
            border: 1px solid #10b981;
            border-radius: 8px;
            padding: 12px 16px;
            color: #065f46;
            font-size: 0.9rem;
            margin-bottom: 12px;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            padding-top: 1rem;
        }
        .sidebar-title {
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 2px;
        }
        .sidebar-subtitle {
            font-size: 0.8rem;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .guide-box {
            background: rgba(16, 185, 129, 0.05);
            border: 1px solid rgba(16, 185, 129, 0.2);
            border-radius: 8px;
            padding: 12px;
            margin-top: 12px;
        }
        .guide-box p {
            font-size: 0.82rem;
            margin: 4px 0;
        }
        .security-box {
            background: rgba(245, 158, 11, 0.08);
            border: 1px solid rgba(245, 158, 11, 0.3);
            border-radius: 8px;
            padding: 12px;
            margin-top: 12px;
        }
        .security-box p {
            font-size: 0.82rem;
            margin: 2px 0;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 8px 20px;
            border-radius: 8px;
            font-weight: 600;
        }
    </style>
    """, unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div>
            <div class="sidebar-title">⏱️ Teaching Hours Checker</div>
            <div class="sidebar-subtitle">KIỂM SOÁT GIỜ DẠY GV</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Toggle sáng/tối
        st.markdown("**GIAO DIỆN**")
        theme = st.radio(
            "Chọn giao diện",
            ["☀️ Sáng", "🌙 Tối"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Hướng dẫn nhanh
        st.markdown("""
        <div class="guide-box">
            <p><strong>HƯỚNG DẪN NHANH</strong></p>
            <p>① Upload file(s) Lịch kỳ</p>
            <p>② Upload file(s) Teaching Summaries</p>
            <p>③ Upload file(s) Chấm công ĐT</p>
            <p>④ Upload file Danh sách GV</p>
            <p>⑤ Bấm "Bắt đầu kiểm tra"</p>
            <p>⑥ Xem kết quả & tải báo cáo</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Bảo mật
        st.markdown("""
        <div class="security-box">
            <p>🔒 <strong>Bảo mật dữ liệu</strong></p>
            <p>Mọi dữ liệu xử lý 100% tại local.</p>
            <p>Không gửi lên server.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("🏠 [Trang chủ](/)")
        st.markdown("---")
        st.markdown("""<p style="font-size:0.75rem; color:#6b7280;">© 2026 YenLT31<br>FPT Education QA Department</p>""", unsafe_allow_html=True)


# ============================================================
# MAIN CONTENT
# ============================================================
def render_main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>⏱️ Teaching Hours Checker</h1>
    </div>
    <p class="main-description">Kiểm soát giờ dạy GV — Đối chiếu Lịch kỳ, FAP Teaching Summaries & Phiếu chấm công ĐT</p>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab_config, tab_result = st.tabs(["⚙️ Cấu hình", "📊 Kết quả"])
    
    with tab_config:
        render_config_tab()
    
    with tab_result:
        render_result_tab()


def render_config_tab():
    # ============ STEP 01: Upload files kiểm soát giờ dạy ============
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:4px; margin-top:10px;">
        <span class="step-number">01</span>
        <span class="step-title">Tải lên file kiểm soát giờ dạy</span>
    </div>
    <p class="step-desc">Upload các file Lịch kỳ, Teaching Summaries, Chấm công và Danh sách GV</p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="upload-label">📋 FILE LỊCH KỲ FAP</p>', unsafe_allow_html=True)
        files_lich_ky = st.file_uploader(
            "Upload file(s) Lịch kỳ",
            type=['xlsx', 'xls'],
            accept_multiple_files=True,
            key="lich_ky",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown('<p class="upload-label">📄 FILE TEACHING SUMMARIES</p>', unsafe_allow_html=True)
        files_teaching = st.file_uploader(
            "Upload file(s) Teaching Summaries",
            type=['xlsx', 'xls'],
            accept_multiple_files=True,
            key="teaching_summaries",
            label_visibility="collapsed"
        )
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<p class="upload-label">📑 FILE CHẤM CÔNG ĐT</p>', unsafe_allow_html=True)
        files_cham_cong = st.file_uploader(
            "Upload file(s) Chấm công ĐT",
            type=['xlsx', 'xls'],
            accept_multiple_files=True,
            key="cham_cong",
            label_visibility="collapsed"
        )
    
    with col4:
        st.markdown('<p class="upload-label">👥 FILE DANH SÁCH GV</p>', unsafe_allow_html=True)
        file_gv = st.file_uploader(
            "Upload file Danh sách GV",
            type=['xlsx', 'xls'],
            accept_multiple_files=False,
            key="danh_sach_gv",
            label_visibility="collapsed"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ STEP 02: Upload file tính giờ cơ hữu ============
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:4px;">
        <span class="step-number">02</span>
        <span class="step-title">Tải lên file tính giờ dạy cơ hữu HK</span>
    </div>
    <p class="step-desc">Upload file Lịch kỳ toàn kỳ (dùng riêng cho tính giờ cơ hữu)</p>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="upload-label">📋 FILE LỊCH KỲ TOÀN KỲ (CƠ HỮU)</p>', unsafe_allow_html=True)
    files_co_huu = st.file_uploader(
        "Upload file Lịch kỳ toàn kỳ",
        type=['xlsx', 'xls'],
        accept_multiple_files=True,
        key="lich_ky_co_huu",
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ STEP 03: Bắt đầu kiểm tra ============
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:4px;">
        <span class="step-number">03</span>
        <span class="step-title">Bắt đầu kiểm tra</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Kiểm tra điều kiện
    can_run = files_lich_ky and files_teaching and files_cham_cong and file_gv
    
    if not can_run:
        st.markdown("""
        <div class="warning-box">
            ⚠️ Cần upload: file Lịch kỳ, Teaching Summaries, Chấm công ĐT và Danh sách GV
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("📊 Bắt đầu kiểm tra", disabled=not can_run, use_container_width=True):
        run_check(files_lich_ky, files_teaching, files_cham_cong, file_gv, files_co_huu)


def run_check(files_lich_ky, files_teaching, files_cham_cong, file_gv, files_co_huu):
    """
    Chạy toàn bộ logic kiểm tra.
    """
    with st.spinner("Đang xử lý dữ liệu..."):
        try:
            # Đọc dữ liệu
            progress = st.progress(0, text="Đọc file Lịch kỳ...")
            df_lich_ky = read_lich_ky(files_lich_ky)
            
            progress.progress(20, text="Đọc file Teaching Summaries...")
            df_teaching = read_teaching_summaries(files_teaching)
            
            progress.progress(40, text="Đọc file Chấm công ĐT...")
            df_cham_cong = read_cham_cong(files_cham_cong)
            
            progress.progress(60, text="Đọc file Danh sách GV...")
            df_gv = read_danh_sach_gv(file_gv)
            
            # Kiểm tra dữ liệu đọc được
            if df_lich_ky.empty:
                st.error("❌ Không đọc được dữ liệu từ file Lịch kỳ!")
                return
            if df_teaching.empty:
                st.error("❌ Không đọc được dữ liệu từ file Teaching Summaries!")
                return
            if df_cham_cong.empty:
                st.error("❌ Không đọc được dữ liệu từ file Chấm công!")
                return
       # Đối sánh
        progress.progress(70, text="Đang đối sánh giờ dạy...")
        st.write("DEBUG LK:", len(df_lich_ky), "rows")
        st.write("DEBUG CC:", len(df_cham_cong), "rows")
        st.write("DEBUG TS:", len(df_teaching), "rows")
        st.write("DEBUG GV:", len(df_gv), "rows")
        if not df_lich_ky.empty:
            st.write("Date dtype:", df_lich_ky['Date'].dtype)
            st.write("Date head:", df_lich_ky['Date'].head(3).tolist())
            st.write("Lecturer head:", df_lich_ky['Lecturer'].head(3).tolist())
        if not df_cham_cong.empty:
            st.write("CC Thang:", df_cham_cong['Thang'].unique().tolist())
            st.write("CC FromDate:", df_cham_cong['FromDate'].iloc[0])
            st.write("CC ToDate:", df_cham_cong['ToDate'].iloc[0])
        st.stop()
        df_doi_sanh = doi_sanh_gio_day(df_lich_ky, df_teaching, df_cham_cong, df_gv)
            
            
            progress.progress(100, text="Hoàn tất!")
            
            # Lưu kết quả vào session state
            st.session_state['doi_sanh'] = df_doi_sanh
            st.session_state['wasnot_taken'] = df_wasnot
            st.session_state['co_huu'] = df_co_huu
            st.session_state['check_done'] = True
            
            st.markdown("""
            <div class="success-box">
                ✅ Kiểm tra hoàn tất! Chuyển sang tab "Kết quả" để xem chi tiết.
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Lỗi xử lý: {str(e)}")
            import traceback
            st.code(traceback.format_exc())


def render_result_tab():
    """
    Hiển thị kết quả kiểm tra.
    """
    if not st.session_state.get('check_done', False):
        st.info("Chưa có kết quả. Vui lòng upload file và bấm 'Bắt đầu kiểm tra' ở tab Cấu hình.")
        return
    
    df_doi_sanh = st.session_state.get('doi_sanh', None)
    df_wasnot = st.session_state.get('wasnot_taken', None)
    df_co_huu = st.session_state.get('co_huu', None)
    
    # ===== Thống kê tổng quan =====
    if df_doi_sanh is not None and not df_doi_sanh.empty:
        total_gv = len(df_doi_sanh)
        total_true = len(df_doi_sanh[df_doi_sanh['KetQua'] == True])
        total_false = len(df_doi_sanh[df_doi_sanh['KetQua'] == False])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Tổng GV kiểm tra", total_gv)
        col2.metric("Khớp (TRUE)", total_true, delta=None)
        col3.metric("Lệch (FALSE)", total_false, delta=None, delta_color="inverse")
        
        st.markdown("---")
    
    # ===== Sheet 1: Đối sánh =====
    st.markdown("### 📊 Đối sánh giờ dạy")
    if df_doi_sanh is not None and not df_doi_sanh.empty:
        # Highlight FALSE
        def highlight_false(row):
            if row.get('KetQua') == False:
                return ['background-color: #fee2e2'] * len(row)
            return [''] * len(row)
        
        st.dataframe(
            df_doi_sanh.style.apply(highlight_false, axis=1),
            use_container_width=True,
            height=400
        )
    else:
        st.warning("Không có dữ liệu đối sánh.")
    
    st.markdown("---")
    
    # ===== Sheet 2: WasNot Taken =====
    st.markdown("### 📋 Chi tiết WasNot Taken")
    if df_wasnot is not None and not df_wasnot.empty:
        st.dataframe(df_wasnot, use_container_width=True, height=300)
    else:
        st.info("Không có GV nào bị WasNot Taken.")
    
    st.markdown("---")
    
    # ===== Sheet 3: Giờ cơ hữu =====
    if df_co_huu is not None and not df_co_huu.empty:
        st.markdown("### 🏫 Giờ dạy cơ hữu HK")
        
        tong_co_huu = df_co_huu[df_co_huu['LaCoHuu'] == True]['TongGio'].sum()
        tong_all = df_co_huu['TongGio'].sum()
        ti_le = (tong_co_huu / tong_all * 100) if tong_all > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Tổng giờ cơ hữu", f"{tong_co_huu:,.1f}h")
        col2.metric("Tổng giờ tất cả", f"{tong_all:,.1f}h")
        col3.metric("Tỉ lệ cơ hữu", f"{ti_le:.1f}%")
        
        st.dataframe(df_co_huu, use_container_width=True, height=300)
        st.markdown("---")
    
    # ===== Xuất Excel =====
    st.markdown("### 💾 Tải báo cáo")
    excel_file = export_to_excel(
        df_doi_sanh if df_doi_sanh is not None else pd.DataFrame(),
        df_wasnot if df_wasnot is not None else pd.DataFrame(),
        df_co_huu
    )
    
    st.download_button(
        label="📥 Tải file Excel báo cáo",
        data=excel_file,
        file_name="Teaching_Hours_Check_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.document",
        use_container_width=True
    )


# ============================================================
# RUN APP
# ============================================================
load_css()
render_sidebar()
render_main()
