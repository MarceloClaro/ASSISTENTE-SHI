"""
Teste completo e automatizado de áudio: TTS e música.
"""
import sys
import subprocess
from pathlib import Path


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
            print(f"✅ Sucesso")
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
    cmd = """python -c "from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume; from comtypes import CLSCTX_ALL; devices = AudioUtilities.GetSpeakers(); interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None); volume = interface.QueryInterface(IAudioEndpointVolume); v = volume.GetMasterVolumeLevelScalar(); print(f'Volume: {int(v*100)}%'); volume.SetMasterVolumeLevelScalar(0.6, None) if v < 0.3 else None; print('Volume ajustado para 60%') if v < 0.3 else print('Volume OK')" """
    return run_command(cmd, "Verificando e ajustando volume do sistema")


def test_pyttsx3():
    """Testa TTS com pyttsx3."""
    cmd = """python -c "import pyttsx3; engine = pyttsx3.init(); engine.setProperty('rate', 150); engine.setProperty('volume', 1.0); print('Falando: Teste de áudio'); engine.say('Teste de áudio bem sucedido'); engine.runAndWait(); print('TTS concluído')" """
    return run_command(cmd, "Testando TTS local (pyttsx3)")


def test_ollama():
    """Testa se Ollama está rodando."""
    cmd = 'curl -s http://localhost:11434/api/tags'
    return run_command(cmd, "Verificando Ollama")


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
    cmd = """python -c "from src.mcp.tools.camera.vl_camera import VLCamera; print('VLCamera importado com sucesso')" """
    return run_command(cmd, "Testando imports da câmera")


def test_music_player_import():
    """Testa imports do player de música."""
    cmd = """python -c "from src.mcp.tools.music.music_player import MusicPlayer; print('MusicPlayer importado com sucesso')" """
    return run_command(cmd, "Testando imports do player de música")


def create_sample_mp3():
    """Cria um arquivo MP3 de teste (silêncio de 5s) se não existir."""
    print(f"\n{'='*60}")
    print("🔍 Verificando arquivo MP3 de teste")
    print(f"{'='*60}")
    
    music_dir = Path("C:/Users/marce/AppData/Local/py-xiaozhi-main/cache/music/local")
    test_file = music_dir / "teste_audio.mp3"
    
    if test_file.exists():
        print(f"✅ Arquivo de teste já existe: {test_file.name}")
        return True, str(test_file)
    
    # Tentar criar com ffmpeg
    cmd = f'ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 5 -q:a 9 -acodec libmp3lame "{test_file}" -y'
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
    cmd = "ffmpeg -version"
    return run_command(cmd, "Verificando FFmpeg")


def main():
    """Executa todos os testes."""
    print("\n" + "="*60)
    print("🚀 TESTE COMPLETO E AUTOMATIZADO DE ÁUDIO")
    print("="*60)
    
    results = {}
    
    # 1. Volume
    success, _ = test_volume()
    results['volume'] = success
    
    # 2. TTS local
    success, _ = test_pyttsx3()
    results['tts'] = success
    
    # 3. Ollama
    success, _ = test_ollama()
    results['ollama'] = success
    
    # 4. FFmpeg
    success, _ = test_ffmpeg()
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
    success, _ = test_camera_import()
    results['camera_import'] = success
    
    success, _ = test_music_player_import()
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
