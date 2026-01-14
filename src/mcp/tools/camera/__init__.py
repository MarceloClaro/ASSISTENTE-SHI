"""
Camera tool for MCP.
"""

from src.utils.config_manager import ConfigManager
from src.utils.logging_config import get_logger

from .normal_camera import NormalCamera
from .vl_camera import VLCamera

logger = get_logger(__name__)


def get_camera_instance():
    """
    configuraçãoRetornode.
    """
    config = ConfigManager.get_instance()

    # PesquisarAI
    vl_key = config.get_config("CAMERA_OPTIONS.VL_API_KEY")
    vl_url = config.get_config("CAMERA_OPTIONS.LOCAL_VL_URL")

    if vl_url:
        logger.info(f"Initializing VL Camera with URL: {vl_url}")
        camera = VLCamera.get_instance()
        camera.set_explain_url(vl_url)
        if vl_key:
            camera.set_explain_token(vl_key)
        return camera

    logger.info("VL configuration not found, using normal Camera implementation")
    camera = NormalCamera.get_instance()
    # Configurar URL padrão para câmera normal
    default_url = config.get_config("CAMERA_OPTIONS.LOCAL_VL_URL", "https://api.tenclass.net/xiaozhi/vision/explain")
    if default_url:
        camera.set_explain_url(default_url)
        logger.info(f"Normal camera configured with URL: {default_url}")
    return camera


def take_photo(arguments: dict) -> str:
    """
    de.
    """
    import json
    import re
    
    camera = get_camera_instance()
    logger.info(f"Using camera implementation: {camera.__class__.__name__}")

    question = arguments.get("question", "")
    context = arguments.get("context", "")
    logger.info(f"Taking photo with question: {question}, context: {context[:50] if context else 'None'}...")

    # 
    success = camera.capture()
    if not success:
        logger.error("Failed to capture photo")
        return "Falha ao capturar foto da câmera"

    # 
    logger.info("Photo captured, starting analysis...")
    result = camera.analyze(question, context)
    
    # Parsear o JSON retornado e extrair o texto da descrição
    try:
        result_dict = json.loads(result)
        if result_dict.get("success") and "text" in result_dict:
            description = result_dict["text"].strip()
            
            # Limpar a descrição: remover quebras de linha, espaços extras
            description = re.sub(r'\s+', ' ', description)
            description = description.replace('"', '')  # Remover aspas
            description = description.replace('\\', '')  # Remover barras
            description = description.replace('\n', ' ')  # Quebras de linha
            description = description.replace('\r', ' ')  # Retorno de carro
            
            logger.info(f"✅ Descrição limpa: {description[:100]}...")
            # Retornar apenas o texto da descrição para o LLM processar
            return description
        else:
            error_msg = result_dict.get("message", "Erro desconhecido")
            logger.error(f"❌ Análise falhou: {error_msg}")
            return f"Erro ao analisar imagem: {error_msg}"
    except json.JSONDecodeError as e:
        logger.error(f"❌ Erro ao parsear resposta: {e}")
        # Se não for JSON válido, retornar mensagem de erro
        return "Erro ao processar resposta da análise de imagem"
