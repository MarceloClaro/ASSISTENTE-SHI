#!/usr/bin/env python3
"""
🚀 EXEMPLO RÁPIDO - Como usar SmolVLM2 no ASSISTENTE-SHI

Este arquivo mostra 3 formas diferentes de usar SmolVLM2 + OpenVINO.
"""

import asyncio
from pathlib import Path

# Exemplo 1: Uso Direto (Simples)
# ═════════════════════════════════════════════════════════════════


async def exemplo_1_direto():
    """Forma mais simples: importar e usar"""
    print("\n" + "=" * 70)
    print("📝 EXEMPLO 1: Uso Direto do SmolVLM2")
    print("=" * 70)
    
    from src.mcp.tools.camera.smolvlm2_optimized import SmolVLM2Optimized
    
    # Criar instância
    model = SmolVLM2Optimized()
    print(f"📊 Dispositivo: {model._detect_device()}")
    
    # Inicializar (primeira vez: 30-60s, próximas: <1s)
    print("⏳ Inicializando modelo...")
    await model.initialize()
    print("✅ Modelo pronto!")
    
    # Analisar uma imagem
    # (você precisará de uma imagem real para isso)
    # result = await model.analyze_image("foto.jpg")
    # print(f"⏱️ Tempo: {result['elapsed_time_seconds']:.1f}s")
    # print(f"📝 Descrição: {result['description']}")


# Exemplo 2: Via Wrapper Otimizado
# ═════════════════════════════════════════════════════════════════


async def exemplo_2_wrapper():
    """Usar via wrapper que gerencia tudo"""
    print("\n" + "=" * 70)
    print("📝 EXEMPLO 2: Uso via Wrapper Otimizado")
    print("=" * 70)
    
    from src.mcp.tools.camera.optimized_camera_tool import OptimizedCameraTool
    
    camera = OptimizedCameraTool()
    
    # Tirar foto e analisar em uma chamada
    # (requer câmera conectada)
    # result = await camera.take_photo_and_analyze(
    #     custom_prompt="Descreva tudo que você vê em detalhes"
    # )
    # print(f"✅ Sucesso: {result['success']}")
    # print(f"⏱️ Tempo: {result['time_seconds']:.1f}s")
    # print(f"🖼️ Caminho: {result['image_path']}")


# Exemplo 3: Integração com Sistema Existente
# ═════════════════════════════════════════════════════════════════


async def exemplo_3_sistema():
    """Usar através do sistema existente"""
    print("\n" + "=" * 70)
    print("📝 EXEMPLO 3: Integração com Sistema Existente")
    print("=" * 70)
    
    from src.mcp.tools.camera import get_camera_instance, SMOLVLM2_AVAILABLE
    
    print(f"SmolVLM2 disponível: {SMOLVLM2_AVAILABLE}")
    
    # Obter instância (usa VLCamera, NormalCamera ou SmolVLM2)
    camera = get_camera_instance()
    print(f"Camera em uso: {camera.__class__.__name__}")
    
    # Usar normalmente
    # success = camera.capture()
    # if success:
    #     result = camera.analyze("Descreva a imagem")
    #     print(result)


# Exemplo 4: Benchmark de Performance
# ═════════════════════════════════════════════════════════════════


async def exemplo_4_benchmark():
    """Rodar benchmark de performance"""
    print("\n" + "=" * 70)
    print("📝 EXEMPLO 4: Benchmark de Performance")
    print("=" * 70)
    
    from src.mcp.tools.camera.smolvlm2_optimized import benchmark
    
    print("⏳ Executando benchmark (cria imagem de teste)...")
    await benchmark()


# Main
# ═════════════════════════════════════════════════════════════════


async def main():
    """Executa todos os exemplos"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "🚀 EXEMPLOS DE USO - SmolVLM2 + OpenVINO no ASSISTENTE-SHI".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    # Executar exemplos (comente os que quer pular)
    
    print("\n📌 IMPORTANTE:")
    print("   - Exemplo 1 e 2: Requerem câmera ou imagem existente")
    print("   - Exemplo 3: Testa integração com sistema")
    print("   - Exemplo 4: Benchmark automático (recomendado primeiro!)")
    
    try:
        # Executar exemplo 4 (o mais seguro - não precisa câmera)
        await exemplo_4_benchmark()
        
        # Descomente para testar outros exemplos:
        # await exemplo_1_direto()
        # await exemplo_2_wrapper()
        # await exemplo_3_sistema()
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
