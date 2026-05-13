<!DOCTYPE html>
<html class="light" lang="vi">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Digital Registrar | Rà soát Dữ liệu Xét tốt nghiệp</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
<script id="tailwind-config">
tailwind.config={darkMode:"class",theme:{extend:{colors:{"primary":"#1A237E","on-primary":"#ffffff","primary-container":"#E8EAF6","on-primary-container":"#1A237E","secondary":"#5C6BC0","on-secondary":"#ffffff","secondary-container":"#E8EAF6","on-secondary-container":"#1A237E","error":"#B71C1C","error-container":"#FFEBEE","surface":"#F8F9FA","on-surface":"#1A1C1E","surface-variant":"#E1E2EC","on-surface-variant":"#44474E","outline":"#74777F","outline-variant":"#C4C6CF","background":"#F8F9FA"},borderRadius:{DEFAULT:"0.375rem",lg:"0.5rem",xl:"0.75rem","2xl":"1rem","3xl":"1.5rem",full:"9999px"},fontFamily:{headline:["Be Vietnam Pro"],body:["Inter"],label:["Inter"]}}}}
</script>
<style>
.material-symbols-outlined{font-variation-settings:'FILL' 0,'wght' 400,'GRAD' 0,'opsz' 24;vertical-align:middle;}
body{font-family:'Inter',sans-serif;}
h1,h2,h3,.font-headline{font-family:'Be Vietnam Pro',sans-serif;}
.card-shadow{box-shadow:0 4px 20px -2px rgba(0,0,0,0.04);}
.panel{display:none;}.panel.active{display:block;}
.cell-ok{background-color:rgba(34,197,94,0.1);color:#15803d;font-weight:700;border-radius:9999px;padding:2px 12px;display:inline-flex;align-items:center;justify-content:center;min-width:60px;font-size:10px;text-transform:uppercase;}
.cell-err{background-color:#fee2e2;color:#b91c1c;font-weight:700;border-radius:9999px;padding:2px 12px;display:inline-flex;align-items:center;justify-content:center;min-width:60px;font-size:10px;text-transform:uppercase;}
.cell-warn{background-color:#fef3c7;color:#92400e;font-weight:700;border-radius:9999px;padding:2px 12px;display:inline-flex;align-items:center;justify-content:center;min-width:60px;font-size:10px;text-transform:uppercase;}
.cell-info{background-color:#dbeafe;color:#1d4ed8;font-weight:700;border-radius:9999px;padding:2px 12px;display:inline-flex;align-items:center;justify-content:center;min-width:60px;font-size:10px;text-transform:uppercase;}
.upload-card.loaded{border-color:#1A237E;background-color:#E8EAF6;}
.upload-card.error{border-color:#B71C1C;background-color:#FFEBEE;}
/* Search result styles */
.stu-card{border-top:1px solid #E1E2EC;padding:20px;}
.stu-header{display:flex;align-items:center;gap:12px;margin-bottom:12px;padding-bottom:12px;border-bottom:2px solid #E8EAF6;}
.stu-avatar{width:40px;height:40px;border-radius:50%;background:#E8EAF6;color:#1A237E;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:16px;flex-shrink:0;}
.stu-section{margin-bottom:16px;}
.stu-section h4{font-size:12px;font-weight:700;color:#1A237E;margin-bottom:8px;padding:4px 0;border-bottom:1px solid #E1E2EC;text-transform:uppercase;letter-spacing:.05em;}
.stu-mini-table{width:100%;border-collapse:collapse;font-size:11px;max-height:320px;overflow-y:auto;display:block;}
.stu-mini-table th{background:#F8F9FA;padding:6px 10px;text-align:left;font-weight:700;color:#44474E;border-bottom:1px solid #E1E2EC;position:sticky;top:0;white-space:nowrap;font-size:10px;text-transform:uppercase;letter-spacing:.05em;}
.stu-mini-table td{padding:6px 10px;border-bottom:1px solid #F8F9FA;color:#44474E;}
.stu-mini-table tr:hover td{background:#F8F9FA;}
</style>
</head>
<body class="bg-surface text-on-surface" style="--tw-selection-bg:#FDE68A;--tw-selection-text:#1A237E">
<style>::selection{background:#FDE68A;color:#1A237E;}</style>

<!-- HEADER -->
<header class="bg-white border-b border-surface-variant sticky top-0 z-50">
<div class="flex justify-between items-center w-full px-12 py-5 max-w-screen-2xl mx-auto">
  <div class="flex items-center gap-10">
    <span class="text-xl font-black text-primary tracking-tight">Graduation Data Reviewer</span>
    <nav class="hidden md:flex items-center gap-8 text-sm">
      <a class="text-on-surface-variant font-medium hover:text-primary transition-colors cursor-pointer" onclick="goToStep(1)">Upload</a>
      <a class="text-on-surface-variant font-medium hover:text-primary transition-colors cursor-pointer" id="nav-processing">Processing</a>
      <a class="text-on-surface-variant font-medium hover:text-primary transition-colors cursor-pointer" id="nav-results">Results</a>
    </nav>
  </div>
</div>
</header>

<main class="max-w-screen-2xl mx-auto px-12 py-10">

<!-- PANEL 1: UPLOAD -->
<section class="panel active space-y-10" id="panel1">
<div class="space-y-2">
  <h2 class="text-3xl font-black text-on-surface tracking-tight">Tải lên dữ liệu</h2>
  <p class="text-on-surface-variant">Vui lòng tải lên 5 tệp dữ liệu cần thiết để bắt đầu rà soát.</p>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
  <div class="bg-white p-6 rounded-3xl border-2 border-dashed border-outline-variant hover:border-primary transition-all cursor-pointer relative upload-card" id="card_cancheck">
    <input accept=".xlsx,.xls" class="absolute inset-0 opacity-0 cursor-pointer" onclick="this.value=''" onchange="handleFile(event,'cancheck')" type="file"/>
    <div class="space-y-4">
      <div class="w-12 h-12 bg-primary-container rounded-2xl flex items-center justify-center text-primary"><span class="material-symbols-outlined text-2xl">description</span></div>
      <div><h4 class="font-bold text-on-surface">File Can Check</h4><p class="text-[10px] text-on-surface-variant mt-1">DS SV đủ điều kiện TN từ ĐT</p></div>
      <div class="bg-surface p-3 rounded-xl"><p class="text-[9px] font-bold text-primary uppercase tracking-tighter">Bắt buộc:</p><p class="text-[10px] text-on-surface-variant">RollNumber, FullName, Điểm TB/GPA</p></div>
      <div id="status_cancheck"></div>
    </div>
  </div>
  <div class="bg-white p-6 rounded-3xl border-2 border-dashed border-outline-variant hover:border-primary transition-all cursor-pointer relative upload-card" id="card_currstudent">
    <input accept=".xlsx,.xls" class="absolute inset-0 opacity-0 cursor-pointer" onclick="this.value=''" onchange="handleFile(event,'currstudent')" type="file"/>
    <div class="space-y-4">
      <div class="w-12 h-12 bg-primary-container rounded-2xl flex items-center justify-center text-primary"><span class="material-symbols-outlined text-2xl">person_pin</span></div>
      <div><h4 class="font-bold text-on-surface">CurriculumStudent</h4><p class="text-[10px] text-on-surface-variant mt-1">Mapping SV — Khung CT</p></div>
      <div class="bg-surface p-3 rounded-xl"><p class="text-[9px] font-bold text-primary uppercase tracking-tighter">Bắt buộc:</p><p class="text-[10px] text-on-surface-variant">RollNumber, CurriculumCode</p></div>
      <div id="status_currstudent"></div>
    </div>
  </div>
  <div class="bg-white p-6 rounded-3xl border-2 border-dashed border-outline-variant hover:border-primary transition-all cursor-pointer relative upload-card" id="card_currsubject">
    <input accept=".xlsx,.xls" class="absolute inset-0 opacity-0 cursor-pointer" onclick="this.value=''" onchange="handleFile(event,'currsubject')" type="file"/>
    <div class="space-y-4">
      <div class="w-12 h-12 bg-primary-container rounded-2xl flex items-center justify-center text-primary"><span class="material-symbols-outlined text-2xl">menu_book</span></div>
      <div><h4 class="font-bold text-on-surface">CurriculumSubject</h4><p class="text-[10px] text-on-surface-variant mt-1">DS môn theo khung CT</p></div>
      <div class="bg-surface p-3 rounded-xl"><p class="text-[9px] font-bold text-primary uppercase tracking-tighter">Bắt buộc:</p><p class="text-[10px] text-on-surface-variant">CurriculumCode, SubjectCode, Credits</p></div>
      <div id="status_currsubject"></div>
    </div>
  </div>
  <div class="bg-white p-6 rounded-3xl border-2 border-dashed border-outline-variant hover:border-primary transition-all cursor-pointer relative upload-card" id="card_mark">
    <input accept=".xlsx,.xls" class="absolute inset-0 opacity-0 cursor-pointer" onclick="this.value=''" onchange="handleFile(event,'mark')" type="file"/>
    <div class="space-y-4">
      <div class="w-12 h-12 bg-primary-container rounded-2xl flex items-center justify-center text-primary"><span class="material-symbols-outlined text-2xl">analytics</span></div>
      <div><h4 class="font-bold text-on-surface">File Mark (FAP)</h4><p class="text-[10px] text-on-surface-variant mt-1">Dữ liệu điểm từ hệ thống FAP</p></div>
      <div class="bg-surface p-3 rounded-xl"><p class="text-[9px] font-bold text-primary uppercase tracking-tighter">Bắt buộc:</p><p class="text-[10px] text-on-surface-variant">RollNumber, SubjectCode, AverageMark, Status, EndDate, Credits</p></div>
      <div id="status_mark"></div>
    </div>
  </div>
  <div class="bg-white p-6 rounded-3xl border-2 border-dashed border-outline-variant hover:border-primary transition-all cursor-pointer relative upload-card" id="card_replacecode">
    <input accept=".xlsx,.xls" class="absolute inset-0 opacity-0 cursor-pointer" onclick="this.value=''" onchange="handleFile(event,'replacecode')" type="file"/>
    <div class="space-y-4">
      <div class="w-12 h-12 bg-primary-container rounded-2xl flex items-center justify-center text-primary"><span class="material-symbols-outlined text-2xl">swap_horiz</span></div>
      <div><h4 class="font-bold text-on-surface">ReplaceCode</h4><p class="text-[10px] text-on-surface-variant mt-1">Bảng danh mục môn thay thế</p></div>
      <div class="bg-surface p-3 rounded-xl"><p class="text-[9px] font-bold text-primary uppercase tracking-tighter">Bắt buộc:</p><p class="text-[10px] text-on-surface-variant">SubjectCode, replacecode, equivalent, note</p></div>
      <div id="status_replacecode"></div>
    </div>
  </div>
</div>
<div class="flex flex-col items-center gap-4 pt-6">
  <button class="px-10 py-4 bg-primary text-on-primary font-black rounded-2xl shadow-lg shadow-primary/20 disabled:opacity-30 disabled:shadow-none hover:opacity-90 transition-all flex items-center gap-3" disabled id="btnProcess" onclick="startProcessing()">
    <span class="material-symbols-outlined">play_circle</span> Bắt đầu rà soát
  </button>
  <div class="hidden max-w-2xl w-full p-4 bg-error-container text-error rounded-2xl border border-error/20 text-center font-bold text-sm" id="rerunBanner">
    ⚠ Một hoặc nhiều tệp vừa được thay đổi. Vui lòng chạy lại rà soát để cập nhật kết quả.
  </div>
</div>
</section>

<!-- PANEL 2: PROCESSING -->
<section class="panel space-y-10" id="panel2">
<div class="max-w-2xl mx-auto space-y-8 bg-white p-10 rounded-3xl card-shadow border border-surface-variant">
  <div class="flex items-center gap-4">
    <div class="animate-spin text-primary"><span class="material-symbols-outlined text-3xl">sync</span></div>
    <div><h3 class="text-xl font-bold">Đang xử lý dữ liệu...</h3><p class="text-sm text-on-surface-variant">Vui lòng không đóng trình duyệt.</p></div>
  </div>
  <div class="space-y-2">
    <div class="process-step flex items-center gap-4 p-4 rounded-2xl transition-colors" id="ps1"><div class="process-icon w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center text-xs font-bold">1</div><div class="flex-1"><p class="text-sm font-bold">Đọc &amp; chuẩn hóa dữ liệu</p><p class="process-detail text-xs text-on-surface-variant">Chuẩn hóa mã môn (đ/Đ/Ð → D), trim, uppercase RollNumber</p></div></div>
    <div class="process-step flex items-center gap-4 p-4 rounded-2xl transition-colors" id="ps2"><div class="process-icon w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center text-xs font-bold">2</div><div class="flex-1"><p class="text-sm font-bold">Khởi tạo Mark_DT</p><p class="process-detail text-xs text-on-surface-variant">Hợp nhất dữ liệu từ file Can Check</p></div></div>
    <div class="process-step flex flex-col gap-2 p-4 rounded-2xl transition-colors" id="ps3">
      <div class="flex items-center gap-4">
        <div class="process-icon w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center text-xs font-bold">3</div>
        <div class="flex-1"><p class="text-sm font-bold">Khởi tạo Mark_FAP</p><p class="process-detail text-xs text-on-surface-variant" id="ps3detail">Lọc SV, chuẩn hóa mã môn, lần học gần nhất theo EndDate</p></div>
      </div>
      <div class="hidden pl-12" id="ps3progress">
        <div class="w-full h-2 bg-surface-variant rounded-full overflow-hidden"><div class="h-full bg-primary transition-all duration-300" id="ps3bar" style="width:0%"></div></div>
        <p class="text-[10px] font-bold text-primary mt-1" id="ps3pct">0%</p>
      </div>
    </div>
    <div class="process-step flex items-center gap-4 p-4 rounded-2xl transition-colors" id="ps4"><div class="process-icon w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center text-xs font-bold">4</div><div class="flex-1"><p class="text-sm font-bold">Đối chiếu điểm (Check Mark)</p><p class="process-detail text-xs text-on-surface-variant">So khớp điểm Đào tạo vs FAP</p></div></div>
    <div class="process-step flex items-center gap-4 p-4 rounded-2xl transition-colors" id="ps5"><div class="process-icon w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center text-xs font-bold">5</div><div class="flex-1"><p class="text-sm font-bold">Kiểm tra môn thay thế (Check Replace)</p><p class="process-detail text-xs text-on-surface-variant">Rà soát các mã môn tương đương</p></div></div>
    <div class="process-step flex items-center gap-4 p-4 rounded-2xl transition-colors" id="ps6"><div class="process-icon w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center text-xs font-bold">6</div><div class="flex-1"><p class="text-sm font-bold">Tính toán GPA</p><p class="process-detail text-xs text-on-surface-variant">Đối chiếu GPA tích lũy</p></div></div>
    <div class="process-step flex items-center gap-4 p-4 rounded-2xl transition-colors" id="ps7"><div class="process-icon w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center text-xs font-bold">7</div><div class="flex-1"><p class="text-sm font-bold">Tổng hợp kết quả</p><p class="process-detail text-xs text-on-surface-variant">Phân tích và tổng hợp dữ liệu cuối</p></div></div>
  </div>
  <div class="pt-6 border-t border-surface-variant" id="perfInfo"></div>
  <div id="processError"></div>
</div>
</section>

<!-- PANEL 3: RESULTS -->
<section class="panel space-y-10" id="panel3">
<div class="flex items-center justify-between flex-wrap gap-4">
  <div class="space-y-1">
    <h2 class="text-3xl font-black text-on-surface tracking-tight">Kết quả rà soát</h2>
    <p class="text-on-surface-variant font-medium text-sm" id="lastUpdated">Cập nhật lần cuối: --:--</p>
  </div>
  <div class="flex flex-wrap gap-3">
    <button class="px-5 py-2.5 bg-white text-primary border border-primary/20 font-bold text-xs rounded-xl flex items-center gap-2 hover:bg-primary-container transition-all shadow-sm" onclick="downloadResult()"><span class="material-symbols-outlined text-lg">description</span> Tải báo cáo</button>
    <button class="px-5 py-2.5 bg-secondary-container text-on-secondary-container font-bold text-xs rounded-xl flex items-center gap-2 hover:opacity-90 transition-all shadow-sm" onclick="downloadMarkFAP()"><span class="material-symbols-outlined text-lg">sync_alt</span> Xuất Mark_FAP</button>
    <button class="px-5 py-2.5 bg-primary text-on-primary font-bold text-xs rounded-xl flex items-center gap-2 hover:opacity-90 transition-all shadow-lg shadow-primary/10" onclick="downloadMarkDT()"><span class="material-symbols-outlined text-lg">cloud_download</span> Xuất Mark_DT</button>
  </div>
</div>
<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-7 gap-4" id="summaryCards"></div>
<div class="bg-white rounded-3xl card-shadow border border-surface-variant overflow-hidden">
  <div class="flex items-center justify-between border-b border-surface-variant px-8">
    <div class="flex overflow-x-auto" id="resultTabs"></div>
    <div class="pr-4 hidden xl:flex items-center gap-2 text-xs font-semibold text-green-600 shrink-0">
      <span class="flex h-2 w-2 rounded-full bg-green-500 animate-pulse"></span>Hệ thống sẵn sàng
    </div>
  </div>
  <div class="min-h-[600px]" id="resultContent"></div>
</div>
</section>
</main>

<footer class="bg-white border-t border-surface-variant mt-20">
<div class="flex flex-col md:flex-row justify-between items-center px-12 py-12 w-full max-w-screen-2xl mx-auto text-sm text-on-surface-variant">
  <div class="mb-6 md:mb-0 space-y-2 text-center md:text-left">
    <span class="text-lg font-black text-primary">Graduation Data Reviewer</span>
    <p>© 2025 Phòng Đảm bảo Chất lượng. Dữ liệu được bảo mật tuyệt đối tại Local.</p>
  </div>
  <div class="flex flex-wrap justify-center gap-8 font-medium">
    <a class="hover:text-primary transition-colors cursor-pointer">Bảo mật dữ liệu</a>
    <a class="hover:text-primary transition-colors cursor-pointer">Hỗ trợ hệ thống</a>
    <a class="hover:text-primary transition-colors cursor-pointer" onclick="resetAll()">Làm lại rà soát</a>
  </div>
</div>
</footer>

<div class="fixed inset-0 bg-white/90 z-[100] flex-col items-center justify-center gap-4 hidden" id="loadingOverlay">
  <div class="w-12 h-12 border-4 border-surface-variant border-t-primary rounded-full animate-spin"></div>
  <p class="font-bold text-primary" id="loadingText">Đang tải...</p>
</div>

<script>
// ==================== State ====================
const FILES={},FILE_KEYS=['cancheck','currstudent','currsubject','mark','replacecode'];
const FILE_BUFFERS={}; // raw ArrayBuffers for worker transfer
let RESULT={},processStartTime=null,perfStats={},_currentRollTokens=[],searchDebounce=null;
const DT={};

// ==================== Worker Code ====================
// Worker 1: XLSX.read only (for 4 small files)
const XLSX_WORKER_CODE=`importScripts('https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js');
self.onmessage=function(e){
  try{const wb=XLSX.read(e.data,{type:'array',cellDates:true});self.postMessage({ok:true,wb});}
  catch(er){self.postMessage({ok:false,error:er.message});}
};`;

// Worker 2: XLSX.read + full Mark_FAP processing (for large mark file)
const FAP_WORKER_CODE=`importScripts('https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js');
function cS(v){return v==null?'':String(v).trim();}
function cC(v){if(v==null)return'';return String(v).normalize('NFC').trim().replace(/[\u0110\u0111\u00D0\u00F0\u0111\u0110]/g,'D').replace(/[dD]\u0301/g,'D');}
function cN(v){if(v==null)return null;if(typeof v==='number')return v;const n=parseFloat(String(v).trim().replace(',','.'));return isNaN(n)?null:n;}
function sVN(s){return s?s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[dD]\u0323/g,'D').replace(/[dD]\u0301/g,'D'):'';}
function fC(h,cands){
  const norm=h.map(x=>sVN(x).toLowerCase().replace(/\\s+/g,''));
  for(const c of cands){const cn=sVN(c).toLowerCase().replace(/\\s+/g,'');const i=norm.indexOf(cn);if(i>=0)return h[i];}
  for(const c of cands){const cn=sVN(c).toLowerCase().replace(/\\s+/g,'');const i=norm.findIndex(x=>x.includes(cn)||cn.includes(x));if(i>=0)return h[i];}
  return null;
}
function dDF(rows,col){
  for(const row of rows.slice(0,200)){const v=row[col];if(!v||v instanceof Date)continue;const s=cS(String(v));const m=s.match(/^(\\d{1,2})[\\/\\-\\.](\\d{1,2})[\\/\\-\\.](\\d{4})$/);if(!m)continue;if(+m[1]>12)return'dmy';if(+m[2]>12)return'mdy';}return'dmy';
}
function pD(val,fmt){
  fmt=fmt||'dmy';if(!val)return null;if(val instanceof Date)return isNaN(val.getTime())?null:val;
  const s=cS(String(val));if(!s)return null;
  const dmy=s.match(/^(\\d{1,2})[\\/\\-\\.](\\d{1,2})[\\/\\-\\.](\\d{4})$/);
  if(dmy){const p1=+dmy[1],p2=+dmy[2],yr=+dmy[3];const day=fmt==='mdy'?p2:p1,mon=fmt==='mdy'?p1:p2;if(mon>=1&&mon<=12&&day>=1&&day<=31){const d=new Date(yr,mon-1,day);if(!isNaN(d.getTime()))return d;}}
  const ymd=s.match(/^(\\d{4})[\\/\\-\\.](\\d{1,2})[\\/\\-\\.](\\d{1,2})$/);if(ymd){const d=new Date(+ymd[1],+ymd[2]-1,+ymd[3]);if(!isNaN(d.getTime()))return d;}
  return null;
}
self.onmessage=function(e){
  const {buffer,studentSet}=e.data;
  const stuLookup=new Set(studentSet);
  try{
    self.postMessage({type:'progress',pct:10,text:'Đang đọc file...',detail:'XLSX.read — vui lòng chờ'});
    const wb=XLSX.read(new Uint8Array(buffer),{type:'array',cellDates:true});
    self.postMessage({type:'progress',pct:35,text:'Đang phân tích cột...',detail:'Xác định cấu trúc dữ liệu'});
    const firstRows=XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]],{defval:'',range:0});
    if(!firstRows.length){self.postMessage({type:'error',message:'File Mark trống'});return;}
    const h=Object.keys(firstRows[0]);
    const rollCol=fC(h,['RollNumber','Roll Number','MSSV','Rollnumber']);
    const subCol=fC(h,['SubjectCode','Subject Code','MaMon']);
    const markCol=fC(h,['AverageMark','Average Mark','Diem','Mark','Averagemark']);
    const statusCol=fC(h,['Status','TrangThai']);
    const endDateCol=fC(h,['EndDate','End Date','NgayKT','Enddate']);
    const startDateCol=fC(h,['StartDate','Start Date','NgayBD','Startdate']);
    const creditsCol=fC(h,['Credits','SoTC','TinChi','Credit']);
    if(!rollCol||!subCol){self.postMessage({type:'error',message:'File Mark thiếu cột RollNumber hoặc SubjectCode'});return;}
    const sampleRows=XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]],{defval:'',range:{s:{r:0,c:0},e:{r:200,c:99}}});
    const dateCol=startDateCol||endDateCol;
    const dateFmt=dateCol?dDF(sampleRows,dateCol):'dmy';
    let totalRows=0;
    wb.SheetNames.forEach(sn=>{const ws=wb.Sheets[sn];if(ws['!ref'])totalRows+=XLSX.utils.decode_range(ws['!ref']).e.r;});
    const grouped={};let processed=0;const CHUNK=50000;
    for(const sheetName of wb.SheetNames){
      const ws=wb.Sheets[sheetName];if(!ws['!ref'])continue;
      const allRows=XLSX.utils.sheet_to_json(ws,{defval:'',cellDates:true});const len=allRows.length;
      for(let j=0;j<len;j++){
        const row=allRows[j];
        const roll=cS(row[rollCol]).toUpperCase();if(!roll||!stuLookup.has(roll))continue;
        const subCode=cC(row[subCol]).replace(/[đĐ]/g,'D');if(!subCode)continue;
        const endDate=endDateCol?pD(row[endDateCol],dateFmt):null;
        const startDate=startDateCol?pD(row[startDateCol],dateFmt):null;
        let avgMark=markCol?row[markCol]:null,numMark=null,textMark='';
        if(avgMark!=null&&avgMark!==''){numMark=cN(avgMark);if(numMark===null)textMark=cS(String(avgMark));}
        const rec={RollNumber:roll,SubjectCode:subCode,AverageMark:numMark!==null?numMark:textMark,AverageMarkNum:numMark,Status:statusCol?cS(row[statusCol]):'',StartDate:startDate,EndDate:endDate,Credits:creditsCol?cN(row[creditsCol]):null};
        const key=roll+'|'+subCode;
        if(!grouped[key])grouped[key]=rec;
        else{const ex=grouped[key];
          if(rec.EndDate&&ex.EndDate){if(rec.EndDate.getTime()>ex.EndDate.getTime())grouped[key]=rec;}
          else if(rec.EndDate&&!ex.EndDate)grouped[key]=rec;
          else if(!rec.EndDate&&!ex.EndDate)grouped[key]=rec;}
        processed++;
        if(processed%CHUNK===0){
          const pct=Math.min(95,35+Math.round(processed/totalRows*60));
          self.postMessage({type:'progress',pct,text:processed.toLocaleString()+'/'+totalRows.toLocaleString()+' ('+pct+'%)',detail:'Sheet "'+sheetName+'" | Ngày: '+(dateFmt==='mdy'?'mm/dd/yyyy':'dd/mm/yyyy')});
        }
      }
    }
    self.postMessage({type:'done',result:Object.values(grouped)});
  }catch(err){self.postMessage({type:'error',message:err.message});}
};`;

function makeWorkerURL(code){return URL.createObjectURL(new Blob([code],{type:'application/javascript'}));}

// ==================== DataTable ====================
class DataTable{
constructor(id,cols,data,opts={}){this.id=id;this.cols=cols;this.allData=data;this.filteredData=data;this.sortCol=null;this.sortDir='asc';this.page=0;this.pageSize=opts.pageSize||100;this.searchText='';this.errorsOnly=false;this.checkCol=opts.checkCol||'Check';this.okValues=opts.okValues||['OK'];this.hasFilter=opts.hasFilter!==false;this.render();}
applyFilters(){let d=this.allData;if(this.errorsOnly)d=d.filter(r=>!this.okValues.some(v=>String(r[this.checkCol]).startsWith(v)));if(this.searchText){const q=this.searchText.toLowerCase();d=d.filter(r=>this.cols.some(c=>String(r[c]||'').toLowerCase().includes(q)));}if(this.sortCol!==null){const col=this.cols[this.sortCol],dir=this.sortDir==='asc'?1:-1;d=[...d].sort((a,b)=>{let va=a[col]??'',vb=b[col]??'';const na=parseFloat(va),nb=parseFloat(vb);if(!isNaN(na)&&!isNaN(nb))return(na-nb)*dir;return String(va).localeCompare(String(vb),'vi')*dir;});}this.filteredData=d;this.page=0;}
tp(){return Math.max(1,Math.ceil(this.filteredData.length/this.pageSize));}
pd(){return this.filteredData.slice(this.page*this.pageSize,(this.page+1)*this.pageSize);}
esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
render(){
const el=document.getElementById(this.id);if(!el)return;
const t=this.filteredData.length,a=this.allData.length,pg=this.pd(),tp=this.tp();
let h=`<div><div class="px-5 py-3 bg-surface/30 border-b border-surface-variant flex items-center gap-3">
<div class="relative flex-1 min-w-0"><span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-outline text-base">search</span>
<input class="w-full pl-11 pr-4 py-2.5 bg-white border border-surface-variant rounded-2xl focus:ring-4 focus:ring-primary/10 text-sm transition-all" placeholder="Tìm tên, mã SV, mã môn..." type="text" onkeyup="DT['${this.id}'].onSearch(this.value)" value="${this.esc(this.searchText)}"></div>
${this.hasFilter?`<label style="white-space:nowrap;flex-shrink:0;display:flex;align-items:center;gap:6px;padding:8px 14px;border-radius:14px;font-size:11px;font-weight:900;cursor:pointer;user-select:none;transition:all .2s;${this.errorsOnly?'background:#1A237E;color:#fff;box-shadow:0 4px 12px rgba(26,35,126,.25)':'background:#E8EAF6;color:#1A237E;border:2px solid #9FA8DA'}"><input type="checkbox" style="display:none" ${this.errorsOnly?'checked':''} onchange="DT['${this.id}'].toggleErr(this.checked)"><span class="material-symbols-outlined" style="font-size:16px;color:#FDD835;${this.errorsOnly?'filter:drop-shadow(0 0 4px rgba(253,216,53,.6))':''}">warning</span>Chỉ hiện lỗi</label>`:''}
<span style="white-space:nowrap;flex-shrink:0;font-size:10px;font-weight:700;color:#74777F;letter-spacing:.06em;text-transform:uppercase">${t.toLocaleString()} / ${a.toLocaleString()}</span>
</div>
</div>
<div style="overflow-y:auto;max-height:560px;overflow-x:hidden">
<table style="width:100%;border-collapse:separate;border-spacing:0;table-layout:auto;font-size:12px">
<thead><tr style="position:sticky;top:0;z-index:10">`;
this.cols.forEach((c,i)=>{
const ar=this.sortCol===i?(this.sortDir==='asc'?'arrow_upward':'arrow_downward'):'unfold_more';
const isCheck=(c===this.checkCol),isStt=(c==='Stt');
const extraW=isStt?'width:52px;min-width:52px;max-width:52px;text-align:center;padding:10px 4px;':isCheck?'min-width:190px;':'';
h+=`<th style="background:#ECEEF8;border-bottom:2px solid #C4C6CF;padding:10px 12px;font-size:10px;font-weight:900;text-transform:uppercase;letter-spacing:.06em;color:#44474E;cursor:pointer;text-align:left;white-space:nowrap;${extraW}" onclick="DT['${this.id}'].onSort(${i})"><div style="display:flex;align-items:center;gap:3px">${c}<span class="material-symbols-outlined" style="font-size:12px;opacity:.4">${ar}</span></div></th>`;});
h+=`</tr></thead><tbody>`;
if(!pg.length)h+=`<tr><td colspan="${this.cols.length}" style="padding:48px;text-align:center;color:#74777F;font-style:italic">Không tìm thấy dữ liệu phù hợp</td></tr>`;
else pg.forEach((row,ri)=>{
const rowBg=ri%2===0?'#ffffff':'#FAFAFA';
h+=`<tr onmouseover="this.style.background='#EEF0FC'" onmouseout="this.style.background='${rowBg}'" style="background:${rowBg}">`;
this.cols.forEach(c=>{
let v=row[c]!==undefined?row[c]:'',innerCls='';
const isCheck=(c===this.checkCol),isStt=(c==='Stt');
if(isCheck){const sv=String(v);if(this.okValues.some(x=>sv.startsWith(x)))innerCls='cell-ok';else if(sv.includes('kỹ thuật'))innerCls='cell-info';else if(sv.includes('Lệch')||sv==='Not ok')innerCls='cell-err';else if(sv.includes('Thiếu')||sv.includes('Không'))innerCls='cell-warn';else if(sv!=='')innerCls='cell-err';}
const isBold=(c==='FullName'||c==='RollNumber');
const tdStyle=isStt
  ?'padding:9px 4px;border-bottom:1px solid #F0F1F5;vertical-align:middle;white-space:nowrap;text-align:center;color:#74777F;width:52px;max-width:52px;font-size:11px'
  :`padding:9px 12px;border-bottom:1px solid #F0F1F5;vertical-align:top;word-break:break-word;color:${isBold?'#1A237E':'#44474E'};font-weight:${isBold?700:400}`;
const badgeStyle=innerCls?'white-space:nowrap':'';
h+=`<td style="${tdStyle}"><span class="${innerCls}" style="${badgeStyle}">${this.esc(String(v))}</span></td>`;});
h+=`</tr>`;});
h+=`</tbody></table></div>
<div class="px-6 py-4 flex items-center justify-between border-t border-surface-variant flex-wrap gap-4">
<div class="flex items-center gap-3"><span class="text-xs text-on-surface-variant font-medium">Trang ${this.page+1} / ${tp}</span>
<select class="text-xs border border-surface-variant rounded-lg py-1.5 px-2 focus:ring-primary/20" onchange="DT['${this.id}'].onPS(+this.value)">${[50,100,200,500].map(n=>`<option value="${n}" ${this.pageSize===n?'selected':''}>${n} dòng</option>`).join('')}</select></div>
<div class="flex gap-1">
<button class="w-9 h-9 flex items-center justify-center rounded-xl border border-surface-variant text-primary hover:bg-surface-variant transition-all disabled:opacity-20" ${this.page===0?'disabled':''} onclick="DT['${this.id}'].gp(0)"><span class="material-symbols-outlined text-sm">first_page</span></button>
<button class="w-9 h-9 flex items-center justify-center rounded-xl border border-surface-variant text-primary hover:bg-surface-variant transition-all disabled:opacity-20" ${this.page===0?'disabled':''} onclick="DT['${this.id}'].gp(${this.page-1})"><span class="material-symbols-outlined text-sm">chevron_left</span></button>
<button class="w-9 h-9 flex items-center justify-center rounded-xl border border-surface-variant text-primary hover:bg-surface-variant transition-all disabled:opacity-20" ${this.page>=tp-1?'disabled':''} onclick="DT['${this.id}'].gp(${this.page+1})"><span class="material-symbols-outlined text-sm">chevron_right</span></button>
<button class="w-9 h-9 flex items-center justify-center rounded-xl border border-surface-variant text-primary hover:bg-surface-variant transition-all disabled:opacity-20" ${this.page>=tp-1?'disabled':''} onclick="DT['${this.id}'].gp(${tp-1})"><span class="material-symbols-outlined text-sm">last_page</span></button>
</div></div></div>`;
el.innerHTML=h;
// Restore focus & cursor to search input after re-render
const newInput=el.querySelector('input[type="text"]');
if(newInput&&this._searchFocused){newInput.focus();const pos=this._cursorPos??newInput.value.length;newInput.setSelectionRange(pos,pos);}
this._searchFocused=false;}
onSearch(v){this._searchFocused=true;const inp=document.getElementById(this.id)?.querySelector('input[type="text"]');this._cursorPos=inp?inp.selectionStart:null;this.searchText=v;this.applyFilters();this.render();}
onSort(i){if(this.sortCol===i)this.sortDir=this.sortDir==='asc'?'desc':'asc';else{this.sortCol=i;this.sortDir='asc';}this.applyFilters();this.render();}
toggleErr(v){this.errorsOnly=v;this.applyFilters();this.render();}
gp(p){this.page=Math.max(0,Math.min(p,this.tp()-1));this.render();}
onPS(n){this.pageSize=n;this.page=0;this.render();}
}

// ==================== File ====================
function handleFile(e,key){
const file=e.target.files[0];if(!file)return;
const card=document.getElementById('card_'+key),st=document.getElementById('status_'+key);
st.innerHTML=`<div class="flex items-center gap-2 mt-2"><div class="w-3 h-3 border-2 border-primary border-t-transparent rounded-full animate-spin"></div><span class="text-[10px] font-bold text-primary">Đang đọc...</span></div>`;
card.classList.remove('loaded','error');
const reader=new FileReader();
reader.onload=function(ev){
  const buffer=ev.target.result;
  if(key==='mark'){
    // Mark file: save raw buffer only — will process in FAP Worker during startProcessing
    FILE_BUFFERS.mark=buffer;
    FILES.mark='__pending__'; // flag as loaded
    const sizeMB=(buffer.byteLength/1024/1024).toFixed(1);
    card.classList.add('loaded');
    st.innerHTML=`<div class="mt-2 flex items-center gap-1 text-[10px] font-bold text-primary"><span class="material-symbols-outlined text-[14px]">check_circle</span> Đã tải (${sizeMB} MB — xử lý khi bắt đầu)</div>`;
    if(RESULT.summary)document.getElementById('rerunBanner').classList.remove('hidden');
    checkAllLoaded();
  } else {
    // Small files: parse in worker → truly parallel
    const url=makeWorkerURL(XLSX_WORKER_CODE);
    const worker=new Worker(url);
    worker.onmessage=function(msg){
      worker.terminate();URL.revokeObjectURL(url);
      if(msg.data.ok){
        FILES[key]=msg.data.wb;card.classList.add('loaded');
        const tr=msg.data.wb.SheetNames.reduce((s,n)=>{const ws=msg.data.wb.Sheets[n];if(!ws['!ref'])return s;return s+XLSX.utils.decode_range(ws['!ref']).e.r;},0);
        st.innerHTML=`<div class="mt-2 flex items-center gap-1 text-[10px] font-bold text-primary"><span class="material-symbols-outlined text-[14px]">check_circle</span> Đã tải (${tr.toLocaleString()} dòng)</div>`;
        if(RESULT.summary)document.getElementById('rerunBanner').classList.remove('hidden');
        checkAllLoaded();
      } else {
        card.classList.add('error');st.innerHTML=`<div class="mt-2 text-[10px] font-bold text-error">✗ ${msg.data.error}</div>`;
      }
    };
    worker.postMessage(buffer,[buffer]); // zero-copy transfer
  }
};
reader.readAsArrayBuffer(file);}

function checkAllLoaded(){document.getElementById('btnProcess').disabled=!FILE_KEYS.every(k=>FILES[k]);}

// ==================== Nav ====================
function goToStep(n){
if(n===3&&!RESULT.summary)return;
document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
document.getElementById('panel'+n).classList.add('active');
['nav-processing','nav-results'].forEach(id=>{const el=document.getElementById(id);if(el)el.className='text-on-surface-variant font-medium hover:text-primary transition-colors cursor-pointer';});
if(n===2)document.getElementById('nav-processing').className='text-primary font-bold border-b-2 border-primary pb-1 cursor-pointer';
if(n===3)document.getElementById('nav-results').className='text-primary font-bold border-b-2 border-primary pb-1 cursor-pointer';
}

function quickSearch(v){}

// ==================== Clean ====================
function cleanStr(v){return v==null?'':String(v).trim();}
function cleanCode(v){if(v==null)return'';return String(v).normalize('NFC').trim().replace(/[\u0110\u0111\u00D0\u00F0đĐ]/g,'D');}
function stripVN(s){return s?s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[đĐ]/g,'D'):'';}
function cleanNum(v){if(v==null)return null;if(typeof v==='number')return v;const n=parseFloat(String(v).trim().replace(',','.'));return isNaN(n)?null:n;}
function roundTo(n,d){if(n==null||isNaN(n))return null;return Math.round(n*Math.pow(10,d))/Math.pow(10,d);}
function readAllSheets(wb){let a=[];wb.SheetNames.forEach(sn=>{XLSX.utils.sheet_to_json(wb.Sheets[sn],{defval:''}).forEach(r=>{r._sheetName=sn;a.push(r);});});return a;}
function findCol(h,candidates){const norm=h.map(x=>stripVN(x).toLowerCase().replace(/\s+/g,''));for(const c of candidates){const cn=stripVN(c).toLowerCase().replace(/\s+/g,'');const i=norm.indexOf(cn);if(i>=0)return h[i];}for(const c of candidates){const cn=stripVN(c).toLowerCase().replace(/\s+/g,'');const i=norm.findIndex(x=>x.includes(cn)||cn.includes(x));if(i>=0)return h[i];}return null;}

// ==================== Date ====================
function detectDateFormat(rows,col){
for(const row of rows.slice(0,200)){const v=row[col];if(!v||v instanceof Date)continue;const s=cleanStr(String(v));const m=s.match(/^(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{4})$/);if(!m)continue;if(+m[1]>12)return'dmy';if(+m[2]>12)return'mdy';}return'dmy';}
function parseDate(val,fmt='dmy'){
if(!val)return null;if(val instanceof Date)return isNaN(val.getTime())?null:val;
const s=cleanStr(String(val));if(!s)return null;
const dmy=s.match(/^(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{4})$/);
if(dmy){const p1=+dmy[1],p2=+dmy[2],yr=+dmy[3];const day=fmt==='mdy'?p2:p1,mon=fmt==='mdy'?p1:p2;if(mon>=1&&mon<=12&&day>=1&&day<=31){const d=new Date(yr,mon-1,day);if(!isNaN(d.getTime()))return d;}}
const ymd=s.match(/^(\d{4})[\/\-\.](\d{1,2})[\/\-\.](\d{1,2})$/);if(ymd){const d=new Date(+ymd[1],+ymd[2]-1,+ymd[3]);if(!isNaN(d.getTime()))return d;}
const d=new Date(s);return isNaN(d.getTime())?null:d;}

// ==================== Subject Helpers ====================
function isSkipSubject(c){if(!c)return false;const u=c.toUpperCase();if(u==='PRO001')return true;return['ENT','TRS','OTP','LUK'].some(p=>u.startsWith(p));}
function isExcludeFromGPA(c){if(!c)return false;const u=c.toUpperCase();return['GDQP','OJ','VOV','ENT','TRS','OTP','LUK'].some(p=>u.startsWith(p));}
function isLAB(c){return c&&c.toUpperCase().startsWith('LAB');}
function isGDQP_OJ_LAB(c){if(!c)return false;const u=c.toUpperCase();return u.startsWith('GDQP')||u.startsWith('OJ')||u.startsWith('LAB');}
function isVOV(c){return c&&c.toUpperCase().startsWith('VOV');}
function isPassStatus(s){if(!s)return false;const l=s.toLowerCase().trim();return['pass','passed','is exempt','*','p'].includes(l);}
function isPassStatusVOV(s){if(!s)return false;const l=s.toLowerCase().trim();return['pass','passed','is exempt'].includes(l);}

// ==================== Utils ====================
function formatMs(ms){return ms<1000?Math.round(ms)+'ms':(ms/1000).toFixed(1)+'s';}
function delay(ms){return new Promise(r=>setTimeout(r,ms));}
function setPS(n,s,d){
const el=document.getElementById('ps'+n);if(!el)return;
if(s==='running'){el.classList.add('bg-primary-container/30');el.querySelector('.process-icon').className='process-icon w-8 h-8 rounded-full bg-primary flex items-center justify-center text-xs font-bold text-white animate-pulse';}
else if(s==='done'){el.classList.remove('bg-primary-container/30');el.classList.add('bg-green-50');el.querySelector('.process-icon').innerHTML='<span class="material-symbols-outlined text-sm">check</span>';el.querySelector('.process-icon').className='process-icon w-8 h-8 rounded-full bg-green-500 flex items-center justify-center text-white';}
else if(s==='error'){el.classList.add('bg-red-50');el.querySelector('.process-icon').innerHTML='<span class="material-symbols-outlined text-sm">error</span>';el.querySelector('.process-icon').className='process-icon w-8 h-8 rounded-full bg-error flex items-center justify-center text-white';}
if(d)el.querySelector('.process-detail').textContent=d;}

// ==================== Processing ====================
async function startProcessing(){
processStartTime=new Date();perfStats={};RESULT={};
Object.keys(DT).forEach(k=>delete DT[k]);
clearSearch();
document.getElementById('rerunBanner').classList.add('hidden');
document.getElementById('resultContent').innerHTML='';
document.getElementById('resultTabs').innerHTML='';
goToStep(2);
for(let i=1;i<=7;i++){const el=document.getElementById('ps'+i);el.className='process-step flex items-center gap-4 p-4 rounded-2xl transition-colors';el.querySelector('.process-icon').innerHTML=i;el.querySelector('.process-icon').className='process-icon w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center text-xs font-bold';}
document.getElementById('processError').innerHTML='';document.getElementById('perfInfo').innerHTML='';
document.getElementById('ps3progress').classList.add('hidden');
await delay(100);
try{
let t0=performance.now();setPS(1,'running');await delay(50);setPS(1,'done');perfStats.s1=performance.now()-t0;
t0=performance.now();setPS(2,'running');await delay(10);const markDT=createMarkDT();perfStats.s2=performance.now()-t0;
setPS(2,'done',`${markDT.marks.length.toLocaleString()} bản ghi, ${markDT.students.length} SV — ${formatMs(perfStats.s2)}`);
t0=performance.now();setPS(3,'running');document.getElementById('ps3progress').classList.remove('hidden');
const markFAP=await createMarkFAPChunked(markDT.studentSet);
document.getElementById('ps3progress').classList.add('hidden');perfStats.s3=performance.now()-t0;
setPS(3,'done',`${markFAP.length.toLocaleString()} bản ghi — ${formatMs(perfStats.s3)}`);
t0=performance.now();setPS(4,'running');await delay(10);const ckm=doCheckMark(markDT,markFAP);perfStats.s4=performance.now()-t0;
setPS(4,'done',`${ckm.length.toLocaleString()} môn — ${formatMs(perfStats.s4)}`);
t0=performance.now();setPS(5,'running');await delay(10);const ckr=doCheckReplace(ckm,markDT,markFAP);perfStats.s5=performance.now()-t0;
setPS(5,'done',`${ckr.length} môn — ${formatMs(perfStats.s5)}`);
t0=performance.now();setPS(6,'running');await delay(10);const ckg=doCheckGPA(markDT,markFAP);perfStats.s6=performance.now()-t0;
setPS(6,'done',`${ckg.length} SV — ${formatMs(perfStats.s6)}`);
t0=performance.now();setPS(7,'running');await delay(10);const sum=genSummary(ckm,ckr,ckg,markDT,markFAP);perfStats.s7=performance.now()-t0;setPS(7,'done');
RESULT={checkMark:ckm,checkReplace:ckr,checkGPA:ckg,summary:sum,markDT,markFAP};
const tt=Object.values(perfStats).reduce((a,b)=>a+b,0);
document.getElementById('perfInfo').innerHTML=`<p class="text-[10px] font-bold text-on-surface-variant/40 uppercase tracking-widest">Thời gian thực thi: ${formatMs(tt)} · Mark_FAP: ${formatMs(perfStats.s3)} · Check: ${formatMs(perfStats.s4)}</p>`;
await delay(400);showResults();
}catch(err){const r=document.querySelector('.process-step.running');if(r){r.classList.add('bg-red-50');r.querySelector('.process-icon').className='process-icon w-8 h-8 rounded-full bg-error flex items-center justify-center text-white';r.querySelector('.process-icon').innerHTML='<span class="material-symbols-outlined text-sm">error</span>';}document.getElementById('processError').innerHTML=`<div class="mt-4 p-4 bg-error-container text-error rounded-2xl text-sm font-bold flex items-center gap-2"><span class="material-symbols-outlined">error</span>${err.message}</div><div class="mt-3 flex justify-center"><button onclick="goToStep(1)" class="px-6 py-2 bg-white border border-surface-variant rounded-xl text-sm font-bold hover:bg-surface transition-all">← Quay lại Upload</button></div>`;console.error(err);}
}

// ---- Mark_DT ----
function createMarkDT(){
const wb=FILES.cancheck,students=[],marks=[],gpaMap={},studentSet=new Set(),nameMap={},creditsMap={};
wb.SheetNames.forEach(sn=>{
  const ws=wb.Sheets[sn];
  if(!ws['!ref'])return;
  
  // Read raw data including header rows
  const rawData=XLSX.utils.sheet_to_json(ws,{defval:'',header:1});
  if(rawData.length<2)return;
  
  // Row 0 = headers (subject codes)
  const headerRow=rawData[0];
  
  // Build header index map
  const hIdx={};
  headerRow.forEach((h,i)=>{if(h)hIdx[cleanStr(String(h))]=i;});
  
  // Find key columns
  const rcIdx=Object.keys(hIdx).find(k=>['rollnumber','roll number','mssv','masv','roll'].includes(k.toLowerCase()));
  const ncIdx=Object.keys(hIdx).find(k=>['fullname','full name','hoten','họ tên','name'].includes(k.toLowerCase()));
  const gcIdx=Object.keys(hIdx).find(k=>['điểm tb','diem tb','diemtb','gpa','tb','average'].includes(k.toLowerCase()));
  
  if(!rcIdx)return;
  const rcI=hIdx[rcIdx],ncI=ncIdx?hIdx[ncIdx]:null,gcI=gcIdx?hIdx[gcIdx]:null;
  
  // Detect credits row: check if row 1 has RollNumber or not
  // If row 1 doesn't have valid RollNumber pattern → it's likely credits row
  let creditsRow=null;
  let dataStartRow=1;
  
  if(rawData.length>1){
    const row1=rawData[1];
    const row1Roll=row1&&row1[rcI]?cleanStr(String(row1[rcI])).toUpperCase():'';
    // Check if row1Roll looks like a student ID (e.g., SE123456, DE170495)
    const isValidRoll=/^[A-Z]{2}\d{5,6}$/.test(row1Roll);
    
    if(!isValidRoll&&row1){
      // Row 1 is likely credits row
      creditsRow=row1;
      dataStartRow=2;
    }
  }
  
  // Identify subject columns and their credits
  const meta=new Set([rcIdx,ncIdx,gcIdx].filter(Boolean).map(c=>c.toLowerCase()));
  const skip=['stt','no','note','ghi chu','status','trang thai','curriculum','class','lop','semester','hoc ky','term','khoa','nganh','department'];
  const subColsInfo=[];
  
  headerRow.forEach((h,i)=>{
    if(!h)return;
    const hStr=cleanStr(String(h));
    const cl=hStr.toLowerCase().trim();
    if(meta.has(cl)||skip.some(p=>cl===p||cl.startsWith(p))||cl==='undefined')return;
    
    // Get credits from credits row
    let credits=null;
    if(creditsRow&&creditsRow[i]!=null){
      const cv=cleanNum(creditsRow[i]);
      if(cv!==null&&cv>0&&cv<=20)credits=cv; // Valid credit range 1-20
    }
    
    const subCode=cleanCode(hStr);
    if(subCode){
      subColsInfo.push({col:hStr,idx:i,subCode,credits});
      if(credits)creditsMap[subCode]=credits;
    }
  });
  
  // Process student data
  for(let r=dataStartRow;r<rawData.length;r++){
    const row=rawData[r];
    if(!row||!row[rcI])continue;
    
    const roll=cleanStr(String(row[rcI])).toUpperCase();
    if(!roll||!/^[A-Z]{2}\d{5,6}$/.test(roll))continue; // Skip invalid roll numbers
    
    const name=ncI!==null&&row[ncI]?cleanStr(String(row[ncI])):'';
    studentSet.add(roll);
    if(name)nameMap[roll]=name;
    
    // GPA
    if(gcI!==null&&row[gcI]!=null&&row[gcI]!==''){
      const g=cleanNum(row[gcI]);
      if(g!==null)gpaMap[roll]=roundTo(g,2);
    }
    
    // Subject marks with credits
    subColsInfo.forEach(info=>{
      let val=row[info.idx];
      if(val==null||val==='')return;
      
      let mv=val;
      const sv=cleanStr(String(val));
      if(['pass','passed','fail','is exempt','is suspended','is attendancefail','*'].includes(sv.toLowerCase()))mv=sv;
      else{const n=cleanNum(val);mv=n!==null?n:sv;}
      
      marks.push({
        RollNumber:roll,
        FullName:name,
        SubjectCode:info.subCode,
        AverageMark:mv,
        Credits:info.credits
      });
    });
  }
});

studentSet.forEach(r=>students.push({RollNumber:r,FullName:nameMap[r]||''}));
return{marks,students,gpaMap,studentSet,studentNameMap:nameMap,creditsMap};}

// ---- Mark_FAP — FAP Worker ----
async function createMarkFAPChunked(studentSet){
return new Promise((resolve,reject)=>{
  if(!FILE_BUFFERS.mark){reject(new Error('Không tìm thấy buffer file Mark — vui lòng tải lại file'));return;}
  const url=makeWorkerURL(FAP_WORKER_CODE);
  const worker=new Worker(url);
  worker.onmessage=function(e){
    if(e.data.type==='progress'){
      document.getElementById('ps3bar').style.width=e.data.pct+'%';
      document.getElementById('ps3pct').textContent=e.data.text;
      document.getElementById('ps3detail').textContent=e.data.detail;
    } else if(e.data.type==='done'){
      worker.terminate();URL.revokeObjectURL(url);
      resolve(e.data.result);
    } else if(e.data.type==='error'){
      worker.terminate();URL.revokeObjectURL(url);
      reject(new Error(e.data.message));
    }
  };
  worker.onerror=function(e){worker.terminate();URL.revokeObjectURL(url);reject(new Error(e.message));};
  // Clone buffer so original stays for re-runs
  const bufferCopy=FILE_BUFFERS.mark.slice(0);
  worker.postMessage({buffer:bufferCopy,studentSet:[...studentSet]},[bufferCopy]);
});}

// ---- Lookups ----
function getCurrMap(){const rows=readAllSheets(FILES.currstudent);if(!rows.length)throw new Error('CurriculumStudent trống');const h=Object.keys(rows[0]);const cc=findCol(h,['CurriculumCode','Curriculum Code','MaKhung','curriculumcode']);const rc=findCol(h,['RollNumber','Roll Number','MSSV','Rollnumber','rollnumber']);if(!cc||!rc)throw new Error('CurriculumStudent thiếu cột');const m={};rows.forEach(r=>{const roll=cleanStr(r[rc]).toUpperCase(),curr=cleanCode(r[cc]);if(roll&&curr)m[roll]=curr;});return m;}
function getCurrSubs(){const rows=readAllSheets(FILES.currsubject);if(!rows.length)throw new Error('CurriculumSubject trống');const h=Object.keys(rows[0]);const cc=findCol(h,['CurriculumCode','Curriculum Code','MaKhung','curriculumcode']);const sc=findCol(h,['SubjectCode','Subject Code','MaMon','subjectcode']);const cr=findCol(h,['Credits','SoTC','credits','Credit']);if(!cc||!sc)throw new Error('CurriculumSubject thiếu cột');const m={};rows.forEach(r=>{const curr=cleanCode(r[cc]),sub=cleanCode(r[sc]);if(curr&&sub){if(!m[curr])m[curr]=[];m[curr].push({SubjectCode:sub,Credits:cr?cleanNum(r[cr]):null});}});return m;}
function getRepMap(){const rows=readAllSheets(FILES.replacecode);if(!rows.length)return{};const h=Object.keys(rows[0]);const sc=findCol(h,['SubjectCode','Subject Code','subjectcode']);const rc=findCol(h,['replacecode','ReplaceCode','Replace Code']);const eq=findCol(h,['equivalent','Equivalent']);const nt=findCol(h,['note','Note','GhiChu']);if(!sc||!rc)throw new Error('ReplaceCode thiếu cột');const m={};rows.forEach(r=>{const sub=cleanCode(r[sc]),rep=cleanCode(r[rc]);if(sub&&rep){if(!m[sub])m[sub]=[];m[sub].push({SubjectCode:sub,replacecode:rep,equivalent:eq?cleanStr(r[eq]):'',note:nt?cleanStr(r[nt]):''});}});return m;}

// ---- Check Mark ----
function doCheckMark(markDT,markFAP){
const cm=getCurrMap(),cs=getCurrSubs();
const fL={};markFAP.forEach(r=>{fL[r.RollNumber+'|'+r.SubjectCode]=r;});
const dL={};markDT.marks.forEach(r=>{dL[r.RollNumber+'|'+r.SubjectCode]=r;});
// Build OJ* FAP lookup per student: roll → best OJ* FAP record
const ojtFapMap={};markFAP.forEach(r=>{if(r.SubjectCode.toUpperCase().startsWith('OJ')){if(!ojtFapMap[r.RollNumber]||isPassStatusVOV(r.Status))ojtFapMap[r.RollNumber]=r;}});
const res=[];let stt=0;
markDT.students.forEach(stu=>{const roll=stu.RollNumber,name=stu.FullName,cc=cm[roll]||'',subs=cs[cc]||[];
subs.forEach(sub=>{if(isSkipSubject(sub.SubjectCode)||isVOV(sub.SubjectCode))return;stt++;
const sc=sub.SubjectCode,dtR=dL[roll+'|'+sc],fapR=fL[roll+'|'+sc];
let mDt=dtR?dtR.AverageMark:'',mFap='',status='';
if(fapR){mFap=fapR.AverageMarkNum!=null?roundTo(fapR.AverageMarkNum,1):fapR.AverageMark;status=fapR.Status;}
let check='';
if(sc.toUpperCase().startsWith('OJ')){
  // OJT: mDt từ cột OJT trong ĐT, fap từ bất kỳ OJ* nào
  const ojtDt=dL[roll+'|OJT'];const mDtOjt=ojtDt?ojtDt.AverageMark:mDt;
  const ojtFap=ojtFapMap[roll];const stOjt=ojtFap?ojtFap.Status:'';
  const mFapOjt=ojtFap?(ojtFap.AverageMarkNum!=null?roundTo(ojtFap.AverageMarkNum,1):ojtFap.AverageMark):'';
  check=(isPassStatus(String(mDtOjt))&&isPassStatusVOV(stOjt))?'OK':'Not ok';
  res.push({Stt:stt,RollNumber:roll,FullName:name,CurriculumCode:cc,SubjectCode:sc,Mark_Dt:mDtOjt,Mark_Fap:mFapOjt,Status:stOjt,Check:check});
}
else if(isGDQP_OJ_LAB(sc)){check=(isPassStatus(String(mDt))&&isPassStatus(status))?'OK':'Not ok';res.push({Stt:stt,RollNumber:roll,FullName:name,CurriculumCode:cc,SubjectCode:sc,Mark_Dt:mDt,Mark_Fap:mFap,Status:status,Check:check});}
else{let nD=cleanNum(mDt),nF=cleanNum(mFap);
if(nD!==null&&nF!==null){
  if(roundTo(nD,1)===roundTo(nF,1))check='OK';
  else check=isPassStatus(status)?'Lỗi kỹ thuật':'Lệch điểm';
}else if(mDt===''&&mFap==='')check='Thiếu dữ liệu';
else if(isPassStatus(String(mDt)))check=isPassStatus(status)?'OK':'Not ok';
else check=isPassStatus(status)?'Lỗi kỹ thuật':'Lệch điểm';
res.push({Stt:stt,RollNumber:roll,FullName:name,CurriculumCode:cc,SubjectCode:sc,Mark_Dt:mDt,Mark_Fap:mFap,Status:status,Check:check});}
});
// VOV groups
const vovSubs=subs.filter(s=>isVOV(s.SubjectCode));
if(vovSubs.length){
  const gdtcR=dL[roll+'|GDTC'],gdtcMark=gdtcR?gdtcR.AverageMark:'',dtPassed=isPassStatus(String(gdtcMark));
  const groups={};vovSubs.forEach(s=>{const grp=s.SubjectCode.toUpperCase().substring(0,5);if(!groups[grp])groups[grp]=[];groups[grp].push(s.SubjectCode);});
  Object.entries(groups).forEach(([grp,codes])=>{
    stt++;let bestFap=null;
    for(const code of codes){const fR=fL[roll+'|'+code];if(fR&&isPassStatusVOV(fR.Status)){bestFap=fR;break;}}
    if(!bestFap){for(const code of codes){const fR=fL[roll+'|'+code];if(fR){bestFap=fR;break;}}}
    const fapPassed=bestFap&&isPassStatusVOV(bestFap.Status);
    const mFap=bestFap?(bestFap.AverageMarkNum!=null?roundTo(bestFap.AverageMarkNum,1):bestFap.AverageMark):'';
    const status=bestFap?bestFap.Status:'';
    let check='';
    if(!dtPassed&&!fapPassed)check='Not ok';
    else if(!dtPassed)check='Not ok — ĐT chưa pass GDTC';
    else if(!fapPassed)check=`Not ok — Thiếu ${grp}*`;
    else check='OK';
    res.push({Stt:stt,RollNumber:roll,FullName:name,CurriculumCode:cc,SubjectCode:grp+'*',Mark_Dt:gdtcMark,Mark_Fap:mFap,Status:status,Check:check});
  });}
});return res;}

// ---- Check Replace ----
// Helper: detect combo type and parse replacecode
// Returns: {type: 'single'|'and'|'or', codes: [...]}
function parseReplaceCode(code){
  if(!code)return{type:'single',codes:[]};
  const codeStr=String(code);
  
  // Check OR first (/, or, hoặc) - chỉ cần 1 môn
  if(codeStr.includes('/')||/\bor\b/i.test(codeStr)||/\bhoặc\b/i.test(codeStr)){
    const parts=codeStr.split(/[\/]|\bor\b|\bhoặc\b/i).map(c=>cleanCode(c.trim())).filter(Boolean);
    return{type:'or',codes:parts};
  }
  
  // Check AND (& + ,) - phải tất cả các môn
  if(codeStr.includes('&')||codeStr.includes('+')||codeStr.includes(',')){
    const parts=codeStr.split(/[&+,]/).map(c=>cleanCode(c.trim())).filter(Boolean);
    return{type:'and',codes:parts};
  }
  
  return{type:'single',codes:[cleanCode(codeStr)]};
}

function doCheckReplace(ckm,markDT,markFAP){
const rm=getRepMap();const fL={};markFAP.forEach(r=>{fL[r.RollNumber+'|'+r.SubjectCode]=r;});const dL={};markDT.marks.forEach(r=>{dL[r.RollNumber+'|'+r.SubjectCode]=r;});
const errs=ckm.filter(r=>r.Check==='Lệch điểm'||r.Check==='Not ok'||r.Check==='Thiếu dữ liệu'||r.Check==='Lỗi kỹ thuật');const res=[];let stt=0;

errs.forEach(item=>{const sc=item.SubjectCode,roll=item.RollNumber;let allRC=[];
// Collect all possible replacements
(rm[sc]||[]).forEach(r=>{
  const parsed=parseReplaceCode(r.replacecode);
  allRC.push({code:r.replacecode,note:r.note,parsed});
});
// Also check reverse (equivalent=TRUE)
Object.entries(rm).forEach(([orig,rs])=>{rs.forEach(r=>{if(r.replacecode===sc&&r.equivalent&&r.equivalent.toUpperCase()==='TRUE')allRC.push({code:orig,note:r.note,parsed:{type:'single',codes:[cleanCode(orig)]}});});});

if(!allRC.length){stt++;res.push({Stt:stt,RollNumber:roll,FullName:item.FullName,CurriculumCode:item.CurriculumCode,SubjectCode:sc,Replacecode:'',Note:'',Mark_Dt:item.Mark_Dt,Mark_Fap:'',Status_Fap:'',Check:item.Check});return;}

// Evaluate each replacement option
let bestOption=null,bestPriority=999;

allRC.forEach(rep=>{
  const{type,codes}=rep.parsed;
  
  if(type==='and'&&codes.length>1){
    // AND combo: must pass ALL
    let allOk=true,comboResults=[];
    codes.forEach((partCode,idx)=>{
      const fR=fL[roll+'|'+partCode],dtR=dL[roll+'|'+partCode];
      let mDt=dtR?dtR.AverageMark:'',mFap='',st='';
      if(fR){mFap=fR.AverageMarkNum!=null?roundTo(fR.AverageMarkNum,1):fR.AverageMark;st=fR.Status;}
      
      let ck='';
      if(isPassStatus(st)){ck='OK';}
      else if(mFap===''&&!st){ck='FAP không có điểm';allOk=false;}
      else{ck='Not ok';allOk=false;}
      
      comboResults.push({code:partCode,mDt,mFap,st,ck,idx:idx+1,total:codes.length});
    });
    
    const okCount=comboResults.filter(r=>r.ck==='OK').length;
    let priority=4;
    if(okCount===codes.length)priority=1;
    else if(okCount>0)priority=3;
    
    if(priority<bestPriority){
      bestPriority=priority;
      bestOption={type:'and',results:comboResults,note:rep.note,allOk};
    }
  }
  else if(type==='or'&&codes.length>1){
    // OR combo: only need ONE to pass
    let bestOrResult=null,bestOrPriority=999;
    
    codes.forEach((partCode,idx)=>{
      const fR=fL[roll+'|'+partCode],dtR=dL[roll+'|'+partCode];
      let mDt=dtR?dtR.AverageMark:'',mFap='',st='';
      if(fR){mFap=fR.AverageMarkNum!=null?roundTo(fR.AverageMarkNum,1):fR.AverageMark;st=fR.Status;}
      
      let ck='';
      if(isPassStatus(st)){ck='OK';}
      else if(mFap===''&&!st){ck='FAP không có điểm';}
      else{ck='Not ok';}
      
      let p=4;
      if(ck==='OK')p=1;
      else if(mFap!==''||st!=='')p=3;
      
      if(p<bestOrPriority){
        bestOrPriority=p;
        bestOrResult={code:partCode,mDt,mFap,st,ck,note:rep.note,originalCode:rep.code};
      }
    });
    
    if(bestOrPriority<bestPriority){
      bestPriority=bestOrPriority;
      bestOption={type:'or',result:bestOrResult,note:rep.note};
    }
  }
  else{
    // SINGLE replacement
    const singleCode=codes[0]||cleanCode(rep.code);
    const fR=fL[roll+'|'+singleCode],dtR=dL[roll+'|'+singleCode];
    let mDt=dtR?dtR.AverageMark:'',mFap='',st='';
    if(fR){mFap=fR.AverageMarkNum!=null?roundTo(fR.AverageMarkNum,1):fR.AverageMark;st=fR.Status;}
    const effDt=mDt!==''?String(mDt):String(item.Mark_Dt);
    
    let ck='';
    if(isGDQP_OJ_LAB(sc)){
      const nD=cleanNum(effDt),nF=cleanNum(mFap);
      if(nD!==null&&nF!==null)ck=roundTo(nD,1)===roundTo(nF,1)?'OK':'Lệch điểm';
      else ck=(isPassStatus(effDt)&&isPassStatus(st))?'OK':'Not ok';
    }
    else if(isVOV(sc))ck=isPassStatusVOV(st)?'OK':'Not ok';
    else{
      if(isPassStatus(effDt)&&isPassStatus(st)){ck='OK';}
      else{
        let nD=cleanNum(mDt),nF=cleanNum(mFap);
        if(nD!==null&&nF!==null)ck=roundTo(nD,1)===roundTo(nF,1)?'OK':'Lệch điểm';
        else if(mDt===''&&mFap===''&&!st)ck='Không có dữ liệu thay thế';
        else if(mDt==='')ck='ĐT không dùng môn thay thế này';
        else if(mFap===''&&!st)ck='FAP không có điểm';
        else ck='Lệch điểm';
      }
    }
    
    let priority=4;
    if(ck==='OK')priority=1;
    else if(mDt!==''||effDt!=='')priority=2;
    else if(mFap!==''||st!=='')priority=3;
    
    if(priority<bestPriority){
      bestPriority=priority;
      bestOption={type:'single',code:singleCode,note:rep.note,mDt,mFap,st,ck};
    }
  }
});

// Add results
if(bestOption.type==='and'){
  // AND combo: add multiple rows
  bestOption.results.forEach(r=>{
    stt++;
    const noteWithIdx=bestOption.note?`${bestOption.note} (${r.idx}/${r.total})`:`(${r.idx}/${r.total})`;
    res.push({Stt:stt,RollNumber:roll,FullName:item.FullName,CurriculumCode:item.CurriculumCode,SubjectCode:sc,Replacecode:r.code,Note:noteWithIdx,Mark_Dt:r.mDt,Mark_Fap:r.mFap,Status_Fap:r.st,Check:r.ck});
  });
}else if(bestOption.type==='or'){
  // OR combo: add single best row
  stt++;
  const r=bestOption.result;
  res.push({Stt:stt,RollNumber:roll,FullName:item.FullName,CurriculumCode:item.CurriculumCode,SubjectCode:sc,Replacecode:r.code,Note:r.note||'',Mark_Dt:r.mDt,Mark_Fap:r.mFap,Status_Fap:r.st,Check:r.ck});
}else{
  // Single
  stt++;
  res.push({Stt:stt,RollNumber:roll,FullName:item.FullName,CurriculumCode:item.CurriculumCode,SubjectCode:sc,Replacecode:bestOption.code,Note:bestOption.note,Mark_Dt:bestOption.mDt,Mark_Fap:bestOption.mFap,Status_Fap:bestOption.st,Check:bestOption.ck});
}
});return res;}

// ---- Check GPA ----
function doCheckGPA(markDT,markFAP){
const cm=getCurrMap(),cs=getCurrSubs(),rm=getRepMap();
const fL={};markFAP.forEach(r=>{fL[r.RollNumber+'|'+r.SubjectCode]=r;});
// Build Can Check lookup
const dtL={};markDT.marks.forEach(r=>{dtL[r.RollNumber+'|'+r.SubjectCode]=r;});
const res=[];let stt=0;
const FAIL_STATUS=['fail','is attendancefail','is attendance fail','is suspended'];

markDT.students.forEach(stu=>{const roll=stu.RollNumber,name=stu.FullName,cc=cm[roll]||'',subs=cs[cc]||[],gpaDt=markDT.gpaMap[roll];
let tw=0,tc=0; // FAP weighted sum and credits
const usedReplacements=new Set(); // Track môn thay thế đã dùng
const duplicateWarnings=[]; // Cảnh báo trùng

// GPA_DT_Calc và TC_DT: Tính trực tiếp từ Can Check (Mark_DT)
let twDt=0,tcDt=0;
markDT.marks.forEach(m=>{
  if(m.RollNumber!==roll)return;
  if(isExcludeFromGPA(m.SubjectCode))return;
  const cr=m.Credits||0;
  if(cr<=0)return;
  const mark=typeof m.AverageMark==='number'?m.AverageMark:null;
  if(mark===null)return;
  twDt+=roundTo(mark,1)*cr;
  tcDt+=cr;
});
const gpaDtCalc=tcDt>0?roundTo(twDt/tcDt,2):null;

// Hàm kiểm tra môn có trong Can Check không
const isInCanCheck=(code)=>!!dtL[roll+'|'+code];

// Hàm tìm môn thay thế ưu tiên có trong Can Check và chưa được dùng
const findBestReplacement=(replacements,usedSet)=>{
  if(!replacements||!replacements.length)return null;
  
  // Ưu tiên 1: Môn có trong Can Check VÀ chưa được dùng
  for(const r of replacements){
    const parsed=parseReplaceCode(r.replacecode);
    if(parsed.type==='single'){
      const code=parsed.codes[0];
      if(isInCanCheck(code)&&!usedSet.has(code)){
        const fR=fL[roll+'|'+code];
        if(fR&&fR.AverageMarkNum!==null&&!FAIL_STATUS.includes((fR.Status||'').toLowerCase().trim())){
          return {type:'single',code,record:fR,rule:r};
        }
      }
    }else if(parsed.type==='and'){
      // AND: tất cả phải có trong Can Check, pass, và chưa dùng
      const allInCanCheck=parsed.codes.every(c=>isInCanCheck(c)&&!usedSet.has(c));
      if(allInCanCheck){
        let allValid=true;
        for(const c of parsed.codes){
          const fR=fL[roll+'|'+c];
          if(!fR||fR.AverageMarkNum===null||FAIL_STATUS.includes((fR.Status||'').toLowerCase().trim())){
            allValid=false;break;
          }
        }
        if(allValid)return {type:'and',codes:parsed.codes,rule:r};
      }
    }else if(parsed.type==='or'){
      // OR: ưu tiên môn có trong Can Check và chưa dùng
      for(const c of parsed.codes){
        if(isInCanCheck(c)&&!usedSet.has(c)){
          const fR=fL[roll+'|'+c];
          if(fR&&fR.AverageMarkNum!==null&&!FAIL_STATUS.includes((fR.Status||'').toLowerCase().trim())){
            return {type:'single',code:c,record:fR,rule:r};
          }
        }
      }
    }
  }
  
  // Ưu tiên 2: Môn có trong Can Check nhưng đã dùng (sẽ cảnh báo trùng)
  for(const r of replacements){
    const parsed=parseReplaceCode(r.replacecode);
    if(parsed.type==='single'){
      const code=parsed.codes[0];
      if(isInCanCheck(code)){
        const fR=fL[roll+'|'+code];
        if(fR&&fR.AverageMarkNum!==null&&!FAIL_STATUS.includes((fR.Status||'').toLowerCase().trim())){
          return {type:'single',code,record:fR,rule:r,isDuplicate:usedSet.has(code)};
        }
      }
    }
  }
  
  // Ưu tiên 3: Fallback - môn có trong FAP và chưa dùng
  for(const r of replacements){
    const parsed=parseReplaceCode(r.replacecode);
    if(parsed.type==='and'&&parsed.codes.length>1){
      const noneUsed=parsed.codes.every(c=>!usedSet.has(c));
      if(noneUsed){
        let allValid=true;
        for(const c of parsed.codes){
          const fR=fL[roll+'|'+c];
          if(!fR||fR.AverageMarkNum===null||FAIL_STATUS.includes((fR.Status||'').toLowerCase().trim())){
            allValid=false;break;
          }
        }
        if(allValid)return {type:'and',codes:parsed.codes,rule:r};
      }
    }else if(parsed.type==='or'){
      for(const c of parsed.codes){
        if(!usedSet.has(c)){
          const fR=fL[roll+'|'+c];
          if(fR&&fR.AverageMarkNum!==null&&!FAIL_STATUS.includes((fR.Status||'').toLowerCase().trim())){
            return {type:'single',code:c,record:fR,rule:r};
          }
        }
      }
    }else{
      const code=parsed.codes[0];
      if(!usedSet.has(code)){
        const fR=fL[roll+'|'+code];
        if(fR&&fR.AverageMarkNum!==null&&!FAIL_STATUS.includes((fR.Status||'').toLowerCase().trim())){
          return {type:'single',code,record:fR,rule:r};
        }
      }
    }
  }
  
  // Ưu tiên 4: Fallback cuối - môn trong FAP đã dùng (cảnh báo trùng)
  for(const r of replacements){
    const parsed=parseReplaceCode(r.replacecode);
    if(parsed.type==='single'||parsed.codes.length===1){
      const code=parsed.codes[0];
      const fR=fL[roll+'|'+code];
      if(fR&&fR.AverageMarkNum!==null&&!FAIL_STATUS.includes((fR.Status||'').toLowerCase().trim())){
        return {type:'single',code,record:fR,rule:r,isDuplicate:usedSet.has(code)};
      }
    }
  }
  
  return null;
};

subs.forEach(sub=>{const sc=sub.SubjectCode;if(isExcludeFromGPA(sc))return;
let fR=fL[roll+'|'+sc];
const isFailing=fR&&fR.Status&&FAIL_STATUS.includes(fR.Status.toLowerCase().trim());

if(!fR||fR.AverageMarkNum===null||isFailing){
  // Try to find replacement
  const best=findBestReplacement(rm[sc]||[],usedReplacements);
  
  if(best){
    if(best.isDuplicate){
      duplicateWarnings.push(`${best.code}(${sc})`);
      // Không tính điểm cho môn trùng
    }else if(best.type==='and'){
      // AND combo
      let comboTw=0,comboTc=0;
      for(const c of best.codes){
        const partR=fL[roll+'|'+c];
        if(partR.Status&&partR.Status.toLowerCase().trim()==='is exempt')continue;
        const partCr=partR.Credits||0;
        if(partCr>0){
          usedReplacements.add(c);
          comboTw+=roundTo(partR.AverageMarkNum,1)*partCr;
          comboTc+=partCr;
        }
      }
      tw+=comboTw;tc+=comboTc;
    }else{
      // Single
      const code=best.code;
      const rr=best.record;
      if(!(rr.Status&&rr.Status.toLowerCase().trim()==='is exempt')){
        const cr=rr.Credits||0;
        if(cr>0){
          usedReplacements.add(code);
          tw+=roundTo(rr.AverageMarkNum,1)*cr;
          tc+=cr;
        }
      }
    }
    return;
  }
  
  // Also check reverse equivalent
  let foundReverse=false;
  Object.entries(rm).forEach(([orig,rs])=>{
    if(foundReverse)return;
    rs.forEach(r=>{
      if(foundReverse)return;
      if(r.replacecode===sc&&r.equivalent&&r.equivalent.toUpperCase()==='TRUE'){
        const ar=fL[roll+'|'+orig];
        if(ar&&ar.AverageMarkNum!==null&&!FAIL_STATUS.includes((ar.Status||'').toLowerCase().trim())){
          if(ar.Status&&ar.Status.toLowerCase().trim()==='is exempt'){foundReverse=true;return;}
          const cr=ar.Credits||0;
          if(cr>0){
            if(usedReplacements.has(orig)){
              duplicateWarnings.push(`${orig}(${sc})`);
            }else{
              usedReplacements.add(orig);
              tw+=roundTo(ar.AverageMarkNum,1)*cr;
              tc+=cr;
            }
          }
          foundReverse=true;
        }
      }
    });
  });
  
  return;
}

// Original subject has valid mark
if(fR.Status&&fR.Status.toLowerCase().trim()==='is exempt')return;
const cr=fR.Credits||0;if(cr<=0)return;
tw+=roundTo(fR.AverageMarkNum,1)*cr;tc+=cr;
});

const gpaFap=tc>0?roundTo(tw/tc,2):null;stt++;

// Check: OK chỉ khi cả 3 GPA bằng nhau
let check='';
if(gpaDt!=null&&gpaDtCalc!==null&&gpaFap!==null){
  if(gpaDt===gpaDtCalc&&gpaDtCalc===gpaFap)check='OK';
  else{
    const parts=[];
    if(gpaDt!==gpaDtCalc)parts.push(`ĐT≠Calc`);
    if(gpaDtCalc!==gpaFap)parts.push(`Calc≠FAP`);
    if(gpaDt!==gpaFap)parts.push(`ĐT≠FAP`);
    check=`Lệch (${parts.join(', ')})`;
  }
}else check='Thiếu dữ liệu';

// Thêm cảnh báo trùng môn thay thế
const dupWarn=duplicateWarnings.length>0?` ⚠ Trùng: ${duplicateWarnings.join(', ')}`:'';

res.push({Stt:stt,RollNumber:roll,FullName:name,GPA_Dt:gpaDt??'',GPA_Dt_Calc:gpaDtCalc??'',GPA_Fap:gpaFap??'',TC_Dt:tcDt,TC_Fap:tc,Check:check+dupWarn});
});return res;}

// ---- Summary ----
function genSummary(ckm,ckr,ckg,markDT,markFAP){
const total=markDT.students.length,notOk=ckm.filter(r=>r.Check!=='OK');
const resolved=new Set();ckr.forEach(r=>{if(r.Check==='OK')resolved.add(r.RollNumber+'|'+r.SubjectCode);});
const stillNotOkAfterReplace=ckr.filter(r=>r.Check!=='OK').length;
const collect=items=>{const m={};items.forEach(r=>{if(!m[r.RollNumber])m[r.RollNumber]=[];m[r.RollNumber].push(r.SubjectCode);});return m;};

// VOV: SV đạt khi FAP có ít nhất 1 môn từ mỗi nhóm VOV11*, VOV12*, VOV13* với status Passed/Is Exempt
const VOV_GROUPS=['VOV11','VOV12','VOV13'];
const fapByRoll={};markFAP.forEach(r=>{if(!fapByRoll[r.RollNumber])fapByRoll[r.RollNumber]=[];fapByRoll[r.RollNumber].push(r);});
const vovBadDetails={};
markDT.students.forEach(stu=>{
  const roll=stu.RollNumber,fapMarks=fapByRoll[roll]||[];
  const missingGroups=VOV_GROUPS.filter(g=>!fapMarks.some(r=>r.SubjectCode.toUpperCase().startsWith(g)&&isPassStatusVOV(r.Status)));
  if(missingGroups.length>0)vovBadDetails[roll]=missingGroups.map(g=>g+'*');
});
const vovBad=new Set(Object.keys(vovBadDetails));

// OJT: SV đạt khi FAP có ít nhất 1 môn OJ* Passed/Is Exempt
const fapByRollOjt={};markFAP.forEach(r=>{if(r.SubjectCode.toUpperCase().startsWith('OJ')&&isPassStatusVOV(r.Status)){if(!fapByRollOjt[r.RollNumber])fapByRollOjt[r.RollNumber]=r;}});
const ojtBadDetails={};
markDT.students.forEach(stu=>{if(!fapByRollOjt[stu.RollNumber])ojtBadDetails[stu.RollNumber]='Chưa có OJ* Passed trong FAP';});
const ojtBad=new Set(Object.keys(ojtBadDetails));
const gdqpBad=new Set(ckm.filter(r=>r.SubjectCode.toUpperCase().startsWith('GDQP')&&r.Check!=='OK').map(r=>r.RollNumber));
const subErrs={};ckm.filter(r=>r.Check!=='OK').forEach(r=>{subErrs[r.SubjectCode]=(subErrs[r.SubjectCode]||0)+1;});
const topErrs=Object.entries(subErrs).sort((a,b)=>b[1]-a[1]).slice(0,5).map(([code,count])=>({code,count}));
return{totalStudents:total,totalSubjectsChecked:ckm.length,notOkCount:notOk.length,stillNotOkAfterReplace,
vovPassCount:total-vovBad.size,vovNotPassCount:vovBad.size,vovDetails:vovBadDetails,
ojtPassCount:total-ojtBad.size,ojtNotPassCount:ojtBad.size,ojtDetails:ojtBadDetails,
gdqpPassCount:total-gdqpBad.size,gdqpNotPassCount:gdqpBad.size,gdqpDetails:collect(ckm.filter(r=>r.SubjectCode.toUpperCase().startsWith('GDQP')&&r.Check!=='OK')),
gpaMismatch:ckg.filter(r=>!r.Check.startsWith('OK')&&r.Check!=='Thiếu dữ liệu').length,topErrs};}

// ==================== Results ====================
function showResults(){
goToStep(3);
document.getElementById('lastUpdated').textContent=`Cập nhật lần cuối: ${new Date().toLocaleTimeString('vi-VN')} · ${new Date().toLocaleDateString('vi-VN')}`;
const s=RESULT.summary;
document.getElementById('summaryCards').innerHTML=`
<div class="bg-white p-5 rounded-3xl border border-surface-variant card-shadow"><span class="text-[9px] font-bold text-on-surface-variant uppercase tracking-widest block mb-2">Tổng SV</span><span class="text-3xl font-black text-primary">${s.totalStudents.toLocaleString()}</span></div>
<div class="bg-white p-5 rounded-3xl border-l-4 border-l-error border border-surface-variant card-shadow"><span class="text-[9px] font-bold text-error uppercase tracking-widest block mb-2">Lệch Điểm</span><span class="text-3xl font-black text-error">${s.notOkCount}</span></div>
<div class="bg-white p-5 rounded-3xl border-l-4 border-l-green-500 border border-surface-variant card-shadow"><span class="text-[9px] font-bold text-green-600 uppercase tracking-widest block mb-2">Còn lệch sau Replace</span><span class="text-3xl font-black ${s.stillNotOkAfterReplace?'text-error':'text-green-600'}">${s.stillNotOkAfterReplace}</span></div>
<div class="bg-white p-5 rounded-3xl border-l-4 border-l-amber-500 border border-surface-variant card-shadow"><span class="text-[9px] font-bold text-amber-600 uppercase tracking-widest block mb-2">Lệch GPA</span><span class="text-3xl font-black text-amber-600">${s.gpaMismatch}</span></div>
<div class="bg-white p-5 rounded-3xl border border-surface-variant card-shadow"><span class="text-[9px] font-bold text-on-surface-variant uppercase tracking-widest block mb-2">VOV Pass</span><span class="text-3xl font-black ${s.vovPassCount===s.totalStudents?'text-green-600':'text-error'}">${s.vovPassCount}/${s.totalStudents}</span></div>
<div class="bg-white p-5 rounded-3xl border border-surface-variant card-shadow"><span class="text-[9px] font-bold text-on-surface-variant uppercase tracking-widest block mb-2">OJT Pass</span><span class="text-3xl font-black ${s.ojtPassCount===s.totalStudents?'text-green-600':'text-error'}">${s.ojtPassCount}/${s.totalStudents}</span></div>
<div class="bg-white p-5 rounded-3xl border border-surface-variant card-shadow"><span class="text-[9px] font-bold text-on-surface-variant uppercase tracking-widest block mb-2">GDQP Pass</span><span class="text-3xl font-black ${s.gdqpPassCount===s.totalStudents?'text-green-600':'text-error'}">${s.gdqpPassCount}/${s.totalStudents}</span></div>`;
const tabs=[{id:'checkmark',l:'Check Mark',icon:'fact_check',n:RESULT.checkMark.length},{id:'checkreplace',l:'Check Replace',icon:'swap_horiz',n:RESULT.checkReplace.length},{id:'checkgpa',l:'Check GPA',icon:'calculate',n:RESULT.checkGPA.length},{id:'tracuu',l:'Tra cứu SV',icon:'person_search',n:null},{id:'summary',l:'Summary',icon:'summarize',n:null}];
document.getElementById('resultTabs').innerHTML=tabs.map((t,i)=>`<button data-tab="${t.id}" class="px-5 py-5 text-xs font-black uppercase tracking-widest flex items-center gap-2 whitespace-nowrap transition-all ${i===0?'text-primary border-b-2 border-primary':'text-on-surface-variant hover:text-primary border-b-2 border-transparent'}" onclick="switchTab('${t.id}',this)"><span class="material-symbols-outlined text-base">${t.icon}</span>${t.l}${t.n!=null?' ('+t.n.toLocaleString()+')':''}</button>`).join('');
renderTab('checkmark');}

function switchTab(id,btn){
document.querySelectorAll('#resultTabs button').forEach(b=>{b.classList.remove('text-primary','border-primary');b.classList.add('text-on-surface-variant','border-transparent');});
btn.classList.remove('text-on-surface-variant','border-transparent');btn.classList.add('text-primary','border-primary');
renderTab(id);}

function renderTab(id){
const el=document.getElementById('resultContent');
const infoBox=(isErr,txt)=>`<div class="mx-8 mt-6 mb-0 p-4 rounded-2xl text-sm font-bold flex items-center gap-2 ${isErr?'bg-amber-50 text-amber-800 border-l-4 border-amber-500':'bg-green-50 text-green-800 border-l-4 border-green-500'}">${txt}</div>`;
if(id==='checkmark'){
  const d=RESULT.checkMark,e=d.filter(r=>r.Check!=='OK');
  el.innerHTML=infoBox(e.length>0,`Tổng: ${d.length.toLocaleString()} | OK: ${(d.length-e.length).toLocaleString()} | Lỗi: ${e.length.toLocaleString()}`)+`<div id="dt_cm"></div>`;
  if(DT.dt_cm){DT.dt_cm.render();}else{DT.dt_cm=new DataTable('dt_cm',['Stt','RollNumber','FullName','CurriculumCode','SubjectCode','Mark_Dt','Mark_Fap','Status','Check'],d);}
}else if(id==='checkreplace'){
  const d=RESULT.checkReplace,e=d.filter(r=>r.Check!=='OK');
  el.innerHTML=infoBox(e.length>0,`Tổng: ${d.length.toLocaleString()} | OK: ${d.filter(r=>r.Check==='OK').length.toLocaleString()} | Lỗi: ${e.length.toLocaleString()}`)+`<div id="dt_cr"></div>`;
  if(DT.dt_cr){DT.dt_cr.render();}else{DT.dt_cr=new DataTable('dt_cr',['Stt','RollNumber','FullName','CurriculumCode','SubjectCode','Replacecode','Note','Mark_Dt','Mark_Fap','Status_Fap','Check'],d);}
}else if(id==='checkgpa'){
  const d=RESULT.checkGPA,e=d.filter(r=>!r.Check.startsWith('OK')&&r.Check!=='Thiếu dữ liệu');
  el.innerHTML=infoBox(e.length>0,`Tổng: ${d.length.toLocaleString()} | OK: ${(d.length-e.length).toLocaleString()} | Lệch: ${e.length.toLocaleString()}`)+`<div id="dt_gpa"></div>`;
  if(DT.dt_gpa){DT.dt_gpa.render();}else{DT.dt_gpa=new DataTable('dt_gpa',['Stt','RollNumber','FullName','GPA_Dt','GPA_Dt_Calc','GPA_Fap','TC_Dt','TC_Fap','Check'],d);}
}else if(id==='tracuu'){
  el.innerHTML=`<div class="p-8 space-y-4 max-w-4xl">
    <div class="space-y-1"><h3 class="text-lg font-black text-on-surface">Tra cứu sinh viên</h3><p class="text-sm text-on-surface-variant">Nhập mã SV hoặc tên để xem toàn bộ điểm ĐT + FAP + kết quả kiểm tra</p></div>
    <div class="relative"><span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-outline">person</span><input id="searchInput" type="text" class="w-full pl-12 pr-12 py-3.5 bg-white border border-surface-variant rounded-2xl focus:ring-4 focus:ring-primary/10 text-sm transition-all" placeholder="Nhập mã SV hoặc tên sinh viên (phân tách bằng dấu phẩy)..." oninput="handleSearch(this.value)"><button id="searchClear" onclick="clearSearch()" style="display:none" class="absolute right-4 top-1/2 -translate-y-1/2 w-6 h-6 bg-surface-variant text-on-surface-variant rounded-full flex items-center justify-center text-xs hover:bg-outline-variant transition-all">✕</button></div>
    <div id="searchFilterRow" style="display:none"><div class="relative"><span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-outline">menu_book</span><input id="subjectFilter" type="text" class="w-full pl-12 pr-12 py-3.5 bg-white border border-surface-variant rounded-2xl focus:ring-4 focus:ring-primary/10 text-sm transition-all" placeholder="Lọc theo mã môn (tuỳ chọn — VD: IOT102, LAB, OJ)..." oninput="handleSubjectFilter(this.value)"><button id="subjectFilterClear" onclick="clearSubjectFilter()" style="display:none" class="absolute right-4 top-1/2 -translate-y-1/2 w-6 h-6 bg-surface-variant text-on-surface-variant rounded-full flex items-center justify-center text-xs hover:bg-outline-variant transition-all">✕</button></div></div>
    <p class="text-xs text-on-surface-variant">💡 Nhập mã SV để xem chi tiết · Ô lọc môn xuất hiện sau khi tìm được SV</p>
    <div id="searchResults"></div>
  </div>`;
}else if(id==='summary'){
  const s=RESULT.summary,elapsed=processStartTime?Math.round((new Date()-processStartTime)/1000):'—';
  let h=`<div class="p-8 space-y-8 max-w-3xl">
    <div class="text-xs text-on-surface-variant/60 font-bold uppercase tracking-widest">${elapsed}s · ${new Date().toLocaleString('vi-VN')}</div>
    <div class="bg-white rounded-2xl border border-surface-variant overflow-hidden">
      <table class="w-full text-sm"><tbody>
        <tr class="border-b border-surface-variant"><td class="px-6 py-4 text-on-surface-variant font-medium">SV đã kiểm tra</td><td class="px-6 py-4 font-black text-primary text-right">${s.totalStudents.toLocaleString()}</td></tr>
        <tr class="border-b border-surface-variant"><td class="px-6 py-4 text-on-surface-variant font-medium">Tổng môn kiểm tra</td><td class="px-6 py-4 font-black text-right">${s.totalSubjectsChecked.toLocaleString()}</td></tr>
        <tr class="border-b border-surface-variant"><td class="px-6 py-4 text-on-surface-variant font-medium">Môn lệch / Not ok</td><td class="px-6 py-4 font-black text-right ${s.notOkCount?'text-error':'text-green-600'}">${s.notOkCount}</td></tr>
        <tr class="border-b border-surface-variant"><td class="px-6 py-4 text-on-surface-variant font-medium">Còn lệch sau Replace</td><td class="px-6 py-4 font-black text-right ${s.stillNotOkAfterReplace?'text-error':'text-green-600'}">${s.stillNotOkAfterReplace}</td></tr>
        <tr class="border-b border-surface-variant"><td class="px-6 py-4 text-on-surface-variant font-medium">SV đạt VOV</td><td class="px-6 py-4 font-black text-right ${s.vovPassCount===s.totalStudents?'text-green-600':'text-amber-600'}">${s.vovPassCount} / ${s.totalStudents}</td></tr>
        <tr class="border-b border-surface-variant"><td class="px-6 py-4 text-on-surface-variant font-medium">SV đạt OJT</td><td class="px-6 py-4 font-black text-right ${s.ojtPassCount===s.totalStudents?'text-green-600':'text-amber-600'}">${s.ojtPassCount} / ${s.totalStudents}</td></tr>
        <tr class="border-b border-surface-variant"><td class="px-6 py-4 text-on-surface-variant font-medium">SV đạt GDQP</td><td class="px-6 py-4 font-black text-right ${s.gdqpPassCount===s.totalStudents?'text-green-600':'text-amber-600'}">${s.gdqpPassCount} / ${s.totalStudents}</td></tr>
        <tr><td class="px-6 py-4 text-on-surface-variant font-medium">SV lệch GPA</td><td class="px-6 py-4 font-black text-right ${s.gpaMismatch?'text-error':'text-green-600'}">${s.gpaMismatch}</td></tr>
      </tbody></table>
    </div>`;
  if(s.topErrs&&s.topErrs.length){h+=`<div><h4 class="text-xs font-black uppercase tracking-widest text-on-surface-variant mb-3">Top môn lệch nhiều nhất</h4><div class="space-y-2">`;s.topErrs.forEach(e=>{const w=Math.round(e.count/s.topErrs[0].count*100);h+=`<div class="flex items-center gap-3"><span class="text-xs font-black text-primary w-20 shrink-0">${e.code}</span><div class="flex-1 bg-surface-variant rounded-full h-2 overflow-hidden"><div class="bg-error h-full rounded-full" style="width:${w}%"></div></div><span class="text-xs font-bold text-error w-8 text-right">${e.count}</span></div>`;});h+=`</div></div>`;}
  if(s.vovNotPassCount>0){
    h+=`<div><h4 class="text-xs font-black uppercase tracking-widest text-error mb-3">SV chưa đạt GDTC (${s.vovNotPassCount})</h4>
    <div class="bg-white rounded-2xl border border-surface-variant overflow-hidden"><div style="max-height:280px;overflow-y:auto"><table class="w-full text-xs"><thead><tr class="bg-surface-variant/30 border-b border-surface-variant sticky top-0"><th class="px-4 py-3 text-left font-black text-on-surface-variant uppercase tracking-widest">RollNumber</th><th class="px-4 py-3 text-left font-black text-on-surface-variant uppercase tracking-widest">Nhóm còn thiếu</th></tr></thead><tbody>`;
    Object.entries(s.vovDetails).forEach(([roll,groups])=>{h+=`<tr class="border-b border-surface-variant last:border-0"><td class="px-4 py-3 font-bold text-primary">${roll}</td><td class="px-4 py-3 text-error font-bold">${groups.join(', ')}</td></tr>`;});
    h+=`</tbody></table></div></div></div>`;
  }
  if(s.ojtNotPassCount>0){
    h+=`<div><h4 class="text-xs font-black uppercase tracking-widest text-error mb-3">SV chưa đạt OJT (${s.ojtNotPassCount})</h4>
    <div class="bg-white rounded-2xl border border-surface-variant overflow-hidden"><div style="max-height:280px;overflow-y:auto"><table class="w-full text-xs"><thead><tr class="bg-surface-variant/30 border-b border-surface-variant sticky top-0"><th class="px-4 py-3 text-left font-black text-on-surface-variant uppercase tracking-widest">RollNumber</th><th class="px-4 py-3 text-left font-black text-on-surface-variant uppercase tracking-widest">Ghi chú</th></tr></thead><tbody>`;
    Object.entries(s.ojtDetails).forEach(([roll,note])=>{h+=`<tr class="border-b border-surface-variant last:border-0"><td class="px-4 py-3 font-bold text-primary">${roll}</td><td class="px-4 py-3 text-error">${note}</td></tr>`;});
    h+=`</tbody></table></div></div></div>`;
  }
  if(s.gdqpNotPassCount>0){
    h+=`<div><h4 class="text-xs font-black uppercase tracking-widest text-error mb-3">SV chưa đạt GDQP (${s.gdqpNotPassCount})</h4>
    <div class="bg-white rounded-2xl border border-surface-variant overflow-hidden"><div style="max-height:280px;overflow-y:auto"><table class="w-full text-xs"><thead><tr class="bg-surface-variant/30 border-b border-surface-variant sticky top-0"><th class="px-4 py-3 text-left font-black text-on-surface-variant uppercase tracking-widest">RollNumber</th><th class="px-4 py-3 text-left font-black text-on-surface-variant uppercase tracking-widest">Môn</th></tr></thead><tbody>`;
    Object.entries(s.gdqpDetails).forEach(([r,ss])=>{h+=`<tr class="border-b border-surface-variant last:border-0"><td class="px-4 py-3 font-bold text-primary">${r}</td><td class="px-4 py-3 text-error">${ss.join(', ')}</td></tr>`;});
    h+=`</tbody></table></div></div></div>`;
  }
  h+=`</div>`;el.innerHTML=h;}}

// ==================== SEARCH ====================
function handleSearch(q){
clearTimeout(searchDebounce);
const cb=document.getElementById('searchClear'),rd=document.getElementById('searchResults'),fr=document.getElementById('searchFilterRow');
if(!q||!q.trim()){if(cb)cb.style.display='none';if(rd)rd.style.display='none';if(fr)fr.style.display='none';return;}
if(cb)cb.style.display='flex';
searchDebounce=setTimeout(()=>_runSearch(),250);}

function handleSubjectFilter(v){
clearTimeout(searchDebounce);
const cb=document.getElementById('subjectFilterClear');if(cb)cb.style.display=v&&v.trim()?'flex':'none';
searchDebounce=setTimeout(()=>_runSearch(),250);}

function clearSubjectFilter(){
const sf=document.getElementById('subjectFilter'),cb=document.getElementById('subjectFilterClear');
if(sf)sf.value='';if(cb)cb.style.display='none';_runSearch();}

function _runSearch(){
const siEl=document.getElementById('searchInput'),sfEl=document.getElementById('subjectFilter');
const rd=document.getElementById('searchResults'),fr=document.getElementById('searchFilterRow');
if(!siEl||!rd)return;
const q=siEl.value,sf=sfEl?sfEl.value:'';
const tokens=q.split(/[,;]+/).map(t=>t.trim().toLowerCase()).filter(Boolean);
const subTk=sf.split(/[,;]+/).map(t=>t.trim().toLowerCase()).filter(Boolean);
if(!tokens.length){rd.style.display='none';if(fr)fr.style.display='none';return;}
const rollTk=[],subjFromMain=[];
tokens.forEach(t=>{if(RESULT.markDT.students.some(s=>s.RollNumber.toLowerCase().includes(t)||s.FullName.toLowerCase().includes(t)))rollTk.push(t);else if(RESULT.checkMark.some(r=>r.SubjectCode.toLowerCase().includes(t)))subjFromMain.push(t);});
const allSubFilter=[...new Set([...subTk,...subjFromMain])];
if(!rollTk.length&&allSubFilter.length){showSubSearch(allSubFilter,rd);if(fr)fr.style.display='none';return;}
let matched=[];if(rollTk.length){const seen=new Set();rollTk.forEach(t=>{RESULT.markDT.students.forEach(s=>{if(!seen.has(s.RollNumber)&&(s.RollNumber.toLowerCase().includes(t)||s.FullName.toLowerCase().includes(t))){seen.add(s.RollNumber);matched.push(s);}});});}
if(fr)fr.style.display=matched.length?'block':'none';
if(!matched.length){rd.innerHTML=`<div class="py-6 text-center text-sm text-on-surface-variant italic">Không tìm thấy sinh viên phù hợp</div>`;rd.style.display='block';return;}
if(matched.length>20){let h=`<div class="border border-surface-variant rounded-2xl overflow-hidden mt-2">`;matched.slice(0,20).forEach(s=>{h+=`<div class="px-5 py-3 cursor-pointer hover:bg-primary-container/20 flex items-center gap-3 border-b border-surface-variant last:border-0 transition-colors" onclick="document.getElementById('searchInput').value='${s.RollNumber}';_runSearch()"><span class="material-symbols-outlined text-primary text-base">person</span><span class="font-black text-primary text-sm">${s.RollNumber}</span><span class="text-sm text-on-surface-variant">${s.FullName}</span></div>`;});if(matched.length>20)h+=`<div class="px-5 py-3 text-xs text-on-surface-variant/60 font-bold">... và ${matched.length-20} SV khác</div>`;h+=`</div>`;rd.innerHTML=h;rd.style.display='block';return;}
const sf2=allSubFilter.length?allSubFilter:null;
let h=`<div class="border border-surface-variant rounded-2xl overflow-hidden mt-2">`;
matched.slice(0,20).forEach((s,i)=>{if(i)h+=`<hr class="border-primary-container border-4">`;h+=buildStuHTML(s.RollNumber,sf2);});
h+=`</div>`;rd.innerHTML=h;rd.style.display='block';}

function showSubSearch(subTk,rd){
let h=`<div class="border border-surface-variant rounded-2xl overflow-hidden mt-2">`;
subTk.forEach((st,i)=>{if(i)h+=`<hr class="border-surface-variant">`;
const items=RESULT.checkMark.filter(r=>r.SubjectCode.toLowerCase().includes(st)),errs=items.filter(r=>r.Check!=='OK');
h+=`<div class="p-5"><h4 class="text-xs font-black uppercase tracking-widest text-primary mb-3 flex items-center gap-2"><span class="material-symbols-outlined text-sm">school</span>${st.toUpperCase()} — ${items.length} bản ghi, ${errs.length} lỗi</h4>`;
h+=errs.length?renderMT(errs.slice(0,100),['RollNumber','FullName','SubjectCode','Mark_Dt','Mark_Fap','Status','Check']):`<p class="text-sm text-green-600 font-bold flex items-center gap-1"><span class="material-symbols-outlined text-base">check_circle</span>OK — không có lỗi</p>`;
h+=`</div>`;});h+=`</div>`;rd.innerHTML=h;rd.style.display='block';}

function buildStuHTML(roll,sf){
const stu=RESULT.markDT.students.find(s=>s.RollNumber===roll);if(!stu)return'';
const name=stu.FullName,init=name?name.charAt(name.lastIndexOf(' ')+1):roll.charAt(0);
let cm=RESULT.checkMark.filter(r=>r.RollNumber===roll);
let cr=RESULT.checkReplace.filter(r=>r.RollNumber===roll);
const cg=RESULT.checkGPA.filter(r=>r.RollNumber===roll);
const dtMarksAll=RESULT.markDT.marks.filter(r=>r.RollNumber===roll);
const fapMarksAll=RESULT.markFAP.filter(r=>r.RollNumber===roll);
let dtMarks=dtMarksAll,fapMarks=fapMarksAll;
if(sf&&sf.length){cm=cm.filter(r=>sf.some(f=>r.SubjectCode.toLowerCase().includes(f)));cr=cr.filter(r=>sf.some(f=>r.SubjectCode.toLowerCase().includes(f)));dtMarks=dtMarksAll.filter(r=>sf.some(f=>r.SubjectCode.toLowerCase().includes(f)));fapMarks=fapMarksAll.filter(r=>sf.some(f=>r.SubjectCode.toLowerCase().includes(f)));}
const errs=cm.filter(r=>r.Check!=='OK'),gpa=cg[0];
const fapDisplay=fapMarks.map(r=>({SubjectCode:r.SubjectCode,AverageMark:r.AverageMarkNum!=null?roundTo(r.AverageMarkNum,1):r.AverageMark,Status:r.Status,Credits:r.Credits||'',EndDate:r.EndDate?r.EndDate.toLocaleDateString('vi-VN'):''}));
const filterBadge=sf&&sf.length?`<span class="ml-2 text-[10px] px-2 py-0.5 bg-primary-container text-primary rounded-full font-bold">🔎 ${sf.map(f=>f.toUpperCase()).join(', ')}</span>`:'';
const showTotal=sf&&sf.length;
let h=`<div class="stu-card"><div class="stu-header"><div class="stu-avatar">${init}</div><div class="flex-1"><div class="flex items-center flex-wrap gap-1"><h3 class="font-black text-on-surface text-sm">${name||roll}</h3>${filterBadge}</div><p class="text-xs text-on-surface-variant mt-0.5">${roll}${gpa?` · GPA ĐT: <strong>${gpa.GPA_Dt||'—'}</strong> · Calc: <strong>${gpa.GPA_Dt_Calc||'—'}</strong> · FAP: <strong>${gpa.GPA_Fap||'—'}</strong> · <span class="${gpa.Check.startsWith('OK')?'text-green-600':'text-error'} font-bold">${gpa.Check}</span>`:''}</p></div></div>`;
h+=`<div class="flex gap-2 flex-wrap mb-4">
<span class="text-[10px] px-3 py-1 bg-surface rounded-full border border-surface-variant font-bold">${cm.length}${showTotal?'/'+RESULT.checkMark.filter(r=>r.RollNumber===roll).length:''} môn check</span>
<span class="text-[10px] px-3 py-1 rounded-full border font-bold ${errs.length?'bg-red-50 border-red-200 text-error':'bg-green-50 border-green-200 text-green-700'}">${errs.length} lỗi</span>
<span class="text-[10px] px-3 py-1 bg-surface rounded-full border border-surface-variant font-bold">${dtMarks.length}${showTotal?'/'+dtMarksAll.length:''} môn ĐT</span>
<span class="text-[10px] px-3 py-1 bg-surface rounded-full border border-surface-variant font-bold">${fapMarks.length}${showTotal?'/'+fapMarksAll.length:''} môn FAP</span>
</div>`;
if(errs.length)h+=`<div class="stu-section"><h4>⚠ Check Mark — Lỗi (${errs.length})</h4>${renderMT(errs,['SubjectCode','Mark_Dt','Mark_Fap','Status','Check'])}</div>`;
else if(cm.length)h+=`<div class="stu-section"><h4 class="!text-green-600">✓ Check Mark OK (${cm.length} môn)</h4></div>`;
if(cr.length)h+=`<div class="stu-section"><h4>🔄 Check Replace (${cr.length})</h4>${renderMT(cr,['SubjectCode','Replacecode','Note','Mark_Dt','Mark_Fap','Check'])}</div>`;
h+=`<div class="stu-section"><h4>📋 Mark_DT (${dtMarks.length}${showTotal?'/'+dtMarksAll.length:''} môn)</h4>${renderMT(dtMarks,['SubjectCode','AverageMark','Credits'])}</div>`;
h+=`<div class="stu-section"><h4>📊 Mark_FAP (${fapMarks.length}${showTotal?'/'+fapMarksAll.length:''} môn)</h4>${renderMT(fapDisplay,['SubjectCode','AverageMark','Status','Credits','EndDate'])}</div>`;
h+=`</div>`;return h;}

function renderMT(data,cols){
if(!data||!data.length)return`<p class="text-xs text-on-surface-variant/50 italic py-2">Không có dữ liệu</p>`;
let h=`<div style="overflow-x:auto;max-height:300px;overflow-y:auto"><table class="stu-mini-table"><thead><tr>`;
cols.forEach(c=>{h+=`<th>${c}</th>`;});h+=`</tr></thead><tbody>`;
data.forEach(row=>{h+=`<tr>`;cols.forEach(c=>{let v=row[c]!==undefined?row[c]:'',cls='';if(c==='Check'){const sv=String(v);if(sv==='OK')cls='color:#15803d;font-weight:700';else if(sv.includes('kỹ thuật'))cls='color:#1d4ed8;font-weight:700;background:#dbeafe';else if(sv.includes('Lệch')||sv==='Not ok')cls='color:#b91c1c;font-weight:700;background:#fee2e2';else if(sv)cls='color:#92400e;font-weight:700;background:#fef3c7';}h+=`<td style="${cls}">${v}</td>`;});h+=`</tr>`;});
h+=`</tbody></table></div>`;return h;}

function clearSearch(){
const ids=['searchInput','subjectFilter'];ids.forEach(id=>{const el=document.getElementById(id);if(el)el.value='';});
['searchClear','subjectFilterClear'].forEach(id=>{const el=document.getElementById(id);if(el)el.style.display='none';});
const rd=document.getElementById('searchResults'),fr=document.getElementById('searchFilterRow');
if(rd)rd.style.display='none';if(fr)fr.style.display='none';
_currentRollTokens=[];}

// ==================== Downloads ====================
function getTS(){const n=new Date();return n.getFullYear()+String(n.getMonth()+1).padStart(2,'0')+String(n.getDate()).padStart(2,'0');}
function getFullTS(){return new Date().toLocaleString('vi-VN',{day:'2-digit',month:'2-digit',year:'numeric',hour:'2-digit',minute:'2-digit',second:'2-digit'});}
function downloadResult(){const wb=XLSX.utils.book_new(),ts=getFullTS();
const addSh=(name,title,data,nc)=>{const hdr=[[title],['Thời gian: '+ts],[]];const ws=XLSX.utils.aoa_to_sheet(hdr);XLSX.utils.sheet_add_json(ws,data,{origin:'A4'});ws['!merges']=[{s:{r:0,c:0},e:{r:0,c:nc-1}},{s:{r:1,c:0},e:{r:1,c:nc-1}}];const cols=[];for(let i=0;i<nc;i++)cols.push({wch:18});ws['!cols']=cols;XLSX.utils.book_append_sheet(wb,ws,name);};
addSh('Check Mark','BÁO CÁO CHECK MARK',RESULT.checkMark,9);addSh('Check Replace','BÁO CÁO CHECK REPLACE',RESULT.checkReplace,11);addSh('Check GPA','BÁO CÁO CHECK GPA',RESULT.checkGPA,9);
const s=RESULT.summary,sd=[['TỔNG HỢP KẾT QUẢ RÀ SOÁT'],['Thời gian: '+ts],[],['Nội dung','Giá trị'],['1. SV đã kiểm tra',s.totalStudents],['2. Tổng môn kiểm tra',s.totalSubjectsChecked],['3. Môn lệch/Not ok',s.notOkCount],['4. Còn lệch sau Replace',s.stillNotOkAfterReplace],['5. SV đạt VOV',s.vovPassCount+'/'+s.totalStudents],['6. SV đạt OJT',s.ojtPassCount+'/'+s.totalStudents],['7. SV đạt GDQP',s.gdqpPassCount+'/'+s.totalStudents],['8. SV lệch GPA',s.gpaMismatch],[]];
// Top môn lệch
if(s.topErrs&&s.topErrs.length){sd.push(['TOP MÔN LỆCH NHIỀU NHẤT']);sd.push(['Mã môn','Số lượng']);s.topErrs.forEach(e=>sd.push([e.code,e.count]));sd.push([]);}
// SV chưa đạt GDQP
if(s.gdqpNotPassCount>0&&s.gdqpDetails){sd.push(['SV CHƯA ĐẠT GDQP ('+s.gdqpNotPassCount+')']);sd.push(['RollNumber','Môn']);Object.entries(s.gdqpDetails).forEach(([roll,subs])=>sd.push([roll,subs.join(', ')]));sd.push([]);}
// SV chưa đạt VOV
if(s.vovNotPassCount>0&&s.vovDetails){sd.push(['SV CHƯA ĐẠT VOV ('+s.vovNotPassCount+')']);sd.push(['RollNumber','Nhóm còn thiếu']);Object.entries(s.vovDetails).forEach(([roll,groups])=>sd.push([roll,groups.join(', ')]));sd.push([]);}
// SV chưa đạt OJT
if(s.ojtNotPassCount>0&&s.ojtDetails){sd.push(['SV CHƯA ĐẠT OJT ('+s.ojtNotPassCount+')']);sd.push(['RollNumber','Ghi chú']);Object.entries(s.ojtDetails).forEach(([roll,note])=>sd.push([roll,note]));sd.push([]);}
const ws4=XLSX.utils.aoa_to_sheet(sd);ws4['!cols']=[{wch:45},{wch:30}];XLSX.utils.book_append_sheet(wb,ws4,'Summary');
XLSX.writeFile(wb,`${getTS()}-Result_XetTN.xlsx`);}
function downloadMarkDT(){const wb=XLSX.utils.book_new(),ts=getFullTS();
const dtData=RESULT.markDT.marks.map(r=>({RollNumber:r.RollNumber,FullName:r.FullName,SubjectCode:r.SubjectCode,AverageMark:r.AverageMark,Credits:r.Credits??''}));
const hdr=[['MARK_DT — Điểm từ ĐT'],['Thời gian: '+ts],[`Tổng: ${RESULT.markDT.marks.length} bản ghi, ${RESULT.markDT.students.length} SV`],[]];const ws=XLSX.utils.aoa_to_sheet(hdr);XLSX.utils.sheet_add_json(ws,dtData,{origin:'A5'});ws['!cols']=[{wch:16},{wch:28},{wch:16},{wch:14},{wch:10}];XLSX.utils.book_append_sheet(wb,ws,'Mark_DT');XLSX.writeFile(wb,`${getTS()}-Mark_DT.xlsx`);}
function downloadMarkFAP(){const wb=XLSX.utils.book_new(),ts=getFullTS();
const fap=RESULT.markFAP.map(r=>({RollNumber:r.RollNumber,SubjectCode:r.SubjectCode,AverageMark:r.AverageMarkNum!=null?roundTo(r.AverageMarkNum,1):r.AverageMark,Status:r.Status,Credits:r.Credits??'',StartDate:r.StartDate?r.StartDate.toLocaleDateString('vi-VN'):'',EndDate:r.EndDate?r.EndDate.toLocaleDateString('vi-VN'):''}));
const hdr=[['MARK_FAP — Điểm từ FAP (lọc DS ĐT, lần học gần nhất)'],['Thời gian: '+ts],[`Tổng: ${fap.length} bản ghi`],[]];
const ws=XLSX.utils.aoa_to_sheet(hdr);XLSX.utils.sheet_add_json(ws,fap,{origin:'A5'});ws['!cols']=[{wch:16},{wch:16},{wch:14},{wch:16},{wch:10},{wch:14},{wch:14}];XLSX.utils.book_append_sheet(wb,ws,'Mark_FAP');XLSX.writeFile(wb,`${getTS()}-Mark_FAP.xlsx`);}

// ==================== Reset ====================
function resetAll(){
const hi=document.getElementById('headerSearchInput');if(hi)hi.value='';
FILE_KEYS.forEach(k=>{delete FILES[k];delete FILE_BUFFERS[k];const c=document.getElementById('card_'+k);if(c){c.classList.remove('loaded','error');const inp=c.querySelector('input[type="file"]');if(inp)inp.value='';const st=document.getElementById('status_'+k);if(st)st.innerHTML='';}});
RESULT={};Object.keys(DT).forEach(k=>delete DT[k]);clearSearch();
document.getElementById('btnProcess').disabled=true;
document.getElementById('rerunBanner').classList.add('hidden');
document.getElementById('resultContent').innerHTML='';
document.getElementById('resultTabs').innerHTML='';
document.getElementById('summaryCards').innerHTML='';
goToStep(1);}

// DnD support
document.addEventListener('DOMContentLoaded',()=>{
document.querySelectorAll('.upload-card').forEach(card=>{
card.addEventListener('dragover',e=>{e.preventDefault();card.style.borderColor='#1A237E';card.style.background='#E8EAF6';});
card.addEventListener('dragleave',()=>{card.style.borderColor='';card.style.background='';});
card.addEventListener('drop',e=>{e.preventDefault();card.style.borderColor='';card.style.background='';const inp=card.querySelector('input[type="file"]');if(e.dataTransfer.files.length){inp.files=e.dataTransfer.files;inp.dispatchEvent(new Event('change'));}});});});
</script>
</body>
</html>
