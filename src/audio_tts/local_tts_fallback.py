"""
Fallback de TTS local quando servidor não envia dados de áudio.

Uso: Se o servidor não enviar frames de áudio Opus após TTS start,
usar gTTS para gerar áudio.
"""

import asyncio
import io
from typing import Optional

from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class LocalTTSFallback:
    """Gera áudio TTS localmente como fallback."""

    def __init__(self):
        self.enabled = True
        self._engine = None

    async def initialize(self):
        """Inicializa TTS local (gTTS via internet)."""
        try:
            import gtts
            self._engine = "gtts"
            logger.info("LocalTTSFallback: gTTS OK")
        except ImportError:
            logger.warning("gTTS não disponível")
            self.enabled = False

    async def generate_audio(
        self, text: str, lang: str = "pt"
    ) -> Optional[bytes]:
        """Gera áudio MP3 a partir de texto."""
        if not self.enabled or not self._engine:
            return None

        try:
            if self._engine == "gtts":
                loop = asyncio.get_event_loop()
                audio_bytes = (
                    await loop.run_in_executor(
                        None, self._gtts_generate, text, lang
                    )
                )
                return audio_bytes
        except Exception as e:
            logger.warning(f"TTS falha: {e}")
            return None

    @staticmethod
    def _gtts_generate(text: str, lang: str) -> bytes:
        """Executa geração gTTS (síncrono)."""
        from gtts import gTTS

        try:
            if len(text) > 200:
                text = text[:200] + "..."

            tts = gTTS(text=text, lang=lang, slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp.read()
        except Exception as e:
            raise RuntimeError(f"gTTS failed: {e}")


_local_tts: Optional[LocalTTSFallback] = None


async def get_local_tts() -> Optional[LocalTTSFallback]:
    """Obtém instância global de TTS local."""
    global _local_tts
    if _local_tts is None:
        _local_tts = LocalTTSFallback()
        await _local_tts.initialize()
    return _local_tts
