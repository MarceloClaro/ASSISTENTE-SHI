# -*- coding: utf-8 -*-
"""
GUI Janela Dados Modelo - Síncrono entre Python e QML dados.
"""

import json
from pathlib import Path
from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal


class GuiDisplayModel(QObject):
    """
    GUI Janela Dados Modelo - Sincroniza Python e QML.
    """

    # Conversão
    statusTextChanged = pyqtSignal()
    emotionPathChanged = pyqtSignal()
    ttsTextChanged = pyqtSignal()
    buttonTextChanged = pyqtSignal()
    modeTextChanged = pyqtSignal()
    autoModeChanged = pyqtSignal()
    musicPathChanged = pyqtSignal()

    # Operação
    manualButtonPressed = pyqtSignal()
    manualButtonReleased = pyqtSignal()
    autoButtonClicked = pyqtSignal()
    abortButtonClicked = pyqtSignal()
    modeButtonClicked = pyqtSignal()
    sendButtonClicked = pyqtSignal(str)  # Entrada de texto
    settingsButtonClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Estados
        self._status_text = "Estado: Não Conexão"
        self._emotion_path = ""  # Caminho ou emoji
        self._tts_text = ""
        self._button_text = "Começar"
        self._mode_text = ""
        self._auto_mode = False
        self._is_connected = False
        
        # Configuração de música local
        self._music_path = self._load_music_path_config()

    def _load_music_path_config(self) -> str:
        """Carrega caminho de música do arquivo de configuração."""
        try:
            config_path = Path("config/music_config.json")
            if config_path.exists():
                with open(config_path, "r") as f:
                    config = json.load(f)
                    return config.get(
                        "music_path",
                        self._get_default_music_path()
                    )
        except Exception:
            pass
        return self._get_default_music_path()

    @staticmethod
    def _get_default_music_path() -> str:
        """Retorna caminho padrão de música local."""
        # Usa Downloads do usuário como padrão
        downloads_path = Path.home() / "Downloads"
        return str(downloads_path)

    # Propriedades Qt
    @pyqtProperty(str, notify=statusTextChanged)
    def statusText(self):
        return self._status_text

    @statusText.setter
    def statusText(self, value):
        if self._status_text != value:
            self._status_text = value
            self.statusTextChanged.emit()

    @pyqtProperty(str, notify=emotionPathChanged)
    def emotionPath(self):
        return self._emotion_path

    @emotionPath.setter
    def emotionPath(self, value):
        if self._emotion_path != value:
            self._emotion_path = value
            self.emotionPathChanged.emit()

    @pyqtProperty(str, notify=ttsTextChanged)
    def ttsText(self):
        return self._tts_text

    @ttsText.setter
    def ttsText(self, value):
        if self._tts_text != value:
            self._tts_text = value
            self.ttsTextChanged.emit()

    @pyqtProperty(str, notify=buttonTextChanged)
    def buttonText(self):
        return self._button_text

    @buttonText.setter
    def buttonText(self, value):
        if self._button_text != value:
            self._button_text = value
            self.buttonTextChanged.emit()

    @pyqtProperty(str, notify=modeTextChanged)
    def modeText(self):
        return self._mode_text

    @modeText.setter
    def modeText(self, value):
        if self._mode_text != value:
            self._mode_text = value
            self.modeTextChanged.emit()

    @pyqtProperty(bool, notify=autoModeChanged)
    def autoMode(self):
        return self._auto_mode

    @autoMode.setter
    def autoMode(self, value):
        if self._auto_mode != value:
            self._auto_mode = value
            self.autoModeChanged.emit()

    @pyqtProperty(str, notify=musicPathChanged)
    def musicPath(self):
        return self._music_path

    @musicPath.setter
    def musicPath(self, value):
        if self._music_path != value:
            self._music_path = value
            self.musicPathChanged.emit()

    # Métodos públicos
    def update_status(self, status: str, connected: bool):
        """Atualiza status e conexão."""
        self.statusText = f"Estado: {status}"
        self._is_connected = connected

    def update_text(self, text: str):
        """Atualiza texto TTS."""
        self.ttsText = text

    def update_emotion(self, emotion_path: str):
        """Atualiza caminho da emoção."""
        self.emotionPath = emotion_path

    def update_button_text(self, text: str):
        """Atualiza texto do botão automático."""
        self.buttonText = text

    def update_mode_text(self, text: str):
        """Atualiza texto do modo."""
        self.modeText = text

    def set_auto_mode(self, is_auto: bool):
        """Configura modo automático/manual."""
        self.autoMode = is_auto
        if is_auto:
            self.modeText = "Automático"
        else:
            self.modeText = "Modo manual"

    def saveMusicPathConfig(self):
        """Salva caminho de música em arquivo de configuração."""
        try:
            config_dir = Path("config")
            config_dir.mkdir(parents=True, exist_ok=True)
            
            config_path = config_dir / "music_config.json"
            config = {
                "music_path": self._music_path,
                "version": "1.0"
            }
            
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
            
            # Integra com MusicPlayer se disponível
            self._apply_music_path_to_player()
        except Exception as e:
            print(f"Erro ao salvar configuração de música: {e}")

    def _apply_music_path_to_player(self):
        """
        Aplica o caminho customizado ao reprodutor de música.
        """
        try:
            from src.mcp.tools.music.music_player import MusicPlayer
            player = MusicPlayer()
            if player.set_custom_music_path(self._music_path):
                print(f"Caminho de música aplicado ao player: {self._music_path}")
            else:
                print(f"Falha ao aplicar caminho: {self._music_path}")
        except Exception as e:
            print(f"Erro ao integrar com MusicPlayer: {e}")
