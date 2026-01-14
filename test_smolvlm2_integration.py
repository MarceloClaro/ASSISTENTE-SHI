#!/usr/bin/env python3
"""
🧪 Teste Rápido de Integração - SmolVLM2 + OpenVINO

Verifica se SmolVLM2 está integrado corretamente e funciona.
"""

import asyncio
import sys
from pathlib import Path
import json

# Adicionar projeto ao path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.utils.logging_config import get_logger

logger = get_logger(__name__)


async def test_smolvlm2_import():
    """✅ Teste 1: Importação do módulo"""
    logger.info("=" * 60)
    logger.info("🧪 TESTE 1: Importação do SmolVLM2")
    logger.info("=" * 60)
    
    try:
        from src.mcp.tools.camera.smolvlm2_optimized import SmolVLM2Optimized
        logger.info("✅ SmolVLM2Optimized importado com sucesso!")
        return True
    except Exception as e:
        logger.error(f"❌ Falha ao importar: {e}")
        return False


async def test_smolvlm2_device_detection():
    """✅ Teste 2: Detecção de dispositivo"""
    logger.info("\n" + "=" * 60)
    logger.info("🧪 TESTE 2: Detecção de Dispositivo")
    logger.info("=" * 60)
    
    try:
        from src.mcp.tools.camera.smolvlm2_optimized import SmolVLM2Optimized
        
        model = SmolVLM2Optimized()
        device = model._detect_device()
        
        logger.info(f"✅ Dispositivo detectado: {device}")
        
        if device in ["cuda", "mps", "cpu"]:
            logger.info(f"✅ Dispositivo válido: {device}")
            return True
        else:
            logger.warning(f"⚠️ Dispositivo desconhecido: {device}")
            return False
    
    except Exception as e:
        logger.error(f"❌ Erro ao detectar dispositivo: {e}")
        return False


async def test_smolvlm2_initialization():
    """✅ Teste 3: Inicialização do modelo"""
    logger.info("\n" + "=" * 60)
    logger.info("🧪 TESTE 3: Inicialização do Modelo")
    logger.info("=" * 60)
    
    try:
        from src.mcp.tools.camera.smolvlm2_optimized import SmolVLM2Optimized
        
        logger.info("⏳ Inicializando modelo SmolVLM2...")
        logger.info("⚠️ Isso pode levar 30-60 segundos na primeira vez")
        logger.info("(Fazendo download do modelo ~2.5 GB)")
        
        model = SmolVLM2Optimized()
        success = await model.initialize()
        
        if success:
            logger.info("✅ Modelo inicializado com sucesso!")
            logger.info(f"   - Dispositivo: {model.device}")
            logger.info(f"   - OpenVINO: {'ativado' if model.openvino_available else 'não disponível'}")
            return True
        else:
            logger.error("❌ Falha ao inicializar modelo")
            return False
    
    except Exception as e:
        logger.error(f"❌ Erro durante inicialização: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_camera_integration():
    """✅ Teste 4: Integração com camera tool"""
    logger.info("\n" + "=" * 60)
    logger.info("🧪 TESTE 4: Integração com Camera Tool")
    logger.info("=" * 60)
    
    try:
        from src.mcp.tools.camera import (
            get_camera_instance,
            SMOLVLM2_AVAILABLE
        )
        
        logger.info(f"SmolVLM2 disponível: {SMOLVLM2_AVAILABLE}")
        
        camera = get_camera_instance()
        logger.info(f"✅ Camera instance obtida: {camera.__class__.__name__}")
        
        return True
    
    except Exception as e:
        logger.error(f"❌ Erro ao integrar com camera: {e}")
        import traceback
        traceback.print_exc()
        return False


async def run_all_tests():
    """Executa todos os testes"""
    logger.info("\n")
    logger.info("╔" + "=" * 58 + "╗")
    logger.info("║" + " " * 58 + "║")
    logger.info("║" + "  🚀 TESTES DE INTEGRAÇÃO SMOLVLM2 + OPENVINO".center(58) + "║")
    logger.info("║" + " " * 58 + "║")
    logger.info("╚" + "=" * 58 + "╝")
    
    results = {
        "import": await test_smolvlm2_import(),
        "device_detection": await test_smolvlm2_device_detection(),
        "initialization": await test_smolvlm2_initialization(),
        "camera_integration": await test_camera_integration(),
    }
    
    # Resumo
    logger.info("\n" + "=" * 60)
    logger.info("📊 RESUMO DOS TESTES")
    logger.info("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    test_names = {
        "import": "Importação",
        "device_detection": "Detecção de dispositivo",
        "initialization": "Inicialização do modelo",
        "camera_integration": "Integração com camera",
    }
    
    for test_key, test_name in test_names.items():
        status = "✅ PASSOU" if results[test_key] else "❌ FALHOU"
        logger.info(f"{test_name}: {status}")
    
    logger.info("=" * 60)
    logger.info(f"Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        logger.info("🎉 TODOS OS TESTES PASSARAM!")
        return 0
    else:
        logger.error(f"⚠️ {total - passed} teste(s) falharam")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
