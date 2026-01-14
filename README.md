# ASSISTENTE-SHI - Xiaozhi AI Assistant 🤖

<p align="center">
  <img src="assets/emojis/winking.gif" alt="Assistente Shi Piscando" width="80" height="80"/>
</p>

<p align="center">
  <a href="https://github.com/MarceloClaro/ASSISTENTE-SHI/releases/latest">
    <img src="https://img.shields.io/github/v/release/MarceloClaro/ASSISTENTE-SHI?style=flat-square&logo=github&color=blue" alt="Release"/>
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/Licença-MIT-green.svg?style=flat-square" alt="License: MIT"/>
  </a>
  <a href="https://github.com/MarceloClaro/ASSISTENTE-SHI/stargazers">
    <img src="https://img.shields.io/github/stars/MarceloClaro/ASSISTENTE-SHI?style=flat-square&logo=github" alt="Estrelas"/>
  </a>
</p>

**Português Brasileiro** | [中文简体](README.zh-CN.md) | [English](README.en.md)

## 📋 Sobre o Projeto

**ASSISTENTE-SHI** é um cliente Python avançado de inteligência artificial (IA) baseado na arquitetura do Xiaozhi. Ele permite interação por voz com IA de forma natural e fluida, oferecendo suporte completo a múltiplas ferramentas MCP, integração IoT, processamento de áudio de alta qualidade e interface gráfica moderna.

Este é um fork personalizado do [py-xiaozhi](https://github.com/huangjunsen0406/py-xiaozhi) com melhorias, correções e otimizações específicas.

## ✨ Características Principais

### 🖼️ Interface do Sistema

![Interface GUI do ASSISTENTE-SHI](https://github.com/huangjunsen0406/py-xiaozhi/blob/main/documents/docs/guide/images/%E7%B3%BB%E7%BB%9F%E7%95%8C%E9%9D%A2.png?raw=true)

*A interface moderna PyQt5 com suporte a múltiplas expressões e interação fluida com IA.*

### 🎯 Funcionalidades de IA

- **Interação por Voz com IA**: Suporte completo a entrada de voz, reconhecimento de fala e resposta inteligente
- **Visão Computacional**: Reconhecimento e processamento de imagens com capacidades multi-modal
- **Despertar Inteligente**: Múltiplas palavras-chave de ativação (configuráveis)
- **Modo de Conversa Contínua**: Experiência de conversa fluida e natural

## 🧠 Modelo de IA

### Configuração do Modelo LLM

O ASSISTENTE-SHI utiliza **LLaVA + Ollama** como modelo de IA principal, oferecendo visão computacional **100% gratuita e local**.

#### ⭐ **LLaVA (Ollama Local) - MODELO PRINCIPAL**

```
📌 Status: Ativo e Funcional
🔐 Modelo: LLaVA 1.6 (7B/13B/34B - Configurável)
🖥️ Execução: 100% Local (sem internet necessária)
💰 Custo: Completamente Gratuito (Open Source)
⚙️ Requisitos: Ollama instalado + 8GB+ RAM + CPU rápida
```

**Vantagens Técnicas do LLaVA + Ollama:**
- ✅ **100% Gratuito** - Sem custos operacionais
- ✅ **Privacidade Total** - Execução completamente local
- ✅ **Sem Dependência de Internet** - Funciona offline
- ✅ **Sem Limite de Tokens** - Uso ilimitado
- ✅ **Sem Rate Limiting** - Velocidade consistente
- ✅ **Customizável** - Modelos ajustáveis (7B/13B/34B)
- ✅ **Open Source** - Código aberto e auditável
- ✅ **Visão Computacional** - Análise de imagens integrada
- ✅ **Contexto Expandido** - Suporta até 4K+ tokens
- ✅ **Sem Autenticação** - Funciona sem credenciais
- ✅ **Multi-Modal** - Suporta texto + imagens

**⚠️ LIMITAÇÕES IMPORTANTES DO LLaVA:**
- ❌ **REQUER HARDWARE POTENTE** - CPU rápida obrigatória
- ❌ **Tempo de processamento: 40-90s** - Pode exceder timeout do servidor (60s)
- ❌ **Incompatível com hardware lento** - Causa desconexão por timeout
- ⚠️ Requer instalação prévia do Ollama
- ⚠️ Modelos maiores (34B) precisam 24GB+ RAM
- ⚠️ **Xiaozhi limita execução a 60 segundos** - Hardware lento causa falha

**Instalação do Ollama + LLaVA:**

```bash
# 1. Instalar Ollama
# Windows: https://ollama.com/download/windows
# macOS: https://ollama.com/download/mac
# Linux: curl -fsSL https://ollama.ai/install.sh | sh

# 2. Baixar modelo LLaVA
ollama pull llava:7b          # Rápido, 4GB RAM
# ou
ollama pull llava:13b         # Mais preciso, 8GB RAM
# ou
ollama pull llava:34b         # Mais poderoso, 24GB RAM

# 3. Iniciar serviço Ollama (roda em localhost:11434)
ollama serve
```

**Configuração (config/config.json):**

```json
{
  "CAMERA": {
    "camera_index": 0,
    "frame_width": 640,
    "frame_height": 480,
    "fps": 30,
    "Local_VL_url": "http://localhost:11434",
    "VLapi_key": "ollama",
    "models": "llava:7b"
  }
}
```

---

### 📊 Especificações dos Modelos LLaVA

| Modelo | RAM | Tempo Médio | Qualidade | Recomendado Para |
|--------|-----|-------------|-----------|------------------|
| **llava:7b** | 4GB | ⚡ 40-60s | ⭐⭐⭐ | Hardware potente |
| **llava:13b** | 8GB | ⚡⚡ 60-90s | ⭐⭐⭐⭐ | Máquinas rápidas |
| **llava:34b** | 24GB | ⚡⚡⚡ >90s | ⭐⭐⭐⭐⭐ | Servidores dedicados |

⚠️ **AVISO CRÍTICO**: Todos os modelos LLaVA podem exceder o limite de 60 segundos do servidor Xiaozhi em hardware comum. Considere usar API online se tiver problemas de timeout.

---

### 🔄 Estratégia de Fallback (REMOVIDA)

**NOTA**: A estratégia de fallback automático GLM-4V → LLaVA foi removida. O sistema agora usa **apenas LLaVA local** para análise de imagens.

---

### 💡 Recomendação de Uso

**⚠️ HARDWARE LENTO?** Use API online (OpenAI/Google Vision):
- Respostas em 2-5 segundos garantidas
- Não excede timeout do servidor
- Custo: ~$0.01-0.05 por imagem

**🏠 Hardware Potente (CPU Rápido)?** Use LLaVA Local:
- Gratuito, sem limite de uso
- Execução offline garantida
- **Requer completar análise em <60s**

**⚠️ PROBLEMA CONHECIDO:**
Em hardware comum/lento, LLaVA pode levar 60-90+ segundos para processar, causando desconexão do servidor Xiaozhi (limite de 60s). Nesses casos, recomenda-se usar API online paga.

---

## 🔌 Endpoint MCP (Model Context Protocol)

### Informações de Conexão do Agente

```
🔗 Protocolo: WebSocket Seguro (WSS)
📊 Status: Não Conectado
🎯 Endpoint: wss://api.xiaozhi.me/mcp/
🔐 Autenticação: JWT Token
```

### URL Completa do Endpoint

```
wss://api.xiaozhi.me/mcp/?token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjc2NjcwOSwiYWdlbnRJZCI6MTMzMzQ2NywiZW5kcG9pbnRJZCI6ImFnZW50XzEzMzM0NjciLCJwdXJwb3NlIjoibWNwLWVuZHBvaW50IiwiaWF0IjoxNzY4MjcxMDQ3LCJleHAiOjE3OTk4Mjg2NDd9.ceUsIEiALsqTY8L4lfYncUe26KKB92ITCmc_AYZWqUOZ9ChJZWv97UvYiQLAavsFTc7CB0n0xkpVZvqwoMnWfg
```

### Detalhes do Token JWT

**Headers:**
```json
{
  "alg": "ES256",
  "typ": "JWT"
}
```

**Seu token é como uma senha - guarde com segurança!** ✨

A conexão acontece automaticamente quando você inicia o assistente. Você não precisa fazer nada além de colocar o token no arquivo de configuração.

---

## ⭐ Vantagens de Usar Xiaozhi.me

### 🆓 Partes GRATUITAS do Serviço Xiaozhi.me

O ASSISTENTE-SHI utiliza o serviço **xiaozhi.me de forma gratuita** nas seguintes áreas:

#### **1. Acesso ao Endpoint MCP (Gratuito)**
```
✅ Conexão WebSocket: wss://api.xiaozhi.me/mcp/
✅ Autenticação JWT: Fornecida gratuitamente
✅ Infraestrutura: Servidores xiaozhi.me
✅ Banda: Sem cobranças adicionais
✅ Suporte Técnico: Documentação e exemplos livres
```

#### **2. Ferramentas MCP Básicas (Gratuitas - Até Certo Uso)**

## 🎯 O que o ASSISTENTE-SHI faz?

O assistente oferece 32+ ferramentas prontas para usar:

- 📅 **Calendário** - Criar e gerenciar eventos
- 🎵 **Música** - Tocar suas músicas favoritas
- ⏱️ **Temporizadores** - Definir contagens regressivas
- 🖥️ **Controle do Sistema** - Mudar volume, abrir aplicativos
- 📸 **Câmera** - Tirar fotos e analisar imagens
- 🔍 **Busca na Web** - Pesquisar informações online
- 🗺️ **Mapas** - Encontrar locais e rotas
- E muito mais!

## 🚀 Como Começar em 5 Minutos

### 1️⃣ Pré-requisitos (Antes de Instalar)

Você precisa ter:
- 💻 **Windows 10+**, macOS 10.15+ ou Linux
- 🐍 **Python 3.9 a 3.12** instalado
- 🎤 **Microfone e alto-falante** funcionando
- 🌐 **Internet estável**
- 📀 **2GB de espaço em disco**

**Opcional (para análise de imagens):**
- 💾 4.5GB adicionais para modelo de visão (Ollama)

### 2️⃣ Clonar o Projeto

```bash
git clone https://github.com/MarceloClaro/ASSISTENTE-SHI.git
cd ASSISTENTE-SHI
```

### 3️⃣ Instalação Automática (Recomendado)

**Windows:**
```bash
start.bat
```

**Linux/macOS:**
```bash
chmod +x start.sh
./start.sh
```

O script instalará automaticamente tudo!

### 4️⃣ Obter Token de Acesso

1. Vá em [xiaozhi.me/console](https://xiaozhi.me/console)
2. Faça login ou crie uma conta
3. Vá em "Agents" → "Config"
4. Clique em "Generate Token" e copie
5. Cole no arquivo de configuração (`config/config.json`)

### 5️⃣ Iniciar o Assistente

```bash
python main.py --mode gui --protocol websocket
```

**Pronto!** 🎉 O assistente está rodando!

---

## 📖 Documentação e Guias

- **[Guia Completo VSCode (PT)](GUIA_VSCODE_PT.md)** - Configuração detalhada do VSCode
- **[Documentação Técnica](docs/)** - Arquitetura e desenvolvimento
- **[FAQ - Perguntas Frequentes](docs/FAQ.md)** - Dúvidas comuns

## 🏗️ Arquitetura Técnica

### Design de Arquitetura

- **Arquitetura Orientada por Eventos**: Loop assíncrono asyncio com processamento de alta concorrência
- **Design em Camadas**: Separação clara entre aplicação, protocolo, dispositivos e UI
- **Padrão Singleton**: Componentes principais com gerenciamento centralizado de recursos
- **Arquitetura Plugável**: Sistema MCP e dispositivos IoT extensíveis

### Componentes Principais

- **Processamento de Áudio**: Opus, WebRTC AEC, reamostragem, gravação do sistema
- **Reconhecimento de Fala**: Sherpa-ONNX offline, VAD, detecção de palavra-chave
- **Protocolos**: WebSocket/MQTT dual, transmissão criptografada, reconexão automática
- **Sistema de Configuração**: Configuração em camadas, acesso por pontos, JSON/YAML

### Otimizações de Desempenho

- **Assincronismo Completo**: Sem operações bloqueantes
- **Gerenciamento de Memória**: Cache inteligente e coleta de lixo
- **Áudio de Baixa Latência**: Processamento em 5ms com gerenciamento de fila
- **Controle de Concorrência**: Pool de tarefas, semáforos, segurança de thread

## 📁 Estrutura do Projeto

```
ASSISTENTE-SHI/
├── main.py                          # Ponto de entrada
├── src/
│   ├── application.py               # Lógica central
│   ├── audio_codecs/                # Codificação de áudio
│   ├── audio_processing/            # Processamento de áudio
│   ├── core/                        # Componentes principais
│   ├── display/                     # Camada abstrata de interface
│   ├── iot/                         # Gerenciamento IoT
│   ├── mcp/                         # Sistema de ferramentas MCP
│   ├── protocols/                   # Protocolos de comunicação
│   ├── utils/                       # Funções utilitárias
│   └── views/                       # Componentes de UI
├── config/                          # Arquivos de configuração
├── models/                          # Modelos de IA
├── logs/                            # Arquivos de log
└── requirements.txt                 # Dependências Python
```

## 🔄 Fluxos e Diagramas do Projeto

### 1️⃣ Fluxo de Estados da Aplicação

```
                              INICIALIZAÇÃO DO SISTEMA
                                      |
                                      v
                          +-------+----------+
                          |   CARREGANDO    |
                          | Configurações   |
                          +-------+----------+
                                  |
                                  v
                          +-------+----------+
                          |   ATIVANDO      |
                          | Dispositivo     |
                          +-------+----------+
                                  |
                                  v
╔══════════════════════════════════════════════════════════╗
║                   MÁQUINA DE ESTADOS PRINCIPAL           ║
║                                                          ║
║     (Palavra-chave) ou (Botão GUI)                      ║
║                      |                                   ║
║                      v                                   ║
║        +---------+        +---------------+              ║
║        | OCIOSO  |------> | CONECTANDO    |              ║
║        +---------+        +-----+---------+              ║
║            ^                    |                        ║
║            |                    |                        ║
║  Encerrou  |                    v                        ║
║   Áudio    |         +----------+----------+              ║
║            |         | ESCUTANDO / AGUARD. |              ║
║            |         +----------+----------+              ║
║            |                    |                        ║
║            |      (Áudio detectado)                      ║
║            |         VAD ativado                         ║
║            |                    |                        ║
║            |                    v                        ║
║            |         +----------+----------+              ║
║            |         | PROCESSANDO ÁUDIO   |              ║
║            |         | (STT em andamento)  |              ║
║            |         +----------+----------+              ║
║            |                    |                        ║
║            |    (STT completo)  |                        ║
║            |                    v                        ║
║            |         +----------+----------+              ║
║            +-------- | CONVERSANDO / LLM  |              ║
║              Fim     | (Processando IA)    |              ║
║                      +----------+----------+              ║
║                                 |                        ║
║                    (Resposta pronta)                     ║
║                                 |                        ║
║                                 v                        ║
║                      +----------+----------+              ║
║                      | REPRODUZINDO ÁUDIO  |              ║
║                      | (TTS em andamento)  |              ║
║                      +----------+----------+              ║
║                                 |                        ║
║                    (Reprodução finalizada)              ║
║                                 |                        ║
║                                 v                        ║
║                      +---------+--------+                ║
║                      | Retorna ESCUTANDO |               ║
║                      | (próxima iteração) |              ║
║                      +-------------------+               ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

### 2️⃣ Arquitetura em Camadas do Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                    CAMADA DE APRESENTAÇÃO                       │
│  ┌──────────────┐                      ┌──────────────┐         │
│  │ Interface    │                      │ Linha de     │         │
│  │ Gráfica      │                      │ Comando      │         │
│  │ (PyQt5)      │                      │ (CLI)        │         │
│  └──────┬───────┘                      └──────┬───────┘         │
│         │                                     │                 │
└─────────┼─────────────────────────────────────┼─────────────────┘
          │                                     │
┌─────────┼─────────────────────────────────────┼─────────────────┐
│ CAMADA  │  Gerenciador de Aplicação (Application.py)           │
│  DE     │  - Controle de Estado                                │
│LÓGICA   │  - Orquestração de Componentes                       │
│         │  - Ciclo de Vida da Aplicação                        │
│         │                                     │                 │
└─────────┼─────────────────────────────────────┼─────────────────┘
          │
┌─────────┴─────────────────────────────────────────────────────────┐
│              CAMADA DE PROCESSAMENTO / NEGÓCIO                    │
│                                                                   │
│  ┌────────────────────┐  ┌────────────────────┐                 │
│  │ Sistema de Audio   │  │ Sistema MCP        │                 │
│  │ - AudioCodec       │  │ - 32+ Ferramentas  │                 │
│  │ - VAD Detector     │  │ - Calendário       │                 │
│  │ - Wake Word        │  │ - Música           │                 │
│  │ - AEC              │  │ - Câmera           │                 │
│  └────────────────────┘  │ - Sistema          │                 │
│                           │ - Mapas, etc      │                 │
│  ┌────────────────────┐  │                    │                 │
│  │ Sistema IoT        │  │                    │                 │
│  │ - Thing Manager    │  │                    │                 │
│  │ - Device Manager   │  │                    │                 │
│  │ - Property Sync    │  │                    │                 │
│  └────────────────────┘  └────────────────────┘                 │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
          │
┌─────────┴────────────────────────────────────────────────────────┐
│              CAMADA DE PROTOCOLO / COMUNICAÇÃO                   │
│                                                                  │
│  ┌─────────────────────────┐  ┌──────────────────────────┐     │
│  │ WebSocket Protocol      │  │ MQTT Protocol            │     │
│  │ - SSL/TLS Encryption    │  │ - Message Queue          │     │
│  │ - Handshake             │  │ - Pub/Sub                │     │
│  │ - Binary Frames         │  │ - Auto Reconnect         │     │
│  │ - Error Recovery        │  │ - Topic Management       │     │
│  └─────────────────────────┘  └──────────────────────────┘     │
│                                                                  │
└────────────────┬─────────────────────────────────────────────────┘
                 │
         ┌───────┴────────┐
         │                │
         v                v
    ┌──────────────┐  ┌──────────────┐
    │ Servidor API │  │ Servidor MQTT │
    │ (Remoto)     │  │ (Remoto)      │
    └──────────────┘  └──────────────┘
```

### 3️⃣ Fluxo de Processamento de Áudio

```
┌──────────────────────────────────────────────────────────────────┐
│                    ENTRADA DE ÁUDIO (MIC)                        │
│                    (48kHz, 2 canais)                            │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         v
┌──────────────────────────────────────────────────────────────────┐
│                   PROCESSAMENTO DE ENTRADA                       │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ 1. Mistura de Canais: 2ch → 1ch                           │  │
│  └────────────────────────────────────────────────────────────┘  │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         v
┌──────────────────────────────────────────────────────────────────┐
│              Reamostragem: 48kHz → 16kHz                         │
│              (Compatível com processamento de fala)              │
└────────────────────────┬─────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         v               v               v
    ┌─────────┐  ┌──────────┐  ┌──────────────┐
    │   VAD   │  │ Wake Word│  │  Streaming   │
    │Detector │  │ Detection│  │ para Servidor│
    │(Detecção│  │(Detecção │  │              │
    │ Atividade)  │Palavra)  │  │              │
    └────┬────┘  └────┬─────┘  └──────┬───────┘
         │            │               │
         └────────────┼───────────────┘
                      │
                      v
         ┌────────────────────────┐
         │ Fila de Áudio Principal│
         │ (BufferManager)        │
         └────────┬───────────────┘
                  │
      ┌───────────┼───────────────┐
      │           │               │
      v           v               v
  ┌────────┐  ┌────────┐  ┌────────────┐
  │  AEC   │  │ Opus   │  │ Enviar para│
  │(Echo   │  │Encoder │  │ IA/Servidor│
  │Cancel) │  │        │  │            │
  └────┬───┘  └───┬────┘  └────┬───────┘
       │          │            │
       └──────────┼────────────┘
                  │
                  v
         ┌──────────────────────┐
         │ WebSocket/MQTT       │
         │ (Envio de Áudio)     │
         └──────────────────────┘
```

### 4️⃣ Arquitetura do Sistema MCP (Model Context Protocol)

```
┌─────────────────────────────────────────────────────────────────┐
│                    SERVIDOR MCP                                 │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              MCPServer (Gerenciador Central)               │ │
│  │  - Registra 32+ ferramentas                               │ │
│  │  - Processa requisições JSON-RPC                          │ │
│  │  - Valida parâmetros                                      │ │
│  │  - Retorna resultados                                     │ │
│  └────────┬─────────────────────────────────────────────────┘ │
│           │                                                    │
│  ┌────────┴────────────────────────────────────────────────┐  │
│  │              FERRAMENTAS REGISTRADAS (32+)               │  │
│  │                                                          │  │
│  │ ┌──────────────────────────────────────────────────┐   │  │
│  │ │ CONTROLE DO SISTEMA (4 ferramentas)             │   │  │
│  │ │ - set_volume()       - get_volume()             │   │  │
│  │ │ - launch()           - list_running()           │   │  │
│  │ └──────────────────────────────────────────────────┘   │  │
│  │                                                          │  │
│  │ ┌──────────────────────────────────────────────────┐   │  │
│  │ │ GERENCIADOR DE CALENDÁRIO (7 ferramentas)       │   │  │
│  │ │ - create_event()     - get_events()             │   │  │
│  │ │ - update_event()     - delete_event()           │   │  │
│  │ │ - get_upcoming_events()                         │   │  │
│  │ │ - get_categories()                              │   │  │
│  │ └──────────────────────────────────────────────────┘   │  │
│  │                                                          │  │
│  │ ┌──────────────────────────────────────────────────┐   │  │
│  │ │ REPRODUTOR DE MÚSICA (7 ferramentas)            │   │  │
│  │ │ - search_and_play()  - pause()                  │   │  │
│  │ │ - resume()           - stop()                   │   │  │
│  │ │ - seek()             - get_lyrics()             │   │  │
│  │ │ - get_local_playlist()                          │   │  │
│  │ └──────────────────────────────────────────────────┘   │  │
│  │                                                          │  │
│  │ ┌──────────────────────────────────────────────────┐   │  │
│  │ │ GERENCIADOR DE TEMPORIZADORES (3 ferramentas)   │   │  │
│  │ │ - start_countdown()  - cancel_countdown()       │   │  │
│  │ │ - get_active_timers()                           │   │  │
│  │ └──────────────────────────────────────────────────┘   │  │
│  │                                                          │  │
│  │ ┌──────────────────────────────────────────────────┐   │  │
│  │ │ VISÃO COMPUTACIONAL (2 ferramentas)             │   │  │
│  │ │ - take_photo()       - take_screenshot()        │   │  │
│  │ └──────────────────────────────────────────────────┘   │  │
│  │                                                          │  │
│  │ ┌──────────────────────────────────────────────────┐   │  │
│  │ │ ASTROLOGIA BA ZI (6 ferramentas)                │   │  │
│  │ │ - get_bazi_detail()                             │   │  │
│  │ │ - analyze_marriage_compatibility()              │   │  │
│  │ │ - get_chinese_calendar()                        │   │  │
│  │ │ - build_bazi_from_lunar_datetime()              │   │  │
│  │ └──────────────────────────────────────────────────┘   │  │
│  │                                                          │  │
│  │ + 3 ferramentas adicionais em desenvolvimento...        │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
└──────────────┬──────────────────────────────────────────────────┘
               │
      ┌────────┴────────┐
      │                 │
      v                 v
 ┌─────────────┐  ┌─────────────┐
 │  IA Remota  │  │  IoT Things │
 │  (OpenAI,   │  │  (Devices)  │
 │   Zhipu)    │  │             │
 └─────────────┘  └─────────────┘
```

### 5️⃣ Fluxo Completo de Interação Usuário → IA → Resposta

```
┌──────────────────────────────────────────────────────────────────┐
│                        USUÁRIO                                   │
│             (Fala próximo ao microfone)                         │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         v (Áudio capturado)
┌──────────────────────────────────────────────────────────────────┐
│              1. CAPTURA E PRÉ-PROCESSAMENTO                      │
│  - AudioCodec (Mistura, Reamostragem)                           │
│  - VAD (Detecção de Atividade de Fala)                          │
│  - AEC (Cancelamento de Eco)                                    │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         v
┌──────────────────────────────────────────────────────────────────┐
│         2. ENVIO PARA SERVIDOR (WebSocket/MQTT)                 │
│  - Serialização JSON                                             │
│  - Criptografia (WSS)                                           │
│  - Compressão de áudio                                          │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         v
┌──────────────────────────────────────────────────────────────────┐
│            3. PROCESSAMENTO NO SERVIDOR REMOTO                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ STT (Speech-to-Text)                                     │  │
│  │ Converte áudio → Texto                                  │  │
│  │ (Engine OpenAI/Zhipu)                                   │  │
│  └──────────┬───────────────────────────────────────────────┘  │
│             │ "Como está o tempo em São Paulo?"                │
│             v                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ LLM (Large Language Model)                               │  │
│  │ Processa texto e gera resposta                          │  │
│  │ Pode chamar MCP tools conforme necessário               │  │
│  └──────────┬───────────────────────────────────────────────┘  │
│             │ "A temperatura está 28°C, ensolarado"             │
│             v                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ TTS (Text-to-Speech)                                     │  │
│  │ Converte texto → Áudio                                  │  │
│  │ (Engine nativa do servidor)                             │  │
│  └──────────┬───────────────────────────────────────────────┘  │
│             │                                                   │
└─────────────┼───────────────────────────────────────────────────┘
              │
              v (Áudio de resposta)
┌──────────────────────────────────────────────────────────────────┐
│         4. RECEPÇÃO DO ÁUDIO DE RESPOSTA                        │
│  - Desserialização JSON                                         │
│  - Descriptografia                                              │
│  - Descompressão de áudio                                       │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         v
┌──────────────────────────────────────────────────────────────────┐
│         5. PROCESSAMENTO DE SAÍDA DE ÁUDIO                      │
│  - AudioCodec (Reamostragem: 24kHz → 44100Hz)                  │
│  - Opus Decode (se necessário)                                  │
│  - Normalização de volume                                       │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         v
┌──────────────────────────────────────────────────────────────────┐
│       6. REPRODUÇÃO DE ÁUDIO (Speaker)                          │
│  - Streaming para saída de áudio                                │
│  - Sincronização com interface                                  │
│  - Feedback visual (animação)                                   │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         v
┌──────────────────────────────────────────────────────────────────┐
│                 USUÁRIO OUVE A RESPOSTA                          │
│        (Sistema retorna ao estado ESCUTANDO)                    │
└──────────────────────────────────────────────────────────────────┘
```

### 6️⃣ Fluxo de Inicialização do Sistema

```
  python main.py --mode gui --protocol websocket
                         │
                         v
         ┌───────────────────────────────┐
         │ parse_args()                  │
         │ (Processar argumentos CLI)    │
         └────────┬────────────────────────┘
                  │
                  v
         ┌───────────────────────────────┐
         │ setup_logging()               │
         │ (Iniciar sistema de logs)     │
         └────────┬────────────────────────┘
                  │
                  v
         ┌───────────────────────────────┐
         │ Detectar Wayland/X11          │
         │ (Configurar variáveis QT)     │
         └────────┬────────────────────────┘
                  │
                  v
         ┌───────────────────────────────┐
         │ Criar qasync event loop       │
         │ (Loop asyncio para Qt5)       │
         └────────┬────────────────────────┘
                  │
                  v
    ┌────────────────────────────────────┐
    │ handle_activation()                │
    │ (Processar ativação do dispositivo)│
    │                                    │
    │ 1. SystemInitializer init          │
    │ 2. Gerar Fingerprint               │
    │ 3. Validar/Criar efuse.json        │
    │ 4. Buscar configuração OTA         │
    │ 5. Verificar WebSocket/MQTT        │
    │ 6. Retornar resultado              │
    └────────┬──────────────────────────┘
             │ (Se ativação falhou)
             v
      ┌──────────────────┐
      │ Encerrar programa│
      │ (Exit code: 1)   │
      └──────────────────┘

    (Se ativação sucedeu)
             │
             v
    ┌────────────────────────────────────┐
    │ Application.get_instance()         │
    │ (Obter instância singleton)        │
    └────────┬──────────────────────────┘
             │
             v
    ┌────────────────────────────────────┐
    │ app.run(mode, protocol)            │
    │                                    │
    │ 1. Inicializar componentes         │
    │ 2. Carregar configurações          │
    │ 3. Inicializar protocolos          │
    │ 4. Registrar ferramentas MCP       │
    │ 5. Iniciar processamento de áudio  │
    │ 6. Abrir interface (GUI/CLI)       │
    │ 7. Entrar no loop de eventos       │
    │                                    │
    └────────┬──────────────────────────┘
             │
             v
    ┌────────────────────────────────────┐
    │ APLICAÇÃO RODANDO                  │
    │ (Aguardando eventos do usuário)    │
    └────────┬──────────────────────────┘
             │
       (Usuário pressiona Ctrl+C)
             │
             v
    ┌────────────────────────────────────┐
    │ Cleanup / Shutdown                 │
    │ 1. Fechar conexões                 │
    │ 2. Parar processamento de áudio    │
    │ 3. Salvar configurações            │
    │ 4. Liberar recursos                │
    │ 5. Encerrar programa               │
    └────────────────────────────────────┘
```

### 7️⃣ Fluxo de Protocolo de Comunicação

```
┌──────────────────────────────────────────────────────────────────┐
│                    ESCOLHA DE PROTOCOLO                          │
└────────────────┬──────────────────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
        v                 v
┌────────────────┐  ┌──────────────────┐
│ WebSocket      │  │ MQTT             │
│ wss://api...   │  │ mqtt://broker... │
└────────┬───────┘  └────────┬─────────┘
         │                   │
         v                   v
  ┌──────────────┐   ┌──────────────┐
  │ Handshake    │   │ Connect      │
  │ TLS/SSL      │   │ CONNACK      │
  │ Upgrade HTTP │   │              │
  └──────┬───────┘   └──────┬───────┘
         │                  │
         v                  v
  ┌──────────────┐   ┌──────────────┐
  │ Autenticar   │   │ Subscribe    │
  │ Token JWT    │   │ Topics       │
  └──────┬───────┘   └──────┬───────┘
         │                  │
         v                  v
  ┌──────────────┐   ┌──────────────┐
  │ Send/Receive │   │ Pub/Sub      │
  │ Binary Frames│   │ Messages     │
  │ (Áudio)      │   │              │
  └──────┬───────┘   └──────┬───────┘
         │                  │
         v                  v
  ┌──────────────┐   ┌──────────────┐
  │ Heartbeat    │   │ Keep Alive   │
  │ (PING/PONG)  │   │ (PINGREQ)    │
  └──────┬───────┘   └──────┬───────┘
         │                  │
         └────────┬─────────┘
                  │
                  v
         ┌──────────────────┐
         │ Conectado e Pronto│
         │ para Trocar Dados │
         └──────────────────┘
```

### 8️⃣ Fluxo de Sincronização de Estado IoT

```
┌──────────────────────────────────────────────────────────────────┐
│                    GERENCIADOR IoT (ThingManager)                │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                 DISPOSITIVOS VIRTUAIS                     │  │
│  │                                                          │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│  │  │ Lâmpada      │  │ Ar-cond.     │  │ Sensor Temp. │  │  │
│  │  │ - power      │  │ - temp       │  │ - temp_read  │  │  │
│  │  │ - brightness │  │ - mode       │  │ - humidity   │  │  │
│  │  │ - color      │  │ - fan_speed  │  │              │  │  │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │  │
│  │         │                 │                 │          │  │
│  └─────────┼─────────────────┼─────────────────┼──────────┘  │
│            │                 │                 │             │
│            └────────┬────────┴────────┬────────┘             │
│                     │                 │                      │
│              ┌──────v────────┐  ┌─────v──────┐              │
│              │ Sincronizar   │  │ Obter      │              │
│              │ Estado com    │  │ Estado     │              │
│              │ Servidor      │  │ Atual      │              │
│              └──────┬────────┘  └─────┬──────┘              │
│                     │                 │                     │
│                     v                 v                     │
│              ┌────────────────────────────┐                 │
│              │ Atualizar Cache Local      │                 │
│              │ (PropertyCache)            │                 │
│              └────────┬───────────────────┘                 │
│                       │                                     │
│            ┌──────────┴────────────┐                       │
│            │                       │                       │
│            v                       v                       │
│     ┌──────────────┐      ┌──────────────┐                │
│     │ Notificar    │      │ Atualizar UI │                │
│     │ Listeners    │      │ / Dashboard  │                │
│     └──────────────┘      └──────────────┘                │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## 🔄 Status Atual do Projeto

### ✅ Totalmente Funcional

- ✅ Interface GUI com WebSocket conectado
- ✅ 32 ferramentas MCP registradas e operacionais
- ✅ Processamento de áudio Opus em tempo real
- ✅ Interação com IA fluida e responsiva
- ✅ Captura de fotos via câmera
- ✅ Gerenciamento de calendário integrado
- ✅ Sistema de lembretes funcionando
- ✅ Injeção de contexto com delay de 2s (corrigido)
- ✅ Retorno de texto plano (sem double JSON encoding)

### ⚠️ Limitações Conhecidas

- ⚠️ **Análise de visão LLaVA**: Requer hardware potente (CPU rápido)
  - Tempo de processamento: 40-90+ segundos em hardware comum
  - **Causa timeout do servidor Xiaozhi (limite: 60s)**
  - **Solução**: Usar API online (OpenAI/Google Vision) em hardware lento
- ⚠️ Modelo de Wake Word ausente (Sherpa-ONNX) - wake word manual apenas

### 🐛 Bugs Corrigidos Recentemente

- ✅ **Bug #1**: TTS não vocalizava descrição (timing de 244ms) → Corrigido com delay de 2s
- ✅ **Bug #2**: Double JSON encoding causava escape de JSON → Corrigido retornando texto plano
- ✅ **Bug #3**: Timeout do Ollama → Configurado para 90s + 15 tokens (hardware lento ainda problemático)

## 🛠️ Desenvolvimento

### Executar em Diferentes Modos

```bash
# Modo GUI com WebSocket (padrão)
python main.py --mode gui --protocol websocket

# Modo CLI com MQTT
python main.py --mode cli --protocol mqtt

# Pular processo de ativação (debug)
python main.py --skip-activation
```

### Adicionando Novas Ferramentas MCP

Estenda a classe em `src/mcp/tools/` e registre em `mcp_server.py`.

### Adicionando Novos Dispositivos IoT

Implemente `Thing` base class em `src/iot/things/`.

## 📊 Estatísticas do Projeto

- **Ferramentas MCP**: 32+ funções integradas
- **Compatibilidade**: 3 sistemas operacionais
- **Protocolos**: 2 opções (WebSocket, MQTT)
- **Modos**: 2 interfaces (GUI, CLI)

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

[MIT License](LICENSE) - Veja o arquivo LICENSE para detalhes

## 🙏 Agradecimentos

Agradecimentos especiais ao projeto original [py-xiaozhi](https://github.com/huangjunsen0406/py-xiaozhi) e todos os contribuidores.

## 📧 Contato e Suporte

Para dúvidas, sugestões ou relatórios de bugs, abra uma issue no repositório GitHub.

---

**Última atualização**: 14 de janeiro de 2026  
**Status**: ✅ Operacional em modo GUI + WebSocket  
**Versão**: 1.1.0 (Com correções de timeout e encoding)
