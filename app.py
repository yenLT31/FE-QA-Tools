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
)
LIGHT = dict(
    bg="#F0F4F8", card="#FFFFFF", card2="#F7F9FC", border="#E2E8F0",
    text="#1A2540", muted="#64748B", accent="#0A9E7F", accent_dim="#077A62",
    green="#16A34A", gbg="#DCFCE7", gtxt="#15803D",
)
T = DARK if st.session_state.theme == "dark" else LIGHT

# ── Data ──────────────────────────────────────────────────────────────────────
TOOLS = [
    dict(id="graduation-reviewer", name="Graduation Reviewer",
         desc="Rà soát dữ liệu xét tốt nghiệp, đối chiếu GPA và điểm số theo phụ lục.",
         icon="📊", status="live", page="/graduation-reviewer", uses=150),
    dict(id="replacecode-manager", name="ReplaceCode Manager",
         desc="Quản lý và cập nhật môn thay thế / tương đương từ Quyết định PDF.",
         icon="📋", status="live", page="/replacecode-manager", uses=80),
]
RELATIONS = [
    dict(from_id="graduation-reviewer", to_id="replacecode-manager",
         desc_short="dùng dữ liệu",
         desc_full="Graduation Reviewer sử dụng dữ liệu môn tương đương từ ReplaceCode Manager."),
]
for tool in TOOLS:
    tool["degree"] = sum(1 for r in RELATIONS if r["from_id"] == tool["id"] or r["to_id"] == tool["id"])

# ── CSS — Chỉ style, KHÔNG ẩn bất kỳ element nào của Streamlit ──────────────
st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">',
    unsafe_allow_html=True
)

st.markdown(f"""<style>
/* Background */
.stApp {{ background: {T['bg']} !important; }}
.block-container {{ padding-top: 0 !important; max-width: 1300px !important; }}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: {T['card']} !important;
    border-right: 1px solid {T['border']} !important;
}}
[data-testid="stSidebarNav"] {{ display: none !important; }}

/* Typography */
.stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: {T['text']} !important;
}}

/* Buttons */
.stButton > button {{
    background: {T['accent']} !important; color: #080D18 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important; font-size: 14px !important;
    border: none !important; border-radius: 10px !important;
    padding: 10px 22px !important;
}}
.stButton > button:hover {{
    background: {T['accent_dim']} !important;
}}

/* Page links */
.stPageLink a {{
    background: {T['card']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 12px !important;
    padding: 14px 20px !important;
    color: {T['text']} !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    text-decoration: none !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}}
.stPageLink a:hover {{
    border-color: {T['accent']} !important;
    background: {T['card2']} !important;
}}
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
tools_json = json.dumps(TOOLS)
relations_json = json.dumps(RELATIONS)

constellation_html = f"""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:transparent;overflow:hidden;font-family:'Plus Jakarta Sans',sans-serif}}
svg{{width:100%;display:block}}
.tooltip{{position:fixed;pointer-events:none;opacity:0;background:{"rgba(13,22,35,0.97)" if is_dark else "rgba(255,255,255,0.97)"};border:1px solid {"rgba(0,212,170,0.35)" if is_dark else "rgba(10,158,127,0.35)"};border-radius:12px;padding:12px 16px;max-width:220px;transition:opacity .15s;z-index:999;box-shadow:0 8px 24px rgba(0,0,0,{".5" if is_dark else ".12"})}}
.tt-name{{font-size:13px;font-weight:700;margin-bottom:5px;color:{"#E8EDF5" if is_dark else "#1A2540"}}}
.tt-desc{{font-size:11px;line-height:1.55;color:{"#8892A4" if is_dark else "#64748B"}}}
.tt-badge{{display:inline-block;margin-top:7px;font-size:10px;font-weight:700;padding:2px 8px;border-radius:20px;background:{"#052E16" if is_dark else "#DCFCE7"};color:{"#22C55E" if is_dark else "#16A34A"}}}
@keyframes dash{{to{{stroke-dashoffset:-30}}}}
@keyframes twinkle{{0%,100%{{opacity:.4}}50%{{opacity:1}}}}
</style>
</head>
<body>
<svg id="svg" viewBox="0 0 800 380" xmlns="http://www.w3.org/2000/svg">
<defs>
<filter id="glow"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M0,0 L10,5 L0,10 Z" fill="{"#00D4AA" if is_dark else "#0A9E7F"}" opacity="0.7"/></marker>
</defs></svg>
<div class="tooltip" id="tooltip"><div class="tt-name" id="tt-name"></div><div class="tt-desc" id="tt-desc"></div><span class="tt-badge" id="tt-badge" style="display:none">● LIVE</span></div>
<script>
const TOOLS={tools_json},RELATIONS={relations_json},IS_DARK={"true" if is_dark else "false"};
const ACCENT=IS_DARK?'#00D4AA':'#0A9E7F',TEXT=IS_DARK?'#E8EDF5':'#1A2540',MUTED=IS_DARK?'#8892A4':'#64748B',CARD=IS_DARK?'#0F1628':'#FFFFFF',BORDER=IS_DARK?'#1E2D4A':'#E2E8F0';
const NS='http://www.w3.org/2000/svg',svg=document.getElementById('svg'),W=800,H=380;
TOOLS.forEach(t=>{{const ds=t.degree/Math.max(...TOOLS.map(x=>x.degree),1);const us=t.uses/Math.max(...TOOLS.map(x=>x.uses),1);t.r=Math.round(28+(ds*0.45+us*0.55)*22);}});
const n=TOOLS.length,cx=W/2,cy=H/2;
if(n===1){{TOOLS[0].x=cx;TOOLS[0].y=cy;}}else if(n===2){{TOOLS[0].x=cx-160;TOOLS[0].y=cy;TOOLS[1].x=cx+160;TOOLS[1].y=cy;}}else{{const sp=Math.min(160,280/n*1.8);TOOLS.forEach((t,i)=>{{const a=(i/n)*2*Math.PI-Math.PI/2;t.x=cx+sp*Math.cos(a);t.y=cy+sp*Math.sin(a);}});}}
for(let i=0;i<70;i++){{const s=document.createElementNS(NS,'circle');s.setAttribute('cx',Math.random()*W);s.setAttribute('cy',Math.random()*H);s.setAttribute('r',Math.random()*1.1+0.2);s.setAttribute('fill',IS_DARK?'rgba(255,255,255,0.18)':'rgba(0,0,0,0.07)');s.style.animation=`twinkle ${{(Math.random()*3+2).toFixed(1)}}s ease-in-out ${{(Math.random()*3).toFixed(1)}}s infinite`;svg.appendChild(s);}}
RELATIONS.forEach(rel=>{{const from=TOOLS.find(t=>t.id===rel.from_id),to=TOOLS.find(t=>t.id===rel.to_id);if(!from||!to)return;const dx=to.x-from.x,dy=to.y-from.y,dist=Math.sqrt(dx*dx+dy*dy),ux=dx/dist,uy=dy/dist,x1=from.x+ux*(from.r+4),y1=from.y+uy*(from.r+4),x2=to.x-ux*(to.r+10),y2=to.y-uy*(to.r+10);
const gl=document.createElementNS(NS,'line');gl.setAttribute('x1',x1);gl.setAttribute('y1',y1);gl.setAttribute('x2',x2);gl.setAttribute('y2',y2);gl.setAttribute('stroke',ACCENT);gl.setAttribute('stroke-width','4');gl.setAttribute('stroke-opacity','0.12');gl.setAttribute('filter','url(#glow)');svg.appendChild(gl);
const ln=document.createElementNS(NS,'line');ln.setAttribute('x1',x1);ln.setAttribute('y1',y1);ln.setAttribute('x2',x2);ln.setAttribute('y2',y2);ln.setAttribute('stroke',ACCENT);ln.setAttribute('stroke-width','1.5');ln.setAttribute('stroke-opacity','0.55');ln.setAttribute('stroke-dasharray','8 5');ln.setAttribute('marker-end','url(#arrow)');ln.style.animation='dash 1.8s linear infinite';svg.appendChild(ln);
const mx=(from.x+to.x)/2,my=(from.y+to.y)/2-14,lt=rel.desc_short||'',lw=lt.length*6.2+16;
const bg=document.createElementNS(NS,'rect');bg.setAttribute('x',mx-lw/2);bg.setAttribute('y',my-11);bg.setAttribute('width',lw);bg.setAttribute('height',16);bg.setAttribute('rx',5);bg.setAttribute('fill',IS_DARK?'#162040':'#F7F9FC');bg.setAttribute('stroke',BORDER);bg.setAttribute('stroke-width','0.5');svg.appendChild(bg);
const lb=document.createElementNS(NS,'text');lb.setAttribute('x',mx);lb.setAttribute('y',my);lb.setAttribute('text-anchor','middle');lb.setAttribute('font-size','9.5');lb.setAttribute('font-family','Plus Jakarta Sans,sans-serif');lb.setAttribute('fill',MUTED);lb.textContent=lt;svg.appendChild(lb);}});
const tooltip=document.getElementById('tooltip'),ttN=document.getElementById('tt-name'),ttD=document.getElementById('tt-desc'),ttB=document.getElementById('tt-badge');
TOOLS.forEach(tool=>{{const g=document.createElementNS(NS,'g');g.style.cursor=tool.status==='live'?'pointer':'default';svg.appendChild(g);
const halo=document.createElementNS(NS,'circle');halo.setAttribute('cx',tool.x);halo.setAttribute('cy',tool.y);halo.setAttribute('r',tool.r+14);halo.setAttribute('fill',ACCENT);halo.setAttribute('fill-opacity',tool.status==='live'?'0.07':'0.03');halo.style.animation=`twinkle ${{(Math.random()*2+2.5).toFixed(1)}}s ease-in-out infinite`;g.appendChild(halo);
const c=document.createElementNS(NS,'circle');c.setAttribute('cx',tool.x);c.setAttribute('cy',tool.y);c.setAttribute('r',tool.r);c.setAttribute('fill',CARD);c.setAttribute('stroke',tool.status==='live'?ACCENT:MUTED);c.setAttribute('stroke-width','1.5');c.setAttribute('filter','url(#glow)');c.style.transition='all .2s';g.appendChild(c);
const ic=document.createElementNS(NS,'text');ic.setAttribute('x',tool.x);ic.setAttribute('y',tool.y+8);ic.setAttribute('text-anchor','middle');ic.setAttribute('font-size',Math.round(tool.r*0.72));ic.setAttribute('dominant-baseline','middle');ic.textContent=tool.icon;ic.style.pointerEvents='none';g.appendChild(ic);
const la=document.createElementNS(NS,'text');la.setAttribute('x',tool.x);la.setAttribute('y',tool.y+tool.r+18);la.setAttribute('text-anchor','middle');la.setAttribute('font-size','12');la.setAttribute('font-weight','600');la.setAttribute('fill',TEXT);la.setAttribute('font-family','Plus Jakarta Sans,sans-serif');la.textContent=tool.name;la.style.pointerEvents='none';g.appendChild(la);
if(tool.status==='live'){{const d=document.createElementNS(NS,'circle');d.setAttribute('cx',tool.x+tool.r*0.7);d.setAttribute('cy',tool.y-tool.r*0.7);d.setAttribute('r',5);d.setAttribute('fill',IS_DARK?'#22C55E':'#16A34A');d.setAttribute('filter','url(#glow)');g.appendChild(d);}}
g.addEventListener('mouseenter',e=>{{if(tool.status!=='live')return;c.setAttribute('stroke-width','2.5');halo.setAttribute('fill-opacity','0.16');ttN.textContent=tool.name;ttD.textContent=tool.desc;ttB.style.display='inline-block';tooltip.style.opacity='1';pos(e);}});
g.addEventListener('mousemove',e=>pos(e));
g.addEventListener('mouseleave',()=>{{c.setAttribute('stroke-width','1.5');halo.setAttribute('fill-opacity','0.07');tooltip.style.opacity='0';}});
g.addEventListener('click',()=>{{if(tool.status!=='live')return;c.setAttribute('stroke-width','4');halo.setAttribute('fill-opacity','0.28');halo.setAttribute('r',tool.r+22);setTimeout(()=>{{window.parent.location.href=tool.page;}},280);}});}});
function pos(e){{const x=e.clientX,y=e.clientY;tooltip.style.left=(x+244>window.innerWidth?x-244:x+14)+'px';tooltip.style.top=(y+104>window.innerHeight?y-104:y+14)+'px';}}
</script></body></html>
"""

components.html(constellation_html, height=400, scrolling=False)

# ── Quick Links ───────────────────────────────────────────────────────────────
st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
st.markdown(f"""<div style="text-align:center;margin-bottom:12px">
<span style="font-size:11px;color:{T['muted']};font-weight:600;letter-spacing:1px;text-transform:uppercase;font-family:'Plus Jakarta Sans',sans-serif">Truy cập nhanh</span></div>""", unsafe_allow_html=True)

live_tools = [t for t in TOOLS if t["status"] == "live"]
cols = st.columns(len(live_tools))
for i, tool in enumerate(live_tools):
    with cols[i]:
        st.page_link(f"pages/{tool['id']}.py", label=f"{tool['icon']}  {tool['name']}", use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
st.markdown(f"""
<div style="background:{T['card']};border:1px solid {T['border']};border-radius:16px;padding:20px 26px">
    <div style="font-size:14px;font-weight:700;color:{T['text']};margin-bottom:6px;font-family:'Plus Jakarta Sans',sans-serif">💡 Thông tin bảo mật</div>
    <p style="color:{T['muted']};font-size:13px;line-height:1.7;margin:0;font-family:'Plus Jakarta Sans',sans-serif">
        Toàn bộ dữ liệu được xử lý tại trình duyệt (Local). Không lưu trữ thông tin sinh viên trên server.
    </p>
</div>
<div style="height:36px"></div>
<div style="text-align:center"><span style="color:{T['muted']};font-size:12px;font-family:'Plus Jakarta Sans',sans-serif">© 2026 YenLT31 — FE Education QA Department</span></div>
<div style="height:20px"></div>
""", unsafe_allow_html=True)
