# 🚀 GUIA RÁPIDO - Instalação e Uso do Assistente Xiaozhi AI

## ⚡ Instalação em 30 Segundos

### Windows
```cmd
start.bat
```

### Linux/macOS
```bash
chmod +x start.sh && ./start.sh
```

**Pronto!** O script automaticamente:
- ✅ Verifica Python e dependências
- ✅ Instala Ollama se necessário
- ✅ Baixa modelo LLaVA (4.5GB)
- ✅ Inicia o assistente

---

## 📖 Passo a Passo Detalhado

### 1️⃣ Clone o Repositório
```bash
git clone https://github.com/MarceloClaro/ASSISTENTE-SHI.git
cd ASSISTENTE-SHI
```

### 2️⃣ Execute o Launcher

**Opção A - Automático (Recomendado):**
```bash
# Windows
start.bat

# Linux/macOS
chmod +x start.sh
./start.sh
```

**Opção B - Manual:**
```bash
# 1. Instalar Ollama
python setup_ollama.py

# 2. Iniciar aplicação
python main.py --mode gui --protocol websocket
```

### 3️⃣ Primeira Execução

O sistema verificará:
```
🔍 Verificando dependências do sistema...
✅ Ollama e LLaVA configurados corretamente
```

Se Ollama não estiver instalado:
```
❌ OLLAMA NÃO INSTALADO
Deseja instalar automaticamente? (s/N): s
```

### 4️⃣ Ativação do Dispositivo

Na primeira execução, você verá uma tela para adicionar dispositivo:

1. Acesse: https://xiaozhi.me/console
2. Faça login/cadastro
3. Clique em "Add Device"
4. Escanei o QR Code mostrado no aplicativo

---

## 💻 Comandos Úteis

### Verificar Instalação
```bash
# Python
python --version

# Ollama
ollama --version
ollama list

# Serviço Ollama
curl http://localhost:11434/api/tags
```

### Modos de Execução
```bash
# Interface Gráfica (padrão)
python main.py --mode gui

# Linha de Comando
python main.py --mode cli

# Protocolo específico
python main.py --mode gui --protocol mqtt

# Pular ativação (debug)
python main.py --skip-activation
```

### Diagnóstico
```bash
# Verificação completa do sistema
python diagnose_system.py

# Download de modelo wake-word
python download_wake_word_model.py
```

---

## 🛠️ Solução de Problemas Comuns

### ❌ "Ollama não encontrado"
```bash
# Instalar manualmente
python setup_ollama.py
```

### ❌ "Serviço Ollama não está rodando"
```bash
# Iniciar serviço
ollama serve
```

### ❌ "Modelo LLaVA não encontrado"
```bash
# Baixar modelo (4.5GB)
ollama pull llava:7b
```

### ❌ "Wake Word model missing"
```bash
# Baixar modelos de detecção
python download_wake_word_model.py
```

### ❌ "ModuleNotFoundError"
```bash
# Instalar dependências
pip install -r requirements.txt
```

### ❌ "Port 11434 already in use"
```bash
# Verificar processo
# Windows
netstat -ano | findstr :11434

# Linux/macOS
lsof -i :11434

# Matar processo existente ou reiniciar
```

---

## 🎯 Recursos Principais

### 🎤 Comando de Voz
- **Palavra de Ativação:** "小智" (Xiaozhi) ou "Hey Xiaozhi"
- **Detecção Offline:** Sherpa-ONNX local
- **Cancelar Audio:** Clique durante gravação

### 📷 Análise de Imagens
- **Modelo:** LLaVA (7B) - 100% gratuito
- **Processamento:** Local (Ollama)
- **Uso:** Capture imagem e pergunte sobre ela

### 🔌 32+ Ferramentas MCP
- **Sistema:** Controle de dispositivos, timer, alarmes
- **Mídia:** Música, podcasts, rádio
- **Informação:** Clima, notícias, busca web
- **Utilitários:** Calculadora, calendário, lembretes
- **Especiais:** Ba Zi (astrologia chinesa), receitas

### 🌐 Protocolos
- **WebSocket** (padrão): Baixa latência, tempo real
- **MQTT**: Fallback para redes instáveis

---

## 📊 Requisitos do Sistema

### Mínimo
- **OS:** Windows 10+, macOS 10.15+, Linux (Ubuntu 18.04+)
- **CPU:** Dual-core 2.0 GHz
- **RAM:** 4 GB
- **Disco:** 8 GB (5GB para Ollama + modelo)
- **Internet:** Para ativação e MCP cloud tools

### Recomendado
- **CPU:** Quad-core 3.0 GHz (AVX2 support)
- **RAM:** 8 GB+
- **Disco:** 16 GB SSD
- **Internet:** Banda larga 5+ Mbps

### Aceleração GPU (Opcional)
- **NVIDIA:** CUDA 11.8+
- **AMD:** ROCm 5.0+
- **Apple:** Metal (M1/M2/M3)

---

## 🔐 Configuração de Segurança

### Token MCP
Seu token JWT já está configurado em `config/config.json`:
```json
{
  "token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Validade:** Até 26 de Janeiro de 2027

### Renovar Token
1. Acesse: https://xiaozhi.me/console
2. Configurações → API Keys
3. Gere novo token
4. Atualize `config/config.json`

---

## 📈 Uso de Recursos

### Ollama/LLaVA
- **Memória:** 4-8 GB RAM durante análise
- **CPU:** 50-100% durante inferência
- **Duração:** 2-5 segundos por imagem

### Audio Processing
- **Memória:** ~100 MB
- **CPU:** 5-10% contínuo
- **Latência:** <50ms

### GUI
- **Memória:** ~200 MB
- **CPU:** 1-5%

---

## 🎨 Personalização

### Alterar Modelo LLaVA

**Modelos Disponíveis:**
- `llava:7b` - Rápido, 4.5GB (padrão)
- `llava:13b` - Melhor qualidade, 8GB
- `llava:34b` - Máxima precisão, 20GB

**Como Trocar:**
```bash
# Baixar novo modelo
ollama pull llava:13b

# Editar config/config.json
"models": "llava:13b"

# Reiniciar aplicação
```

### Configurar Palavra de Ativação

Edite `config/wake_word_config.json`:
```json
{
  "keywords": ["xiaozhi", "小智", "hey xiaozhi"],
  "threshold": 0.5
}
```

### Temas GUI

Edite `src/views/themes.json`:
```json
{
  "theme": "dark",  // dark, light, auto
  "accent_color": "#2196F3"
}
```

---

## 📚 Documentação Completa

### Arquivos de Referência
- **[README.md](README.md)** - Visão geral completa
- **[INSTALACAO_OLLAMA_DOCUMENTACAO.md](INSTALACAO_OLLAMA_DOCUMENTACAO.md)** - Detalhes técnicos da instalação
- **[SOLUCOES_PROBLEMAS.md](SOLUCOES_PROBLEMAS.md)** - Troubleshooting avançado
- **[docs/](docs/)** - Documentação técnica da arquitetura

### Links Externos
- **Website Oficial:** https://xiaozhi.me
- **Console Web:** https://xiaozhi.me/console
- **Ollama Docs:** https://ollama.ai/docs
- **LLaVA Model:** https://llava-vl.github.io

---

## 💡 Dicas e Truques

### ⚡ Performance

**1. Usar GPU para Ollama:**
```bash
# Verificar suporte CUDA
nvidia-smi

# Ollama usa GPU automaticamente se disponível
```

**2. Reduzir Latência Audio:**
```json
// config/audio_config.json
{
  "buffer_size": 512,  // Menor = menos latência
  "sample_rate": 16000
}
```

**3. Cache de Modelos:**
```bash
# Pré-carregar modelo na memória
ollama run llava:7b
> /bye
```

### 🔧 Desenvolvimento

**Modo Debug:**
```bash
# Logs detalhados
export LOG_LEVEL=DEBUG  # Linux/macOS
set LOG_LEVEL=DEBUG     # Windows

python main.py --mode gui
```

**Hot Reload:**
```bash
# Modificar código sem reiniciar
# Pressione Ctrl+R na GUI
```

**Testes:**
```bash
# Executar suite de testes
python -m pytest tests/

# Teste específico
python test_camera_vision.py
```

---

## 🤝 Contribuindo

### Reportar Bugs
1. Verifique issues existentes: https://github.com/MarceloClaro/ASSISTENTE-SHI/issues
2. Execute `python diagnose_system.py` e anexe output
3. Descreva passos para reproduzir

### Sugerir Features
- Abra issue com tag [FEATURE REQUEST]
- Descreva caso de uso
- Mockups são bem-vindos

### Pull Requests
1. Fork o repositório
2. Crie branch: `git checkout -b feature/nome`
3. Commit: `git commit -m "feat: descrição"`
4. Push: `git push origin feature/nome`
5. Abra PR no GitHub

---

## 📞 Suporte

### Comunidade
- **Issues GitHub:** https://github.com/MarceloClaro/ASSISTENTE-SHI/issues
- **Discussões:** https://github.com/MarceloClaro/ASSISTENTE-SHI/discussions

### Contato Direto
- **Email:** suporte@xiaozhi.me (se aplicável)
- **Discord:** [Link para servidor] (se aplicável)

---

## 📝 Changelog

### v1.0.0 (13/01/2026)
- ✨ Instalação automática do Ollama
- ✨ Launchers Windows/Linux/macOS
- ✨ Integração com main.py
- 💰 Remoção de APIs pagas (Zhipu/Gemini)
- 🎯 100% gratuito com LLaVA
- 📚 Documentação completa em PT-BR
- 🔧 Scripts de diagnóstico
- 🎨 README com diagramas ASCII

---

## ⭐ Agradecimentos

- **py-xiaozhi** - Projeto original
- **Ollama** - Runtime local de LLMs
- **LLaVA** - Modelo multimodal open-source
- **Sherpa-ONNX** - Wake word detection
- **PyQt5** - Framework GUI

---

**🎉 Você está pronto para usar o Assistente Xiaozhi AI!**

Execute `start.bat` (Windows) ou `./start.sh` (Linux/macOS) e comece! 🚀
