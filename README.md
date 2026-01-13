# ASSISTENTE-SHI - Xiaozhi AI Assistant 🤖

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

### 🎯 Funcionalidades de IA

- **Interação por Voz com IA**: Suporte completo a entrada de voz, reconhecimento de fala e resposta inteligente
- **Visão Computacional**: Reconhecimento e processamento de imagens com capacidades multi-modal
- **Despertar Inteligente**: Múltiplas palavras-chave de ativação (configuráveis)
- **Modo de Conversa Contínua**: Experiência de conversa fluida e natural

### 🔧 Ecossistema de Ferramentas MCP (32+ Ferramentas)

- **Controle de Sistema**: Monitoramento, gerenciamento de aplicativos, controle de volume
- **Gerenciador de Agenda**: Criar, consultar, atualizar, deletar eventos com lembretes inteligentes
- **Tarefas Agendadas**: Temporizadores com suporte a execução atrasada
- **Reprodutor de Música**: Busca online, controle de reprodução, letras, cache local
- **Consulta de Passagens Aéreas**: Integração com serviços de transporte
- **Busca na Web**: Pesquisa Bing e análise de conteúdo
- **Receitas**: Banco de dados rico de receitas com recomendações
- **Mapas**: Serviços de mapeamento com geocodificação, planejamento de rotas, busca por proximidade
- **Ba Zi (Astrologia Chinesa)**: Análise de compatibilidade matrimonial e calendário lunar
- **Câmera**: Captura de imagens e análise com IA

### 🏠 Integração IoT

- **Gerenciamento Unificado**: Arquitetura baseada em padrão Thing para controle de dispositivos
- **Controle de Casa Inteligente**: Luzes, volume, sensores de temperatura
- **Sincronização de Estado em Tempo Real**: Monitoramento contínuo com atualizações incrementais
- **Design Extensível**: Drivers modulares para novos dispositivos

### 🎵 Processamento de Áudio Avançado

- **Processamento Multinível**: Codec Opus, reamostragem em tempo real
- **Detecção de Atividade de Fala (VAD)**: Interrupção inteligente de áudio
- **Detecção de Palavra-Chave**: Modelos Sherpa-ONNX com suporte a pinyin
- **Gerenciamento de Stream**: Entradas/saídas independentes com recuperação de erros
- **Cancelamento de Eco**: Integração com módulo de processamento de áudio WebRTC
- **Gravação de Áudio do Sistema**: Captura de áudio do sistema operacional

### 🖥️ Interface do Usuário

- **Interface Gráfica**: GUI moderna baseada em PyQt5 com expressões e exibição de texto
- **Modo Linha de Comando**: CLI para ambientes sem GUI
- **Bandeja do Sistema**: Suporte para execução em background
- **Atalhos Globais**: Teclas de atalho personalizáveis
- **Painel de Configurações**: Interface completa para personalização

### 🔒 Segurança e Estabilidade

- **Transmissão de Áudio Criptografada**: Protocolo WSS seguro
- **Sistema de Ativação de Dispositivo**: Suporte a protocolos v1/v2
- **Recuperação de Erros**: Reconexão automática e tratamento robusto

### 🌐 Suporte Multiplataforma

- **Compatibilidade**: Windows 10+, macOS 10.15+, Linux
- **Protocolos**: WebSocket e MQTT
- **Modos**: GUI e CLI
- **Otimização**: Específica para cada plataforma

## 🚀 Início Rápido

### Requisitos do Sistema

**Mínimo:**
- Python 3.9 - 3.12
- Windows 10+, macOS 10.15+, ou Linux
- Microfone e alto-falante
- Conexão de internet estável

**Recomendado:**
- 8GB+ RAM
- CPU com suporte AVX
- 2GB espaço em disco
- Áudio com taxa de amostragem de 16kHz

### Instalação

```bash
# Clonar repositório
git clone https://github.com/MarceloClaro/ASSISTENTE-SHI.git
cd ASSISTENTE-SHI

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação (GUI)
python main.py --mode gui --protocol websocket

# Ou modo CLI
python main.py --mode cli
```

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

## 🔄 Status Atual

### ✅ Funcional

- ✅ Interface GUI com WebSocket
- ✅ 32 ferramentas MCP registradas
- ✅ Processamento de áudio Opus
- ✅ Interação com IA em tempo real
- ✅ Suporte a câmera (captura de fotos)
- ✅ Gerenciamento de calendário
- ✅ Sistema de lembretes

### ⚠️ Conhecido

- ⚠️ Modelo de Wake Word ausente (Sherpa-ONNX)
- ⚠️ API de Visão Remota retornando 404
- ⚠️ Timeout de conexão WebSocket após ~1 minuto em teste

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

**Última atualização**: 13 de janeiro de 2026
**Status**: ✅ Operacional em modo GUI + WebSocket
>>>>>>> master
