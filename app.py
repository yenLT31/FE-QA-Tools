import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="FE QA Tools",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Theme ─────────────────────────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

DARK = dict(
    bg="#080D18", card="#0F1628", card2="#162040", border="#1E2D4A",
    text="#E8EDF5", muted="#8892A4", accent="#00D4AA", accent_dim="#00A882",
    green="#22C55E", gbg="#052E16", gtxt="#22C55E",
    tooltip_bg="rgba(13,22,35,0.97)",
)
LIGHT = dict(
    bg="#F0F4F8", card="#FFFFFF", card2="#F7F9FC", border="#E2E8F0",
    text="#1A2540", muted="#64748B", accent="#0A9E7F", accent_dim="#077A62",
    green="#16A34A", gbg="#DCFCE7", gtxt="#15803D",
    tooltip_bg="rgba(255,255,255,0.97)",
)
T = DARK if st.session_state.theme == "dark" else LIGHT

# ── Data ──────────────────────────────────────────────────────────────────────
# Thêm tool mới vào đây
TOOLS = [
    dict(
        id="graduation-reviewer",
        name="Graduation Reviewer",
        desc="Rà soát dữ liệu xét tốt nghiệp, đối chiếu GPA và điểm số theo phụ lục.",
        icon="📊",
        status="live",
        page="/graduation-reviewer",
        uses=150,
    ),
    dict(
        id="replacecode-manager",
        name="ReplaceCode Manager",
        desc="Quản lý và cập nhật môn thay thế / tương đương từ Quyết định PDF.",
        icon="📋",
        status="live",
        page="/replacecode-manager",
        uses=80,
    ),
    # dict(
    #     id="new-tool",
    #     name="Tool mới",
    #     desc="Mô tả tool mới...",
    #     icon="📈",
    #     status="coming",
    #     page="/new-tool",
    #     uses=0,
    # ),
]

# Mối quan hệ giữa các tool
# desc_short hiện trên đường nối; desc_full cho tooltip
RELATIONS = [
    dict(
        from_id="graduation-reviewer",
        to_id="replacecode-manager",
        desc_short="dùng dữ liệu",
        desc_full="Graduation Reviewer sử dụng dữ liệu môn tương đương từ ReplaceCode Manager để đối chiếu khi xét tốt nghiệp.",
    ),
]

# Tính degree (số quan hệ mỗi tool)
for tool in TOOLS:
    tool["degree"] = sum(
        1 for r in RELATIONS
        if r["from_id"] == tool["id"] or r["to_id"] == tool["id"]
    )

# ── Fonts + CSS ───────────────────────────────────────────────────────────────
st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">',
    unsafe_allow_html=True
)
st.markdown(f"""<style>:root{{
--bg:{T['bg']};--card:{T['card']};--card2:{T['card2']};--border:{T['border']};
--text:{T['text']};--muted:{T['muted']};--accent:{T['accent']};--adim:{T['accent_dim']};
--green:{T['green']};--gbg:{T['gbg']};--gtxt:{T['gtxt']};
}}</style>""", unsafe_allow_html=True)

st.markdown("""<style>
.stApp { background: var(--bg) !important; }
header[data-testid="stHeader"] { display: none !important; }
.block-container { padding-top: 0 !important; max-width: 1300px !important; }
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebar"] { background: var(--card) !important; border-right: 1px solid var(--border) !important; }
.stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    font-family: 'Plus Jakarta Sans', sans-serif !important; color: var(--text) !important;
}
.stButton > button {
    background: var(--accent) !important; color: #080D18 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 700 !important;
    font-size: 14px !important; border: none !important; border-radius: 10px !important;
    padding: 10px 22px !important; transition: all .2s !important;
}
.stButton > button:hover { background: var(--adim) !important; transform: translateY(-1px) !important; }
</style>""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:16px 0 20px;border-bottom:1px solid {T['border']};margin-bottom:20px">
        <div style="font-size:15px;font-weight:800;color:{T['accent']};
                    font-family:'Plus Jakarta Sans',sans-serif">🔧 FE QA Tools</div>
        <div style="font-size:10px;color:{T['muted']};font-weight:600;letter-spacing:.9px;
                    text-transform:uppercase;margin-top:3px;font-family:'Plus Jakarta Sans',sans-serif">
            QA Department — FE
        </div>
    </div>
    <p style="font-size:10px;color:{T['muted']};font-weight:700;letter-spacing:.9px;
              text-transform:uppercase;margin-bottom:8px;font-family:'Plus Jakarta Sans',sans-serif">
        Giao diện
    </p>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("☀ Sáng", use_container_width=True, key="btn_light"):
            st.session_state.theme = "light"; st.rerun()
    with c2:
        if st.button("🌙 Tối", use_container_width=True, key="btn_dark"):
            st.session_state.theme = "dark"; st.rerun()

    st.markdown(f'<div style="height:1px;background:{T["border"]};margin:18px 0"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <p style="font-size:10px;color:{T['muted']};font-weight:700;letter-spacing:.9px;
              text-transform:uppercase;margin-bottom:10px;font-family:'Plus Jakarta Sans',sans-serif">
        Công cụ
    </p>""", unsafe_allow_html=True)

    for tool in TOOLS:
        if tool["status"] == "live":
            st.page_link(f"pages/{tool['id']}.py", label=f"{tool['icon']}  {tool['name']}")

    st.markdown(f"""
    <div style="height:1px;background:{T['border']};margin:18px 0"></div>
    <div style="font-size:11px;color:{T['muted']};line-height:1.7;font-family:'Plus Jakarta Sans',sans-serif">
        © 2026 YenLT31<br>FE Education QA Department
    </div>""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(160deg,{T['card']} 0%,{T['card2']} 55%,{T['bg']} 100%);
            border-bottom:1px solid {T['border']};padding:48px 0 36px;
            margin:-1rem -1rem 0;text-align:center">
    <div style="font-size:12px;color:{T['accent']};font-weight:700;letter-spacing:1.2px;
                text-transform:uppercase;margin-bottom:12px;font-family:'Plus Jakarta Sans',sans-serif">
        🔧 FE QA Tools
    </div>
    <h1 style="font-size:36px;font-weight:800;color:{T['text']};letter-spacing:-.8px;
               margin:0 0 12px;line-height:1.2;font-family:'Plus Jakarta Sans',sans-serif">
        Hệ sinh thái công cụ<br>
        <span style="color:{T['accent']}">Đảm bảo chất lượng — FE</span>
    </h1>
    <p style="color:{T['muted']};font-size:14px;margin:0 auto;max-width:460px;
              line-height:1.7;font-family:'Plus Jakarta Sans',sans-serif">
        Các công cụ kết nối với nhau thành một hệ thống —
        click vào từng sao để khám phá.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Constellation ─────────────────────────────────────────────────────────────
is_dark = st.session_state.theme == "dark"

tools_json    = json.dumps(TOOLS)
relations_json = json.dumps(RELATIONS)

constellation_html = f"""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:transparent; overflow:hidden; font-family:'Plus Jakarta Sans',sans-serif; }}
svg {{ width:100%; display:block; }}
.tooltip {{
    position:fixed; pointer-events:none; opacity:0;
    background:{"rgba(13,22,35,0.97)" if is_dark else "rgba(255,255,255,0.97)"};
    border:1px solid {"rgba(0,212,170,0.35)" if is_dark else "rgba(10,158,127,0.35)"};
    border-radius:12px; padding:12px 16px; max-width:220px;
    transition:opacity .15s; z-index:999;
    box-shadow:0 8px 24px rgba(0,0,0,{".5" if is_dark else ".12"});
}}
.tt-name {{
    font-size:13px; font-weight:700; margin-bottom:5px;
    color:{"#E8EDF5" if is_dark else "#1A2540"};
}}
.tt-desc {{
    font-size:11px; line-height:1.55;
    color:{"#8892A4" if is_dark else "#64748B"};
}}
.tt-badge {{
    display:inline-block; margin-top:7px;
    font-size:10px; font-weight:700; padding:2px 8px; border-radius:20px;
    background:{"#052E16" if is_dark else "#DCFCE7"};
    color:{"#22C55E" if is_dark else "#16A34A"};
}}
@keyframes dash {{ to {{ stroke-dashoffset: -30; }} }}
@keyframes twinkle {{ 0%,100%{{opacity:.4}} 50%{{opacity:1}} }}
@keyframes pulse-halo {{ 0%,100%{{r:0;opacity:.4}} 100%{{r:40;opacity:0}} }}
</style>
</head>
<body>

<svg id="svg" viewBox="0 0 800 380" xmlns="http://www.w3.org/2000/svg">
<defs>
  <filter id="glow">
    <feGaussianBlur stdDeviation="5" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="glow-lg">
    <feGaussianBlur stdDeviation="10" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
          markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 Z" fill="{"#00D4AA" if is_dark else "#0A9E7F"}" opacity="0.7"/>
  </marker>
</defs>
</svg>

<div class="tooltip" id="tooltip">
  <div class="tt-name" id="tt-name"></div>
  <div class="tt-desc" id="tt-desc"></div>
  <span class="tt-badge" id="tt-badge" style="display:none">● LIVE</span>
</div>

<script>
const TOOLS = {tools_json};
const RELATIONS = {relations_json};
const IS_DARK = {"true" if is_dark else "false"};
const ACCENT = IS_DARK ? '#00D4AA' : '#0A9E7F';
const TEXT   = IS_DARK ? '#E8EDF5' : '#1A2540';
const MUTED  = IS_DARK ? '#8892A4' : '#64748B';
const CARD   = IS_DARK ? '#0F1628' : '#FFFFFF';
const BORDER = IS_DARK ? '#1E2D4A' : '#E2E8F0';
const BG     = IS_DARK ? '#080D18' : '#F0F4F8';

const NS  = 'http://www.w3.org/2000/svg';
const svg = document.getElementById('svg');
const W = 800, H = 380;

// ── Size calculation ──────────────────────────────────────────────────────────
const maxDeg  = Math.max(...TOOLS.map(t => t.degree), 1);
const maxUses = Math.max(...TOOLS.map(t => t.uses), 1);
const MIN_R = 28, MAX_R = 50;

TOOLS.forEach(t => {{
    const ds = t.degree / maxDeg;
    const us = t.uses   / maxUses;
    t.r = Math.round(MIN_R + (ds * 0.45 + us * 0.55) * (MAX_R - MIN_R));
}});

// ── Layout ────────────────────────────────────────────────────────────────────
const n = TOOLS.length;
const cx = W / 2, cy = H / 2;

if (n === 1) {{
    TOOLS[0].x = cx; TOOLS[0].y = cy;
}} else if (n === 2) {{
    TOOLS[0].x = cx - 160; TOOLS[0].y = cy;
    TOOLS[1].x = cx + 160; TOOLS[1].y = cy;
}} else {{
    const spread = Math.min(160, 280 / n * 1.8);
    TOOLS.forEach((t, i) => {{
        const angle = (i / n) * 2 * Math.PI - Math.PI / 2;
        t.x = cx + spread * Math.cos(angle);
        t.y = cy + spread * Math.sin(angle);
    }});
}}

// ── Decorative background stars ───────────────────────────────────────────────
for (let i = 0; i < 70; i++) {{
    const s = document.createElementNS(NS, 'circle');
    s.setAttribute('cx', Math.random() * W);
    s.setAttribute('cy', Math.random() * H);
    s.setAttribute('r',  Math.random() * 1.1 + 0.2);
    s.setAttribute('fill', IS_DARK ? 'rgba(255,255,255,0.18)' : 'rgba(0,0,0,0.07)');
    s.style.animation = `twinkle ${{(Math.random()*3+2).toFixed(1)}}s ease-in-out ${{(Math.random()*3).toFixed(1)}}s infinite`;
    svg.appendChild(s);
}}

// ── Connection lines ──────────────────────────────────────────────────────────
RELATIONS.forEach(rel => {{
    const from = TOOLS.find(t => t.id === rel.from_id);
    const to   = TOOLS.find(t => t.id === rel.to_id);
    if (!from || !to) return;

    // Compute offset points (stop at node border)
    const dx = to.x - from.x, dy = to.y - from.y;
    const dist = Math.sqrt(dx*dx + dy*dy);
    const ux = dx/dist, uy = dy/dist;
    const x1 = from.x + ux * (from.r + 4);
    const y1 = from.y + uy * (from.r + 4);
    const x2 = to.x   - ux * (to.r   + 10);
    const y2 = to.y   - uy * (to.r   + 10);

    // Glow
    const g = document.createElementNS(NS, 'line');
    g.setAttribute('x1',x1); g.setAttribute('y1',y1);
    g.setAttribute('x2',x2); g.setAttribute('y2',y2);
    g.setAttribute('stroke', ACCENT);
    g.setAttribute('stroke-width','4');
    g.setAttribute('stroke-opacity','0.12');
    g.setAttribute('filter','url(#glow)');
    svg.appendChild(g);

    // Animated dash
    const line = document.createElementNS(NS, 'line');
    line.setAttribute('x1',x1); line.setAttribute('y1',y1);
    line.setAttribute('x2',x2); line.setAttribute('y2',y2);
    line.setAttribute('stroke', ACCENT);
    line.setAttribute('stroke-width','1.5');
    line.setAttribute('stroke-opacity','0.55');
    line.setAttribute('stroke-dasharray','8 5');
    line.setAttribute('marker-end','url(#arrow)');
    line.style.animation = 'dash 1.8s linear infinite';
    svg.appendChild(line);

    // Midpoint label
    const mx = (from.x + to.x) / 2;
    const my = (from.y + to.y) / 2 - 14;

    const lblBg = document.createElementNS(NS, 'rect');
    const lblText = rel.desc_short || '';
    const lw = lblText.length * 6.2 + 16;
    lblBg.setAttribute('x', mx - lw/2);
    lblBg.setAttribute('y', my - 11);
    lblBg.setAttribute('width', lw);
    lblBg.setAttribute('height', 16);
    lblBg.setAttribute('rx', 5);
    lblBg.setAttribute('fill', IS_DARK ? '#162040' : '#F7F9FC');
    lblBg.setAttribute('stroke', BORDER);
    lblBg.setAttribute('stroke-width', '0.5');
    svg.appendChild(lblBg);

    const lbl = document.createElementNS(NS, 'text');
    lbl.setAttribute('x', mx); lbl.setAttribute('y', my);
    lbl.setAttribute('text-anchor','middle');
    lbl.setAttribute('font-size','9.5');
    lbl.setAttribute('font-family','Plus Jakarta Sans,sans-serif');
    lbl.setAttribute('fill', MUTED);
    lbl.textContent = lblText;
    svg.appendChild(lbl);
}});

// ── Tool nodes ────────────────────────────────────────────────────────────────
const tooltip  = document.getElementById('tooltip');
const ttName   = document.getElementById('tt-name');
const ttDesc   = document.getElementById('tt-desc');
const ttBadge  = document.getElementById('tt-badge');

TOOLS.forEach(tool => {{
    const g = document.createElementNS(NS, 'g');
    g.style.cursor = tool.status === 'live' ? 'pointer' : 'default';
    svg.appendChild(g);

    // Outer halo (animated)
    const halo = document.createElementNS(NS, 'circle');
    halo.setAttribute('cx', tool.x); halo.setAttribute('cy', tool.y);
    halo.setAttribute('r', tool.r + 14);
    halo.setAttribute('fill', ACCENT);
    halo.setAttribute('fill-opacity', tool.status === 'live' ? '0.07' : '0.03');
    halo.style.animation = `twinkle ${{(Math.random()*2+2.5).toFixed(1)}}s ease-in-out infinite`;
    g.appendChild(halo);

    // Main circle
    const circle = document.createElementNS(NS, 'circle');
    circle.setAttribute('cx', tool.x); circle.setAttribute('cy', tool.y);
    circle.setAttribute('r', tool.r);
    circle.setAttribute('fill', CARD);
    circle.setAttribute('stroke', tool.status === 'live' ? ACCENT : MUTED);
    circle.setAttribute('stroke-width', '1.5');
    circle.setAttribute('filter', 'url(#glow)');
    circle.style.transition = 'all .2s';
    g.appendChild(circle);

    // Icon
    const icon = document.createElementNS(NS, 'text');
    icon.setAttribute('x', tool.x); icon.setAttribute('y', tool.y + 8);
    icon.setAttribute('text-anchor','middle');
    icon.setAttribute('font-size', Math.round(tool.r * 0.72));
    icon.setAttribute('dominant-baseline','middle');
    icon.textContent = tool.icon;
    icon.style.pointerEvents = 'none';
    g.appendChild(icon);

    // Name label
    const label = document.createElementNS(NS, 'text');
    label.setAttribute('x', tool.x); label.setAttribute('y', tool.y + tool.r + 18);
    label.setAttribute('text-anchor','middle');
    label.setAttribute('font-size','12');
    label.setAttribute('font-weight','600');
    label.setAttribute('fill', TEXT);
    label.setAttribute('font-family','Plus Jakarta Sans,sans-serif');
    label.textContent = tool.name;
    label.style.pointerEvents = 'none';
    g.appendChild(label);

    // Status dot
    if (tool.status === 'live') {{
        const dot = document.createElementNS(NS, 'circle');
        dot.setAttribute('cx', tool.x + tool.r * 0.7);
        dot.setAttribute('cy', tool.y - tool.r * 0.7);
        dot.setAttribute('r', 5);
        dot.setAttribute('fill', IS_DARK ? '#22C55E' : '#16A34A');
        dot.setAttribute('filter','url(#glow)');
        g.appendChild(dot);
    }}

    // ── Events ────────────────────────────────────────────────────────────────
    g.addEventListener('mouseenter', e => {{
        if (tool.status !== 'live') return;
        circle.setAttribute('stroke-width','2.5');
        halo.setAttribute('fill-opacity','0.16');

        ttName.textContent  = tool.name;
        ttDesc.textContent  = tool.desc;
        ttBadge.style.display = 'inline-block';

        tooltip.style.opacity = '1';
        posTooltip(e);
    }});

    g.addEventListener('mousemove', e => posTooltip(e));

    g.addEventListener('mouseleave', () => {{
        circle.setAttribute('stroke-width','1.5');
        halo.setAttribute('fill-opacity','0.07');
        tooltip.style.opacity = '0';
    }});

    g.addEventListener('click', () => {{
        if (tool.status !== 'live') return;
        // Flash animation
        circle.setAttribute('stroke-width','4');
        circle.setAttribute('stroke-opacity','1');
        halo.setAttribute('fill-opacity','0.28');
        halo.setAttribute('r', tool.r + 22);
        setTimeout(() => {{
            window.parent.location.href = tool.page;
        }}, 280);
    }});
}});

function posTooltip(e) {{
    const x = e.clientX, y = e.clientY;
    const tw = 230, th = 90;
    const vw = window.innerWidth, vh = window.innerHeight;
    tooltip.style.left = (x + 14 + tw > vw ? x - tw - 14 : x + 14) + 'px';
    tooltip.style.top  = (y + 14 + th > vh ? y - th - 14 : y + 14) + 'px';
}}
</script>
</body>
</html>
"""

components.html(constellation_html, height=400, scrolling=False)

# ── Security note ─────────────────────────────────────────────────────────────
st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
st.markdown(f"""
<div style="background:{T['card']};border:1px solid {T['border']};border-radius:16px;padding:20px 26px">
    <div style="font-size:14px;font-weight:700;color:{T['text']};margin-bottom:6px;
                font-family:'Plus Jakarta Sans',sans-serif">💡 Thông tin bảo mật</div>
    <p style="color:{T['muted']};font-size:13px;line-height:1.7;margin:0;
              font-family:'Plus Jakarta Sans',sans-serif">
        Toàn bộ dữ liệu được xử lý tại trình duyệt (Local). Chúng mình không lưu trữ
        bất kỳ thông tin sinh viên nào trên server để đảm bảo an toàn dữ liệu tuyệt đối
        theo quy định của FE Education.
    </p>
</div>
<div style="height:36px"></div>
<div style="text-align:center">
    <span style="color:{T['muted']};font-size:12px;font-family:'Plus Jakarta Sans',sans-serif">
        © 2026 YenLT31 — FE Education QA Department
    </span>
</div>
<div style="height:20px"></div>
""", unsafe_allow_html=True)
