# 🔧 Guia de Solução de Problemas - ASSISTENTE-SHI

## 📋 Índice

1. [Modelo Wake Word Ausente](#1-modelo-wake-word-ausente)
2. [API Vision Retornando 404](#2-api-vision-retornando-404)
3. [Timeout de Conexão WebSocket](#3-timeout-de-conexão-websocket)
4. [Problemas com Áudio](#4-problemas-com-áudio)
5. [Diagnóstico Automático](#5-diagnóstico-automático)

---

## 1. Modelo Wake Word Ausente

### 🔴 Problema

```
FileNotFoundError: Modelo ausente: models/encoder.onnx
```

O sistema não consegue encontrar os arquivos do modelo Sherpa-ONNX necessários para detectar a palavra de ativação.

### ✅ Solução Automática (Recomendado)

Execute o script de download automático:

```bash
python download_wake_word_model.py
```

O script irá:
- Criar o diretório `models/` se não existir
- Baixar todos os arquivos necessários:
  - `encoder.onnx`
  - `decoder.onnx`
  - `joiner.onnx`
  - `tokens.txt`
  - `keywords.txt`
- Mostrar barra de progresso
- Validar downloads

### ✅ Solução Manual

1. Baixe o modelo do repositório oficial:
   ```
   https://github.com/k2-fsa/sherpa-onnx/releases/
   ```

2. Procure por `sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01`

3. Extraia os arquivos para `models/`:
   ```
   models/
   ├── encoder.onnx
   ├── decoder.onnx
   ├── joiner.onnx
   ├── tokens.txt
   └── keywords.txt
   ```

4. Configure `config/config.json`:
   ```json
   {
     "WAKE_WORD_OPTIONS": {
       "USE_WAKE_WORD": true,
       "MODEL_PATH": "models"
     }
   }
   ```

### 🎯 Configuração de Palavras-Chave

Edite `models/keywords.txt` para adicionar suas palavras de ativação:

```text
xiao zhi
ni hao
hey shi
assistente
```

**Dica:** Use frases curtas (2-3 sílabas) para melhor detecção.

---

## 2. API Vision Retornando 404

### 🔴 Problema

```
API Error 404: Not Found
Failed to analyze image
```

A API GLM-4V (Zhipu) está retornando erro 404 ao tentar analisar imagens.

### 🔍 Causa

- Token de autenticação inválido ou expirado
- URL da API incorreta
- Serviço temporariamente indisponível

### ✅ Solução 1: Usar LLaVA Local (Recomendado - Gratuito)

O sistema agora faz fallback automático para Ollama+LLaVA quando a API falha.

**1. Instale o Ollama:**
```bash
# Windows
winget install Ollama.Ollama

# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh
```

**2. Baixe o modelo LLaVA:**
```bash
ollama pull llava:7b
```

**3. Configure `config/config.json`:**
```json
{
  "llm": {
    "api": "ollama",
    "model": "llava:7b",
    "base_url": "http://localhost:11434/api"
  }
}
```

**Vantagens:**
- ✅ 100% Gratuito
- ✅ Privacidade total (execução local)
- ✅ Sem limites de requisições
- ✅ Funciona offline

### ✅ Solução 2: Renovar Token GLM-4V

1. Acesse: https://open.bigmodel.cn/

2. Crie/renove sua conta

3. Obtenha novo token em "API Keys"

4. Atualize `config/config.json`:
   ```json
   {
     "llm": {
       "api": "zhipu",
       "model": "glm-4v-plus",
       "token": "SEU_NOVO_TOKEN_AQUI",
       "base_url": "https://open.bigmodel.cn/api/paas/v4/chat/completions"
     }
   }
   ```

### ✅ Solução 3: Usar Gemini Vision (Alternativa)

```json
{
  "llm": {
    "api": "gemini",
    "model": "gemini-pro-vision",
    "token": "SEU_TOKEN_GOOGLE_AI",
    "base_url": "https://generativelanguage.googleapis.com/v1beta"
  }
}
```

Obtenha token em: https://makersuite.google.com/app/apikey

---

## 3. Timeout de Conexão WebSocket

### 🔴 Problema

```
WebSocket connection timeout after ~1 minute
Connection closed unexpectedly
```

### 🔍 Causa

- Firewall bloqueando conexão prolongada
- Proxy intermediário
- Configuração de timeout muito curta

### ✅ Solução 1: Aumentar Timeout

Edite `config/config.json`:

```json
{
  "CONNECTION": {
    "WEBSOCKET_TIMEOUT": 300,
    "PING_INTERVAL": 30,
    "PING_TIMEOUT": 10,
    "MAX_RECONNECT_ATTEMPTS": 5,
    "RECONNECT_DELAY": 3
  }
}
```

### ✅ Solução 2: Verificar Firewall

**Windows:**
```powershell
# Permitir Python no firewall
netsh advfirewall firewall add rule name="ASSISTENTE-SHI" dir=in action=allow program="C:\Python39\python.exe" enable=yes
```

**Linux:**
```bash
# UFW
sudo ufw allow from any to any port 443 proto tcp

# iptables
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

### ✅ Solução 3: Usar MQTT (Alternativa)

```bash
python main.py --mode gui --protocol mqtt
```

Configure `config/config.json`:
```json
{
  "MQTT": {
    "BROKER": "mqtt.xiaozhi.me",
    "PORT": 8883,
    "USE_TLS": true,
    "KEEPALIVE": 60
  }
}
```

---

## 4. Problemas com Áudio

### 🔴 Problema A: Microfone não detectado

```
No input device found
AudioCodec initialization failed
```

**Solução:**

1. Verifique dispositivos disponíveis:
   ```bash
   python -c "import sounddevice as sd; print(sd.query_devices())"
   ```

2. Configure índice correto em `config/config.json`:
   ```json
   {
     "AUDIO": {
       "INPUT_DEVICE_INDEX": 0,
       "OUTPUT_DEVICE_INDEX": 1
     }
   }
   ```

### 🔴 Problema B: Eco durante conversação

```
Echo cancellation not working properly
```

**Solução:**

1. Ative AEC (Acoustic Echo Cancellation):
   ```json
   {
     "AUDIO_PROCESSING": {
       "USE_AEC": true,
       "AEC_FILTER_LENGTH": 1024
     }
   }
   ```

2. Use fone de ouvido (reduz eco físico)

### 🔴 Problema C: Opus library not found

```
OSError: libopus.dll not found
```

**Solução Windows:**
```powershell
# Copiar DLL para System32
copy libs\libopus\libopus.dll C:\Windows\System32\
```

**Solução macOS:**
```bash
brew install opus
```

**Solução Linux:**
```bash
sudo apt-get install libopus0
```

---

## 5. Diagnóstico Automático

### 🔍 Execute Verificação Completa

```bash
python diagnose_system.py
```

O script verifica:
- ✅ Modelo Wake Word
- ✅ Arquivo de configuração
- ✅ Dependências Python
- ✅ Vision API
- ✅ Conectividade de rede

### Exemplo de Saída

```
====================================================================
DIAGNÓSTICO DO SISTEMA ASSISTENTE-SHI
====================================================================

[1/5] Verificando Modelo Wake Word...
  ✅ Modelo Wake Word completo

[2/5] Verificando Configuração...
  ⚠️  Token GLM-4V ausente (usará LLaVA local)
  ✅ Configuração válida

[3/5] Verificando Dependências Python...
  ✅ pyqt5
  ✅ aiohttp
  ✅ websockets
  ✅ opus
  ✅ sherpa-onnx
  ✅ opencv-python
  ✅ numpy

[4/5] Verificando Vision API...
  ⚠️  Token GLM-4V inválido
     Fallback: LLaVA (Ollama local)
     Instale: https://ollama.com/
     Execute: ollama pull llava:7b

[5/5] Verificando Conectividade...
  ✅ DNS funcional
  ✅ Conexão HTTPS funcional

====================================================================
RESUMO DO DIAGNÓSTICO
====================================================================

✅ Verificações OK: 7
⚠️  Avisos: 2
❌ Erros: 0

====================================================================
✅ SISTEMA PRONTO PARA EXECUÇÃO!

Execute: python main.py --mode gui --protocol websocket
====================================================================
```

---

## 📚 Recursos Adicionais

### Links Úteis

- **Documentação Oficial:** https://huangjunsen0406.github.io/py-xiaozhi/
- **Repositório Original:** https://github.com/huangjunsen0406/py-xiaozhi
- **Issues GitHub:** https://github.com/MarceloClaro/ASSISTENTE-SHI/issues
- **Ollama Download:** https://ollama.com/
- **Sherpa-ONNX Models:** https://github.com/k2-fsa/sherpa-onnx/releases

### Comandos Úteis

```bash
# Diagnóstico completo
python diagnose_system.py

# Download modelo Wake Word
python download_wake_word_model.py

# Testar configuração
python -m src.utils.config_manager

# Listar dispositivos de áudio
python -c "import sounddevice as sd; print(sd.query_devices())"

# Verificar versão Sherpa-ONNX
python -c "import sherpa_onnx; print(sherpa_onnx.__version__)"

# Executar em modo debug
python main.py --mode gui --protocol websocket --log-level DEBUG
```

### Estrutura de Logs

```
logs/
├── application.log       # Log principal
├── mcp_server.log       # MCP tools
├── audio_processing.log # Áudio e VAD
├── wake_word.log        # Detecção de ativação
└── protocols.log        # WebSocket/MQTT
```

---

## 🆘 Suporte

Se o problema persistir após seguir este guia:

1. Execute: `python diagnose_system.py > diagnostico.txt`
2. Abra uma issue em: https://github.com/MarceloClaro/ASSISTENTE-SHI/issues
3. Anexe o arquivo `diagnostico.txt`
4. Descreva o problema detalhadamente

---

**Última Atualização:** 13 de Janeiro de 2026  
**Status:** ✅ Validado e Testado
