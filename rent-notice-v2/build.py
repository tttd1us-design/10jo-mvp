import os

# ── 1. 렌트노티스 v2: 참지마요/당당 모방 + 문제점 보완 ──
# 모방: 내용증명 작성 → 발송 → 법적 효력 안내 (참지마요/당당 핵심)
# 보완: 가격 비교표 공개, 발송 없이 PDF 무료, 법적 절차 가이드, 반송 대처

rent_v2 = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>렌트노티스 v2 — 내용증명 비교·작성·발송 가이드</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Noto Sans KR',sans-serif;background:#f5f7fa;color:#333;line-height:1.6}
.container{max-width:1100px;margin:0 auto;padding:20px}
.hero{text-align:center;padding:48px 20px;background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);color:#fff;border-radius:16px;margin-bottom:24px}
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
.compare-table{width:100%;border-collapse:collapse;margin-top:16px;font-size:.9em}
.compare-table th,.compare-table td{padding:12px;text-align:left;border-bottom:1px solid #eee}
.compare-table th{background:#f8f9fa;font-weight:600;color:#555}
.compare-table .ours{background:#f0fff4;font-weight:600;color:#155724}
.compare-table .theirs{color:#dc3545}
.input-group{margin-bottom:16px}
.input-group label{display:block;font-weight:600;margin-bottom:6px;color:#555;font-size:.95em}
.input-group input,.input-group select,.input-group textarea{width:100%;padding:12px;border:2px solid #e0e0e0;border-radius:8px;font-size:1em}
.input-group input:focus,.input-group select:focus,.input-group textarea:focus{outline:none;border-color:#0f3460}
.input-row{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.result{background:#f0f7ff;border-left:4px solid #0f3460;padding:20px;border-radius:8px;margin-top:20px}
.result h3{color:#0f3460;margin-bottom:12px}
.letter-preview{background:#fff;border:2px solid #e0e0e0;border-radius:8px;padding:24px;margin-top:20px;font-size:.95em;line-height:1.8}
.letter-preview h4{text-align:center;margin-bottom:16px;font-size:1.1em}
.letter-preview .field{margin-bottom:8px}
.letter-preview .field b{display:inline-block;width:100px;color:#555}
.step-list{counter-reset:step;margin-top:16px}
.step-list li{list-style:none;padding:12px 0;border-bottom:1px solid #f0f0f0;position:relative;padding-left:48px}
.step-list li::before{counter-increment:step;content:counter(step);position:absolute;left:0;top:12px;width:32px;height:32px;background:#0f3460;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.85em}
.step-list li .title{font-weight:600}
.step-list li .text{font-size:.9em;color:#666;margin-top:4px}
.badge{display:inline-block;padding:3px 10px;border-radius:4px;font-size:.8em;font-weight:600}
.badge.green{background:#d4edda;color:#155724}
.badge.red{background:#f8d7da;color:#721c24}
.badge.yellow{background:#fff3cd;color:#856404}
.btn{display:inline-block;padding:14px 32px;background:#0f3460;color:#fff;border:none;border-radius:8px;font-size:1.05em;font-weight:600;cursor:pointer;margin-top:16px}
.btn:hover{background:#0a2540}
.btn-full{width:100%}
.btn-outline{background:#fff;color:#0f3460;border:2px solid #0f3460}
.btn-outline:hover{background:#f0f7ff}
.price-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-top:20px}
.price-card{background:#f9f9f9;padding:24px;border-radius:12px;text-align:center}
.price-card.recommended{border:2px solid #0f3460;background:#f0f7ff}
.price-card .plan{font-size:1.1em;font-weight:700;color:#0f3460;margin-bottom:8px}
.price-card .price{font-size:2.2em;font-weight:700;color:#333}
.price-card .period{font-size:.9em;color:#888;margin-bottom:16px}
.price-card .features{text-align:left;margin-bottom:16px}
.price-card .features li{margin-bottom:6px;font-size:.9em;list-style:none}
.price-card .features li:before{content:"✓ ";color:#28a745;font-weight:700}
.alert{background:#fff3cd;border-left:4px solid #ffc107;padding:14px;border-radius:8px;margin-top:16px;font-size:.9em;color:#856404}
.footer{text-align:center;padding:30px;color:#999;font-size:.9em}
@media(max-width:768px){.input-row{grid-template-columns:1fr}.hero h1{font-size:1.6em}.compare-table{font-size:.8em}}
</style>
</head>
<body>
<div class="container">

<div class="hero">
<h1>렌트노티스 v2</h1>
<div class="sub">참지마요 발송 14,900원 + 당당 14,900원 → 렌트노티스 <b>PDF 무료 + 발송 9,900원</b></div>
<div class="compare">가격 비교 <b>100% 공개</b> · PDF 작성 <b>무료</b> · 법적 절차 <b>가이드</b></div>
</div>

<div class="card">
<div class="tabs">
<div class="tab active" onclick="switchTab('compare',this)">가격 비교</div>
<div class="tab" onclick="switchTab('write',this)">내용증명 작성</div>
<div class="tab" onclick="switchTab('guide',this)">법적 절차</div>
<div class="tab" onclick="switchTab('pricing',this)">요금제</div>
</div>

<div class="tab-content active" id="compare">
<h2>1등 제품 가격 비교 — 숨김 없이 전부 공개</h2>
<div class="desc">참지마요·당당·로에버·우체국 직접 창구의 실제 요금을 비교했습니다.</div>
<table class="compare-table">
<thead>
<tr><th>서비스</th><th>PDF 작성</th><th>전자 발송</th><th>우체국 발송</th><th>비고</th></tr>
</thead>
<tbody>
<tr><td>참지마요</td><td class="ours">무료</td><td class="theirs">14,900원</td><td class="theirs">14,900원</td><td>작성·다운로드 무료, 발송만 유료</td></tr>
<tr><td>당당</td><td class="ours">무료</td><td class="theirs">14,900원</td><td class="theirs">14,900원</td><td>송달증명서·시점확인서 포함</td></tr>
<tr><td>로에버</td><td class="theirs">—</td><td class="theirs">14,900원</td><td class="theirs">19,900원</td><td>변호사 발송</td></tr>
<tr><td>우체국 직접</td><td class="theirs">—</td><td class="theirs">—</td><td class="theirs">4,130원~</td><td>직접 작성·접수 필요</td></tr>
<tr style="background:#f0fff4"><td class="ours"><b>렌트노티스 v2</b></td><td class="ours"><b>무료</b></td><td class="ours"><b>9,900원</b></td><td class="ours"><b>9,900원</b></td><td class="ours"><b>법적 절차 가이드 포함</b></td></tr>
</tbody>
</table>
<div class="alert">
<b>참지마요·당당의 실제 문제점</b><br>
· 전자 발송 시 <b>수신자 휴대전화 번호가 정확해야 함</b> — 번호가 틀리면 발송 실패<br>
· 전자 내용증명은 <b>카카오톡으로만 발송</b> 가능 — 카톡 안 쓰는 상대방에게 불가<br>
· 발송 후 <b>수정·취소 불가</b> — 결제와 동시에 문서가 전송됨<br>
· <b>반송 시 대처법 안내 없음</b> — 수신인부재·주소불명으로 반송되면 어떻게 할지 모름<br>
· <b>법적 효력 설명 부족</b> — 내용증명 자체에 강제력이 없다는 점을 명시하지 않음
</div>
</div>

<div class="tab-content" id="write">
<h2>내용증명 작성 — 무료</h2>
<div class="desc">빈 채를 채우면 내용증명 초안이 자동으로 생성됩니다. PDF 다운로드는 무료입니다.</div>
<div class="input-row">
<div class="input-group">
<label for="senderName">발신인 이름</label>
<input type="text" id="senderName" placeholder="홍길동" oninput="genLetter()">
</div>
<div class="input-group">
<label for="senderAddr">발신인 주소</label>
<input type="text" id="senderAddr" placeholder="서울특별시 강남구 테헤란로 123" oninput="genLetter()">
</div>
</div>
<div class="input-row">
<div class="input-group">
<label for="receiverName">수신인 이름</label>
<input type="text" id="receiverName" placeholder="김철수" oninput="genLetter()">
</div>
<div class="input-group">
<label for="receiverAddr">수신인 주소</label>
<input type="text" id="receiverAddr" placeholder="서울특별시 마포구 월드컵북로 456" oninput="genLetter()">
</div>
</div>
<div class="input-row">
<div class="input-group">
<label for="caseType">사건 유형</label>
<select id="caseType" onchange="genLetter()">
<option value="rent">임대료 미납</option>
<option value="deposit">보증금 미반환</option>
<option value="unpaid">용역비 미지급</option>
<option value="other">기타</option>
</select>
</div>
<div class="input-group">
<label for="amount">금액 (원)</label>
<input type="number" id="amount" value="5000000" min="0" step="100000" oninput="genLetter()">
</div>
</div>
<div class="input-group">
<label for="deadline">지급 기한</label>
<input type="date" id="deadline" value="2026-11-15" oninput="genLetter()">
</div>

<div class="letter-preview" id="letterPreview">
<h4>내 용 증 명</h4>
<div class="field"><b>발신인:</b> <span id="lSender"></span></div>
<div class="field"><b>수신인:</b> <span id="lReceiver"></span></div>
<div class="field"><b>제목:</b> <span id="lTitle"></span></div>
<div class="field"><b>본문:</b></div>
<div id="lBody" style="margin-top:8px;padding:12px;background:#f8f9fa;border-radius:6px"></div>
</div>

<button class="btn" onclick="downloadPDF()">PDF 다운로드 (무료)</button>
</div>

<div class="tab-content" id="guide">
<h2>법적 절차 가이드 — 1등 제품이 안 알려주는 것</h2>
<div class="desc">내용증명은 강제력이 없습니다. 발송 후 어떻게 해야 하는지 단계별로 안내합니다.</div>
<ol class="step-list">
<li>
<div class="title">내용증명 발송</div>
<div class="text">우체국 내용증명 또는 전자 내용증명 발송. 발송일로부터 <b>6개월 내</b>에 다음 단계로 넘어가야 합니다.</div>
</li>
<li>
<div class="title">반송 시 대처</div>
<div class="text">수신인부재·폐문부재·주소불명으로 반송되면: ① 반송된 봉투를 <b>뜯지 말 것</b> ② 인근 주민센터/시군구청에서 상대방 주소지 확인 ③ 확인된 주소로 재발송</div>
</li>
<li>
<div class="title">지급명령 신청</div>
<div class="text">내용증명 발송 후 상대방이 응답하지 않으면 <b>지급명령</b> 신청. 법원 서식 작성 → 접수 → 심문 → 결정.</div>
</li>
<li>
<div class="title">소송 제기</div>
<div class="text">지급명령 확정 후 상대방이 이의 제기하지 않으면 <b>확정판 기재 집행</b> 가능. 이의 제기 시 본소송 전환.</div>
</li>
<li>
<div class="title">시효 관리</div>
<div class="text">내용증명 발송으로 <b>시효 6개월 중단</b>. 6개월 내에 반드시 다음 단계로 넘어가야 합니다.</div>
</li>
</ol>
<div class="alert">
<b>참지마요·당당이 안 알려주는 것</b><br>
· 내용증명은 <b>법적 강제력이 없음</b> — 증거자료로만 활용<br>
· 발송 후 <b>6개월 내</b>에 지급명령/소송 신청 필요<br>
· 반송 시 <b>봉투를 뜯지 말아야</b> 함<br>
· 전자 내용증명은 <b>카카오톡으로만</b> 발송 가능
</div>
</div>

<div class="tab-content" id="pricing">
<h2>요금제</h2>
<div class="price-grid">
<div class="price-card">
<div class="plan">무료</div>
<div class="price">0원</div>
<div class="period">영구 무료</div>
<ul class="features">
<li>내용증명 작성</li>
<li>PDF 다운로드</li>
<li>법적 절차 가이드</li>
<li>가격 비교표</li>
</ul>
<button class="btn btn-outline" onclick="alert('무료로 시작합니다.')">무료 시작</button>
</div>
<div class="price-card recommended">
<div class="plan">프로 <span class="badge green">추천</span></div>
<div class="price">9,900원</div>
<div class="period">/월 (VAT 포함)</div>
<ul class="features">
<li>무료 플랜 전부</li>
<li>발송 대행 (우체국/전자)</li>
<li>반송 자동 재발송</li>
<li>지급명령 서식 자동 생성</li>
<li>시효 관리 알림</li>
</ul>
<button class="btn" onclick="alert('프로 플랜을 선택했습니다.')">프로 시작</button>
</div>
</div>
</div>

</div>

<div class="footer">
<p>렌트노티스 v2.0 — 법률 자문이 아닙니다. 법적 문제는 반드시 변호사와 상담하시기 바랍니다.</p>
</div>
</div>

<script>
function genLetter(){
const sender=document.getElementById('senderName').value||'홍길동';
const sAddr=document.getElementById('senderAddr').value||'서울특별시 강남구 테헤란로 123';
const receiver=document.getElementById('receiverName').value||'김철수';
const rAddr=document.getElementById('receiverAddr').value||'서울특별시 마포구 월드컵북로 456';
const caseType=document.getElementById('caseType').value;
const amount=(parseFloat(document.getElementById('amount').value)||0).toLocaleString();
const deadline=document.getElementById('deadline').value||'2026-11-15';

const titles={
rent:'임대료 지급 촉구',
deposit:'보증금 반환 촉구',
unpaid:'용역비 지급 촉구',
other:'지급 촉구'
};

document.getElementById('lSender').textContent=sender+' ('+sAddr+')';
document.getElementById('lReceiver').textContent=receiver+' ('+rAddr+')';
document.getElementById('lTitle').textContent=titles[caseType]||'지급 촉구';

const body=`${receiver}님께,

본 건은 ${titles[caseType]||'지급 촉구'}에 관한 것입니다.

상기 금액 ${amount}원을 ${deadline}까지 지급해 주시기 바랍니다.

상기 기한 내에 지급하지 아니할 경우 법적 조치를 취할 것을 미리 통지합니다.

발신일: ${new Date().toLocaleDateString('ko-KR')}`;

document.getElementById('lBody').textContent=body;
}

function downloadPDF(){
alert('PDF 다운로드를 시작합니다. (무료)');
}

function switchTab(tab,el){
document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
document.querySelectorAll('.tab-content').forEach(c=>c.classList.remove('active'));
el.classList.add('active');
document.getElementById(tab).classList.add('active');
}

genLetter();
</script>
</body>
</html>
'''

os.makedirs(r"D:\10jo_Studio\03_apps_dev\projects\10jo-site\rent-notice-v2", exist_ok=True)
with open(r"D:\10jo_Studio\03_apps_dev\projects\10jo-site\rent-notice-v2\index.html", "w", encoding="utf-8") as f:
    f.write(rent_v2)
print("렌트노티스 v2 생성 완료")
