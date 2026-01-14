# 📊 Diagramas Visuais: Como Funciona Vision no py-xiaozhi

## 1️⃣ Fluxo Completo de Análise de Imagem

```
┌──────────────────────────────────────────────────────────────────────┐
│                    👤 USUÁRIO (via Claude Assistante)               │
│                    "O que você vê na câmera?"                       │
└─────────────────────────────┬──────────────────────────────────────┘
                              │
                              │ Pergunta via MCP Protocol
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│              🖥️ MCP SERVER (py-xiaozhi/main.py)                      │
│  Recebe pergunta do assistente                                       │
└─────────────────────────────┬──────────────────────────────────────┘
                              │
                              │ Executa tool: camera_capture_and_analyze()
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│              📷 CAPTURA DE IMAGEM (OpenCV)                           │
│  cap.read() → Frame RGB                                             │
│  Resolução: 640x480                                                 │
│  Tamanho: ~500KB                                                    │
└─────────────────────────────┬──────────────────────────────────────┘
                              │
                              │ Imagem capturada
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│         🔄 CODIFICAÇÃO BASE64 (base64 module)                        │
│  RGB → JPEG comprimido → Base64 string                              │
│  Tamanho reduzido: ~200KB → 270KB em base64                        │
└─────────────────────────────┬──────────────────────────────────────┘
                              │
                              │ Base64 string
                              │ "iVBORw0KGgoAAAANSUhEUgAA..."
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│     🤖 VISION PROVIDER (vllm_provider.py/ZhipuVisionAPIProvider)    │
│                                                                      │
│  1. Monta headers HTTP com Bearer token                             │
│  2. Cria payload JSON:                                              │
│     {                                                               │
│       "model": "glm-4v-flash",                                     │
│       "messages": [{                                                │
│         "role": "user",                                             │
│         "content": [                                                │
│           {"type": "image_url", "image_url": {...}},               │
│           {"type": "text", "text": "O que há aqui?"}              │
│         ]                                                           │
│       }]                                                            │
│     }                                                               │
│  3. Envia POST request via httpx                                    │
│  4. Retry automático (3 tentativas)                                │
│  5. Timeout: 30 segundos                                            │
└─────────────────────────────┬──────────────────────────────────────┘
                              │
                              │ HTTP POST + Base64
                              │ Latência: 1-3 segundos
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│  🌐 ZHIPU VISION API (glm-4v-flash)                                  │
│  https://open.bigmodel.cn/api/paas/v4/chat/completions             │
│                                                                      │
│  ✨ Processa imagem com modelo de visão                             │
│  ✨ Gera análise em português/inglês                                │
│  ✨ Retorna junto com contagem de tokens                            │
│                                                                      │
│  Latência: 2-5 segundos                                             │
│  Tokens usados: 800-1200                                            │
└─────────────────────────────┬──────────────────────────────────────┘
                              │
                              │ Resposta JSON
                              │ {
                              │   "choices": [{
                              │     "message": {
                              │       "content": "A imagem mostra..."
                              │     }
                              │   }],
                              │   "usage": {...}
                              │ }
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│      📥 PROCESSAMENTO DE RESPOSTA (vllm_provider.py)                │
│  Parse JSON                                                         │
│  Extrai análise: "A imagem mostra uma sala com..."                 │
│  Extrai tokens: 850 tokens gastos                                   │
└─────────────────────────────┬──────────────────────────────────────┘
                              │
                              │ Dict com resultado
                              │ {
                              │   "status": "success",
                              │   "analysis": "A imagem mostra...",
                              │   "tokens": 850
                              │ }
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│          ↩️ MCP SERVER → Claude Assistente                           │
│  Retorna resultado da ferramenta                                    │
└─────────────────────────────┬──────────────────────────────────────┘
                              │
                              │ MCP Protocol
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│          💬 RESPOSTA FINAL (Claude Assistante)                       │
│  "Vejo uma sala com sofá azul, TV na parede, e luz natural..."     │
└──────────────────────────────────────────────────────────────────────┘

⏱️ TEMPO TOTAL: 3-8 segundos
```

---

## 2️⃣ Estrutura de Arquivos Envolvidos

```
py-xiaozhi/
│
├── 🔴 main.py
│   ├── Função: camera_capture_and_analyze()
│   ├── Tool MCP que integra tudo
│   └── Chama VisionProvider
│
├── src/
│   ├── config.py
│   │   └── Carrega VLLM config de config.yaml
│   │
│   └── mcp/
│       └── tools/
│           └── providers/
│               ├── vllm_provider.py 🟢 ARQUIVO PRINCIPAL
│               │   ├── _resolve_env_var()
│               │   ├── ZhipuVisionAPIProvider
│               │   │   └── async def analyze_image()
│               │   ├── VisionProviderFactory
│               │   └── use_vision_api() helper
│               │
│               └── (outros providers)
│
├── config.yaml 🟡 CONFIGURAÇÃO
│   └── VLLM:
│       └── zhipu: {...}
│
└── logs/
    └── vision_*.log 📋 LOGS
```

---

## 3️⃣ Fluxo de Dados (Estrutura de Objetos)

```
PASSO 1: Captura
═══════════════════════════════════════════════════════════
Origem: cap.read() [OpenCV]
Tipo: numpy.ndarray (BGR, 640x480)
Tamanho: ~500KB em memória

  ┌─────────────────────────┐
  │  frame (numpy array)    │
  │  dtype: uint8           │
  │  shape: (480, 640, 3)   │
  │  valor: [[B,G,R], ...] │
  └─────────────────────────┘


PASSO 2: Codificação
═══════════════════════════════════════════════════════════
Origem: base64.b64encode()
Tipo: str (ASCII characters)
Tamanho: ~270KB (base64 expande ~33%)

  ┌──────────────────────────────────────────────┐
  │  "iVBORw0KGgoAAAANSUhEUgAABLAAAAAWCAYAA"  │
  │  "AgICEAAACAAIIAAAAAIfAP//5ZweAMAAQEAAA"  │
  │  ... (muito grande) ...                     │
  └──────────────────────────────────────────────┘


PASSO 3: Request JSON
═══════════════════════════════════════════════════════════
Origem: ZhipuVisionAPIProvider.analyze_image()
Tipo: Dict → JSON string
Tamanho: ~270KB JSON

┌─────────────────────────────────────────────────────────┐
│ {                                                       │
│   "model": "glm-4v-flash",                             │
│   "messages": [                                         │
│     {                                                   │
│       "role": "user",                                  │
│       "content": [                                      │
│         {                                               │
│           "type": "image_url",                         │
│           "image_url": {                               │
│             "url": "data:image/jpeg;base64,iVBO..."   │
│           }                                             │
│         },                                              │
│         {                                               │
│           "type": "text",                              │
│           "text": "O que há nesta imagem?"            │
│         }                                               │
│       ]                                                 │
│     }                                                   │
│   ],                                                    │
│   "max_tokens": 2048,                                  │
│   "temperature": 0.7                                   │
│ }                                                       │
└─────────────────────────────────────────────────────────┘


PASSO 4: Response JSON
═══════════════════════════════════════════════════════════
Origem: Zhipu API
Tipo: Dict
Tamanho: ~2KB (resposta comprimida)

┌────────────────────────────────────────────────────┐
│ {                                                  │
│   "choices": [                                     │
│     {                                              │
│       "message": {                                 │
│         "content": "A imagem mostra uma sala..."  │
│       }                                            │
│     }                                              │
│   ],                                               │
│   "usage": {                                       │
│     "prompt_tokens": 850,                         │
│     "completion_tokens": 120,                     │
│     "total_tokens": 970                           │
│   }                                                │
│ }                                                  │
└────────────────────────────────────────────────────┘


PASSO 5: Resultado Final
═══════════════════════════════════════════════════════════
Origem: ZhipuVisionAPIProvider
Tipo: Dict (Python)
Tamanho: ~2KB

┌──────────────────────────────────────────────────────┐
│ {                                                    │
│   "status": "success",                              │
│   "analysis": "A imagem mostra uma sala com sofá..."│
│   "model": "glm-4v-flash",                          │
│   "tokens": {                                        │
│     "input": 850,                                   │
│     "output": 120,                                  │
│     "total": 970                                    │
│   }                                                  │
│ }                                                    │
└──────────────────────────────────────────────────────┘
```

---

## 4️⃣ Arquitetura de Providers (Factory Pattern)

```
                    VisionProviderFactory
                            │
                            ├─→ PROVIDERS = {
                            │     "zhipu": ZhipuVisionAPIProvider,
                            │     "google": GoogleVisionProvider,  (futuro)
                            │     "openai": OpenAIVisionProvider   (futuro)
                            │   }
                            │
                            └─→ create(provider_type, config)
                                    │
                                    ├─ Se "zhipu"
                                    │   └─→ ZhipuVisionAPIProvider(config)
                                    │       ├─ Zhipu API Key
                                    │       ├─ Model: glm-4v-flash
                                    │       └─ analyze_image()
                                    │
                                    └─ Se outro
                                        └─→ Instancia classe correspondente
```

---

## 5️⃣ Timeline de Execução

```
│ EVENTO                              │ TEMPO    │ DURAÇÃO   │
├─────────────────────────────────────┼──────────┼───────────┤
│ T0: Pergunta enviada ao MCP         │ 00:00s   │           │
│ T1: Captura frame (OpenCV)          │ 00:01s   │ ~10ms     │
│ T2: Codifica em base64              │ 00:02s   │ ~50ms     │
│ T3: Monta request JSON              │ 00:05s   │ ~30ms     │
│ T4: Enviando para Zhipu (network)   │ 00:10s   │ ~100ms    │
│ T5: Processando na API              │ 01:00s   │ ~2-5s     │
│ T6: Recebendo resposta              │ 05:50s   │ ~100ms    │
│ T7: Parse da resposta               │ 06:00s   │ ~50ms     │
│ T8: Retorna ao MCP                  │ 06:10s   │ ~10ms     │
│ T9: Claude formula resposta         │ 07:00s   │ ~500ms    │
│ T10: Resposta exibida ao usuário    │ 08:00s   │           │
│                                     │          │           │
│ TEMPO TOTAL                         │ 08:00s   │ 8 segundos│
└─────────────────────────────────────┴──────────┴───────────┘

Gráfico Visual:
═══════════════════════════════════════════════════════════

00:00 ┌─ Pergunta
      │
01:00 │  ├─ Captura + Codificação
      │  │
05:00 │  │  ├─ Request network
      │  │  │
06:00 │  │  │  ├─────── Zhipu API Processando ───────┐
      │  │  │  │        (tempo de espera)            │
      │  │  │  │                                     │
09:00 │  │  │  └─────────────────────────────────────┤
      │  │  │                         ├─ Response + Parse
10:00 │  │  │                         │
      │  └──────────────────────────────── Resposta retornada
      │
11:00 └─ Resposta ao usuário

Time Investment:
═══════════════════════════════════════════════════════════
  Local (py-xiaozhi):    ~5% (0.4s)   ████
  Network:              ~3% (0.2s)   ██
  Zhipu API:            ~92% (7.4s)  ████████████████████████████████████
```

---

## 6️⃣ Interações com APIs Externas

```
                        py-xiaozhi
                            │
                            │ (Bearer Token + Base64 Image)
                            ▼
                   Zhipu Vision API
                            │
                  Authorization: Bearer {key}
                  POST /api/paas/v4/chat/completions
                            │
                       Headers:
                  ┌─ Content-Type: application/json
                  ├─ Authorization: Bearer XXX
                  └─ User-Agent: Python httpx
                            │
                       Body (JSON):
                  ┌─ model: "glm-4v-flash"
                  ├─ messages[0].content[0].type: "image_url"
                  ├─ messages[0].content[0].image_url.url: "data:image/jpeg;base64,..."
                  ├─ messages[0].content[1].type: "text"
                  ├─ messages[0].content[1].text: "O que há aqui?"
                  ├─ max_tokens: 2048
                  └─ temperature: 0.7
                            │
                            │ (Status 200 OK)
                            ▼
                       Response (JSON):
                  ┌─ choices[0].message.content: "A imagem mostra..."
                  ├─ usage.prompt_tokens: 850
                  ├─ usage.completion_tokens: 120
                  └─ usage.total_tokens: 970
                            │
                            ▼
                        py-xiaozhi
                      (Parse e retorna)
```

---

## 7️⃣ Estados Possíveis e Tratamento de Erros

```
                    Vision API Request
                            │
            ┌───────────────┼───────────────┐
            │               │               │
        ✅ Success      ⚠️ Warning      ❌ Error
            │               │               │
            ▼               ▼               ▼
        Status: 200    Timeout/Retry    4xx (Client)
            │         Rate Limit         Bad Request
        Analysis        Slow             Invalid Image
        + Tokens                         Token Expired
            │               │
            │               ▼
            │           Retry 1/3
            │           (Backoff exp)
            │               │
            │           🔄 Success? ──→ ✅
            │           │
            │           ❌ Falha
            │               │
            │           Retry 2/3
            │               │
            │           🔄 Success? ──→ ✅
            │           │
            │           ❌ Falha
            │               │
            │           Retry 3/3
            │               │
            │           🔄 Success? ──→ ✅
            │           │
            │           ❌ Falha Final
            │               │
            └───────────────┼───────────────┐
                            │
                        Return Error
                        {
                          "status": "error",
                          "error": "Timeout após 3 tentativas"
                        }
```

---

## 8️⃣ Configuração e Variáveis de Ambiente

```
┌──────────────────────────────────────────────────────────┐
│         Arquivo: config.yaml                             │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  VLLM:                                                   │
│    zhipu:                  ← Nome do provider             │
│      type: "zhipu"         ← Tipo                        │
│      api_key: "${ZHIPU_API_KEY}"  ← Variável de env     │
│      model: "glm-4v-flash" ← Modelo                     │
│      api_url: "https://..."← URL da API                 │
│      temperature: 0.7      ← Criatividade                │
│      max_tokens: 2048      ← Limite de resposta         │
│      timeout: 30.0         ← Timeout em segundos        │
│                                                          │
└──────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│    Variáveis de Ambiente (Sistema Operacional)          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ZHIPU_API_KEY=sk-9d9d9d9d9d9d9d9d9d9d9d9d9d9d9d9d9   │
│  export ZHIPU_API_KEY                                    │
│                                                          │
│  Resolvidas em tempo de execução:                        │
│  config.get("api_key")  # "${ZHIPU_API_KEY}"            │
│  _resolve_env_var()     # Verifica os.getenv()          │
│  return env_value       # "sk-9d9d..."                  │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 9️⃣ Performance: Otimizações Possíveis

```
SITUAÇÃO ATUAL
═══════════════════════════════════════════════════════════
Tempo por imagem: 3-8 segundos
  ├─ Captura: ~10ms
  ├─ Base64: ~50ms
  ├─ Network: ~100ms
  └─ API: 2-5s (maior parte)

OTIMIZAÇÕES POSSÍVEIS
═══════════════════════════════════════════════════════════

1️⃣ Cache Redis
   └─ Mesma imagem → resposta em cache (~5ms)
   
2️⃣ Compressão
   └─ Reduzir base64 de 270KB para 150KB
   
3️⃣ Connection Pooling
   └─ Reusar conexão HTTP (economia de ~200ms)
   
4️⃣ Async/Await
   └─ Já implementado! ✅
   
5️⃣ Modelo mais rápido
   └─ glm-4v-flash já é o mais rápido
   
TEMPO OTIMIZADO
═══════════════════════════════════════════════════════════
Com Redis Cache:    ~50ms (5% do tempo original)
Com Compressão:     ~5-6s (20% mais rápido)
Combo Tudo:         ~30-50ms em cache, 2-3s em novo
```

---

**Criado em:** 2024-01-15  
**Formato:** Diagramas ASCII + Fluxogramas  
**Objetivo:** Visualizar o funcionamento completo
