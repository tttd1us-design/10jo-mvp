// 10조 스튜디오 — NVIDIA NIM API 공통 모듈
// 추가비용 없이 적용: API 키 없이도 동작, 키 있으면 NIM 사용
// 무료 1,000 크레딧 소진 시 자동 폴백

class NIMClient {
  constructor(options = {}) {
    this.apiKey = options.apiKey || '';
    this.fallbackMode = options.fallbackMode || 'local';
    this.maxRetries = options.maxRetries || 2;
    this.timeout = options.timeout || 30000;
    this.baseUrl = 'https://integrate.api.nvidia.com/v1';
    
    // 로컬 규칙 기반 응답 데이터베이스
    this.localKnowledge = {
      '부가세': {
        title: '부가가치세 환급 안내',
        content: `### 부가가치세 환급 절차\n\n1. **환급 대상**: 인터넇 쇼핑몰·게임·앱·정보서비스 등 전자상거래·도서·음악·영상 등\n\n2. **환급 신청 기한**: 품목·서비스 개요 등을 확인한 날로부터 3개월\n\n3. **환급 신청 방법**: 홈택스 '부가가치세 환급' → 전자신고 → 확정통지서 발급\n\n4. **환급율**: 국내기업·국가기관 10~20%, 외국기업 0~10%\n\n5. **유의사항**: 매출액 120억 원 이하 사업장 우선, 부정 수임 시 환급 철회 가능`,
        exampleQuery: true
      }
    };
  }

  async chat(options) {
    const { messages, model, temperature = 0.7, maxTokens = 1024 } = options;
    const userMsg = messages.find(m => m.role === 'user')?.content || '';

    // 1. API 키가 있으면 NIM 시도
    if (this.apiKey) {
      try {
        const result = await this._callNIMAPI(messages, model, temperature, maxTokens);
        return { ...result, source: 'nim', provider: 'nvidia' };
      } catch (e) {
        console.warn('NIM API 실패, 폴백:', e.message);
      }
    }

    // 2. 키 없거나 NIM 실패 시 로컬 폴백
    const localResult = this._localFallback(userMsg);
    if (localResult) {
      return {
        text: localResult.content,
        usage: { promptTokens: 0, completionTokens: 0, totalTokens: 0 },
        source: 'local',
        provider: '10jo-rule-based',
        model: 'local-rules'
      };
    }

    // 3. 모의 응답
    return {
      text: 'AI 분석이 필요합니다. 서비스 준비 중입니다.',
      usage: { promptTokens: 0, completionTokens: 0, totalTokens: 0 },
      source: 'mock',
      provider: 'placeholder',
      model: 'mock'
    };
  }

  async _callNIMAPI(messages, model, temperature, maxTokens) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch('https://integrate.api.nvidia.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: model || 'meta/llama-3.3-70b-instruct',
          messages,
          temperature,
          max_tokens: maxTokens
        }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(`HTTP ${response.status}: ${err.error?.message || response.statusText}`);
      }

      const data = await response.json();
      const choice = data.choices?.[0]?.message?.content || '';
      
      return {
        text: choice,
        usage: data.usage || { prompt_tokens: 0, completion_tokens: 0, total_tokens: 0 },
        model: data.model || model
      };
    } catch (e) {
      clearTimeout(timeoutId);
      throw e;
    }
  }

  _localFallback(userMsg) {
    const lowerMsg = userMsg.toLowerCase();
    
    for (const [key, data] of Object.entries(this.localKnowledge)) {
      if (lowerMsg.includes(key)) {
        return { content: data.content, title: data.title };
      }
    }
    
    return null;
  }
}