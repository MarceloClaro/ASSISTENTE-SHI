#!/usr/bin/env python3
"""
Teste Completo da Câmera com LLaVA
===================================

Testa o fluxo completo:
1. Captura de foto da webcam
2. Análise com LLaVA (Ollama)
3. Geração de descrição em texto
4. Validação do resultado
"""

import sys
import os
import time
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from src.mcp.tools.camera.vl_camera import VLCamera
from src.utils.logging_config import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)


def test_camera_complete():
    """Teste completo: câmera + LLaVA + descrição"""
    
    print("\n" + "="*60)
    print("  TESTE COMPLETO - CÂMERA + VISÃO + OLLAMA")
    print("="*60 + "\n")
    
    try:
        # 1. Inicializar câmera
        print("📷 [1/4] Inicializando câmera...")
        camera = VLCamera()  # Sem parâmetros
        print("✅ Câmera inicializada\n")
        
        # 2. Capturar foto
        print("📸 [2/4] Capturando foto...")
        success = camera.capture()
        
        if not success:
            print("❌ Erro ao capturar foto")
            assert False
        
        print("✅ Foto capturada\n")
        
        # 3. Análise com LLaVA
        print("🤖 [3/4] Analisando imagem com LLaVA (Ollama)...")
        print("   Aguarde... (pode demorar 5-10 segundos)\n")
        
        question = "O que você vê nesta imagem? Descreva em português detalhadamente."
        description = camera.analyze(question=question, context="")
        
        if not description:
            print("❌ Nenhuma descrição gerada")
            assert False
        
        print("✅ Análise concluída!\n")
        
        # 4. Exibir resultado
        print("="*60)
        print("  RESULTADO DA ANÁLISE")
        print("="*60)
        print(f"\n{description}\n")
        print("="*60 + "\n")
        
        # 5. Validações
        print("🔍 [4/4] Validando resultado...")
        
        validations = {
            "Descrição não vazia": len(description) > 0,
            "Descrição com mais de 50 caracteres": len(description) > 50,
            "Captura bem-sucedida": success
        }
        
        all_ok = True
        for check, passed in validations.items():
            status = "✅" if passed else "❌"
            print(f"  {status} {check}")
            if not passed:
                all_ok = False
        
        print()
        
        if all_ok:
            print("🎉 TESTE COMPLETO: SUCESSO!")
            print(f"   Tamanho da descrição: {len(description)} caracteres")
        else:
            print("⚠️  TESTE COMPLETO: FALHOU (algumas validações)")
            assert False
        
    except Exception as e:
        print(f"\n❌ ERRO NO TESTE: {e}")
        import traceback
        traceback.print_exc()
        raise


def test_camera_no_ollama():
    """Teste quando Ollama não está disponível"""
    
    print("\n" + "="*60)
    print("  TESTE - FALLBACK SEM OLLAMA")
    print("="*60 + "\n")
    
    try:
        # Forçar URL inválida para testar fallback
        camera = VLCamera()  # Sem parâmetros
        camera.base_url = "http://localhost:99999"  # Porta inválida
        
        print("📷 Capturando foto (sem Ollama disponível)...")
        success = camera.capture()
        
        if success:
            print("✅ Foto capturada (modo fallback)")
        else:
            print("⚠️  Erro esperado")
            assert False
        
    except Exception as e:
        print(f"⚠️  Exceção esperada: {e}")
        raise


def main():
    """Função principal"""
    
    print("\n" + "🚀 "*20)
    print("     SUITE DE TESTES - CÂMERA + VISÃO COMPUTACIONAL")
    print("🚀 "*20 + "\n")
    
    # Criar diretório de output
    os.makedirs("test_output", exist_ok=True)
    
    results = {}
    
    # Teste 1: Fluxo completo
    print("\n" + "🧪 TESTE 1: FLUXO COMPLETO")
    results["completo"] = test_camera_complete()
    
    # Aguardar um pouco
    time.sleep(2)
    
    # Teste 2: Fallback
    print("\n" + "🧪 TESTE 2: FALLBACK SEM OLLAMA")
    results["fallback"] = test_camera_no_ollama()
    
    # Resumo
    print("\n" + "="*60)
    print("  RESUMO DOS TESTES")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"  {test_name.upper()}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\n  Total: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Testes cancelados pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
