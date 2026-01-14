#!/usr/bin/env python
"""Teste completo de foto com injeccao de contexto."""

import asyncio
import json
import sys
import os
from datetime import datetime

sys.path.insert(0, '.')

def check_log_for_context():
    """Verificar log para injeccao de contexto"""
    log_path = 'logs/app.log'
    if not os.path.exists(log_path):
        print(f"[AVISO] Log nao encontrado")
        return False
    
    try:
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        if "Contexto injetado para LLM" in content:
            print("[OK] Log encontrado com injeccao de contexto")
            return True
        print("[AVISO] Log sem indicadores esperados")
        return False
    except Exception as e:
        print(f"[ERRO] Erro ao ler log: {e}")
        return False

async def main():
    """Testar foto com contexto"""
    from src.mcp.tools.camera import take_photo
    
    print("\n" + "="*70)
    print("TESTE: Foto com Injeccao de Contexto")
    print("="*70 + "\n")
    
    arguments = {
        "question": "Descreva o que voce esta vendo na foto",
        "context": "Contexto adicional"
    }
    
    print("[INFO] Iniciando captura de foto...")
    print(f"       Pergunta: {arguments['question']}\n")
    
    timestamp_inicio = datetime.now()
    print(f"       Inicio: {timestamp_inicio.strftime('%H:%M:%S,%f')[:-3]}")
    
    try:
        result = take_photo(arguments)
        
        timestamp_fim = datetime.now()
        duracao = (timestamp_fim - timestamp_inicio).total_seconds()
        
        print(f"       Fim: {timestamp_fim.strftime('%H:%M:%S,%f')[:-3]}")
        print(f"       Duracao: {duracao:.2f}s\n")
        
        result_dict = json.loads(result)
        
        if result_dict.get("isError"):
            print("[ERRO] Falha na requisicao!")
            return False
        
        print("[OK] Foto capturada com sucesso!\n")
        
        context_text = result_dict["content"][0]["text"]
        print(f"[INFO] Contexto ({len(context_text)} chars):")
        print("-"*70)
        print(context_text[:400])
        print("-"*70 + "\n")
        
        print("="*70)
        print("VALIDACOES:")
        print("="*70 + "\n")
        
        validacoes = []
        
        # V1: Duracao >= 2s
        if duracao >= 2.0:
            print(f"[OK] V1 - Delay de 2s: {duracao:.2f}s >= 2.0s")
            validacoes.append(True)
        else:
            print(f"[FALHA] V1 - Delay: {duracao:.2f}s < 2.0s")
            validacoes.append(False)
        
        # V2: Descricao
        if "Uma pessoa" in context_text or "luz" in context_text.lower():
            print("[OK] V2 - Descricao visual presente")
            validacoes.append(True)
        else:
            print("[FALHA] V2 - Descricao ausente")
            validacoes.append(False)
        
        # V3: Pergunta
        if "vendo" in context_text.lower():
            print("[OK] V3 - Pergunta original presente")
            validacoes.append(True)
        else:
            print("[FALHA] V3 - Pergunta ausente")
            validacoes.append(False)
        
        # V4: Instrucoes
        if "Instrucoes" in context_text or "Considere" in context_text:
            print("[OK] V4 - Instrucoes presentes")
            validacoes.append(True)
        else:
            print("[FALHA] V4 - Instrucoes ausentes")
            validacoes.append(False)
        
        # V5: Log
        log_ok = check_log_for_context()
        if log_ok:
            validacoes.append(True)
        else:
            validacoes.append(False)
        
        print()
        total = len(validacoes)
        sucesso = sum(validacoes)
        percentual = (sucesso / total) * 100
        
        print("="*70)
        print(f"RESULTADO: {sucesso}/{total} validacoes ({percentual:.0f}%)")
        print("="*70 + "\n")
        
        if percentual >= 80:
            print("[SUCESSO] Sistema funciona corretamente!")
            print("          A descricao sera vocalizada pelo TTS.\n")
            return True
        else:
            print("[FALHA] Verifique as validacoes acima.\n")
            return False
    
    except Exception as e:
        print(f"[ERRO] Exceccao: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
