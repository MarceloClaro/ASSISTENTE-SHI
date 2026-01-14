#!/bin/bash
# ========================================
#  Script de Inicialização do Assistente
#  Xiaozhi AI - Versão Linux/macOS
# ========================================

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "====================================="
echo "  XIAOZHI AI ASSISTANT - STARTUP"
echo "====================================="
echo ""

# Ativa ambiente virtual se existir
if [ -d ".venv-1" ]; then
    echo -e "${BLUE}[INFO]${NC} Ativando ambiente virtual..."
    source .venv-1/bin/activate
elif [ -d "venv" ]; then
    echo -e "${BLUE}[INFO]${NC} Ativando ambiente virtual..."
    source venv/bin/activate
else
    echo -e "${YELLOW}[AVISO]${NC} Nenhum ambiente virtual encontrado"
fi

# Verifica se Python está disponível
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERRO]${NC} Python3 não encontrado!"
    echo "Por favor, instale Python 3.9+ do python.org"
    exit 1
fi

echo ""
echo -e "${BLUE}[INFO]${NC} Verificando Ollama..."

# Verifica se Ollama está instalado
if ! command -v ollama &> /dev/null; then
    echo ""
    echo "======================================"
    echo "  OLLAMA NÃO INSTALADO"
    echo "======================================"
    echo ""
    echo "O Ollama é necessário para análise de imagens."
    echo "Instalação 100% GRATUITA - Processamento Local"
    echo ""
    echo "Opções:"
    echo "  1. Instalar automaticamente: python3 setup_ollama.py"
    echo "  2. Instalar manualmente: https://ollama.ai/download"
    echo ""
    
    read -p "Deseja instalar automaticamente agora? (s/N): " INSTALL
    if [[ "$INSTALL" =~ ^[sS]$ ]]; then
        echo -e "${BLUE}[INFO]${NC} Executando instalação automática do Ollama..."
        python3 setup_ollama.py
        if [ $? -ne 0 ]; then
            echo -e "${RED}[ERRO]${NC} Falha na instalação"
            exit 1
        fi
    else
        echo -e "${YELLOW}[AVISO]${NC} Sistema iniciará sem suporte a análise de imagens"
    fi
else
    echo -e "${GREEN}[OK]${NC} Ollama instalado"
    
    # Verifica se serviço está rodando
    if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo -e "${BLUE}[INFO]${NC} Iniciando serviço Ollama..."
        ollama serve > /dev/null 2>&1 &
        sleep 3
    fi
    
    # Verifica modelo LLaVA
    if ! ollama list | grep -qi "llava"; then
        echo -e "${YELLOW}[AVISO]${NC} Modelo LLaVA não encontrado"
        echo "Para análise de imagens, execute: python3 setup_ollama.py"
    else
        echo -e "${GREEN}[OK]${NC} Modelo LLaVA disponível"
    fi
fi

echo ""
echo "======================================"
echo "  INICIANDO ASSISTENTE"
echo "======================================"
echo ""

# Inicia o assistente
python3 main.py --mode gui --protocol websocket

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}[ERRO]${NC} Falha ao iniciar assistente"
    exit 1
fi
