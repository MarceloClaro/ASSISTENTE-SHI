"""
Camera tool for MCP.
"""

from src.utils.config_manager import ConfigManager
from src.utils.logging_config import get_logger

from .normal_camera import NormalCamera
from .vl_camera import VLCamera

# 🚀 OTIMIZAÇÃO: SmolVLM2 + OpenVINO (6-9x mais rápido)
# LAZY IMPORT: Importar apenas quando necessário para evitar conflito torch
SMOLVLM2_AVAILABLE = None
SmolVLM2Optimized = None

logger = get_logger(__name__)


def _check_smolvlm2_available():
    """Verificar disponibilidade do SmolVLM2 (lazy load)"""
    global SMOLVLM2_AVAILABLE, SmolVLM2Optimized
    if SMOLVLM2_AVAILABLE is None:
        try:
            from .smolvlm2_optimized import SmolVLM2Optimized as SVL2
            SmolVLM2Optimized = SVL2
            SMOLVLM2_AVAILABLE = True
            logger.info("✅ SmolVLM2 disponível (lazy loaded)")
        except Exception as e:
            SMOLVLM2_AVAILABLE = False
            logger.debug(f"SmolVLM2 não disponível: {e}")
    return SMOLVLM2_AVAILABLE


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

    logger.info(
        "VL configuration not found, "
        "using normal Camera implementation"
    )
    camera = NormalCamera.get_instance()
    # Configurar URL padrão para câmera normal
    default_url = config.get_config(
        "CAMERA_OPTIONS.LOCAL_VL_URL",
        "https://api.tenclass.net/xiaozhi/vision/explain"
    )
    if default_url:
        camera.set_explain_url(default_url)
        logger.info(f"Normal camera configured with URL: {default_url}")
    return camera


def take_photo(arguments: dict) -> str:
    """
    Captura foto e analisa com SmolVLM2 (6-9x mais rápido que LLaVA).
    Fallback automático para LLaVA se SmolVLM2 não disponível.
    
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
    import asyncio
    
    question = arguments.get("question", "")
    context = arguments.get("context", "")
    
    logger.info(
        f"Taking photo with question: {question}, "
        f"context: {context[:50] if context else 'None'}..."
    )

    # ✨ TENTAR USAR SmolVLM2 PRIMEIRO (6-9x mais rápido)
    _check_smolvlm2_available()  # Lazy load
    if SMOLVLM2_AVAILABLE:
        try:
            logger.info("🚀 Usando SmolVLM2 + OpenVINO (6-9x mais rápido)...")
            
            # Capturar foto normal
            camera = NormalCamera.get_instance()
            success = camera.capture()
            if not success:
                logger.error("Failed to capture photo")
                return "Falha ao capturar foto da câmera"
            
            # Salvar foto temporária
            import cv2
            jpeg_data = camera.jpeg_data["buf"]
            import numpy as np
            import tempfile
            
            nparr = np.frombuffer(jpeg_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            with tempfile.NamedTemporaryFile(
                suffix=".jpg",
                delete=False
            ) as tmp:
                cv2.imwrite(tmp.name, frame)
                temp_path = tmp.name
            
            # Analisar com SmolVLM2
            model = SmolVLM2Optimized()
            
            async def analyze_async():
                await model.initialize()
                result = await model.analyze_image(temp_path)
                return result
            
            # Rodar análise async
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # Se já temos um loop rodando, criar task
                    import asyncio
                    result = loop.run_until_complete(analyze_async())
                else:
                    result = asyncio.run(analyze_async())
            except RuntimeError:
                result = asyncio.run(analyze_async())
            
            # Limpar arquivo temporário
            import os
            try:
                os.unlink(temp_path)
            except OSError:
                pass
            
            if result.get("success"):
                description = result.get("description", "").strip()
                
                # Limpar descrição
                description = re.sub(r'\s+', ' ', description)
                description = description.replace('"', '')
                
                logger.info("SmolVLM2 análise bem-sucedida!")
                elapsed = result.get('elapsed_time_seconds', 0)
                logger.info(f"Tempo: {elapsed:.1f}s")
                
                enhanced_context = _enhance_user_context(
                    original_question=question,
                    image_description=description,
                    user_context=context
                )
                
                import time
                time.sleep(2.0)
                return enhanced_context
            else:
                logger.warning(
                    "SmolVLM2 failed, falling back to LLaVA..."
                )
        
        except Exception as e:
            logger.warning(
                f"SmolVLM2 error: {e}, falling back to LLaVA..."
            )
    
    # FALLBACK: Usar LLaVA (original)
    logger.info("📷 Usando LLaVA + Ollama (fallback)...")
    
    camera = get_camera_instance()
    logger.info(
        f"Using camera implementation: {camera.__class__.__name__}"
    )

    # Capturar foto
    success = camera.capture()
    if not success:
        logger.error("Failed to capture photo")
        return "Falha ao capturar foto da câmera"

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
            
            # 🔧 CRITICAL: Aguardar LLM processar a resposta
            # completa antes de retornar. Sem isso, TTS
            # começa com resposta vazia/padrão.
            # LLM normalmente leva 1-2s para processar.
            import time
            time.sleep(2.0)  # 2 segundos para LLM processar
            
            # Retornar APENAS O TEXTO (MCP server faz serialização)
            return enhanced_context
        else:
            error_msg = result_dict.get(
                "message", "Erro desconhecido"
            )
            logger.error(f"❌ Análise falhou: {error_msg}")
            return f"Erro ao analisar imagem: {error_msg}"
    except json.JSONDecodeError as e:
        logger.error(f"❌ Erro ao parsear resposta: {e}")
        return "Erro ao processar resposta da análise de imagem"


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
