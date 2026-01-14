"""
Wrapper para integrar SmolVLM2 no ASSISTENTE-SHI
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from .smolvlm2_optimized import SmolVLM2Optimized

logger = logging.getLogger(__name__)


class OptimizedCameraTool:
    """
    Tool otimizada de câmera usando SmolVLM2
    Resolução de timeout: 6-9x MAIS RÁPIDO
    """
    
    def __init__(self):
        self.model = SmolVLM2Optimized()
        self.initialized = False
        logger.info("🎬 OptimizedCameraTool inicializado")
    
    async def initialize(self) -> bool:
        """
        Inicializa modelo uma única vez (warm cache)
        """
        if self.initialized:
            return True
        
        logger.info("⏳ Inicializando SmolVLM2...")
        success = await self.model.initialize()
        
        if success:
            self.initialized = True
            logger.info("✅ Camera tool pronta!")
        else:
            logger.error("❌ Falha ao inicializar camera tool")
        
        return success
    
    async def take_photo_and_analyze(
        self,
        custom_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Captura foto da câmera e analisa com SmolVLM2
        
        ⏱️ TEMPO ESPERADO: 10-15 segundos (vs 60+ com LLaVA)
        
        Returns:
            Dict com resultado da análise
        """
        # Inicializar se necessário
        if not self.initialized:
            if not await self.initialize():
                return {
                    "success": False,
                    "error": "Falha ao inicializar modelo"
                }
        
        try:
            # Capturar foto da câmera
            logger.info("📷 Capturando foto...")
            image_path = await self._capture_photo()
            
            if not image_path:
                return {
                    "success": False,
                    "error": "Falha ao capturar foto"
                }
            
            logger.info(f"✅ Foto capturada: {image_path}")
            
            # Analisar com SmolVLM2 OTIMIZADO
            logger.info("🤖 Analisando imagem com SmolVLM2 otimizado...")
            result = await self.model.analyze_image(
                image_path,
                prompt=custom_prompt
            )
            
            return {
                "success": result["success"],
                "image_path": str(image_path),
                "description": result.get("description", ""),
                "time_seconds": result["elapsed_time_seconds"],
                "model": "SmolVLM2-1B",
                "device": result.get("device", "cpu"),
                "error": result.get("error", None)
            }
        
        except Exception as e:
            logger.error(f"❌ Erro ao tirar e analisar foto: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _capture_photo(self) -> Optional[str]:
        """
        Captura foto da câmera
        
        Returns:
            Caminho do arquivo da foto ou None se falhar
        """
        try:
            import cv2
            from datetime import datetime
            
            logger.info("📹 Acessando câmera...")
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                logger.error("❌ Câmera não disponível")
                return None
            
            # Capturar um frame
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                logger.error("❌ Falha ao capturar frame")
                return None
            
            # Salvar arquivo
            filename = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            filepath = Path(__file__).parent.parent.parent.parent / "data" / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            cv2.imwrite(str(filepath), frame)
            logger.info(f"💾 Foto salva em: {filepath}")
            
            return str(filepath)
        
        except ImportError:
            logger.error("❌ OpenCV (cv2) não instalado: pip install opencv-python")
            return None
        except Exception as e:
            logger.error(f"❌ Erro ao capturar foto: {e}")
            return None


# Alias para compatibilidade
CameraTool = OptimizedCameraTool
