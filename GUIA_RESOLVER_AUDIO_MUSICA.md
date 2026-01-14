# 🔧 Guia: Resolver TTS Silencioso e Música Não Toca

## Problema 1: TTS não vocaliza (áudio mudo)

### Verificação rápida
1. **Volume do Windows:**
   - Clique no ícone de volume (barra de tarefas)
   - Confirme que está acima de 30%
   - Teste com qualquer vídeo/música do navegador

2. **Dispositivo de áudio padrão:**
   - Configurações → Sistema → Som
   - Confirme que o dispositivo correto está selecionado
   - Se usar fone/caixa USB, verifique se está conectado

3. **Executar comando de teste:**
   ```powershell
   python -c "import pyttsx3; e=pyttsx3.init(); e.say('teste'); e.runAndWait()"
   ```
   - Se não ouvir nada → problema no dispositivo de áudio
   - Se ouvir → problema é no protocolo websocket/TTS do assistente

### Solução se TTS continuar mudo
- O protocolo websocket pode estar enviando áudio para dispositivo errado
- **Workaround:** usar modo CLI/terminal (sem GUI) para testar:
  ```powershell
  python main.py --mode terminal
  ```

---

## Problema 2: Música não toca (timeout no stream)

### Causa
- Host `api.xiaodaokg.com` fora do ar ou bloqueado pela rede
- Timeout após 10s de tentativa

### Solução imediata: Modo offline (100% garantido)

#### Passo 1: Colocar arquivo MP3 no cache
```powershell
# Criar diretório se não existir
New-Item -ItemType Directory -Force -Path "C:\Users\marce\AppData\Local\py-xiaozhi-main\cache\music\local"

# Copiar um MP3 de teste (exemplo: sua pasta Downloads)
Copy-Item "$env:USERPROFILE\Downloads\exemplo.mp3" "C:\Users\marce\AppData\Local\py-xiaozhi-main\cache\music\local\"
```

#### Passo 2: No assistente, pedir:
- **Voz:** "toque exemplo" (sem .mp3)
- **OU via MCP:**
  1. Listar: `music_player.get_local_playlist`
  2. Tocar: `music_player.search_and_play "exemplo"`

#### Resultado esperado
- Player busca no cache local (sem internet)
- Inicia playback em < 2s
- Log mostra caminho local, não URL

---

## Teste rápido: Validar tudo de uma vez

### 1. Verificar volume
```powershell
# No PowerShell, ajustar volume para 50%
[System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")
$wmp = New-Object System.Windows.Media.MediaPlayer
$wmp.Volume = 0.5
```

### 2. Colocar MP3 no cache
```powershell
# Se você tiver um MP3 chamado "teste.mp3" em Downloads:
Copy-Item "$env:USERPROFILE\Downloads\teste.mp3" "C:\Users\marce\AppData\Local\py-xiaozhi-main\cache\music\local\teste.mp3"
```

### 3. Rodar assistente e testar
```powershell
python main.py --mode gui --protocol websocket
```
- Diga: **"tire uma foto"** → deve descrever e **vocalizar**
- Diga: **"toque teste"** → deve tocar o MP3 local

---

## Se ainda não funcionar

### TTS mudo
- Verifique `logs/app.log` para mensagens de erro de áudio
- Teste com outro dispositivo de saída (troque para fone/caixa diferente)
- Último recurso: reinicie o assistente após trocar dispositivo de áudio

### Música offline não toca
- Confirme que o arquivo está em `cache/music/local/`
- Use nome do arquivo sem extensão: "teste" (não "teste.mp3")
- Verifique log: deve aparecer `[MusicPlayer] MúsicaReproduçãoDispositivo` e caminho local

---

## Comandos úteis

```powershell
# Listar arquivos no cache de música
Get-ChildItem "C:\Users\marce\AppData\Local\py-xiaozhi-main\cache\music\local"

# Ver últimas linhas do log (procurar erros)
Get-Content "logs\app.log" -Tail 50

# Verificar se Ollama está rodando
Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -UseBasicParsing | Select-Object -ExpandProperty Content
```

---

**Resultado esperado após seguir este guia:**
- ✅ Foto capturada + descrição **vocalizada** pelo TTS
- ✅ Música local tocando (sem depender de stream externo)
