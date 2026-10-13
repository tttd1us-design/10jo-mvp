// 10조 스튜디오 — Cloudflare Workers AI 프록시
// 추가비용 0원: 무료 플랜 (일일 10,000 Neurons)
// 카드 등록 불필요

export default {
  async fetch(request, env) {
    // CORS 헤더
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    if (request.method !== 'POST') {
      return new Response(JSON.stringify({ error: 'POST only' }), {
        status: 405,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    try {
      const body = await request.json();
      const { messages, model = '@cf/meta/llama-3.1-8b-instruct', temperature = 0.7, max_tokens = 1024 } = body;

      if (!messages || !Array.isArray(messages)) {
        return new Response(JSON.stringify({ error: 'messages required' }), {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      // Workers AI 호출
      const response = await env.AI.run(model, {
        messages,
        temperature,
        max_tokens
      });

      return new Response(JSON.stringify({
        text: response.response,
        model: model,
        source: 'cloudflare-workers-ai',
        provider: 'cloudflare'
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });

    } catch (e) {
      return new Response(JSON.stringify({ error: e.message }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }
  }
};
