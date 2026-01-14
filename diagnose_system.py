"""
Diagnóstico Completo do Sistema ASSISTENTE-SHI
Verifica todos os componentes e configurações.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class SystemDiagnostic:
    """Classe para diagnosticar o sistema completo."""
    
    def __init__(self):
        self.issues: List[Tuple[str, str, str]] = []  # (severity, component, message)
        self.passed: List[Tuple[str, str]] = []  # (component, message)
        
    def add_issue(self, severity: str, component: str, message: str):
        """Adiciona um problema encontrado."""
        self.issues.append((severity, component, message))
        
    def add_pass(self, component: str, message: str):
        """Adiciona verificação bem-sucedida."""
        self.passed.append((component, message))
    
    def check_wake_word_model(self) -> bool:
        """Verifica se o modelo Wake Word está presente."""
        print("\n[1/5] Verificando Modelo Wake Word...")
        
        models_dir = Path("models")
        required_files = [
            "encoder.onnx",
            "decoder.onnx",
            "joiner.onnx",
            "tokens.txt",
            "keywords.txt"
        ]
        
        if not models_dir.exists():
            self.add_issue(
                "ERROR",
                "Wake Word",
                f"Diretório de modelos não encontrado: {models_dir}"
            )
            print("  ❌ Diretório de modelos ausente")
            print(f"     Solução: Execute 'python download_wake_word_model.py'")
            return False
        
        missing_files = []
        for filename in required_files:
            file_path = models_dir / filename
            if not file_path.exists():
                missing_files.append(filename)
        
        if missing_files:
            self.add_issue(
                "ERROR",
                "Wake Word",
                f"Arquivos ausentes: {', '.join(missing_files)}"
            )
            print(f"  ❌ Arquivos ausentes: {', '.join(missing_files)}")
            print(f"     Solução: Execute 'python download_wake_word_model.py'")
            return False
        
        self.add_pass("Wake Word", "Todos os arquivos do modelo presentes")
        print("  ✅ Modelo Wake Word completo")
        return True
    
    def check_config_file(self) -> bool:
        """Verifica arquivo de configuração."""
        print("\n[2/5] Verificando Configuração...")
        
        config_path = Path("config/config.json")
        
        if not config_path.exists():
            self.add_issue(
                "ERROR",
                "Configuração",
                f"Arquivo de configuração não encontrado: {config_path}"
            )
            print("  ❌ config/config.json não encontrado")
            return False
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Verificar configurações críticas
            issues_found = []
            
            # Wake Word
            wake_word_options = config.get("WAKE_WORD_OPTIONS", {})
            if wake_word_options.get("USE_WAKE_WORD"):
                if not wake_word_options.get("MODEL_PATH"):
                    issues_found.append("MODEL_PATH não definido em WAKE_WORD_OPTIONS")
            
            # LLM
            llm_config = config.get("llm", {})
            if not llm_config:
                issues_found.append("Configuração 'llm' ausente")
            else:
                if not llm_config.get("api"):
                    issues_found.append("llm.api não definido")
                if llm_config.get("api") == "zhipu" and not llm_config.get("token"):
                    self.add_issue(
                        "WARNING",
                        "LLM",
                        "Token GLM-4V (Zhipu) não configurado - usando fallback"
                    )
                    print("  ⚠️  Token GLM-4V ausente (usará LLaVA local)")
            
            # MCP
            mcp_config = config.get("mcp", {})
            if not mcp_config:
                issues_found.append("Configuração 'mcp' ausente")
            
            if issues_found:
                for issue in issues_found:
                    self.add_issue("WARNING", "Configuração", issue)
                    print(f"  ⚠️  {issue}")
            else:
                self.add_pass("Configuração", "Arquivo válido e completo")
                print("  ✅ Configuração válida")
            
            return True
            
        except json.JSONDecodeError as e:
            self.add_issue(
                "ERROR",
                "Configuração",
                f"Erro ao parsear JSON: {e}"
            )
            print(f"  ❌ JSON inválido: {e}")
            return False
        except Exception as e:
            self.add_issue(
                "ERROR",
                "Configuração",
                f"Erro ao ler arquivo: {e}"
            )
            print(f"  ❌ Erro ao ler: {e}")
            return False
    
    def check_dependencies(self) -> bool:
        """Verifica dependências Python."""
        print("\n[3/5] Verificando Dependências Python...")
        
        required_packages = [
            ("PyQt5", "pyqt5"),
            ("aiohttp", "aiohttp"),
            ("websockets", "websockets"),
            ("opus", "opus"),
            ("sherpa_onnx", "sherpa-onnx"),
            ("cv2", "opencv-python"),
            ("numpy", "numpy"),
        ]
        
        missing = []
        for module_name, package_name in required_packages:
            try:
                __import__(module_name.lower().replace("-", "_"))
                print(f"  ✅ {package_name}")
            except ImportError:
                missing.append(package_name)
                print(f"  ❌ {package_name} ausente")
        
        if missing:
            self.add_issue(
                "ERROR",
                "Dependências",
                f"Pacotes ausentes: {', '.join(missing)}"
            )
            print(f"\n  Solução: pip install {' '.join(missing)}")
            return False
        
        self.add_pass("Dependências", "Todos os pacotes instalados")
        return True
    
    def check_vision_api(self) -> bool:
        """Verifica configuração da Vision API."""
        print("\n[4/5] Verificando Vision API...")
        
        config_path = Path("config/config.json")
        if not config_path.exists():
            print("  ⏭️  Pulando (config.json ausente)")
            return True
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            llm_config = config.get("llm", {})
            api_type = llm_config.get("api", "")
            
            if api_type == "zhipu":
                token = llm_config.get("token", "")
                if not token or token == "d656b80e-4d21-46d6-a32e-74048bf28a47":
                    self.add_issue(
                        "WARNING",
                        "Vision API",
                        "Token GLM-4V padrão/inválido - sistema usará LLaVA local"
                    )
                    print("  ⚠️  Token GLM-4V inválido")
                    print("     Fallback: LLaVA (Ollama local)")
                    print("     Instale: https://ollama.com/")
                    print("     Execute: ollama pull llava:7b")
                else:
                    self.add_pass("Vision API", "Token GLM-4V configurado")
                    print("  ✅ Token GLM-4V presente")
            elif api_type == "ollama":
                self.add_pass("Vision API", "Configurado para Ollama local")
                print("  ✅ Ollama configurado (gratuito)")
            else:
                self.add_issue(
                    "WARNING",
                    "Vision API",
                    f"API desconhecida: {api_type}"
                )
                print(f"  ⚠️  API desconhecida: {api_type}")
            
            return True
            
        except Exception as e:
            self.add_issue(
                "WARNING",
                "Vision API",
                f"Erro ao verificar: {e}"
            )
            print(f"  ⚠️  Erro ao verificar: {e}")
            return True
    
    def check_network_connectivity(self) -> bool:
        """Verifica conectividade de rede."""
        print("\n[5/5] Verificando Conectividade...")
        
        try:
            import socket
            
            # Testar DNS
            socket.gethostbyname("api.xiaozhi.me")
            print("  ✅ DNS funcional")
            
            # Testar conexão HTTPS
            import urllib.request
            urllib.request.urlopen("https://api.xiaozhi.me", timeout=5)
            print("  ✅ Conexão HTTPS funcional")
            
            self.add_pass("Rede", "Conectividade OK")
            return True
            
        except Exception as e:
            self.add_issue(
                "WARNING",
                "Rede",
                f"Problemas de conectividade: {e}"
            )
            print(f"  ⚠️  Problemas de rede: {e}")
            print("     Sistema funcionará em modo local")
            return True
    
    def print_summary(self):
        """Imprime resumo do diagnóstico."""
        print("\n" + "=" * 70)
        print("RESUMO DO DIAGNÓSTICO")
        print("=" * 70)
        
        errors = [i for i in self.issues if i[0] == "ERROR"]
        warnings = [i for i in self.issues if i[0] == "WARNING"]
        
        print(f"\n✅ Verificações OK: {len(self.passed)}")
        print(f"⚠️  Avisos: {len(warnings)}")
        print(f"❌ Erros: {len(errors)}")
        
        if errors:
            print("\n" + "=" * 70)
            print("ERROS CRÍTICOS (devem ser corrigidos):")
            print("=" * 70)
            for severity, component, message in errors:
                print(f"\n❌ [{component}] {message}")
        
        if warnings:
            print("\n" + "=" * 70)
            print("AVISOS (sistema pode funcionar com limitações):")
            print("=" * 70)
            for severity, component, message in warnings:
                print(f"\n⚠️  [{component}] {message}")
        
        print("\n" + "=" * 70)
        if not errors:
            print("✅ SISTEMA PRONTO PARA EXECUÇÃO!")
            print("\nExecute: python main.py --mode gui --protocol websocket")
        else:
            print("❌ SISTEMA COM PROBLEMAS!")
            print("\nCorreja os erros antes de executar o sistema.")
        print("=" * 70 + "\n")
        
        return len(errors) == 0


def main():
    """Executa diagnóstico completo."""
    print("=" * 70)
    print("DIAGNÓSTICO DO SISTEMA ASSISTENTE-SHI")
    print("=" * 70)
    
    diag = SystemDiagnostic()
    
    # Executar todas as verificações
    diag.check_wake_word_model()
    diag.check_config_file()
    diag.check_dependencies()
    diag.check_vision_api()
    diag.check_network_connectivity()
    
    # Mostrar resumo
    success = diag.print_summary()
    
    return 0 if success else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nDiagnóstico interrompido pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nErro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
