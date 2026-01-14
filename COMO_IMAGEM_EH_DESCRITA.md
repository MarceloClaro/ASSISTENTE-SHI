# 📸 Como o py-xiaozhi Descreve Imagens

## Resumo Executivo

O repositório **py-xiaozhi** implementa uma solução completa de **Vision API** para descrever imagens usando modelos de visão do **Zhipu (GLM-4V)** e outros compatíveis com OpenAI. O sistema integra:

- **Captura de câmera** via OpenCV
- **Codificação base64** de imagens
- **API de visão** (Zhipu GLM-4V, Google Gemini, etc.)
- **Processamento assíncrono** com httpx
- **Integração MCP** para uso automático em ferramentas

---

## 🏗️ Arquitetura de Visão

```
┌─────────────────────────────────────────────────────────────┐
│                    Captura de Imagem                        │
│  (Camera / Arquivo / Base64 Fornecido)                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│         Validação & Codificação Base64                      │
│  (src/mcp/tools/providers/vllm_provider.py)               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│    ZhipuVisionAPIProvider.analyze_image()                   │
│  - Monta headers HTTP (Bearer token)                        │
│  - Cria payload com imagem + pergunta                       │
│  - Configura temperatura e max_tokens                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│        Zhipu Vision API / Google Gemini / Autre             │
│  (https://open.bigmodel.cn/api/paas/v4/chat/completions)  │
│  (https://generativelanguage.googleapis.com/...)           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Análise & Resposta em Texto                    │
│  (Descrição detalhada da imagem em Português/Inglês)      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Arquivos Principais

### 1. **Vision Provider Principal**
**Arquivo:** [src/mcp/tools/providers/vllm_provider.py](src/mcp/tools/providers/vllm_provider.py)

#### Classe: `ZhipuVisionAPIProvider`
```python
class ZhipuVisionAPIProvider:
    """Provider para análise de imagens usando Zhipu Vision API (GLM-4V)"""
    
    async def analyze_image(
        image_base64: str,      # Imagem em base64
        question: str,          # Pergunta sobre a imagem
        context: Optional[str]  # Contexto adicional
    ) -> Dict[str, Any]:
        # Retorna análise da imagem em texto
```

**Funcionalidades:**
- ✅ Suporta múltiplas APIs (Zhipu, Google Gemini, OpenAI-compatible)
- ✅ Codificação automática base64
- ✅ Resolução de variáveis de ambiente (`${API_KEY}`)
- ✅ Timeout configurável (padrão 30s)
- ✅ Retry automático com backoff exponencial
- ✅ Logging detalhado

### 2. **Factory de Providers**
```python
class VisionProviderFactory:
    """Factory para criar providers de Vision baseado no tipo"""
    
    PROVIDERS = {
        "zhipu": ZhipuVisionAPIProvider,
        # Pode ser estendido com outros providers
    }
    
    @staticmethod
    def create(provider_type: str, config: Dict) -> VLLMProviderBase:
        return VisionProviderFactory.PROVIDERS[provider_type](config)
```

---

## ⚙️ Configuração

### `config.yaml` (Seção VLLM)

```yaml
VLLM:
  zhipu:
    type: "zhipu"
    api_key: "${ZHIPU_API_KEY}"  # Variável de ambiente
    model: "glm-4v-flash"         # Modelo de visão
    api_url: "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    temperature: 0.7              # Criatividade (0-1)
    max_tokens: 2048              # Tamanho máximo resposta
    timeout: 30.0                 # Timeout em segundos
```

**Variáveis Suportadas:**
- `${ZHIPU_API_KEY}` - Token Zhipu
- `${GOOGLE_API_KEY}` - Token Google Gemini
- `${OPENAI_API_KEY}` - Token OpenAI (se usar OpenAI)

---

## 🔄 Fluxo Completo de Uso

### Opção 1: Via MCP Tool (Automático)

Quando o assistente quer descrever uma imagem:

```python
# MCP automaticamente:
1. Captura/obtém imagem
2. Converte para base64
3. Chama use_vision_api() helper
4. Processa com ZhipuVisionAPIProvider
5. Retorna análise ao usuário
```

### Opção 2: Uso Direto em Código

```python
from src.mcp.tools.providers.vllm_provider import (
    ZhipuVisionAPIProvider,
    VisionProviderFactory
)

# Criar provider
config = {
    "api_key": "seu_token_aqui",
    "model": "glm-4v-flash",
}
provider = ZhipuVisionAPIProvider(config)

# Analisar imagem
result = await provider.analyze_image(
    image_base64="iVBORw0KGgo...",  # Imagem em base64
    question="O que há nesta imagem?",
    context="Procure por objetos vermelhos"
)

# Resultado
print(result["analysis"])  # Texto da análise
print(result["tokens"])     # Tokens usados
```

---

## 📊 Estrutura de Resposta

```python
{
    "status": "success",
    "analysis": "A imagem mostra uma paisagem urbana com edifícios modernos...",
    "tokens": {
        "input": 850,
        "output": 120,
        "total": 970
    },
    "model": "glm-4v-flash",
    "timestamp": "2024-01-15T10:30:45.123Z"
}
```

---

## 🔐 Segurança

### Validações Implementadas:
1. **Validação de Entrada:**
   - Verifica se image_base64 é válida
   - Valida encoding UTF-8
   - Limita tamanho máximo

2. **Autenticação:**
   - Bearer token para Zhipu/OpenAI
   - x-goog-api-key para Google Gemini
   - Variáveis de ambiente protegidas

3. **Error Handling:**
   - Retry automático (3 tentativas)
   - Backoff exponencial
   - Logging de erros detalhado
   - Mensagens de erro sanitizadas

4. **Rate Limiting:**
   - Respeita limites da API
   - Implementa queue de requisições
   - Throttling automático

---

## 🧪 Teste de Visão

Use o script de verificação incluído:

```bash
python verify_vision_api.py
```

Este script valida:
- ✅ Configuração VLLM em config.yaml
- ✅ Presença de variáveis de ambiente
- ✅ Importação correta de módulos
- ✅ Conectividade com API Zhipu
- ✅ Teste de análise com imagem de exemplo

---

## 📱 Modelos Suportados

### Zhipu (Recomendado)
- `glm-4v-flash` - Rápido, qualidade boa, custo baixo ⭐ **RECOMENDADO**
- `glm-4v` - Alta qualidade, mais lento
- `glm-4-vision` - Versão anterior (deprecated)

### Google Gemini (Alternativa)
- `gemini-1.5-flash` - Rápido, excelente
- `gemini-1.5-pro` - Premium

### OpenAI (Se integrado)
- `gpt-4-vision` - Excelente qualidade
- `gpt-4o` - Multimodal otimizado

---

## 🐛 Troubleshooting

| Problema | Causa | Solução |
|----------|-------|--------|
| "API Key not found" | Variável de ambiente não definida | `export ZHIPU_API_KEY=seu_token` |
| Timeout | Servidor lento ou indisponível | Aumentar `timeout` em config.yaml |
| "Invalid image" | Base64 corrompido | Verificar codificação da imagem |
| Rate limit | Muitas requisições | Implementar queue/delay |
| Resposta genérica | Pergunta mal formulada | Reformular `question` |

---

## 📈 Performance

### Tempos Médios:
- **Codificação Base64:** ~50ms (1MB imagem)
- **Requisição HTTP:** ~1-3s (Zhipu)
- **Processamento API:** ~2-5s (modelo glm-4v-flash)
- **Total:** ~3-8s por imagem

### Otimizações Possíveis:
1. Cache de resultados (mesma imagem)
2. Compressão de imagem (reduz base64)
3. Pool de conexões HTTP
4. Requisições paralelas

---

## 🔗 Integração com Sistemas

### MCP Server
O provider é automaticamente descoberto e usado pelo MCP server para ferramentas que precisam análise visual.

### Assistente IA
Quando o usuário pergunta "O que há nesta imagem?", o assistente:
1. Obtém imagem da câmera/arquivo
2. Chama use_vision_api() automaticamente
3. Retorna análise ao usuário

### APIs Externas
Pode ser integrado com webhooks, APIs REST, etc:
```python
POST /api/analyze-image
{
    "image_base64": "iVBORw0KGgo...",
    "question": "Descreva esta imagem"
}
```

---

## 📚 Referências

- **Zhipu API:** https://open.bigmodel.cn/api/paas/v4/chat/completions
- **Google Gemini:** https://ai.google.dev/
- **OpenAI Vision:** https://platform.openai.com/docs/guides/vision
- **Repositório Original:** https://github.com/MarceloClaro/xiaozhi-esp32-server

---

## 🚀 Próximos Passos

Para melhorar ainda mais o sistema de visão:

1. **[ ] Suporte a Streaming de Vídeo:** Analisar frames em tempo real
2. **[ ] OCR Integrado:** Extrair texto de imagens
3. **[ ] Detecção de Objetos:** Identificar e localizar objetos
4. **[ ] Análise de Documento:** Processar documentos escaneados
5. **[ ] Cache Redis:** Cachear análises anteriores
6. **[ ] Multi-Modal:** Combinar áudio + visão + texto

---

**Última Atualização:** 2024-01-15  
**Status:** ✅ Funcional e Testado
