"""
Teste rápido: verifica se TTS e música funcionam localmente.
"""
import asyncio
from pathlib import Path

async def test_volume():
    """Verifica volume do sistema."""
    try:
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        from comtypes import CLSCTX_ALL
        
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        
        current_volume = volume.GetMasterVolumeLevelScalar()
        print(f"✅ Volume do sistema: {int(current_volume * 100)}%")
        
        if current_volume < 0.1:
            print("⚠️  Volume muito baixo! Ajustando para 50%...")
            volume.SetMasterVolumeLevelScalar(0.5, None)
            print("✅ Volume ajustado para 50%")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao verificar volume: {e}")
        return False

async def test_tts_simple():
    """Testa TTS local com pyttsx3 (fallback simples)."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        
        print("🔊 Testando TTS local...")
        engine.say("Olá, este é um teste de áudio.")
        engine.runAndWait()
        print("✅ TTS funcionou!")
        return True
    except Exception as e:
        print(f"⚠️  pyttsx3 não disponível: {e}")
        return False

async def check_music_cache():
    """Verifica se há arquivos de música no cache local."""
    cache_dir = Path("C:/Users/marce/AppData/Local/py-xiaozhi-main/cache/music")
    
    if not cache_dir.exists():
        print(f"📁 Criando diretório de cache: {cache_dir}")
        cache_dir.mkdir(parents=True, exist_ok=True)
    
    music_files = list(cache_dir.glob("*.mp3")) + list(cache_dir.glob("*.m4a"))
    
    if music_files:
        print(f"✅ Encontrados {len(music_files)} arquivos de música:")
        for f in music_files[:5]:
            print(f"   - {f.name}")
    else:
        print("⚠️  Nenhum arquivo de música local encontrado.")
        print(f"💡 Coloque arquivos MP3 em: {cache_dir}")
    
    return len(music_files) > 0

async def main():
    print("=" * 60)
    print("🔍 DIAGNÓSTICO RÁPIDO DE ÁUDIO")
    print("=" * 60)
    
    print("\n1️⃣ Verificando volume do sistema...")
    await test_volume()
    
    print("\n2️⃣ Testando TTS local...")
    await test_tts_simple()
    
    print("\n3️⃣ Verificando cache de música...")
    await check_music_cache()
    
    print("\n" + "=" * 60)
    print("✅ Diagnóstico concluído!")
    print("=" * 60)
    print("\n💡 PRÓXIMOS PASSOS:")
    print("   1. Se TTS não funcionou, verifique dispositivo de áudio padrão")
    print("   2. Para música, coloque um MP3 no cache e peça 'toque <nome>'")
    print("   3. Execute o assistente e teste novamente\n")

if __name__ == "__main__":
    asyncio.run(main())
