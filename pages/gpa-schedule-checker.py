import streamlit as st
import importlib.util
import pandas as pd
import os
import hashlib
from datetime import datetime
from io import BytesIO

# ============================================================
#  LOAD LOGIC
# ============================================================
SCRIPT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'scripts', 'gpa_schedule_checker.py')
)
spec = importlib.util.spec_from_file_location("gpa_schedule_checker", SCRIPT_PATH)
logic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(logic)

# ============================================================
#  PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="GPA Schedule Checker | FE QA Tools",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
#  THEME
# ============================================================
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

DARK = dict(
    bg="#080D18", card="#0F1628", card2="#162040", border="#1E2D4A",
    text="#E8EDF5", muted="#8892A4", accent="#00D4AA", accent_dim="#00A882",
    green="#22C55E", gbg="#052E16", gtxt="#22C55E",
    red="#EF4444", rbg="#1C1012", rtxt="#F87171",
    yellow="#EAB308", ybg="#1A1800", ytxt="#FACC15",
    blue="#3B82F6", bbg="#0C1529", btxt="#60A5FA",
    orange="#F97316", obg="#1A1008", otxt="#FB923C",
)
LIGHT = dict(
    bg="#F0F4F8", card="#FFFFFF", card2="#F7F9FC", border="#E2E8F0",
    text="#1A2540", muted="#64748B", accent="#0A9E7F", accent_dim="#077A62",
    green="#16A34A", gbg="#DCFCE7", gtxt="#15803D",
    red="#DC2626", rbg="#FEF2F2", rtxt="#DC2626",
    yellow="#CA8A04", ybg="#FEFCE8", ytxt="#A16207",
    blue="#2563EB", bbg="#EFF6FF", btxt="#1D4ED8",
    orange="#EA580C", obg="#FFF7ED", otxt="#C2410C",
)
T = DARK if st.session_state.theme == "dark" else LIGHT

# ============================================================
#  SESSION STATE
# ============================================================
defaults = {
    "gpa_result_excel": None,
    "gpa_summary_excel": None,
    "gpa_processed_signature": None,
    "gpa_done": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if "gpa_upload_key_version" not in st.session_state:
    st.session_state.gpa_upload_key_version = 0


def reset_gpa_session():
    """Xóa kết quả và làm mới file uploader để tránh giữ file cũ sau reset."""
    for k, v in defaults.items():
        st.session_state[k] = v
    st.session_state.gpa_upload_key_version += 1


def get_upload_key(file_type):
    return f"{file_type}_upload_{st.session_state.gpa_upload_key_version}"


def get_uploaded_file_hash(uploaded_file):
    return hashlib.sha256(uploaded_file.getvalue()).hexdigest()


def get_input_signature(schedule_files, gpa_files):
    """Nhận diện bộ file upload hiện tại để biết kết quả đã cũ hay chưa."""
    schedule_hashes = sorted(get_uploaded_file_hash(f) for f in (schedule_files or []))
    gpa_hashes = sorted(get_uploaded_file_hash(f) for f in (gpa_files or []))
    return tuple(schedule_hashes), tuple(gpa_hashes)


def get_current_uploads_from_state():
    schedule_files = st.session_state.get(get_upload_key("schedule"), []) or []
    gpa_files = st.session_state.get(get_upload_key("gpa"), []) or []
    return schedule_files, gpa_files


def is_result_stale():
    if not st.session_state.gpa_done or not st.session_state.gpa_processed_signature:
        return False

    schedule_files, gpa_files = get_current_uploads_from_state()
    if not schedule_files and not gpa_files:
        return False

    return get_input_signature(schedule_files, gpa_files) != st.session_state.gpa_processed_signature

# ============================================================
#  CSS
# ============================================================
st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">',
    unsafe_allow_html=True,
)

st.markdown(f"""<style>
.stApp {{ background: {T['bg']} !important; }}
.block-container {{ padding-top: 1rem !important; max-width: 1200px !important; }}
[data-testid="stSidebar"] {{
    background: {T['card']} !important;
    border-right: 1px solid {T['border']} !important;
}}
[data-testid="stSidebarNav"] {{ display: none !important; }}
.stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
.stMarkdown li, .stMarkdown span, label {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: {T['text']} !important;
}}
.stTabs [data-baseweb="tab-list"] {{
    gap: 0; background: {T['card']} !important; border-radius: 12px;
    padding: 4px; border: 1px solid {T['border']};
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 8px; padding: 8px 24px;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600; font-size: 13px; color: {T['muted']} !important;
    border: none !important;
}}
.stTabs [aria-selected="true"] {{
    background: {T['accent']} !important; color: #080D18 !important;
}}
[data-testid="stFileUploader"] section {{
    border: 2px dashed {T['border']} !important; border-radius: 12px !important;
    background: {T['card2']} !important; padding: 20px !important;
}}
[data-testid="stFileUploader"] section:hover {{ border-color: {T['accent']} !important; }}
.stButton > button {{
    background: {T['accent']} !important; color: #080D18 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important; border: none !important; border-radius: 10px !important;
    padding: 12px 28px !important;
}}
.stButton > button:hover {{ background: {T['accent_dim']} !important; }}
.stDownloadButton > button {{
    background: {T['card']} !important; color: {T['accent']} !important;
    border: 1px solid {T['accent']} !important; border-radius: 10px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
}}
.stDownloadButton > button:hover {{
    background: {T['accent']} !important; color: #080D18 !important;
}}
[data-testid="stDataFrame"] {{
    border: 1px solid {T['border']} !important; border-radius: 12px !important;
}}
</style>""", unsafe_allow_html=True)

# ============================================================
#  HELPERS
# ============================================================
def step_badge(num, title, desc=""):
    desc_html = (
        f'<div style="font-size:12.5px;color:{T["muted"]};margin-top:3px">{desc}</div>'
        if desc else ""
    )
    html = (
        '<div style="display:flex;align-items:flex-start;gap:12px;margin-bottom:16px">'
        f'<span style="display:inline-flex;align-items:center;justify-content:center;'
        f'width:30px;height:30px;border-radius:9px;background:{T["accent"]};color:#080D18;'
        f'font-size:13px;font-weight:800;flex-shrink:0">{num:02d}</span>'
        '<div>'
        f'<div style="font-size:17px;font-weight:700;color:{T["text"]}">{title}</div>'
        f'{desc_html}'
        '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def card_metric(label, value, color, bg):
    return f"""
    <div style="background:{bg};border:1px solid {color}33;border-radius:12px;padding:18px">
        <div style="font-size:10px;color:{color};font-weight:700;text-transform:uppercase;
                    letter-spacing:.8px;margin-bottom:6px">{label}</div>
        <div style="font-size:30px;font-weight:800;color:{color}">{value}</div>
    </div>"""


def divider():
    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:28px 0"></div>',
                unsafe_allow_html=True)


# ============================================================
#  SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(f"""
    <div style="padding:16px 0 20px;border-bottom:1px solid {T['border']};margin-bottom:20px">
        <div style="display:flex;align-items:center;gap:10px">
            <div style="width:36px;height:36px;border-radius:10px;
                        background:linear-gradient(135deg,{T['accent']},{T['accent_dim']});
                        display:flex;align-items:center;justify-content:center;font-size:18px">📋</div>
            <div>
                <div style="font-size:14px;font-weight:800;color:{T['accent']}">GPA Schedule Checker</div>
                <div style="font-size:10px;color:{T['muted']};font-weight:600;letter-spacing:.8px;
                            text-transform:uppercase">Đối sánh GPA & Lịch kỳ</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"<p style='font-size:10px;color:{T['muted']};font-weight:700;letter-spacing:.9px;\
                text-transform:uppercase;margin-bottom:8px'>Giao diện</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("☀ Sáng", use_container_width=True, key="btn_light"):
            st.session_state.theme = "light"
            st.rerun()
    with c2:
        if st.button("🌙 Tối", use_container_width=True, key="btn_dark"):
            st.session_state.theme = "dark"
            st.rerun()

    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:18px 0"></div>',
                unsafe_allow_html=True)

    st.markdown(f"""
    <p style="font-size:10px;color:{T['muted']};font-weight:700;letter-spacing:.9px;\
              text-transform:uppercase;margin-bottom:10px">Hướng dẫn nhanh</p>
    <div style="font-size:12px;color:{T['muted']};line-height:2.1">
        <div>① Upload file(s) Lịch kỳ</div>
        <div>② Upload file(s) GPA Feedback</div>
        <div>③ Bấm "Bắt đầu đối sánh"</div>
        <div>④ Tải báo cáo kết quả</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:18px 0"></div>',
                unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:{T['accent']}11;border:1px solid {T['accent']}33;
                border-radius:10px;padding:12px">
        <div style="font-size:12px;font-weight:700;color:{T['accent']};margin-bottom:4px">
            🔒 Bảo mật dữ liệu</div>
        <div style="font-size:11px;color:{T['muted']};line-height:1.5">
            Dữ liệu được xử lý tạm thời trong phiên làm việc của ứng dụng.</div>
            <div> Công cụ không chủ động lưu file PDF, MSSV hoặc kết quả tra cứu vào cơ sở dữ liệu; sau khi tải kết quả, người dùng có thể làm mới phiên để xoá dữ liệu tạm.
    </div>""", unsafe_allow_html=True)

    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:18px 0"></div>',
                unsafe_allow_html=True)

    st.page_link("app.py", label="🏠  Trang chủ")

    st.markdown(f"""
    <div style="margin-top:24px;padding-top:14px;border-top:1px solid {T['border']};text-align:center">
        <div style="font-size:11px;color:{T['muted']}">
            © 2026 <strong style="color:{T['accent']}">YenLT31</strong></div>
    </div>""", unsafe_allow_html=True)

# ============================================================
#  HEADER
# ============================================================
st.markdown(f"""
<div style="margin-bottom:12px">
    <div style="display:flex;align-items:center;gap:14px">
        <div style="width:44px;height:44px;border-radius:14px;
                    background:linear-gradient(135deg,{T['accent']},{T['accent_dim']});
                    display:flex;align-items:center;justify-content:center;font-size:22px">📋</div>
        <div>
            <h1 style="font-size:26px;font-weight:800;color:{T['text']};margin:0;line-height:1.2">
                GPA Schedule Checker</h1>
            <p style="font-size:13px;color:{T['muted']};margin:0">
                Đối sánh lịch kỳ và GPA – kiểm tra GV đủ 30%, phát hiện lớp GPA dưới 3.4, kiểm tra tỷ lệ phản hồi</p>
        </div>
    </div>
</div>""", unsafe_allow_html=True)

# ============================================================
#  DOWNLOAD BUTTONS (hàng gọn ngay dưới header, căn phải)
# ============================================================
result_stale = is_result_stale()

if st.session_state.gpa_done and not result_stale:
    today_str = datetime.now().strftime('%Y%m%d')
    _, col_dl1, col_dl2, col_dl3 = st.columns([4, 1.5, 1.5, 0.6])
    with col_dl1:
        st.download_button(
            label="📥 Result GPA",
            data=st.session_state.gpa_result_excel,
            file_name=logic.generate_output_filename(),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
    with col_dl2:
        st.download_button(
            label="📥 Tổng hợp GPA",
            data=st.session_state.gpa_summary_excel,
            file_name=f"{today_str}-Tong hop GPA.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
    with col_dl3:
        if st.button("🔄", use_container_width=True, key="btn_reset_top", help="Làm lại đối sánh mới"):
            reset_gpa_session()
            st.rerun()
elif result_stale:
    st.markdown(f"""<div style="background:{T['ybg']};border:1px solid {T['yellow']}55;
        border-radius:12px;padding:14px 16px;margin:12px 0 18px">
        <span style="font-size:13px;color:{T['ytxt']}">
            ⚠️ Bộ file upload đã thay đổi sau lần đối sánh gần nhất.
            Kết quả cũ đã được ẩn để tránh tải nhầm. Vui lòng bấm
            <strong>Bắt đầu đối sánh</strong> để tạo kết quả mới.</span>
    </div>""", unsafe_allow_html=True)

# ============================================================
#  MAIN WORKFLOW
# ============================================================
with st.container():
    step_badge(1, "Tải lên file", "Upload file Lịch kỳ và các file GPA Feedback")

    col_schedule, col_gpa = st.columns(2)
    with col_schedule:
        st.markdown(f"<p style='font-size:11px;color:{T['muted']};font-weight:700;\
                    text-transform:uppercase;margin-bottom:8px'>📅 File Lịch kỳ</p>",
                    unsafe_allow_html=True)
        schedule_files = st.file_uploader(
            "Upload Lịch kỳ (có cột: GroupName, SubjectCode, Lecturer...)",
            type=["xlsx", "xls"],
            accept_multiple_files=True,
            key=get_upload_key("schedule"),
            label_visibility="collapsed",
        )
    with col_gpa:
        st.markdown(f"<p style='font-size:11px;color:{T['muted']};font-weight:700;\
                    text-transform:uppercase;margin-bottom:8px'>📊 File GPA Feedback</p>",
                    unsafe_allow_html=True)
        gpa_files = st.file_uploader(
            "Upload GPA (có cột: GV, Lớp, Môn, GPA, Comments...)",
            type=["xlsx", "xls"],
            accept_multiple_files=True,
            key=get_upload_key("gpa"),
            label_visibility="collapsed",
        )

    result_stale = is_result_stale()

    # Xác nhận dữ liệu
    if schedule_files or gpa_files:
        divider()
        step_badge(2, "Xác nhận dữ liệu")
        mc1, mc2, mc3 = st.columns(3)

        with mc1:
            sch_count = len(schedule_files) if schedule_files else 0
            if sch_count > 0:
                st.markdown(f"""<div style="background:{T['card']};border:1px solid {T['border']};
                    border-radius:12px;padding:18px">
                    <div style="font-size:10px;color:{T['muted']};font-weight:700;
                        text-transform:uppercase;margin-bottom:6px">File Lịch kỳ</div>
                    <div style="font-size:30px;font-weight:800;color:{T['accent']}">{sch_count}</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style="background:{T['card']};border:2px dashed {T['border']};
                    border-radius:12px;padding:18px;text-align:center">
                    <div style="font-size:20px;margin-bottom:4px">📅</div>
                    <div style="font-size:12px;color:{T['muted']}">Chưa upload file Lịch kỳ</div>
                </div>""", unsafe_allow_html=True)

        with mc2:
            gpa_count = len(gpa_files) if gpa_files else 0
            if gpa_count > 0:
                st.markdown(f"""<div style="background:{T['card']};border:1px solid {T['border']};
                    border-radius:12px;padding:18px">
                    <div style="font-size:10px;color:{T['muted']};font-weight:700;
                        text-transform:uppercase;margin-bottom:6px">File GPA</div>
                    <div style="font-size:30px;font-weight:800;color:{T['blue']}">{gpa_count}</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style="background:{T['card']};border:2px dashed {T['border']};
                    border-radius:12px;padding:18px;text-align:center">
                    <div style="font-size:20px;margin-bottom:4px">📊</div>
                    <div style="font-size:12px;color:{T['muted']}">Chưa upload file GPA</div>
                </div>""", unsafe_allow_html=True)

        with mc3:
            ready = bool(schedule_files and gpa_files)
            st.markdown(f"""<div style="background:{T['card']};border:1px solid {T['border']};
                border-radius:12px;padding:18px">
                <div style="font-size:10px;color:{T['muted']};font-weight:700;
                    text-transform:uppercase;margin-bottom:6px">Trạng thái</div>
                <div style="font-size:30px;margin-bottom:2px">{"✅" if ready else "⏳"}</div>
                <div style="font-size:11px;color:{T['green'] if ready else T['yellow']};font-weight:600">
                    {"Sẵn sàng đối sánh" if ready else "Đang chờ dữ liệu"}</div>
            </div>""", unsafe_allow_html=True)

    divider()
    step_badge(3, "Bắt đầu đối sánh")

    can_run = bool(schedule_files and gpa_files)
    if not can_run:
        st.markdown(f"""<div style="background:{T['ybg']};border:1px solid {T['yellow']}33;
            border-radius:10px;padding:12px 16px">
            <span style="font-size:13px;color:{T['ytxt']}">
                ⚠️ Cần upload: file Lịch kỳ và file(s) GPA Feedback</span>
        </div>""", unsafe_allow_html=True)

    run_label = "🔁  Chạy lại đối sánh" if result_stale else "📋  Bắt đầu đối sánh"
    if st.button(run_label, use_container_width=True,
                 disabled=not can_run, key="btn_run"):
        progress = st.progress(0, text="Đang chuẩn bị...")

        # Bước 1: Gộp lịch kỳ
        progress.progress(0.1, text="Đang gộp file lịch kỳ...")
        schedule_df, schedule_skipped = logic.merge_schedule_files(schedule_files)

        # Bước 2: Gộp GPA
        progress.progress(0.3, text="Đang gộp file GPA...")
        gpa_df, gpa_skipped = logic.merge_gpa_files(gpa_files)

        # Không hiển thị tên file/sheet hoặc chi tiết dữ liệu trên giao diện.
        all_skipped = schedule_skipped + gpa_skipped
        if all_skipped:
            st.warning(f"⚠️ Có {len(all_skipped)} sheet/file không phù hợp và đã được bỏ qua.")

        if schedule_df.empty:
            st.error("❌ File lịch kỳ không có dữ liệu.")
            st.stop()
        if gpa_df.empty:
            st.error("❌ File GPA không có dữ liệu.")
            st.stop()

        # Bước 3: Tính tỷ lệ GV
        progress.progress(0.4, text="Đang tính tỷ lệ GV...")
        lecturer_pct = logic.calculate_lecturer_percentage(schedule_df)

        # Bước 4: Kiểm tra tỷ lệ phản hồi
        progress.progress(0.5, text="Đang kiểm tra tỷ lệ phản hồi...")
        gpa_with_status, low_response_df, response_stats = logic.check_response_rate(gpa_df)

        # Bước 5: Tạo báo cáo đối sánh
        progress.progress(0.7, text="Đang tạo báo cáo...")
        report1, report2, report3, error = logic.generate_reports(schedule_df, gpa_df)

        if error:
            st.error(f"❌ {error}")
            st.stop()

        # Bước 6: Tạo tổng kết
        progress.progress(0.85, text="Đang tạo tổng kết...")

        # Tính thêm thống kê GPA
        gpa_score_col = None
        for col in gpa_df.columns:
            if col.upper() == 'GPA':
                gpa_score_col = col
                break

        total_gpa_classes = len(gpa_df)
        gpa_pass = 0
        gpa_low = 0
        if gpa_score_col:
            gpa_df[gpa_score_col] = pd.to_numeric(gpa_df[gpa_score_col], errors='coerce')
            gpa_pass = len(gpa_df[gpa_df[gpa_score_col] >= 3.4])
            gpa_low = len(gpa_df[gpa_df[gpa_score_col] < 3.4])

        gpa_stats = {
            'total_gpa_classes': total_gpa_classes,
            'gpa_pass': gpa_pass,
            'gpa_low': gpa_low,
            'eligible_no_gpa': len(report2) if report2 is not None and not report2.empty else 0,
            'not_eligible_has_gpa': len(report3) if report3 is not None and not report3.empty else 0,
            'total_gv': len(lecturer_pct),
            'low_response': response_stats.get('classes_fail', 0),
            'success_rate': response_stats.get('success_rate', 0),
        }

        summary_df = logic.generate_summary(gpa_stats, response_stats)

        # Tạo file tải xuống ngay sau khi xử lý. Không lưu DataFrame kết quả
        # trong session và không hiển thị dữ liệu trên giao diện.
        result_excel = logic.export_reports_to_excel(
            report1,
            report2,
            report3,
            gpa_with_status,
            low_response_df,
            summary_df,
        )

        output_gpa_only = BytesIO()
        with pd.ExcelWriter(output_gpa_only, engine='openpyxl') as writer:
            gpa_with_status.to_excel(writer, sheet_name='Tổng hợp GPA', index=False)
        output_gpa_only.seek(0)

        st.session_state.gpa_result_excel = result_excel
        st.session_state.gpa_summary_excel = output_gpa_only.getvalue()
        st.session_state.gpa_processed_signature = get_input_signature(schedule_files, gpa_files)
        st.session_state.gpa_done = True

        progress.progress(1.0, text="✅ Hoàn tất!")
        st.rerun()

if st.session_state.gpa_done and not result_stale:
    divider()
    st.markdown(f"""<div style="background:{T['gbg']};border:1px solid {T['green']}33;
        border-radius:12px;padding:24px;text-align:center;margin-top:24px">
        <div style="font-size:36px;margin-bottom:10px">✅</div>
        <div style="color:{T['gtxt']};font-size:16px;font-weight:700">
            Xử lý hoàn tất</div>
        <div style="color:{T['muted']};font-size:12px;margin-top:6px">
            Dữ liệu kết quả không được hiển thị trên giao diện.<br>
            Sử dụng các nút tải xuống phía trên để nhận file Excel.</div>
    </div>""", unsafe_allow_html=True)

    divider()
    if st.button("🔄  Làm lại đối sánh mới", key="btn_reset_bottom", use_container_width=True):
        reset_gpa_session()
        st.rerun()
