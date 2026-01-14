"""
Script para baixar modelo Wake Word (Sherpa-ONNX)
Automatiza o download dos arquivos necessários para detecção de palavra-chave.
"""

import os
import sys
import urllib.request
import tarfile
import tempfile
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


def extract_model_archive(archive_path: Path, target_dir: Path) -> bool:
    """Extrai tar.bz2 e copia onnx/tokens para target_dir."""
    try:
        print(f"Extraindo {archive_path.name}...")
        with tarfile.open(archive_path, "r:bz2") as tar:
            with tempfile.TemporaryDirectory() as tmpdir:
                tar.extractall(tmpdir)
                tmp_path = Path(tmpdir)
                patterns = {
                    "encoder.onnx": [
                        "encoder.onnx",
                        "encoder-epoch-99-avg-1-chunk-16-left-64.int8.onnx",
                        "encoder-epoch-99-avg-1-chunk-16-left-64.onnx",
                    ],
                    "decoder.onnx": [
                        "decoder.onnx",
                        "decoder-epoch-99-avg-1-chunk-16-left-64.int8.onnx",
                        "decoder-epoch-99-avg-1-chunk-16-left-64.onnx",
                    ],
                    "joiner.onnx": [
                        "joiner.onnx",
                        "joiner-epoch-99-avg-1-chunk-16-left-64.int8.onnx",
                        "joiner-epoch-99-avg-1-chunk-16-left-64.onnx",
                    ],
                    "tokens.txt": ["tokens.txt"],
                    "keywords.txt": ["keywords.txt", "test_keywords.txt"],
                }
                found = 0
                for target, candidates in patterns.items():
                    match = None
                    for pattern in candidates:
                        found_match = next(tmp_path.rglob(pattern), None)
                        if found_match:
                            match = found_match
                            break
                    if match:
                        dest = target_dir / target
                        dest.write_bytes(match.read_bytes())
                        print(f"✅ {target} extraído")
                        found += 1
                    else:
                        print(f"⚠️  Não encontrado no pacote: {target}")

                if found < 5:
                    print(
                        "⚠️  Arquivos ausentes no pacote. Download incompleto."
                    )
                    return False
        print("Extração concluída.")
        return True
    except Exception as e:
        print(f"Erro ao extrair {archive_path.name}: {e}")
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
    
    # Pacote oficial (contém encoder/decoder/joiner/tokens/keywords)
    base_url = (
        "https://github.com/k2-fsa/sherpa-onnx/releases/download/kws-models/"
    )
    model_name = "sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01"
    archive_name = f"{model_name}.tar.bz2"
    archive_url = f"{base_url}{archive_name}"
    
    print(f"Modelo selecionado: {model_name}")
    print(f"Destino: {models_dir.absolute()}")
    print()
    
    required_files = [
        "encoder.onnx",
        "decoder.onnx",
        "joiner.onnx",
        "tokens.txt",
        "keywords.txt",
    ]

    existing_files = []
    missing_files = []

    for filename in required_files:
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
        print('    "MODEL_PATH": "models"')
        print('  }')
        return 0
    
    print(f"Arquivos a baixar: {len(missing_files)} (pacote: {archive_name})")
    for f in missing_files:
        print(f"  ⬇️  {f}")
    print()
    
    # Confirmar download (pode ser forçado com --yes ou
    # AUTO_DOWNLOAD_WAKE_WORD=1)
    auto_confirm = (
        "--yes" in sys.argv
        or "-y" in sys.argv
        or os.environ.get("AUTO_DOWNLOAD_WAKE_WORD") == "1"
    )

    if not auto_confirm:
        response = input("Deseja continuar com o download? (s/n): ").lower()
        if response not in ['s', 'sim', 'y', 'yes']:
            print("Download cancelado.")
            return 1
    else:
        print(
            "Confirmação automática habilitada (--yes) "
            "ou AUTO_DOWNLOAD_WAKE_WORD=1"
        )
    
    print()
    print("Iniciando download do pacote...")
    print()

    archive_path = models_dir / archive_name
    success_count = 0

    if download_file(archive_url, archive_path):
        if extract_model_archive(archive_path, models_dir):
            success_count = len(required_files)
        archive_path.unlink(missing_ok=True)
    
    # Resumo
    print("=" * 60)
    print("RESUMO DO DOWNLOAD")
    print("=" * 60)
    print(f"Sucesso: {success_count} arquivo(s)")
    print(f"Falhas: {len(required_files) - success_count} arquivo(s)")
    print()
    
    if success_count == len(required_files):
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
        print(f"  {archive_url}")
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
