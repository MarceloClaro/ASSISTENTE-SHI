"""
Teste completo e automatizado de áudio: TTS e música.
"""
import sys
import subprocess
import importlib
import shutil
from pathlib import Path

import pytest

# Comando para validar e ajustar volume (quebrado em partes para lint)
VOLUME_CMD = (
    "python -c \"from pycaw.pycaw import AudioUtilities, "
    "IAudioEndpointVolume; from comtypes import CLSCTX_ALL; "
    "devices = AudioUtilities.GetSpeakers(); "
    "interface = devices.Activate(IAudioEndpointVolume._iid_, "
    "CLSCTX_ALL, None); "
    "volume = interface.QueryInterface(IAudioEndpointVolume); "
    "v = volume.GetMasterVolumeLevelScalar(); "
    "print(f'Volume: {int(v*100)}%'); "
    "volume.SetMasterVolumeLevelScalar(0.6, None) if v < 0.3 else None; "
    "print('Volume ajustado para 60%') if v < 0.3 else print('Volume OK')\""
)


def require_module(module_name: str, reason: str):
    """Skipa teste se módulo não estiver disponível ou falhar ao importar."""
    try:
        importlib.import_module(module_name)
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"{reason}: {exc}")


def run_command(cmd, description):
    """Executa comando e retorna resultado."""
    print(f"\n{'='*60}")
    print(f"🔍 {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=True,
            timeout=30
        )
        if result.returncode == 0:
            print("✅ Sucesso")
            if result.stdout.strip():
                print(result.stdout)
            return True, result.stdout
        else:
            print(f"❌ Erro (código {result.returncode})")
            if result.stderr.strip():
                print(result.stderr)
            return False, result.stderr
    except subprocess.TimeoutExpired:
        print("⏱️  Timeout (>30s)")
        return False, "timeout"
    except Exception as e:
        print(f"❌ Exceção: {e}")
        return False, str(e)


def test_volume():
    """Testa volume do sistema."""
    require_module(
        "pycaw.pycaw",
        "pycaw/comtypes indisponível no ambiente do teste (somente Windows)"
    )
    success, _ = run_command(
        VOLUME_CMD,
        "Verificando e ajustando volume do sistema",
    )
    assert success


def test_pyttsx3():
    """Testa TTS com pyttsx3."""
    require_module(
        "pyttsx3",
        "pyttsx3/comtypes indisponível no ambiente do teste (somente Windows)"
    )
    require_module(
        "comtypes",
        "comtypes indisponível no ambiente do teste (somente Windows)"
    )
    cmd = (
        "python -c \"import pyttsx3; engine = pyttsx3.init(); "
        "engine.setProperty('rate', 150); engine.setProperty('volume', 1.0); "
        "print('Falando: Teste de áudio'); "
        "engine.say('Teste de áudio bem sucedido'); engine.runAndWait(); "
        "print('TTS concluído')\""
    )
    success, _ = run_command(cmd, "Testando TTS local (pyttsx3)")
    assert success


def test_ollama():
    """Testa se Ollama está rodando."""
    cmd = 'curl -s http://localhost:11434/api/tags'
    success, _ = run_command(cmd, "Verificando Ollama")
    assert success


def check_cache_dirs():
    """Verifica e cria diretórios de cache."""
    print(f"\n{'='*60}")
    print("🔍 Verificando diretórios de cache")
    print(f"{'='*60}")
    
    cache_base = Path("C:/Users/marce/AppData/Local/py-xiaozhi-main/cache")
    music_dir = cache_base / "music" / "local"
    photos_dir = cache_base / "photos"
    
    for d in [music_dir, photos_dir]:
        if not d.exists():
            print(f"📁 Criando: {d}")
            d.mkdir(parents=True, exist_ok=True)
        else:
            print(f"✅ Existe: {d}")
    
    # Listar arquivos de música
    music_files = list(music_dir.glob("*.mp3")) + list(music_dir.glob("*.m4a"))
    if music_files:
        print(f"\n🎵 Arquivos de música encontrados ({len(music_files)}):")
        for f in music_files[:10]:
            size_mb = f.stat().st_size / (1024*1024)
            print(f"   - {f.name} ({size_mb:.1f} MB)")
    else:
        print("\n⚠️  Nenhum arquivo de música no cache local")
        print(f"💡 Copie MP3s para: {music_dir}")
    
    return True, len(music_files)


def test_camera_import():
    """Testa imports da câmera."""
    cmd = (
        "python -c \"from src.mcp.tools.camera.vl_camera import VLCamera; "
        "print('VLCamera importado com sucesso')\""
    )
    success, _ = run_command(cmd, "Testando imports da câmera")
    assert success


def test_music_player_import():
    """Testa imports do player de música."""
    cmd = (
        "python -c \"from src.mcp.tools.music.music_player import "
        "MusicPlayer; print('MusicPlayer importado com sucesso')\""
    )
    success, _ = run_command(cmd, "Testando imports do player de música")
    assert success


def create_sample_mp3():
    """Cria um arquivo MP3 de teste (silêncio de 5s) se não existir."""
    print(f"\n{'='*60}")
    print("🔍 Verificando arquivo MP3 de teste")
    print(f"{'='*60}")
    
    music_dir = Path(
        "C:/Users/marce/AppData/Local/py-xiaozhi-main/cache/music/local"
    )
    test_file = music_dir / "teste_audio.mp3"
    
    if test_file.exists():
        print(f"✅ Arquivo de teste já existe: {test_file.name}")
        return True, str(test_file)
    
    # Tentar criar com ffmpeg
    cmd = (
        "ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 5 -q:a 9 "
        f"-acodec libmp3lame \"{test_file}\" -y"
    )
    success, _ = run_command(cmd, "Criando MP3 de teste (5s silêncio)")
    
    if success and test_file.exists():
        print(f"✅ Arquivo de teste criado: {test_file.name}")
        return True, str(test_file)
    else:
        print("⚠️  Não foi possível criar arquivo de teste")
        print("💡 Copie manualmente um MP3 para o diretório de cache")
        return False, None


def test_ffmpeg():
    """Verifica se FFmpeg está disponível."""
    if shutil.which("ffmpeg") is None:
        pytest.skip("FFmpeg não encontrado no PATH do ambiente de teste")
    cmd = "ffmpeg -version"
    success, _ = run_command(cmd, "Verificando FFmpeg")
    assert success


def main():
    """Executa todos os testes."""
    print("\n" + "="*60)
    print("🚀 TESTE COMPLETO E AUTOMATIZADO DE ÁUDIO")
    print("="*60)
    
    results = {}
    
    # 1. Volume
    success, _ = run_command(
        VOLUME_CMD,
        "Verificando e ajustando volume do sistema",
    )
    results['volume'] = success
    
    # 2. TTS local
    success, _ = run_command(
        (
            "python -c \"import pyttsx3; engine = pyttsx3.init(); "
            "engine.setProperty('rate', 150); "
            "engine.setProperty('volume', 1.0); "
            "print('Falando: Teste de áudio'); "
            "engine.say('Teste de áudio bem sucedido'); "
            "engine.runAndWait(); print('TTS concluído')\""
        ),
        "Testando TTS local (pyttsx3)",
    )
    results['tts'] = success
    
    # 3. Ollama
    success, _ = run_command(
        'curl -s http://localhost:11434/api/tags',
        "Verificando Ollama",
    )
    results['ollama'] = success
    
    # 4. FFmpeg
    success, _ = run_command(
        "ffmpeg -version",
        "Verificando FFmpeg",
    )
    results['ffmpeg'] = success
    
    # 5. Diretórios
    success, music_count = check_cache_dirs()
    results['cache'] = success
    
    # 6. Arquivo de teste
    if music_count == 0:
        success, test_file = create_sample_mp3()
        results['sample_mp3'] = success
    else:
        results['sample_mp3'] = True
    
    # 7. Imports
    success, _ = run_command(
        (
            "python -c \"from src.mcp.tools.camera.vl_camera import VLCamera; "
            "print('VLCamera importado com sucesso')\""
        ),
        "Testando imports da câmera",
    )
    results['camera_import'] = success
    
    success, _ = run_command(
        (
            "python -c \"from src.mcp.tools.music.music_player import "
            "MusicPlayer; print('MusicPlayer importado com sucesso')\""
        ),
        "Testando imports do player de música",
    )
    results['music_import'] = success
    
    # Resumo
    print("\n" + "="*60)
    print("📊 RESUMO DOS TESTES")
    print("="*60)
    
    for test, passed in results.items():
        status = "✅" if passed else "❌"
        print(f"{status} {test}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ TODOS OS TESTES PASSARAM!")
        print("\n💡 Próximo passo:")
        print("   python main.py --mode gui --protocol websocket")
        print('   Diga: "tire uma foto" e depois "toque teste_audio"')
    else:
        print("⚠️  ALGUNS TESTES FALHARAM")
        print("\n💡 Ações necessárias:")
        if not results.get('volume'):
            print("   - Verifique dispositivo de áudio do Windows")
        if not results.get('tts'):
            print("   - Instale: pip install pyttsx3")
        if not results.get('ffmpeg'):
            print("   - Instale FFmpeg: https://ffmpeg.org/download.html")
        if not results.get('sample_mp3') and music_count == 0:
            print("   - Copie um MP3 para cache/music/local/")
    print("="*60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
