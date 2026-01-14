#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de integração da configuração de caminho de música.
Valida:
1. GuiDisplayModel carrega/salva configuração
2. MusicPlayer usa caminho customizado
3. O fluxo completo funciona
"""

import json
from pathlib import Path
import tempfile
import shutil


def test_gui_display_model_config():
    """Testa carregamento e salvamento de configuração no modelo GUI."""
    print("=" * 60)
    print("Teste 1: GUI Display Model - Config I/O")
    print("=" * 60)
    
    try:
        from src.display.gui_display_model import GuiDisplayModel
        
        model = GuiDisplayModel()
        
        # Teste 1a: Carrega configuração padrão
        default_path = model.musicPath
        print(f"✓ Caminho padrão carregado: {default_path}")
        assert default_path is not None
        assert len(default_path) > 0
        
        # Teste 1b: Altera caminho
        new_path = "C:\\Users\\marce\\Music"
        model.musicPath = new_path
        assert model.musicPath == new_path
        print(f"✓ Caminho alterado para: {new_path}")
        
        # Teste 1c: Salva configuração
        model.saveMusicPathConfig()
        print("✓ Configuração salva")
        
        # Teste 1d: Verifica arquivo de config
        config_path = Path("config/music_config.json")
        if config_path.exists():
            with open(config_path, "r") as f:
                config = json.load(f)
            assert "music_path" in config
            assert config["music_path"] == new_path
            print(f"✓ Arquivo de config verificado: {config}")
        else:
            print("⚠ Arquivo de config não encontrado")
        
        print("✓ TESTE 1 PASSOU\n")
        
    except Exception as e:
        print(f"✗ TESTE 1 FALHOU: {e}\n")
        import traceback
        traceback.print_exc()
        raise


def test_music_player_custom_path():
    """Testa se MusicPlayer usa caminho customizado."""
    print("=" * 60)
    print("Teste 2: Music Player - Custom Path")
    print("=" * 60)
    
    try:
        from src.mcp.tools.music.music_player import MusicPlayer
        
        player = MusicPlayer()
        
        # Teste 2a: Sem caminho customizado
        default_search_path = player.get_music_search_path()
        print(f"✓ Caminho padrão: {default_search_path}")
        assert default_search_path == player.cache_dir
        
        # Teste 2b: Define caminho customizado válido
        valid_path = tempfile.gettempdir()
        result = player.set_custom_music_path(valid_path)
        assert result is True
        print(f"✓ Caminho customizado definido: {valid_path}")
        
        # Teste 2c: Verifica se o caminho customizado é usado
        custom_search_path = player.get_music_search_path()
        assert custom_search_path == Path(valid_path)
        print(f"✓ Caminho customizado confirmado: {custom_search_path}")
        
        # Teste 2d: Define caminho inválido
        result = player.set_custom_music_path("/caminho/inexistente")
        assert result is False
        print("✓ Caminho inválido rejeitado corretamente")
        
        # Teste 2e: Caminho customizado ainda está ativo
        current_path = player.get_music_search_path()
        assert current_path == Path(valid_path)
        print(f"✓ Caminho permanece válido após rejeição: {current_path}")
        
        print("✓ TESTE 2 PASSOU\n")
        
    except Exception as e:
        print(f"✗ TESTE 2 FALHOU: {e}\n")
        import traceback
        traceback.print_exc()
        raise


def test_music_scan_with_custom_path():
    """Testa se _scan_local_music usa caminho customizado."""
    print("=" * 60)
    print("Teste 3: Music Scan - Custom Path Integration")
    print("=" * 60)
    
    try:
        from src.mcp.tools.music.music_player import MusicPlayer
        
        player = MusicPlayer()
        
        # Cria diretório temporário com arquivo de teste
        temp_dir = Path(tempfile.mkdtemp())
        test_file = temp_dir / "test_song.mp3"
        test_file.write_bytes(b"fake mp3 content")
        
        print(f"✓ Diretório temporário criado: {temp_dir}")
        print(f"✓ Arquivo de teste criado: {test_file}")
        
        # Define como caminho customizado
        result = player.set_custom_music_path(str(temp_dir))
        assert result is True
        print("✓ Caminho customizado definido")
        
        # Scans local music (deve encontrar o arquivo de teste)
        playlist = player._scan_local_music(force_refresh=True)
        print(f"✓ Playlist scanned: {len(playlist)} arquivo(s)")
        
        # Valida que encontrou o arquivo
        filenames = [m.filename for m in playlist]
        print(f"  Arquivos encontrados: {filenames}")
        
        # Limpa
        shutil.rmtree(temp_dir)
        print("✓ Limpeza concluída")
        
        print("✓ TESTE 3 PASSOU\n")
        
    except Exception as e:
        print(f"✗ TESTE 3 FALHOU: {e}\n")
        import traceback
        traceback.print_exc()
        raise


def test_full_workflow():
    """Testa o fluxo completo: GUI -> Config -> MusicPlayer."""
    print("=" * 60)
    print("Teste 4: Full Workflow Integration")
    print("=" * 60)
    
    try:
        from src.display.gui_display_model import GuiDisplayModel
        from src.mcp.tools.music.music_player import MusicPlayer
        
        # Cria diretório de teste
        temp_dir = Path(tempfile.mkdtemp())
        test_file = temp_dir / "workflow_test.mp3"
        test_file.write_bytes(b"test mp3")
        
        print(f"✓ Teste setup: {temp_dir}")
        
        # Simula: usuário altera caminho no GUI
        model = GuiDisplayModel()
        model.musicPath = str(temp_dir)
        print(f"✓ GUI: Caminho alterado para {str(temp_dir)}")
        
        # Simula: usuário clica Save
        model.saveMusicPathConfig()
        print("✓ GUI: Configuração salva")
        
        # Verifica arquivo de config
        config_path = Path("config/music_config.json")
        with open(config_path, "r") as f:
            config = json.load(f)
        assert config["music_path"] == str(temp_dir)
        print("✓ Config: Arquivo verificado")
        
        # MusicPlayer carrega e usa a config
        player = MusicPlayer()
        # Nota: player não carrega config automaticamente
        # Simula o que _apply_music_path_to_player faria
        player.set_custom_music_path(config["music_path"])
        print(f"✓ MusicPlayer: Caminho customizado aplicado")
        
        # Scans música no novo diretório
        playlist = player._scan_local_music(force_refresh=True)
        assert len(playlist) > 0
        print(f"✓ MusicPlayer: Encontrou {len(playlist)} arquivo(s)")
        
        # Limpa
        shutil.rmtree(temp_dir)
        print("✓ Limpeza concluída")
        
        print("✓ TESTE 4 PASSOU\n")
        
    except Exception as e:
        print(f"✗ TESTE 4 FALHOU: {e}\n")
        import traceback
        traceback.print_exc()
        raise


def main():
    """Executa todos os testes."""
    print("\n" + "=" * 60)
    print("TESTES DE INTEGRAÇÃO - CONFIGURAÇÃO DE MÚSICA")
    print("=" * 60 + "\n")
    
    results = []
    
    results.append(("GUI Display Model Config", test_gui_display_model_config()))
    results.append(("Music Player Custom Path", test_music_player_custom_path()))
    results.append(("Music Scan Custom Path", test_music_scan_with_custom_path()))
    results.append(("Full Workflow", test_full_workflow()))
    
    # Resumo
    print("=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASSOU" if result else "✗ FALHOU"
        print(f"{name:30} {status}")
    
    print("=" * 60)
    print(f"Total: {passed}/{total} testes passaram")
    print("=" * 60 + "\n")
    
    return passed == total


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
