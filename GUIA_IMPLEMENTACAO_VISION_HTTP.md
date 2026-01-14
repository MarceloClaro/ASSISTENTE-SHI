# 🔧 Guia Prático: Implementar Vision do esp32-server no py-xiaozhi

## Objetivo

Integrar o sistema de **Vision HTTP Endpoint** do `xiaozhi-esp32-server` no seu `py-xiaozhi` para ter:

✅ Endpoint HTTP `/mcp/vision/explain`  
✅ Autenticação JWT  
✅ Suporte a múltiplos providers (OpenAI-compatible)  
✅ Rate limiting e validação  

---

## 🏗️ Arquitetura Proposta

```
┌─────────────────────────────────────────┐
│   Assistente IA (Claude via MCP)       │
└────────────────┬────────────────────────┘
                 │ MCP Protocol
                 ▼
┌─────────────────────────────────────────┐
│      MCP Server (py-xiaozhi)           │
│  - camera_capture_and_analyze tool      │
└────────────────┬────────────────────────┘
                 │ HTTP POST + JWT Token
                 ▼
┌─────────────────────────────────────────┐
│   Vision Handler (novo módulo)          │
│  - src/api/vision_handler.py            │
│  - Validação JWT                        │
│  - Suporte OpenAI-compatible            │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│   VLLMProvider (OpenAI)                 │
│  - Zhipu, Alibaba, OpenAI, etc.        │
└─────────────────────────────────────────┘
```

---

## 📋 Pré-requisitos

1. ✅ py-xiaozhi rodando (com MCP server)
2. ✅ Zhipu API key (`ZHIPU_API_KEY`)
3. ✅ Python 3.9+
4. ✅ Conhecimento básico de HTTP/JWT

---

## 📝 Implementação Passo a Passo

### Passo 1: Instalar Dependências Adicionais

```bash
cd py-xiaozhi
pip install pyjwt python-multipart
```

**Explicação:**
- `pyjwt`: Geração/validação de tokens JWT
- `python-multipart`: Parse de formulários multipart (upload de arquivos)

### Passo 2: Criar Estrutura de Diretórios

```bash
mkdir -p src/api
mkdir -p src/utils
```

### Passo 3: Implementar JWT Manager

**Arquivo:** `src/utils/auth.py`

```python
"""JWT Authentication Manager"""
import jwt
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class JWTManager:
    """Gerencia tokens JWT para autenticação"""
    
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        """
        Inicializa JWT manager
        
        Args:
            secret_key: Chave secreta para assinar tokens
            algorithm: Algoritmo de assinatura (padrão HS256)
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expiry = 3600  # 1 hora
    
    def create_token(
        self,
        data: Dict[str, Any],
        expires_in: Optional[int] = None
    ) -> str:
        """
        Cria um novo token JWT
        
        Args:
            data: Dados a incluir no token
            expires_in: Tempo de expiração em segundos (padrão 1 hora)
        
        Returns:
            Token JWT
        """
        if expires_in is None:
            expires_in = self.token_expiry
        
        payload = {
            **data,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(seconds=expires_in)
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        logger.info(f"Token criado para: {data.get('user_id', 'unknown')}")
        return token
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verifica e decodifica um token JWT
        
        Args:
            token: Token JWT a validar
        
        Returns:
            Dados do token se válido, None se inválido
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expirado")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Token inválido: {e}")
            return None

# Instância global (será inicializada no boot)
jwt_manager: Optional[JWTManager] = None

def init_jwt(secret_key: str):
    """Inicializa o JWT manager"""
    global jwt_manager
    jwt_manager = JWTManager(secret_key)
    logger.info("JWT Manager inicializado")

def require_auth(token: str) -> Optional[Dict[str, Any]]:
    """Helper para validar token em requisições"""
    if not jwt_manager:
        logger.error("JWT Manager não foi inicializado")
        return None
    
    # Remove "Bearer " prefix se presente
    if token.startswith("Bearer "):
        token = token[7:]
    
    return jwt_manager.verify_token(token)
```

### Passo 4: Expandir VLLMProvider para OpenAI-Compatible

**Arquivo:** `src/mcp/tools/providers/vllm_openai_provider.py`

```python
"""OpenAI-Compatible Vision Provider"""
import logging
from typing import Dict, Any, Optional
import openai
import base64

logger = logging.getLogger(__name__)

class OpenAICompatibleVisionProvider:
    """
    Vision provider compatível com qualquer API OpenAI-compatible
    (Zhipu, Alibaba, OpenAI, etc)
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa provider
        
        Args:
            config:
                - api_key: Token de autenticação
                - model: Nome do modelo
                - base_url: URL da API (opcional)
                - max_tokens: Máximo de tokens
                - temperature: Temperatura (0-1)
        """
        self.api_key = config.get("api_key")
        self.model = config.get("model", "glm-4v-flash")
        self.base_url = config.get("base_url")
        self.max_tokens = config.get("max_tokens", 2048)
        self.temperature = config.get("temperature", 0.7)
        
        # Criar cliente OpenAI
        if self.base_url:
            self.client = openai.OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        else:
            # Usar Zhipu padrão
            self.client = openai.OpenAI(
                api_key=self.api_key,
                base_url="https://open.bigmodel.cn/api/paas/v4"
            )
        
        logger.info(f"OpenAI Provider inicializado: {self.model}")
    
    def analyze_image(
        self,
        image_base64: str,
        question: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analisa imagem usando Vision API OpenAI-compatible
        
        Args:
            image_base64: Imagem em base64
            question: Pergunta sobre a imagem
            context: Contexto adicional (opcional)
        
        Returns:
            Dict com análise
        """
        try:
            # Validar entrada
            if not image_base64:
                raise ValueError("Imagem não fornecida")
            if not question:
                question = "Descreva detalhadamente tudo que você vê nesta imagem"
            
            # Montar mensagem
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        },
                        {
                            "type": "text",
                            "text": question
                        }
                    ]
                }
            ]
            
            # Adicionar contexto se fornecido
            if context:
                messages[0]["content"].append({
                    "type": "text",
                    "text": f"\n\nContexto: {context}"
                })
            
            # Chamar API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            analysis = response.choices[0].message.content
            
            return {
                "status": "success",
                "analysis": analysis,
                "model": self.model,
                "tokens": {
                    "input": response.usage.prompt_tokens,
                    "output": response.usage.completion_tokens,
                    "total": response.usage.total_tokens
                }
            }
        
        except Exception as e:
            logger.error(f"Erro na análise: {e}")
            return {
                "status": "error",
                "error": str(e),
                "analysis": None
            }
```

### Passo 5: Criar Vision Handler com HTTP Endpoint

**Arquivo:** `src/api/vision_handler.py`

```python
"""Vision HTTP Endpoint Handler"""
import logging
from typing import Dict, Any, Optional, Tuple
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
import base64
import io
from PIL import Image

from src.utils.auth import require_auth
from src.mcp.tools.providers.vllm_openai_provider import (
    OpenAICompatibleVisionProvider
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/vision", tags=["vision"])

# Cache de providers (evita criar novo a cada requisição)
_provider_cache: Dict[str, OpenAICompatibleVisionProvider] = {}

def get_vision_provider(config: Dict[str, Any]) -> OpenAICompatibleVisionProvider:
    """Factory com cache para providers"""
    config_key = config.get("model")
    
    if config_key not in _provider_cache:
        _provider_cache[config_key] = OpenAICompatibleVisionProvider(config)
    
    return _provider_cache[config_key]

async def verify_bearer_token(authorization: str) -> Optional[Dict[str, Any]]:
    """Dependency para validar Bearer token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    
    payload = require_auth(authorization)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    return payload

@router.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    question: str = Form(...),
    context: Optional[str] = Form(None),
    device_id: Optional[str] = Form(None),
    config_key: str = Form(default="default"),
    auth_payload: Dict[str, Any] = Depends(verify_bearer_token)
) -> JSONResponse:
    """
    Analisa uma imagem via upload
    
    Args:
        file: Arquivo de imagem (JPEG, PNG, etc)
        question: Pergunta sobre a imagem
        context: Contexto adicional (opcional)
        device_id: ID do dispositivo que enviou (para logging)
        config_key: Qual config usar (padrão ou custom)
        auth_payload: Token JWT validado (automático)
    
    Returns:
        JSON com análise da imagem
    """
    try:
        # Validar arquivo
        if not file:
            raise ValueError("Arquivo não fornecido")
        
        # Validar tamanho (máx 5MB)
        content = await file.read()
        if len(content) > 5 * 1024 * 1024:
            raise ValueError("Arquivo muito grande (máx 5MB)")
        
        # Validar tipo de arquivo
        allowed_types = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}
        if file.content_type not in allowed_types:
            raise ValueError(f"Tipo de arquivo não permitido: {file.content_type}")
        
        # Validar que é imagem real
        try:
            Image.open(io.BytesIO(content))
        except Exception as e:
            raise ValueError(f"Arquivo não é imagem válida: {e}")
        
        # Converter para base64
        image_base64 = base64.b64encode(content).decode('utf-8')
        
        # Obter provider (TODO: usar config_key para selecionar)
        from src.config import config
        vllm_config = config.get_config("VLLM", {})
        zhipu_config = vllm_config.get("zhipu", {})
        
        provider = get_vision_provider(zhipu_config)
        
        # Analisar imagem
        result = provider.analyze_image(image_base64, question, context)
        
        # Log da requisição bem-sucedida
        logger.info(
            f"Análise concluída - "
            f"device_id={device_id}, "
            f"user={auth_payload.get('user_id')}, "
            f"tokens={result.get('tokens', {}).get('total')}"
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "action": "RESPONSE",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
        )
    
    except ValueError as e:
        logger.warning(f"Validação falhou: {e}")
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": str(e)}
        )
    except Exception as e:
        logger.error(f"Erro ao processar imagem: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "Erro interno do servidor"}
        )

@router.get("/health")
async def health_check() -> JSONResponse:
    """Verifica status do serviço de visão"""
    return JSONResponse(
        status_code=200,
        content={
            "status": "ok",
            "vision_available": True,
            "providers": ["openai-compatible"],
            "timestamp": datetime.now().isoformat()
        }
    )
```

### Passo 6: Integrar no FastAPI Principal

**Arquivo:** `src/main.py` (ou equivalente do seu FastAPI app)

```python
"""Integração dos novos endpoints no app principal"""
from fastapi import FastAPI
from src.api.vision_handler import router as vision_router
from src.utils.auth import init_jwt
from src.config import config

app = FastAPI(title="py-xiaozhi com Vision API")

# Inicializar JWT
auth_key = config.get_config("auth_key", "seu_secret_key_aqui")
init_jwt(auth_key)

# Registrar routers
app.include_router(vision_router)

# Seu código existente aqui...
```

### Passo 7: Configurar em config.yaml

```yaml
# Seu config.yaml existente + novo:

# Chave para JWT
auth_key: "${AUTH_SECRET_KEY}"  # Ou use string fixa em dev

# VLLM providers
VLLM:
  zhipu:
    type: "openai"
    api_key: "${ZHIPU_API_KEY}"
    model: "glm-4v-flash"
    base_url: "https://open.bigmodel.cn/api/paas/v4"
    max_tokens: 2048
    temperature: 0.7
  
  alibaba:
    type: "openai"
    api_key: "${ALIBABA_API_KEY}"
    model: "qwen2.5-vl-3b-instructh"
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    max_tokens: 2048
    temperature: 0.7
```

### Passo 8: Atualizar main.py para Usar Vision Handler

**Modificar MCP Tool:**

```python
async def camera_capture_and_analyze(question: str) -> str:
    """
    MCP Tool: Captura imagem e analisa com Vision Handler
    """
    try:
        # 1. Capturar imagem
        frame = cap.read()[1]
        if frame is None:
            return "Erro: Não consegui capturar imagem da câmera"
        
        # 2. Converter para base64
        _, buffer = cv2.imencode('.jpg', frame)
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # 3. Chamar Vision Handler (localizado)
        from src.mcp.tools.providers.vllm_openai_provider import (
            OpenAICompatibleVisionProvider
        )
        from src.config import config
        
        vllm_config = config.get_config("VLLM", {})
        zhipu_config = vllm_config.get("zhipu", {})
        
        provider = OpenAICompatibleVisionProvider(zhipu_config)
        result = provider.analyze_image(image_base64, question)
        
        if result["status"] == "success":
            return result["analysis"]
        else:
            return f"Erro na análise: {result.get('error')}"
    
    except Exception as e:
        logger.error(f"Erro ao analisar imagem: {e}", exc_info=True)
        return f"Erro interno: {str(e)}"
```

---

## 🧪 Teste de Integração

### 1. Gerar Token JWT

```python
from src.utils.auth import jwt_manager

token = jwt_manager.create_token({
    "user_id": "teste",
    "device_id": "device_001"
})
print(f"Token: {token}")
```

### 2. Testar Endpoint via cURL

```bash
curl -X POST http://localhost:8000/api/vision/analyze \
  -H "Authorization: Bearer $TOKEN" \
  -F "question=O que há nesta imagem?" \
  -F "file=@test_image.jpg"
```

### 3. Testar via Python

```python
import httpx
import base64

# Criar token
token = jwt_manager.create_token({"user_id": "teste"})

# Preparar imagem
with open("test_image.jpg", "rb") as f:
    image_data = f.read()

# Fazer requisição
async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/api/vision/analyze",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "question": "Descreva esta imagem",
            "context": "Procure por objetos vermelhos"
        },
        files={"file": image_data}
    )
    
    result = response.json()
    print(f"Análise: {result['data']['analysis']}")
    print(f"Tokens: {result['data']['tokens']}")
```

---

## 📊 Checklist de Implementação

- [ ] Instalar dependências (`pyjwt`, `python-multipart`)
- [ ] Criar estrutura de diretórios (`src/api`, `src/utils`)
- [ ] Implementar `src/utils/auth.py` (JWT Manager)
- [ ] Implementar `src/mcp/tools/providers/vllm_openai_provider.py`
- [ ] Implementar `src/api/vision_handler.py`
- [ ] Integrar routers no FastAPI principal
- [ ] Atualizar `config.yaml` com VLLM config
- [ ] Gerar JWT secret key segura
- [ ] Testar endpoints com cURL/Python
- [ ] Integrar Vision Handler no MCP Tool
- [ ] Testar fluxo completo (câmera → análise → resposta)

---

## 🚀 Próximas Melhorias

1. **Rate Limiting:**
   ```python
   from slowapi import Limiter
   from slowapi.util import get_remote_address
   
   limiter = Limiter(key_func=get_remote_address)
   
   @router.post("/analyze")
   @limiter.limit("10/minute")
   async def analyze_image(...):
       pass
   ```

2. **Cache Redis:**
   ```python
   import redis
   
   r = redis.Redis(host='localhost', port=6379)
   
   cache_key = f"vision:{image_hash}"
   if r.exists(cache_key):
       return r.get(cache_key)
   ```

3. **Streaming Video:**
   ```python
   @router.websocket("/ws/video-analyze")
   async def websocket_vision(websocket):
       # Receber frames em tempo real
       # Analisar continuamente
   ```

---

**Última Atualização:** 2024-01-15  
**Status:** ✅ Guia Completo e Pronto para Implementação
