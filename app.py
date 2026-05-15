import streamlit as st
import streamlit.components.v1 as components
import math
import json

st.set_page_config(
    page_title="FPT QA Tools",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme ─────────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

DARK = dict(
    bg="#080D18", card="#0F1628", card2="#162040", border="#1E2D4A",
    text="#E8EDF5", muted="#8892A4", accent="#00D4AA", accent_dim="#00A882",
    green="#22C55E", gbg="#052E16", gtxt="#22C55E",
)
LIGHT = dict(
    bg="#F0F4F8", card="#FFFFFF", card2="#F7F9FC", border="#E2E8F0",
    text="#1A2540", muted="#64748B", accent="#0A9E7F", accent_dim="#077A62",
    green="#16A34A", gbg="#DCFCE7", gtxt="#15803D",
)
T = DARK if st.session_state.theme == "dark" else LIGHT

# ── Data ──────────────────────────────────────────────────────
TOOLS = [
    dict(id="graduation-reviewer", name="Graduation Reviewer",
         desc="Rà soát dữ liệu xét tốt nghiệp, đối chiếu GPA và điểm số theo phụ lục.",
         icon="📊", status="live", page="pages/graduation-reviewer.py", uses=150),
    dict(id="replacecode-manager", name="ReplaceCode Manager",
         desc="Quản lý và cập nhật môn thay thế / tương đương từ Quyết định PDF.",
         icon="📋", status="live", page="pages/replacecode-manager.py", uses=80),
    dict(id="decision-lookup", name="Decision Lookup",
         desc="Tra cứu MSSV trong các file Quyết định PDF — tìm nhanh sinh viên thuộc QĐ nào.",
         icon="🔍", status="live", page="pages/decision-lookup.py", uses=60),
    # Thêm tool mới vào đây — tự động cân chỉnh layout
]

RELATIONS = [
    dict(from_id="graduation-reviewer", to_id="replacecode-manager", label="dùng dữ liệu"),
]

# ── CSS ───────────────────────────────────────────────────────
st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">',
    unsafe_allow_html=True,
)
st.markdown(f"""<style>
.stApp {{ background: {T['bg']} !important; }}
header[data-testid="stHeader"] {{
    background: transparent !important; border-bottom: none !important;
    height: 2.875rem !important; overflow: visible !important;
}}
.block-container {{ padding-top: 0 !important; max-width: 1300px !important; }}
[data-testid="stSidebarNav"] {{ display: none !important; }}
[data-testid="stSidebar"] {{
    background: {T['card']} !important;
    border-right: 1px solid {T['border']} !important;
}}
.stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: {T['text']} !important;
}}
.stButton > button {{
    background: {T['accent']} !important; color: #080D18 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important; font-size: 14px !important;
    border: none !important; border-radius: 10px !important;
    padding: 10px 22px !important; transition: all .2s !important;
}}
.stButton > button:hover {{
    background: {T['accent_dim']} !important;
    transform: translateY(-1px) !important;
}}
section[data-testid="stMain"] {{ padding-left: 1rem !important; }}
/* hide iframe border */
iframe {{ border: none !important; }}
</style>""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:16px 0 20px;border-bottom:1px solid {T['border']};margin-bottom:20px">
        <div style="font-size:15px;font-weight:800;color:{T['accent']};
                    font-family:'Plus Jakarta Sans',sans-serif">🔧 FPT QA Tools</div>
        <div style="font-size:10px;color:{T['muted']};font-weight:600;letter-spacing:.9px;
                    text-transform:uppercase;margin-top:3px;font-family:'Plus Jakarta Sans',sans-serif">
            QA Department — FE</div>
    </div>
    <p style="font-size:10px;color:{T['muted']};font-weight:700;letter-spacing:.9px;
              text-transform:uppercase;margin-bottom:8px;font-family:'Plus Jakarta Sans',sans-serif">
        Giao diện</p>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("☀ Sáng", use_container_width=True, key="btn_light"):
            st.session_state.theme = "light"; st.rerun()
    with c2:
        if st.button("🌙 Tối", use_container_width=True, key="btn_dark"):
            st.session_state.theme = "dark"; st.rerun()

    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:18px 0"></div>',
                unsafe_allow_html=True)
    st.markdown(f"""<p style="font-size:10px;color:{T['muted']};font-weight:700;letter-spacing:.9px;
              text-transform:uppercase;margin-bottom:10px;font-family:'Plus Jakarta Sans',sans-serif">
        Công cụ</p>""", unsafe_allow_html=True)

    for t in TOOLS:
        if t["status"] == "live":
            st.page_link(t["page"], label=f"{t['icon']}  {t['name']}")

    st.markdown(f"""
    <div style="height:1px;background:{T['border']};margin:18px 0"></div>
    <div style="font-size:11px;color:{T['muted']};line-height:1.7;font-family:'Plus Jakarta Sans',sans-serif">
        © 2026 YenLT31<br>FPT Education QA Department
    </div>""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(160deg,{T['card']} 0%,{T['card2']} 55%,{T['bg']} 100%);
            border-bottom:1px solid {T['border']};padding:20px 0 18px;
            margin:-1rem -1rem 0;text-align:center">
    <div style="font-size:12px;color:{T['accent']};font-weight:700;letter-spacing:1.2px;
                text-transform:uppercase;margin-bottom:12px;font-family:'Plus Jakarta Sans',sans-serif">
        🔧 FPT QA Tools</div>
    <h1 style="font-size:22px;font-weight:800;color:{T['text']};letter-spacing:-.8px;
               margin:0 0 12px;line-height:1.2;font-family:'Plus Jakarta Sans',sans-serif">
        Hệ sinh thái công cụ<br>
        <span style="color:{T['accent']}">Đảm bảo chất lượng — FE</span></h1>
    <p style="color:{T['muted']};font-size:13px;margin:0 auto;max-width:460px;
              line-height:1.7;font-family:'Plus Jakarta Sans',sans-serif">
        Các công cụ kết nối với nhau thành một hệ thống —
        click vào từng sao để khám phá.</p>
</div>
""", unsafe_allow_html=True)

# ── Constellation (HTML/JS/SVG — clickable, auto-layout) ─────
# Tính toán vị trí cho JS
n = len(TOOLS)
tool_positions = []
for i, t in enumerate(TOOLS):
    angle = (i / n) * 2 * math.pi - math.pi / 2
    tool_positions.append({
        "id": t["id"],
        "name": t["name"],
        "desc": t["desc"],
        "icon": t["icon"],
        "status": t["status"],
        "page": t["page"],
        "uses": t["uses"],
    })

tools_json = json.dumps(tool_positions, ensure_ascii=False)
relations_json = json.dumps(RELATIONS, ensure_ascii=False)
theme_json = json.dumps(T, ensure_ascii=False)

constellation_html = f"""
<div id="constellation" style="width:100%;height:340px;position:relative;overflow:hidden;
     font-family:'Plus Jakarta Sans',Arial,sans-serif;user-select:none"></div>

<script>
(function() {{
    const TOOLS = {tools_json};
    const RELATIONS = {relations_json};
    const T = {theme_json};
    const container = document.getElementById('constellation');
    const W = container.offsetWidth;
    const H = 340;
    const CX = W / 2;
    const CY = H / 2;
    const n = TOOLS.length;

    // ── Auto-layout: phân bố đều trên ellipse ──
    // Ellipse rộng hơn chiều ngang, hẹp chiều dọc
    const RX = Math.min(W * 0.35, 320);  // bán kính ngang
    const RY = Math.min(H * 0.30, 110);  // bán kính dọc

    // Node radius dựa trên uses
    const maxUses = Math.max(...TOOLS.map(t => t.uses), 1);
    const MIN_R = 36, MAX_R = 52;

    TOOLS.forEach((t, i) => {{
        const angle = (i / n) * 2 * Math.PI - Math.PI / 2;
        t.cx = CX + RX * Math.cos(angle);
        t.cy = CY + RY * Math.sin(angle);
        t.r = MIN_R + (t.uses / maxUses) * (MAX_R - MIN_R);
    }});

    // ── SVG layer ──
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', W);
    svg.setAttribute('height', H);
    svg.style.cssText = 'position:absolute;top:0;left:0;pointer-events:none';

    // Decorative stars
    for (let i = 0; i < 50; i++) {{
        const star = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        star.setAttribute('cx', Math.random() * W);
        star.setAttribute('cy', Math.random() * H);
        star.setAttribute('r', Math.random() * 1.5 + 0.5);
        star.setAttribute('fill', T.accent);
        star.setAttribute('opacity', Math.random() * 0.15 + 0.05);
        svg.appendChild(star);
    }}

    // Connection lines
    RELATIONS.forEach(rel => {{
        const frm = TOOLS.find(t => t.id === rel.from_id);
        const to = TOOLS.find(t => t.id === rel.to_id);
        if (!frm || !to) return;

        // Dashed line
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', frm.cx); line.setAttribute('y1', frm.cy);
        line.setAttribute('x2', to.cx);  line.setAttribute('y2', to.cy);
        line.setAttribute('stroke', T.accent);
        line.setAttribute('stroke-width', '1.5');
        line.setAttribute('stroke-dasharray', '6 4');
        line.setAttribute('opacity', '0.4');
        svg.appendChild(line);

        // Arrow
        const dx = to.cx - frm.cx, dy = to.cy - frm.cy;
        const dist = Math.sqrt(dx*dx + dy*dy);
        const ux = dx/dist, uy = dy/dist;
        const ax = to.cx - ux * (to.r + 8), ay = to.cy - uy * (to.r + 8);
        const aSize = 8;
        const p1x = ax - ux*aSize - uy*aSize*0.5, p1y = ay - uy*aSize + ux*aSize*0.5;
        const p2x = ax - ux*aSize + uy*aSize*0.5, p2y = ay - uy*aSize - ux*aSize*0.5;
        const arrow = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
        arrow.setAttribute('points', ax+','+ay+' '+p1x+','+p1y+' '+p2x+','+p2y);
        arrow.setAttribute('fill', T.accent);
        arrow.setAttribute('opacity', '0.6');
        svg.appendChild(arrow);

        // Label
        const mx = (frm.cx + to.cx) / 2, my = (frm.cy + to.cy) / 2 - 12;
        const lbl = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        lbl.setAttribute('x', mx); lbl.setAttribute('y', my);
        lbl.setAttribute('text-anchor', 'middle');
        lbl.setAttribute('fill', T.muted);
        lbl.setAttribute('font-size', '10');
        lbl.setAttribute('font-family', 'Plus Jakarta Sans, sans-serif');
        lbl.textContent = rel.label;
        svg.appendChild(lbl);
    }});

    container.appendChild(svg);

    // ── HTML nodes (clickable) ──
    TOOLS.forEach(t => {{
        const isLive = t.status === 'live';

        // Outer halo
        const halo = document.createElement('div');
        halo.style.cssText = `
            position:absolute; left:${{t.cx - t.r*1.3}}px; top:${{t.cy - t.r*1.3}}px;
            width:${{t.r*2.6}}px; height:${{t.r*2.6}}px; border-radius:50%;
            background: radial-gradient(circle, ${{T.accent}}15 0%, transparent 70%);
            pointer-events:none; transition: all 0.3s ease;
        `;
        halo.className = 'halo-' + t.id;
        container.appendChild(halo);

        // Main node
        const node = document.createElement('div');
        node.style.cssText = `
            position:absolute; left:${{t.cx - t.r}}px; top:${{t.cy - t.r}}px;
            width:${{t.r*2}}px; height:${{t.r*2}}px; border-radius:50%;
            background: ${{T.card}};
            border: 2.5px solid ${{isLive ? T.accent : T.muted}};
            display:flex; align-items:center; justify-content:center;
            font-size:${{Math.round(t.r * 0.55)}}px;
            cursor:${{isLive ? 'pointer' : 'default'}};
            transition: all 0.25s ease;
            box-shadow: 0 4px 20px ${{T.accent}}11;
            z-index: 10;
        `;
        node.textContent = t.icon;
        node.title = t.name + '\\n' + t.desc;

        // Hover effects
        node.addEventListener('mouseenter', () => {{
            node.style.transform = 'scale(1.12)';
            node.style.borderColor = T.accent;
            node.style.boxShadow = '0 8px 32px ' + T.accent + '33';
            const h = container.querySelector('.halo-' + t.id);
            if (h) h.style.background = 'radial-gradient(circle, ' + T.accent + '25 0%, transparent 70%)';
        }});
        node.addEventListener('mouseleave', () => {{
            node.style.transform = 'scale(1)';
            node.style.borderColor = isLive ? T.accent : T.muted;
            node.style.boxShadow = '0 4px 20px ' + T.accent + '11';
            const h = container.querySelector('.halo-' + t.id);
            if (h) h.style.background = 'radial-gradient(circle, ' + T.accent + '15 0%, transparent 70%)';
        }});

        // ★ CLICK → navigate
        if (isLive) {{
            node.addEventListener('click', () => {{
                // Streamlit navigation: thay đổi URL path
                const pageName = t.id;  // e.g. "graduation-reviewer"
                window.parent.location.href = '/' + pageName;
            }});
        }}

        container.appendChild(node);

        // Live indicator dot
        if (isLive) {{
            const dot = document.createElement('div');
            dot.style.cssText = `
                position:absolute;
                left:${{t.cx + t.r*0.6}}px; top:${{t.cy - t.r*0.6 - 4}}px;
                width:10px; height:10px; border-radius:50%;
                background:${{T.green}};
                border: 2px solid ${{T.card}};
                z-index: 11;
            `;
            container.appendChild(dot);
        }}

        // Name label
        const label = document.createElement('div');
        label.style.cssText = `
            position:absolute;
            left:${{t.cx - 70}}px; top:${{t.cy + t.r + 8}}px;
            width:140px; text-align:center;
            font-size:12px; font-weight:700;
            color:${{T.text}};
            font-family:'Plus Jakarta Sans', sans-serif;
            pointer-events:none;
            white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
        `;
        label.textContent = t.name;
        container.appendChild(label);
    }});

    // ── Tooltip on hover ──
    const tooltip = document.createElement('div');
    tooltip.style.cssText = `
        position:fixed; padding:12px 16px; border-radius:10px;
        background:${{T.card}}; border:1px solid ${{T.border}};
        box-shadow:0 8px 24px rgba(0,0,0,0.3);
        font-family:'Plus Jakarta Sans',sans-serif;
        pointer-events:none; opacity:0; transition:opacity 0.15s;
        z-index:9999; max-width:260px;
    `;
    document.body.appendChild(tooltip);

    container.querySelectorAll('div').forEach(node => {{
        if (!node.title) return;
        const [name, desc] = node.title.split('\\n');
        node.addEventListener('mouseenter', e => {{
            tooltip.innerHTML = `
                <div style="font-size:13px;font-weight:700;color:${{T.text}};margin-bottom:4px">${{name}}</div>
                <div style="font-size:11px;color:${{T.muted}};line-height:1.5">${{desc || ''}}</div>
                <div style="font-size:10px;color:${{T.accent}};margin-top:6px">Click để mở →</div>
            `;
            tooltip.style.opacity = '1';
            node.title = '';  // prevent native tooltip
            node._tip = [name, desc];
        }});
        node.addEventListener('mousemove', e => {{
            tooltip.style.left = (e.clientX + 16) + 'px';
            tooltip.style.top = (e.clientY - 10) + 'px';
        }});
        node.addEventListener('mouseleave', () => {{
            tooltip.style.opacity = '0';
            if (node._tip) node.title = node._tip.join('\\n');
        }});
    }});
}})();
</script>
"""

components.html(constellation_html, height=370, scrolling=False)

# ── Security note ─────────────────────────────────────────────
st.markdown(f"""
<div style="background:{T['card']};border:1px solid {T['border']};border-radius:16px;
            padding:12px 20px;margin-top:8px">
    <div style="font-size:14px;font-weight:700;color:{T['text']};margin-bottom:6px;
                font-family:'Plus Jakarta Sans',sans-serif">💡 Thông tin bảo mật</div>
    <p style="color:{T['muted']};font-size:13px;line-height:1.7;margin:0;
              font-family:'Plus Jakarta Sans',sans-serif">
        Toàn bộ dữ liệu được xử lý tại trình duyệt (Local). Chúng mình không lưu trữ
        bất kỳ thông tin sinh viên nào trên server để đảm bảo an toàn dữ liệu tuyệt đối
        theo quy định của FPT Education.</p>
</div>
<div style="text-align:center;margin-top:16px">
    <span style="color:{T['muted']};font-size:12px;font-family:'Plus Jakarta Sans',sans-serif">
        © 2026 YenLT31 — FPT Education QA Department</span>
</div>
""", unsafe_allow_html=True)
