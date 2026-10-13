import os

# ── 2. 스토어재고 v2: 이지어드민/사방넷 모방 + 문제점 보완 ──
# 모방: 다채널 주문 수집 → 재고 동기화 → 출고 처리 (이지어드민 핵심)
# 보완: 가입비 0원, 선불제 없음, 무료 플랜 핵심기능 무제한, 1인 셀러 정면 공략

store_v2 = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>스토어재고 — 가입비 0원 재고관리</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Noto Sans KR',sans-serif;background:#f5f7fa;color:#333;line-height:1.6}
.container{max-width:1100px;margin:0 auto;padding:20px}
.hero{text-align:center;padding:48px 20px;background:linear-gradient(135deg,#0f3460 0%,#16213e 50%,#1a1a2e 100%);color:#fff;border-radius:16px;margin-bottom:24px}
.hero h1{font-size:2.2em;margin-bottom:12px}
.hero .sub{font-size:1.1em;opacity:.9;margin-bottom:20px}
.hero .compare{display:inline-block;background:rgba(255,255,255,.1);padding:12px 24px;border-radius:10px;font-size:.95em}
.hero .compare b{color:#4ade80}
.card{background:#fff;border-radius:12px;padding:28px;margin-bottom:20px;box-shadow:0 2px 10px rgba(0,0,0,.08)}
.card h2{font-size:1.25em;margin-bottom:8px;color:#1a1a1a}
.card .desc{color:#666;font-size:.95em;margin-bottom:20px}
.tabs{display:flex;gap:8px;margin-bottom:20px;flex-wrap:wrap}
.tab{padding:10px 20px;border:2px solid #e0e0e0;border-radius:8px;background:#fff;cursor:pointer;font-weight:600;transition:all .2s}
.tab:hover{border-color:#0f3460}
.tab.active{border-color:#0f3460;background:#f0f7ff;color:#0f3460}
.tab-content{display:none}
.tab-content.active{display:block}
.inv-table{width:100%;border-collapse:collapse;margin-top:16px;font-size:.92em}
.inv-table th,.inv-table td{padding:11px;text-align:left;border-bottom:1px solid #eee}
.inv-table th{background:#f8f9fa;font-weight:600;color:#555}
.inv-table tr:hover{background:#fafafa}
.stock-low{color:#dc3545;font-weight:600}
.stock-ok{color:#28a745;font-weight:600}
.channel-badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:.75em;font-weight:600;margin-right:4px}
.ch-naver{background:#03c75a;color:#fff}
.ch-coupang{background:#e52528;color:#fff}
.ch-offline{background:#6c757d;color:#fff}
.btn{display:inline-block;padding:10px 20px;background:#0f3460;color:#fff;border:none;border-radius:6px;font-size:.95em;font-weight:600;cursor:pointer}
.btn:hover{background:#0a2540}
.btn-sm{padding:5px 12px;font-size:.85em}
.btn-danger{background:#dc3545}
.btn-danger:hover{background:#c82333}
.btn-outline{background:#fff;color:#0f3460;border:2px solid #0f3460}
.btn-outline:hover{background:#f0f7ff}
.input-group{margin-bottom:12px}
.input-group label{display:block;font-weight:600;margin-bottom:4px;color:#555;font-size:.9em}
.input-group input,.input-group select{width:100%;padding:10px;border:2px solid #e0e0e0;border-radius:6px;font-size:.95em}
.input-group input:focus,.input-group select:focus{outline:none;border-color:#0f3460}
.input-row{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.sync-bar{display:flex;align-items:center;gap:10px;padding:14px;background:#f0fff4;border-radius:8px;margin-bottom:20px;border-left:4px solid #28a745}
.sync-dot{width:10px;height:10px;border-radius:50%;background:#28a745;animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
.price-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-top:20px}
.price-card{background:#f9f9f9;padding:24px;border-radius:12px;text-align:center;position:relative}
.price-card.recommended{border:2px solid #0f3460;background:#f0f7ff}
.price-card .plan{font-size:1.1em;font-weight:700;color:#0f3460;margin-bottom:8px}
.price-card .price{font-size:2.2em;font-weight:700;color:#333}
.price-card .period{font-size:.9em;color:#888;margin-bottom:16px}
.price-card .features{text-align:left;margin-bottom:16px}
.price-card .features li{margin-bottom:6px;font-size:.9em;list-style:none}
.price-card .features li:before{content:"✓ ";color:#28a745;font-weight:700}
.compare-table{width:100%;border-collapse:collapse;margin-top:16px;font-size:.9em}
.compare-table th,.compare-table td{padding:12px;text-align:left;border-bottom:1px solid #eee}
.compare-table th{background:#f8f9fa;font-weight:600;color:#555}
.compare-table .ours{background:#f0fff4;font-weight:600;color:#155724}
.compare-table .theirs{color:#dc3545}
.badge{display:inline-block;padding:3px 10px;border-radius:4px;font-size:.8em;font-weight:600}
.badge.green{background:#d4edda;color:#155724}
.badge.red{background:#f8d7da;color:#721c24}
.footer{text-align:center;padding:30px;color:#999;font-size:.9em}
@media(max-width:768px){.input-row{grid-template-columns:1fr}.inv-table{font-size:.82em}.compare-table{font-size:.8em}}
</style>
</head>
<body>
<div class="container">

<div class="hero">
<h1>스토어재고</h1>
<div class="sub">이지어드민 월 20만원 + 가입비 10만원 → 스토어재고 <b>0원</b></div>
<div class="compare">가입비 <b>0원</b> · 선불제 <b>없음</b> · 무료 플랜 <b>핵심기능 무제한</b></div>
</div>

<div class="card">
<div class="sync-bar">
<div class="sync-dot"></div>
<div>
<strong>실시간 동기화 활성</strong>
<div style="font-size:.85em;color:#888">마지막 동기화: 방금 전 · 연동 채널 3개</div>
</div>
</div>

<div class="tabs">
<div class="tab active" onclick="switchTab('inventory',this)">재고 관리</div>
<div class="tab" onclick="switchTab('orders',this)">주문 수집</div>
<div class="tab" onclick="switchTab('pricing',this)">요금제</div>
<div class="tab" onclick="switchTab('compare',this)">1등 제품 비교</div>
</div>

<div class="tab-content active" id="inventory">
<h2>재고 목록</h2>
<div class="desc">온라인·오프라인 재고를 한 화면에서 관리합니다. 수량이 바뀌면 모든 채널에 즉시 반영됩니다.</div>
<button class="btn btn-sm" onclick="addItem()">+ 상품 추가</button>
<table class="inv-table">
<thead>
<tr><th>상품명</th><th>SKU</th><th>채널</th><th>온라인</th><th>오프라인</th><th>합계</th><th>상태</th><th>관리</th></tr>
</thead>
<tbody id="invBody"></tbody>
</table>
</div>

<div class="tab-content" id="orders">
<h2>주문 수집</h2>
<div class="desc">여러 쇼핑몰의 주문을 한 번에 수집하고 출고 처리합니다.</div>
<table class="inv-table">
<thead>
<tr><th>주문번호</th><th>채널</th><th>상품</th><th>수량</th><th>상태</th><th>처리</th></tr>
</thead>
<tbody>
<tr><td>ORD-20261013-001</td><td><span class="channel-badge ch-naver">네이버</span></td><td>아메리카노 원두 1kg</td><td>2</td><td>출고대기</td><td><button class="btn btn-sm" onclick="alert('출고 처리되었습니다.')">출고</button></td></tr>
<tr><td>ORD-20261013-002</td><td><span class="channel-badge ch-coupang">쿠팡</span></td><td>카페라떼 시럽 500ml</td><td>1</td><td>출고대기</td><td><button class="btn btn-sm" onclick="alert('출고 처리되었습니다.')">출고</button></td></tr>
<tr><td>ORD-20261013-003</td><td><span class="channel-badge ch-offline">오프라인</span></td><td>텀블러 500ml</td><td>3</td><td>완료</td><td><span class="badge green">처리됨</span></td></tr>
</tbody>
</table>
</div>

<div class="tab-content" id="pricing">
<h2>요금제 — 숨은 비용 없음</h2>
<div class="desc">가입비 0원, 선불제 없음, 언제든 해지 가능합니다.</div>
<div class="price-grid">
<div class="price-card">
<div class="plan">무료</div>
<div class="price">0원</div>
<div class="period">영구 무료</div>
<ul class="features">
<li>상품 500개</li>
<li>채널 3개 연동</li>
<li>실시간 재고 동기화</li>
<li>주문 수집·출고 처리</li>
<li>기본 매출 리포트</li>
</ul>
<button class="btn btn-outline" onclick="alert('무료로 시작합니다.')">무료 시작</button>
</div>
<div class="price-card recommended">
<div class="plan">프로 <span class="badge green">추천</span></div>
<div class="price">9,900원</div>
<div class="period">/월 (VAT 포함)</div>
<ul class="features">
<li>상품 무제한</li>
<li>채널 무제한</li>
<li>실시간 재고 동기화</li>
<li>자동 발주 알림</li>
<li>고급 매출 분석</li>
<li>CS 문의 자동 분류</li>
</ul>
<button class="btn" onclick="alert('프로 플랜을 선택했습니다.')">프로 시작</button>
</div>
</div>
</div>

<div class="tab-content" id="compare">
<h2>1등 제품과 비교</h2>
<div class="desc">이지어드민·사방넷의 실제 요금과 비교했습니다.</div>
<table class="compare-table">
<thead>
<tr><th>항목</th><th>이지어드민</th><th>사방넷</th><th>스토어재고</th></tr>
</thead>
<tbody>
<tr><td>월 요금</td><td class="theirs">20만~200만원</td><td class="theirs">15만~60만원</td><td class="ours">0원 (무료 플랜)</td></tr>
<tr><td>가입비</td><td class="theirs">10만~300만원</td><td class="theirs">10만원</td><td class="ours">0원</td></tr>
<tr><td>계약 방식</td><td class="theirs">6~12개월 선불</td><td class="theirs">3~24개월 선불</td><td class="ours">월 단위, 언제든 해지</td></tr>
<tr><td>무료체험</td><td class="theirs">기간 미표기</td><td class="theirs">없음</td><td class="ours">영구 무료 플랜</td></tr>
<tr><td>1인 셀러 적합성</td><td class="theirs">부담</td><td class="theirs">부담</td><td class="ours">정면 최적화</td></tr>
<tr><td>풀 커스텀</td><td class="theirs">불가</td><td class="theirs">제한적</td><td class="ours">불필요 (단순 설계)</td></tr>
</tbody>
</table>
<div style="background:#f0fff4;border-left:4px solid #28a745;padding:16px;border-radius:8px;margin-top:20px">
<b>1인 셀러 기준 연간 절감액</b><br>
이지어드민 스탠다드(월 20만원 × 12 + 가입비 10만원) = <b>250만원</b><br>
스토어재고 무료 플랜 = <b>0원</b> → <b style="color:#155724">연 250만원 절감</b>
</div>
</div>

</div>

<div class="footer">
<p>스토어재고 v2.0 — 모든 처리는 브라우저 안에서만 이루어집니다.</p>
</div>
</div>

<script>
let inventory=[
{name:'아메리카노 원두 1kg',sku:'COF-001',channels:['네이버','쿠팡','오프라인'],online:45,offline:12},
{name:'카페라떼 시럽 500ml',sku:'COF-002',channels:['네이버','오프라인'],online:32,offline:8},
{name:'카푸치노 파우더',sku:'COF-003',channels:['쿠팡'],online:15,offline:3},
{name:'바닐라 시럽 750ml',sku:'COF-004',channels:['네이버','쿠팡'],online:28,offline:5},
{name:'텀블러 500ml',sku:'ACC-001',channels:['네이버','오프라인'],online:8,offline:2}
];

function chBadge(ch){
const map={'네이버':'ch-naver','쿠팡':'ch-coupang','오프라인':'ch-offline'};
return `<span class="channel-badge ${map[ch]||'ch-offline'}">${ch}</span>`;
}

function renderInv(){
const tbody=document.getElementById('invBody');
tbody.innerHTML=inventory.map((item,i)=>{
const total=item.online+item.offline;
const low=total<20;
return `<tr>
<td>${item.name}</td>
<td>${item.sku}</td>
<td>${item.channels.map(chBadge).join('')}</td>
<td>${item.online}</td>
<td>${item.offline}</td>
<td>${total}</td>
<td class="${low?'stock-low':'stock-ok'}">${low?'부족':'정상'}</td>
<td><button class="btn btn-sm btn-danger" onclick="removeItem(${i})">삭제</button></td>
</tr>`;
}).join('');
}

function addItem(){
const name=prompt('상품명:');
if(!name)return;
const sku=prompt('SKU:');
if(!sku)return;
const online=parseInt(prompt('온라인 재고:'))||0;
const offline=parseInt(prompt('오프라인 재고:'))||0;
inventory.push({name,sku,channels:['네이버'],online,offline});
renderInv();
}

function removeItem(i){
if(confirm('삭제하시겠습니까?')){
inventory.splice(i,1);
renderInv();
}
}

function switchTab(tab,el){
document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
document.querySelectorAll('.tab-content').forEach(c=>c.classList.remove('active'));
el.classList.add('active');
document.getElementById(tab).classList.add('active');
}

renderInv();
</script>
</body>
</html>
'''

os.makedirs(r"D:\10jo_Studio\03_apps_dev\projects\10jo-site\store-inventory-v2", exist_ok=True)
with open(r"D:\10jo_Studio\03_apps_dev\projects\10jo-site\store-inventory-v2\index.html", "w", encoding="utf-8") as f:
    f.write(store_v2)
print("스토어재고 v2 생성 완료")
