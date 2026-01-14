@echo off
REM ========================================
REM  Script de Inicialização do Assistente
REM  Xiaozhi AI - Versão Windows
REM ========================================

echo.
echo =====================================
echo   XIAOZHI AI ASSISTANT - STARTUP
echo =====================================
echo.

REM Ativa ambiente virtual se existir
if exist .venv-1\Scripts\activate.bat (
    echo [INFO] Ativando ambiente virtual...
    call .venv-1\Scripts\activate.bat
) else if exist venv\Scripts\activate.bat (
    echo [INFO] Ativando ambiente virtual...
    call venv\Scripts\activate.bat
) else (
    echo [AVISO] Nenhum ambiente virtual encontrado
)

REM Verifica se Python está disponível
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não encontrado!
    echo Por favor, instale Python 3.9+ de python.org
    pause
    exit /b 1
)

echo.
echo [INFO] Verificando Ollama...

REM Verifica se Ollama está instalado
ollama --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ======================================
    echo  OLLAMA NAO INSTALADO
    echo ======================================
    echo.
    echo O Ollama e necessario para analise de imagens.
    echo Instalacao 100%% GRATUITA - Processamento Local
    echo.
    echo Opcoes:
    echo   1. Instalar automaticamente: python setup_ollama.py
    echo   2. Instalar manualmente: https://ollama.ai/download
    echo.
    
    set /p INSTALL="Deseja instalar automaticamente agora? (S/N): "
    if /i "%INSTALL%"=="S" (
        echo [INFO] Executando instalacao automatica do Ollama...
        python setup_ollama.py
        if errorlevel 1 (
            echo [ERRO] Falha na instalacao
            pause
            exit /b 1
        )
    ) else (
        echo [AVISO] Sistema iniciara sem suporte a analise de imagens
    )
) else (
    echo [OK] Ollama instalado
    
    REM Verifica se serviço está rodando
    curl -s http://localhost:11434/api/tags >nul 2>&1
    if errorlevel 1 (
        echo [INFO] Iniciando servico Ollama...
        start /b ollama serve
        timeout /t 3 /nobreak >nul
    )
    
    REM Verifica modelo LLaVA
    ollama list | findstr /i "llava" >nul
    if errorlevel 1 (
        echo [AVISO] Modelo LLaVA nao encontrado
        echo Para analise de imagens, execute: python setup_ollama.py
    ) else (
        echo [OK] Modelo LLaVA disponivel
    )
)

echo.
echo ======================================
echo  INICIANDO ASSISTENTE
echo ======================================
echo.

REM Inicia o assistente
python main.py --mode gui --protocol websocket

if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao iniciar assistente
    pause
)
