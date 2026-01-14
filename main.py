import argparse
import asyncio
import signal
import subprocess
import sys

from src.application import Application
from src.utils.logging_config import get_logger, setup_logging

logger = get_logger(__name__)


def check_ollama_setup():
    """
    Verifica se o Ollama está instalado e rodando.
    Se não estiver, oferece instalação automática.
    """
    try:
        # Verifica se ollama está instalado
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            raise FileNotFoundError("Ollama não encontrado")
        
        # Verifica se o serviço está rodando
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code != 200:
                raise ConnectionError("Serviço Ollama não está respondendo")
        except:
            logger.warning("⚠️  Serviço Ollama não está rodando")
            logger.info("Iniciando serviço Ollama...")
            
            # Tenta iniciar o serviço
            try:
                subprocess.Popen(
                    ["ollama", "serve"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                import time
                time.sleep(3)  # Aguarda inicialização
                logger.info("✅ Serviço Ollama iniciado")
            except Exception as e:
                logger.error(f"Erro ao iniciar serviço: {e}")
        
        # Verifica se o modelo LLaVA está disponível
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if "llava" not in result.stdout.lower():
            logger.warning("⚠️  Modelo LLaVA não encontrado")
            logger.info("Para análise de imagens, execute: python setup_ollama.py")
        else:
            logger.info("✅ Ollama e LLaVA configurados corretamente")
        
        return True
        
    except FileNotFoundError:
        logger.error("\n" + "="*60)
        logger.error("❌ OLLAMA NÃO INSTALADO")
        logger.error("="*60)
        logger.error("\nO Ollama é necessário para análise de imagens (100% gratuito).")
        logger.error("\nOpções:")
        logger.error("  1. Instalação automática: python setup_ollama.py")
        logger.error("  2. Instalação manual: https://ollama.ai/download")
        logger.error("\n" + "="*60 + "\n")
        
        # Pergunta se quer instalar automaticamente
        try:
            response = input("Deseja instalar o Ollama automaticamente agora? (s/N): ")
            if response.lower() in ['s', 'sim', 'y', 'yes']:
                logger.info("Executando instalação automática...")
                subprocess.run([sys.executable, "setup_ollama.py"], check=True)
                return True
            else:
                logger.warning("Sistema iniciará sem suporte a análise de imagens")
                return False
        except (KeyboardInterrupt, EOFError):
            logger.warning("\nInstalação cancelada. Sistema iniciará sem análise de imagens.")
            return False
    except Exception as e:
        logger.error(f"Erro ao verificar Ollama: {e}")
        return False


def parse_args():
    """
    Analisa argumentos da linha de comando.
    """
    parser = argparse.ArgumentParser(description="Cliente AI Xiaozhi")
    parser.add_argument(
        "--mode",
        choices=["gui", "cli"],
        default="gui",
        help="Modo de execução: gui(interface gráfica) ou cli(linha de comando)",
    )
    parser.add_argument(
        "--protocol",
        choices=["mqtt", "websocket"],
        default="websocket",
        help="Protocolo de comunicação: mqtt ou websocket",
    )
    parser.add_argument(
        "--skip-activation",
        action="store_true",
        help="Pular processo de ativação, iniciar aplicação diretamente (apenas para debug)",
    )
    return parser.parse_args()


async def handle_activation(mode: str) -> bool:
    """Processa o fluxo de ativação do dispositivo, depende do loop de eventos existente.

    Args:
        mode: Modo de execução, "gui" ou "cli"

    Returns:
        bool: Se a ativação foi bem-sucedida
    """
    try:
        from src.core.system_initializer import SystemInitializer

        logger.info("Iniciando verificação do processo de ativação do dispositivo...")

        system_initializer = SystemInitializer()
        # Usa processamento de ativação unificado dentro de SystemInitializer, adaptável para GUI/CLI
        result = await system_initializer.handle_activation_process(mode=mode)
        success = bool(result.get("is_activated", False))
        logger.info(f"Processo de ativação concluído, resultado: {success}")
        return success
    except Exception as e:
        logger.error(f"Exceção no processo de ativação: {e}", exc_info=True)
        return False


async def start_app(mode: str, protocol: str, skip_activation: bool) -> int:
    """
    Ponto de entrada unificado para iniciar a aplicação (executado no loop de eventos existente).
    """
    logger.info("Iniciando Cliente AI Xiaozhi")
    
    # Verifica instalação do Ollama antes de iniciar
    logger.info("\n🔍 Verificando dependências do sistema...")
    check_ollama_setup()

    # Processar fluxo de ativação
    if not skip_activation:
        activation_success = await handle_activation(mode)
        if not activation_success:
            logger.error("Falha na ativação do dispositivo, programa encerrado")
            return 1
    else:
        logger.warning("Pulando processo de ativação (modo de debug)")

    # Criar e iniciar aplicação
    app = Application.get_instance()
    return await app.run(mode=mode, protocol=protocol)


if __name__ == "__main__":
    exit_code = 1
    try:
        args = parse_args()
        setup_logging()

        # WaylandConfigurandoQt
        import os

        is_wayland = (
            os.environ.get("WAYLAND_DISPLAY")
            or os.environ.get("XDG_SESSION_TYPE") == "wayland"
        )

        if args.mode == "gui" and is_wayland:
            # EmWayland，QtUsandode
            if "QT_QPA_PLATFORM" not in os.environ:
                # Usandowayland，Falhaentãoparaxcb（X11）
                os.environ["QT_QPA_PLATFORM"] = "wayland;xcb"
                logger.info("Wayland：ConfigurandoQT_QPA_PLATFORM=wayland;xcb")

            # EmWayland  NãodeQt
            os.environ.setdefault("QT_WAYLAND_DISABLE_WINDOWDECORATION", "1")
            logger.info("WaylandConcluído，JáApp")

        # ConfigurandoProcessando： macOS de SIGTRAP，“trace trap”Processo
        try:
            if hasattr(signal, "SIGINT"):
                #  qasync/Qt Processando Ctrl+C；ou GUI Processando
                pass
            if hasattr(signal, "SIGTERM"):
                # Processo  paraFechandoCaminho
                pass
            if hasattr(signal, "SIGTRAP"):
                signal.signal(signal.SIGTRAP, signal.SIG_IGN)
        except Exception:
            # /NãoSuportadoConfigurando，
            pass

        if args.mode == "gui":
            # No modo GUI, main cria uniformemente QApplication e loop de eventos qasync
            try:
                import qasync
                from PyQt5.QtWidgets import QApplication
            except ImportError as e:
                logger.error(f"Modo GUI requer bibliotecas qasync e PyQt5: {e}")
                sys.exit(1)

            qt_app = QApplication.instance() or QApplication(sys.argv)

            loop = qasync.QEventLoop(qt_app)
            asyncio.set_event_loop(loop)
            logger.info("Loop de eventos qasync criado em main")

            # Garantir que fechar a última janela não saia automaticamente da aplicação, evitando parada prematura do loop de eventos
            try:
                qt_app.setQuitOnLastWindowClosed(False)
            except Exception:
                pass

            with loop:
                exit_code = loop.run_until_complete(
                    start_app(args.mode, args.protocol, args.skip_activation)
                )
        else:
            # Modo CLI usa loop de eventos asyncio padrão
            exit_code = asyncio.run(
                start_app(args.mode, args.protocol, args.skip_activation)
            )

    except KeyboardInterrupt:
        logger.info("Programa interrompido pelo usuário")
        exit_code = 0
    except Exception as e:
        logger.error(f"Programa encerrado com exceção: {e}", exc_info=True)
        exit_code = 1
    finally:
        sys.exit(exit_code)
