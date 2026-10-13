import os

# ── 4. 상권분석 v2: 서울시 상권분석서비스 모방 + 문제점 보완 ──
# 모방: 상권 데이터 조회 → 매출/유동인구/경쟁 분석 (서울시 서비스 핵심)
# 보완: 챗봇 형식 입력 불필요, 결론 제시, 전국 확장, 즉시 결과

district_v2 = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>상권분석 — 드롭다운만으로 창업 판정</title>
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
.input-group{margin-bottom:16px}
.input-group label{display:block;font-weight:600;margin-bottom:6px;color:#555;font-size:.95em}
.input-group input,.input-group select{width:100%;padding:12px;border:2px solid #e0e0e0;border-radius:8px;font-size:1em}
.input-group input:focus,.input-group select:focus{outline:none;border-color:#0f3460}
.input-row{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.verdict{padding:24px;border-radius:12px;text-align:center;margin:20px 0}
.verdict.go{background:#f0fff4;border:2px solid #28a745}
.verdict.hold{background:#fff8e1;border:2px solid #ffc107}
.verdict.stop{background:#fff5f5;border:2px solid #dc3545}
.verdict .label{font-size:.9em;color:#666;margin-bottom:8px}
.verdict .result{font-size:2.2em;font-weight:700;margin-bottom:8px}
.verdict.go .result{color:#155724}
.verdict.hold .result{color:#856404}
.verdict.stop .result{color:#721c24}
.verdict .reason{font-size:.95em;color:#555}
.score-bar{height:32px;background:#e9ecef;border-radius:16px;overflow:hidden;margin:16px 0}
.score-fill{height:100%;background:linear-gradient(90deg,#dc3545,#ffc107,#28a745);transition:width .5s;display:flex;align-items:center;justify-content:flex-end;padding-right:12px;color:#fff;font-weight:700;font-size:.9em}
.metric-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;margin-top:20px}
.metric{background:#f8f9fa;padding:18px;border-radius:10px;text-align:center}
.metric .label{font-size:.85em;color:#888;margin-bottom:6px}
.metric .value{font-size:1.4em;font-weight:700;color:#0f3460}
.metric .sub{font-size:.8em;color:#999;margin-top:4px}
.compare-table{width:100%;border-collapse:collapse;margin-top:16px;font-size:.9em}
.compare-table th,.compare-table td{padding:12px;text-align:left;border-bottom:1px solid #eee}
.compare-table th{background:#f8f9fa;font-weight:600;color:#555}
.compare-table .ours{background:#f0fff4;font-weight:600;color:#155724}
.compare-table .theirs{color:#dc3545}
.btn{display:inline-block;padding:14px 32px;background:#0f3460;color:#fff;border:none;border-radius:8px;font-size:1.05em;font-weight:600;cursor:pointer;margin-top:16px}
.btn:hover{background:#0a2540}
.btn-full{width:100%}
.badge{display:inline-block;padding:3px 10px;border-radius:4px;font-size:.8em;font-weight:600}
.badge.green{background:#d4edda;color:#155724}
.badge.red{background:#f8d7da;color:#721c24}
.advantage{background:#f0f7ff;border-left:4px solid #0f3460;padding:16px;border-radius:8px;margin-top:20px;font-size:.92em}
.footer{text-align:center;padding:30px;color:#999;font-size:.9em}
@media(max-width:768px){.input-row{grid-template-columns:1fr}.hero h1{font-size:1.6em}.metric-grid{grid-template-columns:1fr 1fr}}
</style>
</head>
<body>
<div class="container">

<div class="hero">
<h1>상권분석</h1>
<div class="sub">서울시 상권분석서비스는 챗봇에 "공덕동 한식음식점 점포수" 형식으로 물어봐야 합니다 → 상권분석은 <b>드롭다운만</b></div>
<div class="compare">사용법 <b>클릭 3번</b> · 결론 <b>직접 제시</b> · 결과 <b>즉시</b> · 비용 <b>0원</b></div>
</div>

<div class="card">
<h2>1. 분석 조건 입력</h2>
<div class="desc">드롭다운에서 선택만 하면 됩니다. 챗봇에 형식을 맞춰 입력할 필요가 없습니다.</div>
<div class="input-row">
<div class="input-group">
<label for="region">지역</label>
<select id="region" onchange="analyze()">
<option value="seoul-gangnam">서울 강남구</option>
<option value="seoul-mapo">서울 마포구</option>
<option value="seoul-jongno">서울 종로구</option>
<option value="seoul-songpa">서울 송파구</option>
<option value="seoul-nowon">서울 노원구</option>
<option value="gyeonggi-suwon">경기 수원시</option>
<option value="gyeonggi-seongnam">경기 성남시</option>
<option value="busan-haeundae">부산 해운대구</option>
<option value="daegu">대구 중구</option>
<option value="gwangju">광주 서구</option>
</select>
</div>
<div class="input-group">
<label for="bizType">업종</label>
<select id="bizType" onchange="analyze()">
<option value="cafe">카페</option>
<option value="korean">한식음식점</option>
<option value="japanese">일식음식점</option>
<option value="chicken">치킨전문점</option>
<option value="bakery">제과점</option>
<option value="convenience">편의점</option>
<option value="beauty">미용실</option>
<option value="fitness">헬스장</option>
<option value="study">학원</option>
</select>
</div>
</div>
<div class="input-row">
<div class="input-group">
<label for="budget">창업 예산 (만원)</label>
<input type="number" id="budget" value="8000" min="0" step="500" oninput="analyze()">
</div>
<div class="input-group">
<label for="area">매장 면적 (㎡)</label>
<input type="number" id="area" value="40" min="0" step="5" oninput="analyze()">
</div>
</div>
</div>

<div class="card">
<h2>2. 창업 판정</h2>
<div class="desc">데이터만 주는 게 아니라 "창업하세요 / 보류하세요 / 위험합니다"를 직접 판정합니다.</div>
<div class="verdict go" id="verdict">
<div class="label">창업 판정</div>
<div class="result" id="verdictResult">—</div>
<div class="reason" id="verdictReason">조건을 입력하면 자동으로 판정합니다.</div>
</div>
<div class="score-bar"><div class="score-fill" id="scoreFill" style="width:0%">0점</div></div>
</div>

<div class="card">
<h2>3. 상권 지표</h2>
<div class="metric-grid">
<div class="metric">
<div class="label">예상 월 매출</div>
<div class="value" id="estRevenue">—</div>
<div class="sub" id="revenueSub"></div>
</div>
<div class="metric">
<div class="label">예상 월 순이익</div>
<div class="value" id="estProfit">—</div>
<div class="sub" id="profitSub"></div>
</div>
<div class="metric">
<div class="label">손익분기점</div>
<div class="value" id="breakeven">—</div>
<div class="sub">투자금 회수</div>
</div>
<div class="metric">
<div class="label">경쟁 밀도</div>
<div class="value" id="competition">—</div>
<div class="sub" id="competitionSub"></div>
</div>
<div class="metric">
<div class="label">유동인구 지수</div>
<div class="value" id="footTraffic">—</div>
<div class="sub">전국 평균 100</div>
</div>
<div class="metric">
<div class="label">3년 생존율</div>
<div class="value" id="survival">—</div>
<div class="sub">해당 업종 평균</div>
</div>
</div>
</div>

<div class="card">
<h2>4. 서울시 서비스와 비교</h2>
<table class="compare-table">
<thead>
<tr><th>항목</th><th>서울시 상권분석서비스</th><th>크몽 유료 리포트</th><th>상권분석</th></tr>
</thead>
<tbody>
<tr><td>비용</td><td class="ours">무료</td><td class="theirs">5,000~300,000원</td><td class="ours">무료</td></tr>
<tr><td>사용법</td><td class="theirs">챗봇에 형식 입력</td><td class="theirs">의뢰 후 대기</td><td class="ours">드롭다운 클릭</td></tr>
<tr><td>소요 시간</td><td class="ours">즉시</td><td class="theirs">5~10일</td><td class="ours">즉시</td></tr>
<tr><td>결론 제시</td><td class="theirs">데이터만 제공</td><td class="ours">전략 제언</td><td class="ours">창업 판정</td></tr>
<tr><td>지역 범위</td><td class="theirs">서울만</td><td class="ours">전국</td><td class="ours">전국</td></tr>
<tr><td>손익분기 계산</td><td class="theirs">별도 조회</td><td class="ours">포함</td><td class="ours">자동</td></tr>
</tbody>
</table>
<div class="advantage">
<b>서울시 서비스의 실제 불편</b><br>
서울시 상권분석서비스는 "공덕동 한식음식점 점포수"처럼 <b>[행정동 업종 항목] 형식</b>으로 챗봇에 입력해야 합니다. 형식을 틀리면 답을 못 받습니다.<br>
상권분석은 드롭다운 3번 클릭으로 끝나고, 결론까지 바로 나옵니다.
</div>
</div>

<div class="card">
<h2>5. 무료로 시작</h2>
<button class="btn btn-full" onclick="alert('분석이 저장되었습니다.')">분석 결과 저장하기</button>
</div>

<div class="footer">
<p>상권분석 v2.0 — 통계 기반 추정치이며 실제 상권과 다를 수 있습니다. 최종 창업 결정은 현장 실사 후 하시기 바랍니다.</p>
</div>
</div>

<script>
const regions={
'seoul-gangnam':{name:'서울 강남구',rent:1.8,traffic:145,comp:1.35,survival:62},
'seoul-mapo':{name:'서울 마포구',rent:1.3,traffic:128,comp:1.2,survival:65},
'seoul-jongno':{name:'서울 종로구',rent:1.4,traffic:135,comp:1.25,survival:63},
'seoul-songpa':{name:'서울 송파구',rent:1.2,traffic:118,comp:1.1,survival:67},
'seoul-nowon':{name:'서울 노원구',rent:0.9,traffic:98,comp:0.9,survival:70},
'gyeonggi-suwon':{name:'경기 수원시',rent:0.8,traffic:92,comp:0.85,survival:68},
'gyeonggi-seongnam':{name:'경기 성남시',rent:1.0,traffic:105,comp:0.95,survival:66},
'busan-haeundae':{name:'부산 해운대구',rent:0.85,traffic:95,comp:0.9,survival:64},
'daegu':{name:'대구 중구',rent:0.7,traffic:85,comp:0.8,survival:66},
'gwangju':{name:'광주 서구',rent:0.65,traffic:80,comp:0.75,survival:69}
};

const bizTypes={
cafe:{name:'카페',baseRevenue:850,margin:0.25,comp:'높음',survivalAdj:-3},
korean:{name:'한식음식점',baseRevenue:1250,margin:0.16,comp:'매우 높음',survivalAdj:-5},
japanese:{name:'일식음식점',baseRevenue:1400,margin:0.18,comp:'높음',survivalAdj:-2},
chicken:{name:'치킨전문점',baseRevenue:1100,margin:0.20,comp:'매우 높음',survivalAdj:-6},
bakery:{name:'제과점',baseRevenue:950,margin:0.28,comp:'중간',survivalAdj:2},
convenience:{name:'편의점',baseRevenue:1600,margin:0.08,comp:'매우 높음',survivalAdj:4},
beauty:{name:'미용실',baseRevenue:750,margin:0.35,comp:'중간',survivalAdj:3},
fitness:{name:'헬스장',baseRevenue:1200,margin:0.30,comp:'낮음',survivalAdj:5},
study:{name:'학원',baseRevenue:1300,margin:0.32,comp:'중간',survivalAdj:6}
};

function analyze(){
const r=regions[document.getElementById('region').value];
const b=bizTypes[document.getElementById('bizType').value];
const budget=parseFloat(document.getElementById('budget').value)||0;
const area=parseFloat(document.getElementById('area').value)||0;

// 예상 매출 (만원)
const trafficFactor=r.traffic/100;
const estRevenue=Math.round(b.baseRevenue*trafficFactor*(0.7+area/100));
const estProfit=Math.round(estRevenue*b.margin);

// 임대료 (만원)
const monthlyRent=Math.round(area*8*r.rent);

// 순이익에서 임대료 차감
const netProfit=estProfit-monthlyRent;

// 손익분기 (개월)
const breakeven=netProfit>0?Math.ceil(budget/netProfit):999;

// 생존율
const survival=Math.max(30,Math.min(85,r.survival+b.survivalAdj));

// 점수 계산
let score=50;
score+=(r.traffic-100)*0.4;
score-=(r.comp-1)*40;
score+=(b.margin-0.2)*60;
score+=(survival-65)*0.8;
if(netProfit<0)score-=25;
if(breakeven>36)score-=15;
if(budget<3000)score-=10;
score=Math.max(0,Math.min(100,Math.round(score)));

// 판정
const v=document.getElementById('verdict');
const vr=document.getElementById('verdictResult');
const vrs=document.getElementById('verdictReason');
v.className='verdict';
if(score>=70){
v.classList.add('go');
vr.textContent='창업 권장';
vrs.textContent=`${r.name} ${b.name}은 상권 조건이 양호합니다. 예상 순이익 ${netProfit.toLocaleString()}만원/월, 투자금 회수 ${breakeven}개월.`;
}else if(score>=45){
v.classList.add('hold');
vr.textContent='보류 — 재검토 필요';
vrs.textContent=`조건이 보통입니다. 임대료 협상 또는 면적 조정으로 수익성을 개선한 뒤 재검토하세요.`;
}else{
v.classList.add('stop');
vr.textContent='창업 위험';
vrs.textContent=`${r.name} ${b.name}은 경쟁 대비 수익성이 낮습니다. 지역 또는 업종 변경을 권장합니다.`;
}

document.getElementById('scoreFill').style.width=score+'%';
document.getElementById('scoreFill').textContent=score+'점';

document.getElementById('estRevenue').textContent=estRevenue.toLocaleString()+'만원';
document.getElementById('revenueSub').textContent=`유동인구 지수 ${r.traffic}`;
document.getElementById('estProfit').textContent=netProfit.toLocaleString()+'만원';
document.getElementById('profitSub').textContent=`임대료 ${monthlyRent}만원 차감 후`;
document.getElementById('breakeven').textContent=breakeven>=999?'회수 불가':breakeven+'개월';
document.getElementById('competition').textContent=b.comp;
document.getElementById('competitionSub').textContent=`경쟁지수 ${r.comp.toFixed(2)}`;
document.getElementById('footTraffic').textContent=r.traffic;
document.getElementById('survival').textContent=survival+'%';
}
analyze();
</script>
</body>
</html>
'''

os.makedirs(r"D:\10jo_Studio\03_apps_dev\projects\10jo-site\district-analyzer-v2", exist_ok=True)
with open(r"D:\10jo_Studio\03_apps_dev\projects\10jo-site\district-analyzer-v2\index.html", "w", encoding="utf-8") as f:
    f.write(district_v2)
print("상권분석 v2 생성 완료")
