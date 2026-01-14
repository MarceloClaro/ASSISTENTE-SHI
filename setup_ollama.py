#!/usr/bin/env python3
"""
Script de Instalação Automática do Ollama
==========================================

Este script detecta o sistema operacional e instala o Ollama automaticamente,
além de fazer o download do modelo LLaVA necessário para análise de imagens.

Uso:
    python setup_ollama.py
"""

import os
import platform
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

# Cores para output no terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_banner():
    """Exibe banner inicial"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}")
    print("  🤖 INSTALADOR AUTOMÁTICO DO OLLAMA + LLaVA")
    print(f"{'='*60}{Colors.END}\n")

def print_step(message):
    """Imprime mensagem de passo"""
    print(f"{Colors.BLUE}▶{Colors.END} {message}")

def print_success(message):
    """Imprime mensagem de sucesso"""
    print(f"{Colors.GREEN}✅{Colors.END} {message}")

def print_warning(message):
    """Imprime mensagem de aviso"""
    print(f"{Colors.YELLOW}⚠️{Colors.END}  {message}")

def print_error(message):
    """Imprime mensagem de erro"""
    print(f"{Colors.RED}❌{Colors.END} {message}")

def check_ollama_installed():
    """Verifica se o Ollama já está instalado"""
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            return True, version
        return False, None
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False, None

def check_ollama_running():
    """Verifica se o Ollama está rodando"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False

def install_ollama_windows():
    """Instala Ollama no Windows"""
    print_step("Detectado: Windows")
    print_step("Baixando instalador do Ollama...")
    
    installer_path = Path.home() / "Downloads" / "OllamaSetup.exe"
    
    try:
        url = "https://ollama.ai/download/OllamaSetup.exe"
        urllib.request.urlretrieve(url, installer_path)
        print_success(f"Instalador baixado: {installer_path}")
        
        print_step("Executando instalador...")
        print_warning("ATENÇÃO: Siga as instruções do instalador que será aberto.")
        print_warning("Após a instalação, pressione Enter para continuar...")
        
        # Executa o instalador
        subprocess.Popen([str(installer_path)], shell=True)
        input("\nPressione Enter após concluir a instalação... ")
        
        return True
    except Exception as e:
        print_error(f"Erro ao baixar/instalar: {e}")
        print_warning("Instale manualmente: https://ollama.ai/download")
        return False

def install_ollama_macos():
    """Instala Ollama no macOS"""
    print_step("Detectado: macOS")
    
    # Verifica se Homebrew está instalado
    try:
        subprocess.run(["brew", "--version"], capture_output=True, check=True)
        has_brew = True
    except (FileNotFoundError, subprocess.CalledProcessError):
        has_brew = False
    
    if has_brew:
        print_step("Instalando via Homebrew...")
        try:
            subprocess.run(["brew", "install", "ollama"], check=True)
            print_success("Ollama instalado via Homebrew")
            return True
        except subprocess.CalledProcessError as e:
            print_error(f"Erro ao instalar via Homebrew: {e}")
    
    # Alternativa: download direto
    print_step("Baixando instalador do Ollama...")
    try:
        subprocess.run([
            "curl", "-fsSL", "https://ollama.ai/install.sh",
            "-o", "/tmp/ollama_install.sh"
        ], check=True)
        
        subprocess.run(["sh", "/tmp/ollama_install.sh"], check=True)
        print_success("Ollama instalado com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Erro na instalação: {e}")
        print_warning("Instale manualmente: https://ollama.ai/download")
        return False

def install_ollama_linux():
    """Instala Ollama no Linux"""
    print_step("Detectado: Linux")
    print_step("Executando script de instalação oficial...")
    
    try:
        subprocess.run([
            "curl", "-fsSL", "https://ollama.ai/install.sh"
        ], check=True, stdout=subprocess.PIPE)
        
        # Executa o script com sudo
        install_script = subprocess.run(
            ["curl", "-fsSL", "https://ollama.ai/install.sh"],
            capture_output=True,
            text=True,
            check=True
        )
        
        subprocess.run(
            ["sudo", "sh", "-c", install_script.stdout],
            check=True
        )
        
        print_success("Ollama instalado com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Erro na instalação: {e}")
        print_warning("Tente manualmente:")
        print("  curl -fsSL https://ollama.ai/install.sh | sh")
        return False

def start_ollama_service():
    """Inicia o serviço do Ollama"""
    print_step("Iniciando serviço do Ollama...")
    
    system = platform.system()
    
    try:
        if system == "Windows":
            # No Windows, Ollama inicia automaticamente após instalação
            # Tenta iniciar manualmente se não estiver rodando
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
            )
        elif system == "Darwin":  # macOS
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        elif system == "Linux":
            # Tenta usar systemd primeiro
            try:
                subprocess.run(["sudo", "systemctl", "start", "ollama"], check=True)
            except:
                # Fallback para execução direta
                subprocess.Popen(
                    ["ollama", "serve"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
        
        # Aguarda o serviço iniciar
        print("Aguardando serviço iniciar", end="")
        for _ in range(10):
            time.sleep(1)
            print(".", end="", flush=True)
            if check_ollama_running():
                print()
                print_success("Serviço Ollama iniciado")
                return True
        
        print()
        print_warning("Serviço pode não ter iniciado corretamente")
        return False
        
    except Exception as e:
        print_error(f"Erro ao iniciar serviço: {e}")
        return False

def download_llava_model():
    """Faz download do modelo LLaVA"""
    print_step("Baixando modelo LLaVA (7B) - isso pode demorar...")
    print_warning("Tamanho: ~4.5 GB - aguarde o download completo")
    
    try:
        # Executa o download do modelo
        process = subprocess.Popen(
            ["ollama", "pull", "llava:7b"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Mostra progresso
        for line in process.stdout:
            print(f"  {line.strip()}")
        
        process.wait()
        
        if process.returncode == 0:
            print_success("Modelo LLaVA baixado com sucesso!")
            return True
        else:
            print_error("Erro ao baixar modelo LLaVA")
            return False
            
    except Exception as e:
        print_error(f"Erro no download: {e}")
        return False

def verify_installation():
    """Verifica se tudo está funcionando"""
    print_step("Verificando instalação...")
    
    checks = {
        "Ollama instalado": False,
        "Serviço rodando": False,
        "Modelo LLaVA": False
    }
    
    # Verifica ollama
    installed, version = check_ollama_installed()
    checks["Ollama instalado"] = installed
    if installed:
        print(f"  ✓ Ollama {version}")
    
    # Verifica serviço
    checks["Serviço rodando"] = check_ollama_running()
    if checks["Serviço rodando"]:
        print("  ✓ Serviço ativo em http://localhost:11434")
    
    # Verifica modelo
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if "llava" in result.stdout.lower():
            checks["Modelo LLaVA"] = True
            print("  ✓ Modelo LLaVA disponível")
    except:
        pass
    
    all_ok = all(checks.values())
    
    if all_ok:
        print_success("\n🎉 Instalação completa e funcional!")
    else:
        print_warning("\n⚠️  Alguns componentes podem estar faltando:")
        for check, status in checks.items():
            if not status:
                print(f"  ✗ {check}")
    
    return all_ok

def main():
    """Função principal"""
    print_banner()
    
    # Detecta sistema operacional
    system = platform.system()
    
    # Verifica se já está instalado
    installed, version = check_ollama_installed()
    
    if installed:
        print_success(f"Ollama já instalado: {version}")
        
        # Verifica se está rodando
        if not check_ollama_running():
            print_warning("Serviço não está rodando")
            start_ollama_service()
        else:
            print_success("Serviço já está rodando")
        
        # Verifica modelo
        print_step("Verificando modelo LLaVA...")
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if "llava" not in result.stdout.lower():
                print_warning("Modelo LLaVA não encontrado")
                download_llava_model()
            else:
                print_success("Modelo LLaVA já instalado")
        except:
            print_warning("Não foi possível verificar modelos")
            download_llava_model()
    else:
        # Instala Ollama
        print_step("Ollama não encontrado. Iniciando instalação...")
        
        success = False
        if system == "Windows":
            success = install_ollama_windows()
        elif system == "Darwin":
            success = install_ollama_macos()
        elif system == "Linux":
            success = install_ollama_linux()
        else:
            print_error(f"Sistema operacional não suportado: {system}")
            return 1
        
        if not success:
            print_error("Falha na instalação")
            return 1
        
        # Inicia serviço
        start_ollama_service()
        
        # Baixa modelo
        download_llava_model()
    
    # Verificação final
    print()
    print(f"{Colors.BOLD}Verificação Final{Colors.END}")
    print("=" * 60)
    verify_installation()
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}Próximos passos:{Colors.END}")
    print("1. Execute o assistente: python main.py --mode gui")
    print("2. Use câmera para análise de imagens (100% gratuito e local)")
    print(f"3. Ollama rodando em: {Colors.BLUE}http://localhost:11434{Colors.END}\n")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Instalação cancelada pelo usuário{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Erro inesperado: {e}")
        sys.exit(1)
