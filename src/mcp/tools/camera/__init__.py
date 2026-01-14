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
    Captura foto, analisa com Ollama e injeta descrição como contexto.
    
    Args:
        arguments: {
            "question": "Pergunta sobre a imagem",
            "context": "Contexto adicional (opcional)"
        }
    
    Returns:
        JSON com descrição injetada no contexto do usuário
    """
    import json
    import re
    
    camera = get_camera_instance()
    logger.info(
        f"Using camera implementation: "
        f"{camera.__class__.__name__}"
    )

    question = arguments.get("question", "")
    context = arguments.get("context", "")
    logger.info(
        f"Taking photo with question: {question}, "
        f"context: {context[:50] if context else 'None'}..."
    )

    # Capturar foto
    success = camera.capture()
    if not success:
        logger.error("Failed to capture photo")
        return json.dumps({
            "content": [{
                "type": "text",
                "text": "Falha ao capturar foto da câmera"
            }],
            "isError": True
        })

    # Analisar com Ollama local
    logger.info("Photo captured, starting analysis...")
    result = camera.analyze(question, context)
    
    # Parsear o JSON retornado e extrair o texto da descrição
    try:
        result_dict = json.loads(result)
        if result_dict.get("success") and "text" in result_dict:
            description = result_dict["text"].strip()
            
            # Limpar descrição: remover quebras, espaços extras
            description = re.sub(r'\s+', ' ', description)
            description = description.replace('"', '')
            description = description.replace('\\', '')
            description = description.replace('\n', ' ')
            description = description.replace('\r', ' ')
            
            logger.info(f"✅ Descrição limpa: {description[:100]}...")
            
            # 🆕 INJETAR DESCRIÇÃO NO CONTEXTO DO USUÁRIO
            logger.info(
                "[Camera] Enriquecendo contexto com "
                "descrição visual..."
            )
            enhanced_context = _enhance_user_context(
                original_question=question,
                image_description=description,
                user_context=context
            )
            
            logger.info(
                f"[Camera] Contexto injetado para LLM "
                f"({len(enhanced_context)} chars)"
            )
            
            # Retornar com contexto injetado
            return json.dumps({
                "content": [{
                    "type": "text",
                    "text": enhanced_context
                }],
                "isError": False
            })
        else:
            error_msg = result_dict.get(
                "message", "Erro desconhecido"
            )
            logger.error(f"❌ Análise falhou: {error_msg}")
            return json.dumps({
                "content": [{
                    "type": "text",
                    "text": f"Erro ao analisar imagem: {error_msg}"
                }],
                "isError": True
            })
    except json.JSONDecodeError as e:
        logger.error(f"❌ Erro ao parsear resposta: {e}")
        return json.dumps({
            "content": [{
                "type": "text",
                "text": (
                    "Erro ao processar resposta da análise "
                    "de imagem"
                )
            }],
            "isError": True
        })


def _enhance_user_context(
    original_question: str,
    image_description: str,
    user_context: str = ""
) -> str:
    """
    Cria prompt enriquecido com descrição visual para LLM.
    
    Args:
        original_question: Pergunta do usuário
        image_description: Descrição gerada por Ollama
        user_context: Contexto adicional (opcional)
    
    Returns:
        Prompt enriquecido para LLM processar
    """
    
    # Template do prompt enriquecido
    template = (
        "📸 ANÁLISE DE IMAGEM COM CONTEXTO VISUAL\n\n"
        "**Descrição da Imagem Analisada (Ollama Local):**\n"
        "{description}\n\n"
        "**Pergunta do Usuário:**\n"
        "{question}\n"
        "{context_section}\n\n"
        "**Instruções para Resposta:**\n"
        "1. Considere a descrição visual acima como referência\n"
        "2. Responda de forma detalhada e específica\n"
        "3. Se tiver informações adicionais, compartilhe\n"
        "4. Mantenha tom conversacional e amigável"
    )
    
    # Montar seção de contexto adicional
    context_section = ""
    if user_context:
        context_section = (
            f"\n\n**Contexto Adicional:**\n{user_context}"
        )
    
    # Montar prompt final
    prompt = template.format(
        description=image_description.strip(),
        question=original_question.strip(),
        context_section=context_section.strip()
    )
    
    return prompt.strip()
