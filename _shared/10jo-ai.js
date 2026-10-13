// 10조 스튜디오 — NVIDIA NIM 공통 AI 클라이언트
// 추가비용 0원: 무료 크레딧 1,000 (최대 5,000), 카드 등록 불필요
// 검증 완료: 2026-10-14, 모델 meta/llama-3.2-11b-vision-instruct
//
// 사용법:
//   <script src="../_shared/10jo-ai.js"></script>
//   <script>10joAI.attach({ section: '세무', placeholder: '...' });</script>

(function () {
  'use strict';

  const NIM_URL = 'https://integrate.api.nvidia.com/v1/chat/completions';
  const NIM_MODEL = 'meta/llama-3.2-11b-vision-instruct';
  const KEY_STORAGE = 'nim_api_key';

  function getKey() {
    try { return localStorage.getItem(KEY_STORAGE) || ''; } catch (e) { return ''; }
  }

  function setKey(key) {
    try {
      if (key) localStorage.setItem(KEY_STORAGE, key);
      else localStorage.removeItem(KEY_STORAGE);
    } catch (e) { /* localStorage 차단 환경 무시 */ }
  }

  // NIM API 호출
  async function ask(question, systemPrompt) {
    const key = getKey();
    if (!key) return { ok: false, reason: 'no-key' };

    try {
      const resp = await fetch(NIM_URL, {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + key,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: NIM_MODEL,
          messages: [
            { role: 'system', content: systemPrompt || '당신은 한국 실무 전문가입니다. 정확하고 실용적으로 답변하세요.' },
            { role: 'user', content: question }
          ],
          temperature: 0.3,
          max_tokens: 1024
        })
      });

      if (!resp.ok) {
        const err = await resp.json().catch(function () { return {}; });
        return { ok: false, reason: 'http-' + resp.status, detail: err };
      }

      const data = await resp.json();
      return {
        ok: true,
        text: (data.choices && data.choices[0] && data.choices[0].message.content) || '응답을 받지 못했습니다.',
        model: data.model || NIM_MODEL
      };
    } catch (e) {
      return { ok: false, reason: 'network', detail: e.message };
    }
  }

  // UI 자동 부착 — 기존 페이지에 AI 상담 섹션을 삽입
  function attach(opts) {
    opts = opts || {};
    const mountId = opts.mount || 'ai-consult-mount';
    const mount = document.getElementById(mountId);
    if (!mount) return false;

    const title = opts.title || 'AI 상담';
    const placeholder = opts.placeholder || '궁금한 점을 입력하세요';
    const systemPrompt = opts.system || '당신은 한국 실무 전문가입니다. 정확하고 실용적으로 답변하세요.';
    const localFn = opts.localAnswer || function () { return '구체적인 정보를 입력해 주세요.'; };

    mount.innerHTML =
      '<div class="card">' +
      '<h2>' + title + ' <span class="badge green">NEW</span></h2>' +
      '<div class="desc">NVIDIA NIM API 기반 AI 상담. API 키 없이도 기본 상담이 가능합니다.</div>' +
      '<div class="input-group">' +
      '<label for="10joNimKey">NVIDIA NIM API 키 (선택) — 없어도 기본 상담 가능</label>' +
      '<input type="password" id="10joNimKey" placeholder="nvapi-... (build.nvidia.com에서 무료 발급)">' +
      '<div style="font-size:.85em;color:#888;margin-top:4px">키는 브라우저에만 저장되며 서버로 전송되지 않습니다. 무료 1,000 크레딧, 카드 등록 불필요.</div>' +
      '</div>' +
      '<div class="input-group">' +
      '<label for="10joAiQ">질문</label>' +
      '<textarea id="10joAiQ" rows="3" placeholder="' + placeholder + '"></textarea>' +
      '</div>' +
      '<button class="btn" id="10joAiBtn">AI 상담 받기</button>' +
      '<div id="10joAiResult" class="result" style="display:none;margin-top:20px">' +
      '<h3>AI 상담 결과</h3>' +
      '<div id="10joAiAnswer" style="white-space:pre-wrap;line-height:1.8"></div>' +
      '<div id="10joAiSource" style="font-size:.8em;color:#888;margin-top:12px"></div>' +
      '</div>' +
      '</div>';

    const keyInput = document.getElementById('10joNimKey');
    keyInput.value = getKey();
    keyInput.addEventListener('change', function () { setKey(this.value.trim()); });

    document.getElementById('10joAiBtn').addEventListener('click', async function () {
      const q = document.getElementById('10joAiQ').value.trim();
      if (!q) { alert('질문을 입력하세요.'); return; }

      const resultDiv = document.getElementById('10joAiResult');
      const answerDiv = document.getElementById('10joAiAnswer');
      const sourceDiv = document.getElementById('10joAiSource');

      resultDiv.style.display = 'block';
      answerDiv.textContent = 'AI가 답변을 생성 중입니다...';
      sourceDiv.textContent = '';

      const res = await ask(q, systemPrompt);
      if (res.ok) {
        answerDiv.textContent = res.text;
        sourceDiv.textContent = '응답 소스: NVIDIA NIM (무료) · 모델: ' + res.model;
      } else {
        answerDiv.textContent = localFn(q);
        sourceDiv.textContent = res.reason === 'no-key'
          ? '응답 소스: 로컬 규칙 기반 (API 키 없음, 무료)'
          : '응답 소스: 로컬 규칙 기반 (NIM 호출 실패: ' + res.reason + ')';
      }
    });

    return true;
  }

  window['10joAI'] = { ask: ask, attach: attach, getKey: getKey, setKey: setKey, MODEL: NIM_MODEL };
})();
