#!/usr/bin/env python
"""
Script para testar requisição de foto com injeção de contexto.
Simula uma requisição completa do usuário solicitando foto e descrição.
"""

import asyncio
import json
import sys
from datetime import datetime

# Adicionar raiz do projeto ao PATH
sys.path.insert(0, '.')

async def main():
    """Testar foto com contexto injetado"""
    from src.mcp.tools.camera import take_photo
    
    print(f"\n{'='*60}")
    print(f"TESTE: Foto com Injeção de Contexto")
    print(f"Horário: {datetime.now().strftime('%H:%M:%S,%f')[:-3]}")
    print(f"{'='*60}\n")
    
    # Argumentos para solicitar foto com contexto
    arguments = {
        "question": "Descreva o que você está vendo na foto em detalhes",
        "context": "Contexto adicional para análise visual"
    }
    
    print(f"📷 Iniciando captura de foto...")
    print(f"   Pergunta: {arguments['question']}")
    print(f"   Contexto: {arguments['context']}\n")
    
    timestamp_inicio = datetime.now()
    print(f"   ⏱️ Início: {timestamp_inicio.strftime('%H:%M:%S,%f')[:-3]}")
    
    try:
        # Chamar a função de câmera (deve incluir delay de 2s agora)
        result = take_photo(arguments)
        
        timestamp_fim = datetime.now()
        duracao = (timestamp_fim - timestamp_inicio).total_seconds()
        
        print(f"   ⏱️ Fim: {timestamp_fim.strftime('%H:%M:%S,%f')[:-3]}")
        print(f"   ⏱️ Duração total: {duracao:.2f}s (deve incluir ~2s de delay)\n")
        
        # Parsear resultado
        result_dict = json.loads(result)
        
        if result_dict.get("isError"):
            print(f"❌ Erro na requisição!")
            print(f"   Mensagem: {result_dict['content'][0]['text']}")
            sys.exit(1)
        else:
            print(f"✅ Foto capturada e contexto injetado com sucesso!")
            
            # Mostrar contexto injetado
            context_text = result_dict["content"][0]["text"]
            print(f"\n📝 Contexto injetado ({len(context_text)} chars):")
            print(f"{'-'*60}")
            print(context_text[:500] + ("..." if len(context_text) > 500 else ""))
            print(f"{'-'*60}\n")
            
            # Verificar se delay foi aplicado (duração >= 2s)
            if duracao >= 2.0:
                print(f"✅ VALIDAÇÃO: Delay de 2s foi aplicado corretamente!")
                print(f"   Duração total: {duracao:.2f}s >= 2.0s\n")
            else:
                print(f"⚠️  AVISO: Delay pode não ter sido aplicado")
                print(f"   Duração total: {duracao:.2f}s < 2.0s\n")
    
    except Exception as e:
        print(f"❌ Exceção durante teste: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
