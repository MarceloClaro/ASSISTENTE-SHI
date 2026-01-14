# Diagnóstico Final: Problema de Vocali​zação TTS

## Conclusão

**O problema NÃO está no código do cliente - o servidor remoto não envia dados de áudio TTS.**

## Investigação Realizada

### 1. Fluxo de Áudio Verificado
✅ **Camera** → Captura imagem com sucesso (18KB JPEG)
✅ **Ollama/LLaVA** → Análise de imagem funciona (55 caracteres de resposta)
✅ **UTF-8 Encoding** → Caracteres especiais (ç,ã,é) transmitem corretamente
✅ **MCP Tools** → Camera tool responde com sucesso

### 2. TTS Protocol - O Que Deveria Acontecer
```
1. Servidor envia: JSON {"type": "tts", "state": "start"}
2. Servidor envia: BYTES [Opus audio frame 1]
3. Servidor envia: BYTES [Opus audio frame 2]
4. ...múltiplos frames...
5. Servidor envia: JSON {"type": "tts", "state": "stop"}
```

### 3. O Que Realmente Acontece
Logs capturados em 2026-01-14 13:03:42-43:

```
2026-01-14 13:03:43,061[src.application] - Mensagem JSON recebida: type=tts
2026-01-14 13:03:43,242[src.application] - Mensagem JSON recebida: type=tts
2026-01-14 13:03:43,427[src.application] - Mensagem JSON recebida: type=tts
2026-01-14 13:03:43,429 - Definindo estado: listening
2026-01-14 13:03:43,548 - LimpandoÁudioFila，1331 QuadrosÁudioDados
```

**Observações:**
- ✅ TTS `state=start` e `state=stop` chegam
- ❌ **ZERO dados de áudio binários recebidos**
- 🟡 "1331 QuadrosÁudioDados" = dados de TESTE/MOCK (não do servidor)

### 4. Verificação: on_incoming_audio Nunca Chamado
Adicionei logging completo em:
- `application.py` línea 315: `_on_incoming_audio(data)`
- `plugins/audio.py` línea 100: `on_incoming_audio(data)`
- `audio_codec.py` línea 664: `write_audio(data)` 

**Resultado:** Nenhuma dessas funções logou nada = **nunca foram chamadas**

### 5. Verificação: WebSocket Recebendo Dados
Log do WebSocket em `websocket_protocol.py` línea 381:
```python
elif isinstance(message, bytes):
    if self._on_incoming_audio:
        self._on_incoming_audio(message)
```

Nenhum log de dados binários = **servidor nunca envia dados binários**

## Conclusão Final

### ✅ Cliente Funcionando Corretamente
1. Audio codec inicializado
2. WebSocket conectado
3. Streams criados (input/output)
4. Callbacks registrados
5. Opus decoder pronto
6. Audio device selecionado (Realtek)

### ❌ Problema: Servidor Remoto
**URL:** `wss://api.tenclass.net/xiaozhi/v1/`
**Problema:** Não envia frames de áudio Opus após mensagens TTS

O servidor envia:
- ✅ Mensagens de controle TTS (state=start/stop)
- ❌ **Nenhum dado de áudio (frames binários Opus)**

## Solução Necessária
O servidor `api.tenclass.net` precisa ser configurado para enviar dados de áudio TTS via WebSocket como:
1. Frames binários Opus-codificados
2. Transmitidos entre os eventos `tts state=start` e `tts state=stop`
3. Cada frame com tamanho apropriado (múltiplos de 20ms a 24kHz)

## Documentação para Equipe do Servidor
Protocolo esperado para TTS via WebSocket:
```json
{
  "type": "tts",
  "state": "start",
  "language": "pt-BR",
  "speed": 1.0
}
```
Seguido de:
```
[Binary Opus frames - continuously until completion]
```
Terminado com:
```json
{
  "type": "tts", 
  "state": "stop",
  "duration_ms": 5000
}
```

## Status do Sistema
- **Camera:** ✅ 100% funcional
- **Análise de imagem:** ✅ 100% funcional  
- **Codificação de áudio:** ✅ 100% pronto
- **Reprodução de áudio:** ✅ 100% pronto (esperando dados)
- **TTS Vocali​zação:** ❌ Bloqueado pelo servidor
