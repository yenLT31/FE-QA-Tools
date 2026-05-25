import streamlit as st
import importlib.util
import pandas as pd
import os
import io

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
    page_icon="QA",
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
    "gpa_report1": None, "gpa_report2": None, "gpa_report3": None,
    "gpa_report4": None, "gpa_low_response": None, "gpa_summary": None,
    "gpa_merged_df": None, "gpa_lecturer_pct": None,
    "gpa_done": False, "gpa_stats": {},
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

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
    st.markdown(f"""
    <div style="display:flex;align-items:flex-start;gap:12px;margin-bottom:16px">
        <span style="display:inline-flex;align-items:center;justify-content:center;
            width:30px;height:30px;border-radius:9px;background:{T['accent']};color:#080D18;
            font-size:13px;font-weight:800;flex-shrink:0">{num:02d}</span>
        <div>
            <div style="font-size:17px;font-weight:700;color:{T['text']}">{title}</div>
            {'<div style="font-size:12.5px;color:'+T['muted']+';margin-top:3px">'+desc+'</div>' if desc else ''}
        </div>
    </div>""", unsafe_allow_html=True)


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

    st.markdown(f"<p style='font-size:10px;color:{T['muted']};font-weight:700;letter-spacing:.9px;"
                f"text-transform:uppercase;margin-bottom:8px'>Giao diện</p>", unsafe_allow_html=True)
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
    <p style="font-size:10px;color:{T['muted']};font-weight:700;letter-spacing:.9px;
              text-transform:uppercase;margin-bottom:10px">Hướng dẫn nhanh</p>
    <div style="font-size:12px;color:{T['muted']};line-height:2.1">
        <div>① Upload file(s) Lịch kỳ</div>
        <div>② Upload file(s) GPA Feedback</div>
        <div>③ Bấm "Bắt đầu đối sánh"</div>
        <div>④ Xem kết quả & tải báo cáo</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:18px 0"></div>',
                unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:{T['accent']}11;border:1px solid {T['accent']}33;
                border-radius:10px;padding:12px">
        <div style="font-size:12px;font-weight:700;color:{T['accent']};margin-bottom:4px">
            🔒 Bảo mật dữ liệu</div>
        <div style="font-size:11px;color:{T['muted']};line-height:1.5">
            Mọi dữ liệu xử lý <strong>100% tại local</strong>.<br>Không gửi lên server.</div>
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
<div style="margin-bottom:28px">
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:6px">
        <div style="width:44px;height:44px;border-radius:14px;
                    background:linear-gradient(135deg,{T['accent']},{T['accent_dim']});
                    display:flex;align-items:center;justify-content:center;font-size:22px">📋</div>
        <div>
            <h1 style="font-size:26px;font-weight:800;color:{T['text']};margin:0;line-height:1.2">
                GPA Schedule Checker</h1>
            <p style="font-size:13px;color:{T['muted']};margin:0">
                Đối sánh lịch kỳ và GPA – kiểm tra GV đủ 30%, phát hiện lớp GPA dưới 3.4</p>
        </div>
    </div>
</div>""", unsafe_allow_html=True)


# ============================================================
#  TABS
# ============================================================
tabs = st.tabs(["⚙️  Cấu hình", "📊  Kết quả"])

# ── TAB 1: CẤU HÌNH ──────────────────────────────────────────
with tabs[0]:
    step_badge(1, "Tải lên file", "Upload file Lịch kỳ và các file GPA Feedback")

    col_schedule, col_gpa = st.columns(2)
    with col_schedule:
        st.markdown(f"<p style='font-size:11px;color:{T['muted']};font-weight:700;"
                    f"text-transform:uppercase;margin-bottom:8px'>📅 File Lịch kỳ</p>",
                    unsafe_allow_html=True)
        schedule_files = st.file_uploader(
            "Upload Lịch kỳ", type=["xlsx", "xls"],
            accept_multiple_files=True,
            key="schedule_upload", label_visibility="collapsed"
        )
    with col_gpa:
        st.markdown(f"<p style='font-size:11px;color:{T['muted']};font-weight:700;"
                    f"text-transform:uppercase;margin-bottom:8px'>📊 File GPA Feedback</p>",
                    unsafe_allow_html=True)
        gpa_files = st.file_uploader(
            "Upload GPA", type=["xlsx", "xls"],
            accept_multiple_files=True,
            key="gpa_upload", label_visibility="collapsed"
        )

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

    if st.button("📋  Bắt đầu đối sánh", use_container_width=True,
                 disabled=not can_run, key="btn_run"):
        progress = st.progress(0, text="Đang chuẩn bị...")

        progress.progress(0.1, text="Đang gộp file lịch kỳ...")
        schedule_df = logic.merge_schedule_files(schedule_files)

        progress.progress(0.3, text="Đang gộp file GPA...")
        gpa_df = logic.merge_gpa_files(gpa_files)

        if schedule_df.empty:
            st.error("❌ File lịch kỳ không có dữ liệu.")
            st.stop()
        if gpa_df.empty:
            st.error("❌ File GPA không có dữ liệu.")
            st.stop()

        progress.progress(0.5, text="Đang tính tỷ lệ GV...")
        lecturer_pct = logic.calculate_lecturer_percentage(schedule_df)

        progress.progress(0.7, text="Đang tạo báo cáo...")
        report1, report2, report3, report4, low_response, summary, error = logic.generate_reports(schedule_df, gpa_df)

        if error:
            st.error(f"❌ {error}")
            st.stop()

        # Lưu kết quả
        st.session_state.gpa_report1 = report1
        st.session_state.gpa_report2 = report2
        st.session_state.gpa_report3 = report3
        st.session_state.gpa_report4 = report4
        st.session_state.gpa_low_response = low_response
        st.session_state.gpa_summary = summary
        st.session_state.gpa_merged_df = gpa_df
        st.session_state.gpa_lecturer_pct = lecturer_pct
        st.session_state.gpa_done = True
        st.session_state.gpa_stats = {
            "gpa_low": len(report1) if report1 is not None and not report1.empty else 0,
            "eligible_no_gpa": len(report2) if report2 is not None and not report2.empty else 0,
            "not_eligible_has_gpa": len(report3) if report3 is not None and not report3.empty else 0,
            "gpa_not_in_schedule": len(report4) if report4 is not None and not report4.empty else 0,
            "low_response": len(low_response) if low_response is not None and not low_response.empty else 0,
            "total_gv": len(lecturer_pct),
        }

        progress.progress(1.0, text="✅ Hoàn tất!")
        st.rerun()

# ── TAB 2: KẾT QUẢ ───────────────────────────────────────────
with tabs[1]:
    if not st.session_state.gpa_done:
        st.markdown(f"""<div style="text-align:center;padding:80px 20px">
            <div style="font-size:52px;margin-bottom:16px">📭</div>
            <h3 style="font-size:18px;font-weight:700;color:{T['text']};margin-bottom:8px">
                Chưa có kết quả</h3>
            <p style="font-size:13px;color:{T['muted']}">
                Quay lại tab Cấu hình để upload file và bắt đầu đối sánh</p>
        </div>""", unsafe_allow_html=True)
    else:
        stats = st.session_state.gpa_stats
        report1 = st.session_state.gpa_report1
        report2 = st.session_state.gpa_report2
        report3 = st.session_state.gpa_report3
        report4 = st.session_state.gpa_report4
        low_response = st.session_state.gpa_low_response
        summary = st.session_state.gpa_summary
        gpa_merged_df = st.session_state.gpa_merged_df
        lecturer_pct = st.session_state.gpa_lecturer_pct

        # === NÚT TẢI ĐẶT TRÊN CÙNG ===
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            excel_merged = logic.export_gpa_merged(gpa_merged_df)
            st.download_button(
                label="📥  Tải Tổng hợp GPA (.xlsx)",
                data=excel_merged,
                file_name=logic.get_merged_filename(),
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        with col_dl2:
            excel_report = logic.export_reports_to_excel(
                report1, report2, report3, report4, low_response, summary
            )
            st.download_button(
                label="📥  Tải Result check GPA (.xlsx)",
                data=excel_report,
                file_name=logic.get_report_filename(),
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        # Metric cards
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-bottom:28px">
            {card_metric("GPA dưới 3.4", stats['gpa_low'], T['red'], T['rbg'])}
            {card_metric("Đủ 30% chưa lấy GPA", stats['eligible_no_gpa'], T['yellow'], T['ybg'])}
            {card_metric("Dưới 30% bị lấy GPA", stats['not_eligible_has_gpa'], T['orange'], T['obg'])}
            {card_metric("Không có trong lịch kỳ", stats['gpa_not_in_schedule'], T['blue'], T['bbg'])}
            {card_metric("Phản hồi dưới 60%", stats['low_response'], T['red'], T['rbg'])}
        </div>""", unsafe_allow_html=True)

        # Detail tabs
        detail_tabs = st.tabs([
            f"📋 Tổng kết",
            f"🔴 GPA dưới 3.4 ({stats['gpa_low']})",
            f"🟡 Đủ 30% chưa lấy GPA ({stats['eligible_no_gpa']})",
            f"🟠 Dưới 30% bị lấy GPA ({stats['not_eligible_has_gpa']})",
            f"🔵 Không có trong lịch kỳ ({stats['gpa_not_in_schedule']})",
            f"⚪ Phản hồi dưới 60% ({stats['low_response']})",
            "📊 Tỷ lệ % GV theo lớp"
        ])

        with detail_tabs[0]:
            if summary is not None and not summary.empty:
                st.dataframe(summary, use_container_width=True, hide_index=True)
            else:
                st.info("Không có dữ liệu tổng kết.")

        with detail_tabs[1]:
            if report1 is not None and not report1.empty:
                st.dataframe(report1, use_container_width=True, height=500, hide_index=True)
            else:
                st.markdown(f"""<div style="background:{T['gbg']};border:1px solid {T['green']}33;
                    border-radius:10px;padding:16px;text-align:center">
                    <span style="color:{T['gtxt']};font-size:13px;font-weight:600">
                        ✅ Không có lớp nào GPA dưới 3.4</span>
                </div>""", unsafe_allow_html=True)

        with detail_tabs[2]:
            if report2 is not None and not report2.empty:
                st.dataframe(report2, use_container_width=True, height=500, hide_index=True)
            else:
                st.markdown(f"""<div style="background:{T['gbg']};border:1px solid {T['green']}33;
                    border-radius:10px;padding:16px;text-align:center">
                    <span style="color:{T['gtxt']};font-size:13px;font-weight:600">
                        ✅ Tất cả GV đủ ĐK đã được lấy GPA</span>
                </div>""", unsafe_allow_html=True)

        with detail_tabs[3]:
            if report3 is not None and not report3.empty:
                st.dataframe(report3, use_container_width=True, height=500, hide_index=True)
            else:
                st.markdown(f"""<div style="background:{T['gbg']};border:1px solid {T['green']}33;
                    border-radius:10px;padding:16px;text-align:center">
                    <span style="color:{T['gtxt']};font-size:13px;font-weight:600">
                        ✅ Không có lớp nào vi phạm</span>
                </div>""", unsafe_allow_html=True)

        with detail_tabs[4]:
            if report4 is not None and not report4.empty:
                st.dataframe(report4, use_container_width=True, height=500, hide_index=True)
            else:
                st.markdown(f"""<div style="background:{T['gbg']};border:1px solid {T['green']}33;
                    border-radius:10px;padding:16px;text-align:center">
                    <span style="color:{T['gtxt']};font-size:13px;font-weight:600">
                        ✅ Tất cả lớp lấy GPA đều có trong lịch kỳ</span>
                </div>""", unsafe_allow_html=True)

        with detail_tabs[5]:
            if low_response is not None and not low_response.empty:
                st.dataframe(low_response, use_container_width=True, height=500, hide_index=True)
            else:
                st.markdown(f"""<div style="background:{T['gbg']};border:1px solid {T['green']}33;
                    border-radius:10px;padding:16px;text-align:center">
                    <span style="color:{T['gtxt']};font-size:13px;font-weight:600">
                        ✅ Tất cả lớp đều đạt tỷ lệ phản hồi >= 60%</span>
                </div>""", unsafe_allow_html=True)

        with detail_tabs[6]:
            st.dataframe(lecturer_pct, use_container_width=True, height=500, hide_index=True)

        divider()
        if st.button("🔄  Làm lại đối sánh mới", key="btn_reset"):
            for k in defaults:
                st.session_state[k] = defaults[k]
            st.rerun()
