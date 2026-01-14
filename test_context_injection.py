#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste da Injeção de Contexto Ollama
Valida se a descrição da imagem é corretamente injetada como contexto.
"""

import asyncio
import json
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.append(str(project_root))

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s[%(name)s] - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_context_injection():
    """Testa injeção de contexto da descrição de imagem"""

    print("\n" + "=" * 70)
    print("🧪 TESTE DE INJEÇÃO DE CONTEXTO OLLAMA")
    print("=" * 70 + "\n")

    try:
        from src.mcp.tools.camera import _enhance_user_context

        # Teste 1: Contexto simples
        print("[1/3] Testando contexto simples...")
        description = "Uma pessoa sentada em uma cadeira"
        question = "Tire uma foto"
        
        result = _enhance_user_context(
            original_question=question,
            image_description=description
        )
        
        print(f"  ✅ Descrição: {description}")
        print(f"  ✅ Pergunta: {question}")
        print(f"  ✅ Contexto injetado ({len(result)} chars):\n")
        print("  " + "\n  ".join(result.split("\n")[:5]))
        print("  ...\n")

        # Teste 2: Com contexto adicional
        print("[2/3] Testando com contexto adicional...")
        additional_context = "O usuário está em modo criativo"
        
        result = _enhance_user_context(
            original_question=question,
            image_description=description,
            user_context=additional_context
        )
        
        print(f"  ✅ Contexto adicional: {additional_context}")
        print(f"  ✅ Resultado ({len(result)} chars)")
        assert "Contexto Adicional" in result
        print("  ✅ Contexto adicional injetado corretamente\n")

        # Teste 3: Validar estrutura
        print("[3/3] Validando estrutura do prompt...")
        required_sections = [
            "📸 ANÁLISE DE IMAGEM",
            "Descrição da Imagem",
            "Pergunta do Usuário",
            "Instruções para Resposta"
        ]
        
        for section in required_sections:
            if section in result:
                print(f"  ✅ Seção encontrada: {section}")
            else:
                print(f"  ❌ Seção não encontrada: {section}")
                return False

        print("\n" + "=" * 70)
        print("📊 RESULTADO DO TESTE")
        print("=" * 70)
        print("✅ Injeção de contexto funcionando")
        print("✅ Estrutura do prompt correta")
        print("✅ Contexto adicional suportado\n")

        return True

    except Exception as e:
        print(f"\n❌ ERRO: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Função principal"""
    try:
        result = test_context_injection()
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário")
        sys.exit(1)


if __name__ == "__main__":
    main()
