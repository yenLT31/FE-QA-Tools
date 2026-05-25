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
        report1, report2, report3, report4, error = logic.generate_reports(schedule_df, gpa_df)

        if error:
            st.error(f"❌ {error}")
            st.stop()

        # Lưu kết quả
        st.session_state.gpa_report1 = report1
        st.session_state.gpa_report2 = report2
        st.session_state.gpa_report3 = report3
        st.session_state.gpa_report4 = report4
        st.session_state.gpa_merged_df = gpa_df
        st.session_state.gpa_lecturer_pct = lecturer_pct
        st.session_state.gpa_done = True
        st.session_state.gpa_stats = {
            "gpa_low": len(report1) if report1 is not None and not report1.empty else 0,
            "eligible_no_gpa": len(report2) if report2 is not None and not report2.empty else 0,
            "not_eligible_has_gpa": len(report3) if report3 is not None and not report3.empty else 0,
            "gpa_not_in_schedule": len(report4) if report4 is not None and not report4.empty else 0,
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
        gpa_merged_df = st.session_state.gpa_merged_df
        lecturer_pct = st.session_state.gpa_lecturer_pct

        # Metric cards
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:28px">
            {card_metric("GPA dưới 3.4", stats['gpa_low'], T['red'], T['rbg'])}
            {card_metric("Đủ 30% chưa lấy GPA", stats['eligible_no_gpa'], T['yellow'], T['ybg'])}
            {card_metric("Dưới 30% bị lấy GPA", stats['not_eligible_has_gpa'], T['orange'], T['obg'])}
            {card_metric("GPA không có trong lịch kỳ", stats['gpa_not_in_schedule'], T['blue'], T['bbg'])}
        </div>""", unsafe_allow_html=True)

        # Detail tabs
        detail_tabs = st.tabs([
            f"🔴 GPA dưới 3.4 ({stats['gpa_low']})",
            f"🟡 Đủ 30% chưa lấy GPA ({stats['eligible_no_gpa']})",
            f"🟠 Dưới 30% bị lấy GPA ({stats['not_eligible_has_gpa']})",
            f"🔵 GPA không có trong lịch kỳ ({stats['gpa_not_in_schedule']})",
            "📊 Tỷ lệ % GV theo lớp"
        ])

        with detail_tabs[0]:
            if report1 is not None and not report1.empty:
                st.dataframe(report1, use_container_width=True, height=500, hide_index=True)
            else:
                st.markdown(f"""<div style="background:{T['gbg']};border:1px solid {T['green']}33;
                    border-radius:10px;padding:16px;text-align:center">
                    <span style="color:{T['gtxt']};font-size:13px;font-weight:600">
                        ✅ Không có lớp nào GPA dưới 3.4</span>
                </div>""", unsafe_allow_html=True)

        with detail_tabs[1]:
            if report2 is not None and not report2.empty:
                st.dataframe(report2, use_container_width=True, height=500, hide_index=True)
            else:
                st.markdown(f"""<div style="background:{T['gbg']};border:1px solid {T['green']}33;
                    border-radius:10px;padding:16px;text-align:center">
                    <span style="color:{T['gtxt']};font-size:13px;font-weight:600">
                        ✅ Tất cả GV đủ ĐK đã được lấy GPA</span>
                </div>""", unsafe_allow_html=True)

        with detail_tabs[2]:
            if report3 is not None and not report3.empty:
                st.dataframe(report3, use_container_width=True, height=500, hide_index=True)
            else:
                st.markdown(f"""<div style="background:{T['gbg']};border:1px solid {T['green']}33;
                    border-radius:10px;padding:16px;text-align:center">
                    <span style="color:{T['gtxt']};font-size:13px;font-weight:600">
                        ✅ Không có lớp nào vi phạm</span>
                </div>""", unsafe_allow_html=True)

        with detail_tabs[3]:
            if report4 is not None and not report4.empty:
                st.dataframe(report4, use_container_width=True, height=500, hide_index=True)
            else:
                st.markdown(f"""<div style="background:{T['gbg']};border:1px solid {T['green']}33;
                    border-radius:10px;padding:16px;text-align:center">
                    <span style="color:{T['gtxt']};font-size:13px;font-weight:600">
                        ✅ Tất cả lớp lấy GPA đều có trong lịch kỳ</span>
                </div>""", unsafe_allow_html=True)

        with detail_tabs[4]:
            st.dataframe(lecturer_pct, use_container_width=True, height=500, hide_index=True)

        # Download buttons
        divider()

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
            excel_report = logic.export_reports_to_excel(report1, report2, report3, report4)
            st.download_button(
                label="📥  Tải Result check GPA (.xlsx)",
                data=excel_report,
                file_name=logic.get_report_filename(),
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        if st.button("🔄  Làm lại đối sánh mới", key="btn_reset"):
            for k in defaults:
                st.session_state[k] = defaults[k]
            st.rerun()
