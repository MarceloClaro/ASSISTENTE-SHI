"""
Script para baixar modelo Wake Word (Sherpa-ONNX)
Automatiza o download dos arquivos necessários para detecção de palavra-chave.
"""

import os
import sys
import urllib.request
from pathlib import Path


def download_file(url: str, dest_path: Path) -> bool:
    """Download arquivo com barra de progresso."""
    try:
        print(f"Baixando: {dest_path.name}")
        
        def report_progress(block_num, block_size, total_size):
            """Mostra progresso do download."""
            downloaded = block_num * block_size
            percent = min(100, downloaded * 100 / total_size)
            bar_length = 40
            filled = int(bar_length * percent / 100)
            bar = '█' * filled + '-' * (bar_length - filled)
            print(f'\r[{bar}] {percent:.1f}%', end='', flush=True)
        
        urllib.request.urlretrieve(url, dest_path, report_progress)
        print()  # Nova linha após o progresso
        return True
    except Exception as e:
        print(f"\nErro ao baixar {dest_path.name}: {e}")
        return False


def main():
    """Download todos os arquivos necessários do modelo Wake Word."""
    
    # Diretório de destino
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("DOWNLOAD DO MODELO WAKE WORD (Sherpa-ONNX)")
    print("=" * 60)
    print()
    
    # URLs dos modelos (exemplo com modelo pequeno e eficiente)
    # Nota: Ajuste as URLs conforme o modelo desejado
    base_url = "https://github.com/k2-fsa/sherpa-onnx/releases/download/kws-models/"
    model_name = "sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01"
    
    files_to_download = {
        "encoder.onnx": f"{base_url}{model_name}/encoder.onnx",
        "decoder.onnx": f"{base_url}{model_name}/decoder.onnx",
        "joiner.onnx": f"{base_url}{model_name}/joiner.onnx",
        "tokens.txt": f"{base_url}{model_name}/tokens.txt",
        "keywords.txt": f"{base_url}{model_name}/test_wavs/keywords.txt",
    }
    
    print(f"Modelo selecionado: {model_name}")
    print(f"Destino: {models_dir.absolute()}")
    print()
    
    # Verificar se já existem
    existing_files = []
    missing_files = []
    
    for filename in files_to_download.keys():
        file_path = models_dir / filename
        if file_path.exists():
            existing_files.append(filename)
        else:
            missing_files.append(filename)
    
    if existing_files:
        print("Arquivos já existentes:")
        for f in existing_files:
            print(f"  ✅ {f}")
        print()
    
    if not missing_files:
        print("✅ Todos os arquivos já estão baixados!")
        print()
        print("Configure config/config.json:")
        print('  "WAKE_WORD_OPTIONS": {')
        print('    "USE_WAKE_WORD": true,')
        print(f'    "MODEL_PATH": "models"')
        print('  }')
        return 0
    
    print(f"Arquivos a baixar: {len(missing_files)}")
    for f in missing_files:
        print(f"  ⬇️  {f}")
    print()
    
    # Confirmar download
    response = input("Deseja continuar com o download? (s/n): ").lower()
    if response not in ['s', 'sim', 'y', 'yes']:
        print("Download cancelado.")
        return 1
    
    print()
    print("Iniciando downloads...")
    print()
    
    # Baixar arquivos faltantes
    success_count = 0
    failed_count = 0
    
    for filename in missing_files:
        url = files_to_download[filename]
        dest_path = models_dir / filename
        
        if download_file(url, dest_path):
            success_count += 1
            print(f"✅ {filename} baixado com sucesso!")
        else:
            failed_count += 1
            print(f"❌ Falha ao baixar {filename}")
        print()
    
    # Resumo
    print("=" * 60)
    print("RESUMO DO DOWNLOAD")
    print("=" * 60)
    print(f"Sucesso: {success_count} arquivo(s)")
    print(f"Falhas: {failed_count} arquivo(s)")
    print()
    
    if failed_count == 0:
        print("✅ Modelo Wake Word instalado com sucesso!")
        print()
        print("Próximos passos:")
        print("1. Configure config/config.json:")
        print('   "WAKE_WORD_OPTIONS": {')
        print('     "USE_WAKE_WORD": true,')
        print(f'     "MODEL_PATH": "{models_dir}"')
        print('   }')
        print()
        print("2. Edite models/keywords.txt com suas palavras-chave:")
        print("   xiao zhi")
        print("   ni hao")
        print()
        print("3. Execute o assistente: python main.py")
        return 0
    else:
        print("⚠️  Alguns arquivos falharam no download.")
        print("Tente novamente ou baixe manualmente de:")
        print(f"  {base_url}{model_name}/")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nDownload interrompido pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nErro inesperado: {e}")
        sys.exit(1)
