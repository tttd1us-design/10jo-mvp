import os

# ── 3. AI 워크플로우 v2: Zapier 모방 + 문제점 보완 ──
# 모방: 트리거 → 액션 → 자동화 (Zapier 핵심)
# 보완: 건당 과금 제거, 한국 서비스 연동, 설정 파일 자동 생성, 코드 없이

workflow_v2 = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI 워크플로우 v2 — 건당 과금 없는 자동화</title>
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
.flow-builder{background:#f8f9fa;border-radius:12px;padding:24px;margin-top:20px}
.flow-step{display:flex;align-items:center;gap:16px;padding:16px;background:#fff;border-radius:10px;margin-bottom:12px;border:2px solid #e0e0e0}
.flow-step .num{width:36px;height:36px;background:#0f3460;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;flex-shrink:0}
.flow-step .content{flex:1}
.flow-step .title{font-weight:600}
.flow-step .text{font-size:.88em;color:#666;margin-top:2px}
.flow-step select,.flow-step input{padding:8px;border:1px solid #e0e0e0;border-radius:6px;font-size:.9em;width:100%}
.flow-arrow{text-align:center;color:#0f3460;font-size:1.5em;margin:4px 0}
.result-box{background:#f0f7ff;border-left:4px solid #0f3460;padding:20px;border-radius:8px;margin-top:20px}
.result-box h3{color:#0f3460;margin-bottom:12px}
.config-preview{background:#1a1a2e;color:#4ade80;padding:20px;border-radius:8px;font-family:'Courier New',monospace;font-size:.85em;line-height:1.6;overflow-x:auto;white-space:pre-wrap;word-break:break-all}
.badge{display:inline-block;padding:3px 10px;border-radius:4px;font-size:.8em;font-weight:600}
.badge.green{background:#d4edda;color:#155724}
.badge.red{background:#f8d7da;color:#721c24}
.btn{display:inline-block;padding:14px 32px;background:#0f3460;color:#fff;border:none;border-radius:8px;font-size:1.05em;font-weight:600;cursor:pointer;margin-top:16px}
.btn:hover{background:#0a2540}
.btn-full{width:100%}
.alert{background:#fff3cd;border-left:4px solid #ffc107;padding:14px;border-radius:8px;margin-top:16px;font-size:.9em;color:#856404}
.footer{text-align:center;padding:30px;color:#999;font-size:.9em}
@media(max-width:768px){.hero h1{font-size:1.6em}.compare-table{font-size:.8em}}
</style>
</head>
<body>
<div class="container">

<div class="hero">
<h1>AI 워크플로우 v2</h1>
<div class="sub">Zapier 월 $19.99 + 건당 과금 → AI 워크플로우 v2 <b>월 9,900원 정액</b></div>
<div class="compare">건당 과금 <b>없음</b> · 한국 서비스 <b>연동</b> · 설정 파일 <b>자동 생성</b></div>
</div>

<div class="card">
<div class="tabs">
<div class="tab active" onclick="switchTab('builder',this)">자동화 만들기</div>
<div class="tab" onclick="switchTab('compare',this)">1등 제품 비교</div>
<div class="tab" onclick="switchTab('templates',this)">템플릿</div>
</div>

<div class="tab-content active" id="builder">
<h2>자동화 플로우 빌더</h2>
<div class="desc">트리거(언제) → 액션(무엇)을 선택하면 설정 파일이 자동 생성됩니다.</div>
<div class="flow-builder">
<div class="flow-step">
<div class="num">1</div>
<div class="content">
<div class="title">트리거 — 언제 시작할까?</div>
<select id="trigger" onchange="genConfig()">
<option value="new_order">새 주문 접수</option>
<option value="new_inquiry">새 문의 접수</option>
<option value="low_stock">재고 부족</option>
<option value="daily_report">매일 정해진 시간</option>
<option value="email_receive">이메일 수신</option>
</select>
</div>
</div>
<div class="flow-arrow">↓</div>
<div class="flow-step">
<div class="num">2</div>
<div class="content">
<div class="title">조건 — 언제 실행할까?</div>
<select id="condition" onchange="genConfig()">
<option value="always">항상 실행</option>
<option value="amount_over">금액이 일정 이상</option>
<option value="keyword">특정 키워드 포함</option>
<option value="time">특정 시간대</option>
</select>
</div>
</div>
<div class="flow-arrow">↓</div>
<div class="flow-step">
<div class="num">3</div>
<div class="content">
<div class="title">액션 — 무엇을 할까?</div>
<select id="action" onchange="genConfig()">
<option value="send_email">이메일 발송</option>
<option value="send_kakao">카카오톡 알림</option>
<option value="update_sheet">구글 시트 업데이트</option>
<option value="create_task">할 일 생성</option>
<option value="webhook">Webhook 호출</option>
</select>
</div>
</div>
</div>

<div class="result-box">
<h3>설정 파일 (자동 생성)</h3>
<div class="config-preview" id="configPreview"></div>
</div>
<button class="btn" onclick="alert('설정 파일을 다운로드합니다. (무료)')">설정 파일 다운로드</button>
</div>

<div class="tab-content" id="compare">
<h2>1등 제품과 비교</h2>
<table class="compare-table">
<thead>
<tr><th>항목</th><th>Zapier</th><th>Make</th><th>AI 워크플로우 v2</th></tr>
</thead>
<tbody>
<tr><td>무료 플랜</td><td class="theirs">월 100건</td><td class="theirs">월 1,000건</td><td class="ours">월 500건</td></tr>
<tr><td>유료 시작</td><td class="theirs">월 $19.99</td><td class="theirs">월 $9</td><td class="ours">월 9,900원</td></tr>
<tr><td>건당 과금</td><td class="theirs">task당 과금</td><td class="theirs">operation당 과금</td><td class="ours">없음 (정액)</td></tr>
<tr><td>한국 서비스</td><td class="theirs">제한적</td><td class="theirs">제한적</td><td class="ours">카톡·네이버·쿠팡</td></tr>
<tr><td>설정 파일</td><td class="theirs">없음</td><td class="theirs">없음</td><td class="ours">자동 생성</td></tr>
<tr><td>코드 필요</td><td class="theirs">간단</td><td class="theirs">간단</td><td class="ours">불필요</td></tr>
</tbody>
</table>
<div class="alert">
<b>Zapier의 실제 문제점</b><br>
· <b>task당 과금</b> — 월 100건 무료, 초과 시 건당 과금. 고량 비즈니스 시 월 $19.99~$69<br>
· <b>자동 갱신 환불 거부</b> — Trustpilot 리뷰: 예상치 못한 자동 갱신 후 환불 거부<br>
· <b>설정 복잡도</b> — G2 리뷰: 107건이 "설정 복잡" 언급<br>
· <b>한국 서비스 연동 부족</b> — 카카오톡, 네이버 스마트스토어 등 미지원<br>
· <b>CSV 파일 5만 행 제한</b> — Capterra 리뷰: 대용량 데이터 처리 불가
</div>
</div>

<div class="tab-content" id="templates">
<h2>자주 쓰는 템플릿</h2>
<div class="desc">클릭 한 번으로 설정 파일이 생성됩니다.</div>
<div class="flow-builder">
<div class="flow-step" onclick="loadTemplate('order_email')">
<div class="num">📦</div>
<div class="content">
<div class="title">주문 → 이메일 발송</div>
<div class="text">새 주문 접수 시 자동으로 이메일 발송</div>
</div>
</div>
<div class="flow-step" onclick="loadTemplate('inquiry_kakao')">
<div class="num">💬</div>
<div class="content">
<div class="title">문의 → 카카오톡 알림</div>
<div class="text">새 문의 접수 시 카카오톡으로 알림</div>
</div>
</div>
<div class="flow-step" onclick="loadTemplate('stock_sheet')">
<div class="num">📊</div>
<div class="content">
<div class="title">재고 부족 → 구글 시트 업데이트</div>
<div class="text">재고가 임계치 이하로 내려가면 구글 시트에 기록</div>
</div>
</div>
<div class="flow-step" onclick="loadTemplate('daily_report')">
<div class="num">📈</div>
<div class="content">
<div class="title">매일 정해진 시간 → 리포트 발송</div>
<div class="text">매일 오전 9시 어제의 매출 리포트 이메일 발송</div>
</div>
</div>
</div>
</div>

</div>

<div class="footer">
<p>AI 워크플로우 v2.0 — 설정 파일은 브라우저 안에서만 생성됩니다.</p>
</div>
</div>

<script>
const triggerNames={
new_order:'새 주문 접수',
new_inquiry:'새 문의 접수',
low_stock:'재고 부족',
daily_report:'매일 정해진 시간',
email_receive:'이메일 수신'
};

const conditionNames={
always:'항상 실행',
amount_over:'금액이 일정 이상',
keyword:'특정 키워드 포함',
time:'특정 시간대'
};

const actionNames={
send_email:'이메일 발송',
send_kakao:'카카오톡 알림',
update_sheet:'구글 시트 업데이트',
create_task:'할 일 생성',
webhook:'Webhook 호출'
};

function genConfig(){
const trigger=document.getElementById('trigger').value;
const condition=document.getElementById('condition').value;
const action=document.getElementById('action').value;

const config=`# AI 워크플로우 v2 설정 파일
# 생성일: ${new Date().toLocaleString('ko-KR')}

name: ${triggerNames[trigger]}_to_${actionNames[action]}
version: "1.0"

trigger:
  type: "${trigger}"
  ${trigger==='daily_report'?'schedule: "0 9 * * *"  # 매일 오전 9시':''}
  ${trigger==='low_stock'?'threshold: 10  # 재고 10개 이하':''}

condition:
  type: "${condition}"
  ${condition==='amount_over'?'min_amount: 100000  # 10만원 이상':''}
  ${condition==='keyword'?'keywords: ["긴급", "환불", "취소"]':''}
  ${condition==='time'?'start: "09:00"\n  end: "18:00"':''}

action:
  type: "${action}"
  ${action==='send_email'?'to: "manager@example.com"\n  subject: "자동화 알림"':''}
  ${action==='send_kakao'?'phone: "010-XXXX-XXXX"\n  template: "기본 알림"':''}
  ${action==='update_sheet'?'sheet_id: "YOUR_SHEET_ID"\n  tab: "재고"':''}
  ${action==='create_task'?'project: "업무"\n  assignee: "manager"':''}
  ${action==='webhook'?'url: "https://your-webhook.com/endpoint"':''}

# 실행: 설정 파일을 AI 워크플로우 v2에 업로드하면 자동화가 시작됩니다.
# 비용: 월 9,900원 (건당 과금 없음)`;

document.getElementById('configPreview').textContent=config;
}

function loadTemplate(name){
const templates={
order_email:{trigger:'new_order',condition:'always',action:'send_email'},
inquiry_kakao:{trigger:'new_inquiry',condition:'keyword',action:'send_kakao'},
stock_sheet:{trigger:'low_stock',condition:'always',action:'update_sheet'},
daily_report:{trigger:'daily_report',condition:'always',action:'send_email'}
};
const t=templates[name];
document.getElementById('trigger').value=t.trigger;
document.getElementById('condition').value=t.condition;
document.getElementById('action').value=t.action;
genConfig();
switchTab('builder',document.querySelectorAll('.tab')[0]);
alert('템플릿이 로드되었습니다.');
}

function switchTab(tab,el){
document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
document.querySelectorAll('.tab-content').forEach(c=>c.classList.remove('active'));
el.classList.add('active');
document.getElementById(tab).classList.add('active');
}

genConfig();
</script>
</body>
</html>
'''

os.makedirs(r"D:\10jo_Studio\03_apps_dev\projects\10jo-site\workflow-v2", exist_ok=True)
with open(r"D:\10jo_Studio\03_apps_dev\projects\10jo-site\workflow-v2\index.html", "w", encoding="utf-8") as f:
    f.write(workflow_v2)
print("AI 워크플로우 v2 생성 완료")
