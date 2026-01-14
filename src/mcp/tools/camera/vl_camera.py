"""
VL camera implementation using Zhipu AI with Vision API fallback.
"""

import base64

import cv2
from openai import OpenAI

from src.utils.config_manager import ConfigManager
from src.utils.logging_config import get_logger

from .base_camera import BaseCamera

logger = get_logger(__name__)


class VLCamera(BaseCamera):
    """
    AI.
    """

    _instance = None

    def __init__(self):
        """
        InicializandoAI.
        """
        super().__init__()
        config = ConfigManager.get_instance()

        # Tentar obter config do CAMERA_OPTIONS (preferido)
        # ou CAMERA (fallback)
        # Configuração para Ollama local apenas
        api_key = config.get_config(
            "CAMERA_OPTIONS.VL_API_KEY",
            config.get_config("CAMERA.VLapi_key", "ollama")
        )
        
        base_url = config.get_config(
            "CAMERA_OPTIONS.LOCAL_VL_URL",
            config.get_config(
                "CAMERA.Local_VL_url",
                "http://localhost:11434"
            )
        )
        
        # Guardar base_url para Ollama
        self.base_url = base_url

        self.client = OpenAI(
            api_key=api_key if api_key else "ollama",
            base_url=base_url,
        )
        
        model_val = config.get_config(
            "CAMERA_OPTIONS.MODELS",
            config.get_config("CAMERA.models", "llava:7b")
        )
        self.model = model_val if model_val else "llava:7b"
        
        logger.info(
            f"VL Camera initialized with model: {self.model}, URL: "
            f"{base_url}"
        )

    @classmethod
    def get_instance(cls):
        """
        .
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def capture(self) -> bool:
        """
        Capturandoimagem.
        """
        try:
            logger.info("Accessing camera...")

            # TentativaAbrindo
            cap = cv2.VideoCapture(self.camera_index)
            if not cap.isOpened():
                logger.error(
                    f"Cannot open camera at index {self.camera_index}"
                )
                return False

            # ConfigurandoParâmetro
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)

            #
            ret, frame = cap.read()
            cap.release()

            if not ret:
                logger.error("Failed to capture image")
                return False

            # Original
            height, width = frame.shape[:2]

            # ，para320
            max_dim = max(height, width)
            scale = 320 / max_dim if max_dim > 320 else 1.0

            # Aguardar
            if scale < 1.0:
                new_width = int(width * scale)
                new_height = int(height * scale)
                frame = cv2.resize(
                    frame,
                    (new_width, new_height),
                    interpolation=cv2.INTER_AREA,
                )

            # CodificaçãoparaJPEGBytes
            success, jpeg_data = cv2.imencode(".jpg", frame)

            if not success:
                logger.error("Failed to encode image to JPEG")
                return False

            # BytesDados
            self.set_jpeg_data(jpeg_data.tobytes())
            logger.info(
                "Image captured successfully (size: %d bytes)",
                self.jpeg_data["len"],
            )
            return True

        except Exception as e:
            logger.error(f"Exception during capture: {e}")
            return False

    def analyze(self, question: str, context: str = "") -> str:
        """
        Analisar imagem usando AI com fallback para Cliente AI Xiaozhi.
        """
        try:
            if not self.jpeg_data["buf"]:
                msg = '{"success": false, "message": "Camera buffer is empty"}'
                return msg

            # Converter para Base64
            img_b64 = base64.b64encode(
                self.jpeg_data["buf"]
            ).decode("utf-8")

            # Construir prompt com contexto
            full_prompt = question if question else "O que você vê？"
            if context:
                full_prompt = f"{full_prompt}\n\nContexto: {context}"
                logger.info(f"Sending image with context: {context[:50]}")

            # Usar apenas Ollama local (LLaVA)
            logger.info("Analisando imagem com Ollama/LLaVA (100% gratuito)...")
            return self._analyze_with_ollama(img_b64, full_prompt)

        except Exception as e:
            error_msg = f"Ollama falhou ao analisar imagem: {str(e)}"
            logger.error(error_msg)
            
            msg = f'{{"success": false, "message": "{error_msg}", '\
                  f'"suggestion": "Verifique se Ollama está rodando: ollama serve"}}'
            return msg

    def _analyze_with_openai(self, image_b64: str,
                             prompt: str) -> str:
        """Analisar imagem usando OpenAI-compatible API."""
        
        # DeepSeek usa formato diferente para visão
        if "deepseek" in self.model.lower() or \
           "api.deepseek.com" in str(getattr(self.client, '_base_url', '')):
            # Formato DeepSeek: usar content como array de objetos
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_b64}"
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        else:
            # Formato padrão OpenAI/Zhipu
            messages = [
                {"role": "system",
                 "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_b64}"
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt,
                        },
                    ],
                },
            ]

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            modalities=["text"],
            stream=True,
            stream_options={"include_usage": True},
        )

        result = ""
        for chunk in completion:
            if chunk.choices:
                result += chunk.choices[0].delta.content or ""

        logger.info("Análise Zhipu concluída com sucesso")
        return f'{{"success": true, "text": "{result}"}}'

    def _analyze_with_ollama(self, image_b64: str, prompt: str) -> str:
        """Analisar imagem usando Ollama local (llava)."""
        try:
            import httpx
            
            logger.info("Analisando com Ollama local (llava)...")
            
            # Ollama API endpoint
            url = "http://localhost:11434/api/generate"
            
            # Melhorar o prompt para português e ser mais direto
            # Remover possíveis aspas extras que causam problemas
            clean_prompt = prompt.strip().strip('"').strip("'")
            
            # Palavras que causam recusa do llava por privacidade
            palavras_proibidas = [
                "identificação", "identificar", "identifique",
                "quem é", "quem e", "nome da pessoa", "pessoa é",
                "reconhecer", "reconhecimento facial",
                "identidade", "identificação facial"
            ]
            
            # Verificar se prompt contém palavras proibidas
            prompt_lower = clean_prompt.lower()
            tem_palavra_proibida = any(
                palavra in prompt_lower for palavra in palavras_proibidas
            )
            
            # Se tiver palavra proibida ou prompt vazio, usar seguro
            if tem_palavra_proibida or len(clean_prompt) < 5:
                # Prompt EXTREMAMENTE CONCISO - máximo 60-80 caracteres
                clean_prompt = (
                    "Frase curta (máx 10 palavras): "
                    "cena, objetos principais. Nada mais."
                )
            else:
                # Adicionar aviso de ser MUITO conciso
                clean_prompt = (
                    f"{clean_prompt}. "
                    "Resposta em 1 frase, máx 10 palavras."
                )
            
            logger.info(f"Prompt para Ollama: {clean_prompt[:80]}...")
            
            # Determinar modelo (priorizar modelos rápidos)
            model = self.model.lower()
            if "llava" in model:
                # Tentar usar modelo de visão mais rápido se disponível
                try:
                    import subprocess
                    result = subprocess.run(
                        ["ollama", "list"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    models_available = result.stdout.lower()
                    
                    # Prioridade: minicpm-v > llava:7b > llava
                    if "minicpm-v" in models_available:
                        model = "minicpm-v"
                        logger.info("Usando modelo rápido: minicpm-v")
                    elif "llava:7b" in models_available:
                        model = "llava:7b"
                        logger.info("Usando modelo rápido: llava:7b")
                    else:
                        model = "llava"
                        logger.info(
                            "Usando llava padrão (pode demorar 2-3 min)"
                        )
                except Exception as e:
                    logger.debug(f"Erro detectando modelos: {e}")
                    model = "llava"
            
            # Preparar payload para Ollama
            payload = {
                "model": model,
                "prompt": clean_prompt,
                "images": [image_b64],
                "stream": False,
                "options": {
                    # Tokens reduzidos para respostas EXTREMAMENTE concisas
                    # 70 tokens ≈ 210 caracteres máximo
                    "num_predict": 70,
                    "temperature": 0.3  # Muito baixo para resposta curta
                }
            }
            
            # Fazer requisição
            response = httpx.post(
                url,
                json=payload,
                timeout=300.0
            )
            
            if response.status_code == 200:
                result = response.json()
                text = result.get("response", "")
                
                if text and len(text) > 10:
                    logger.info(
                        f"Análise Ollama concluída: {len(text)} caracteres"
                    )
                    # Escapar aspas duplas e quebras de linha no texto
                    clean_text = text.replace('"', '\\"').replace('\n', ' ')
                    msg = f'{{"success": true, "text": "{clean_text}"}}'
                    return msg
                
                error_msg = "Ollama retornou resposta vazia ou muito curta"
                logger.error(f"{error_msg}: '{text}'")
                msg = f'{{"success": false, "message": "{error_msg}"}}'
                return msg
            else:
                error_msg = (
                    f"Ollama HTTP {response.status_code}: "
                    f"{response.text}"
                )
                logger.error(error_msg)
                msg = f'{{"success": false, "message": "{error_msg}"}}'
                return msg
        
        except Exception as e:
            error_msg = f"Ollama failed: {str(e)}"
            logger.error(error_msg)
            msg = f'{{"success": false, "message": "{error_msg}"}}'
            return msg

    def _analyze_with_gemini(self, image_b64: str,
                             prompt: str) -> str:
        """Analisar imagem usando Google Gemini Vision API."""
        try:
            import os
            import httpx
            
            # Obter chave Gemini
            gemini_key = os.getenv("GEMINI_API_KEY", "")
            if not gemini_key:
                config = ConfigManager.get_instance()
                gemini_key = config.get_config(
                    "CAMERA_OPTIONS.GEMINI_API_KEY", ""
                )
            
            if not gemini_key:
                error_msg = "GEMINI_API_KEY não configurada"
                logger.error(error_msg)
                msg = f'{{"success": false, "message": "{error_msg}"}}'
                return msg
            
            logger.info("Analisando com Gemini Vision API...")
            
            # URL do Gemini
            url = (
                "https://generativelanguage.googleapis.com/v1beta/models/"
                "gemini-2.0-flash-exp:generateContent"
            )
            
            # Preparar payload para Gemini
            gemini_payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "inlineData": {
                                    "mimeType": "image/jpeg",
                                    "data": image_b64
                                }
                            },
                            {"text": prompt}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 2048
                }
            }
            
            # Fazer requisição
            headers = {"Content-Type": "application/json"}
            response = httpx.post(
                f"{url}?key={gemini_key}",
                json=gemini_payload,
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                candidates = result.get("candidates", [])
                if candidates:
                    parts = (
                        candidates[0].get("content", {})
                        .get("parts", [])
                    )
                    if parts:
                        text = parts[0].get("text", "")
                        logger.info(
                            "Análise Gemini concluída com sucesso"
                        )
                        msg = f'{{"success": true, "text": "{text}"}}'
                        return msg
                
                error_msg = "Gemini retornou resposta vazia"
                logger.error(error_msg)
                msg = f'{{"success": false, "message": "{error_msg}"}}'
                return msg
            else:
                error_msg = (
                    f"Gemini HTTP {response.status_code}: "
                    f"{response.text}"
                )
                logger.error(error_msg)
                msg = f'{{"success": false, "message": "{error_msg}"}}'
                return msg
        
        except Exception as e:
            error_msg = f"Gemini analysis failed: {str(e)}"
            logger.error(error_msg)
            msg = f'{{"success": false, "message": "{error_msg}"}}'
            return msg

