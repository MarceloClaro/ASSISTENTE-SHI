import os
import json
import base64
import logging
from io import BytesIO
from typing import Optional, Dict, Any

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form,
    Depends,
    Header,
    HTTPException,
    status,
)

try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    # dotenv é opcional; prossegue se não estiver disponível
    pass

from PIL import Image

from src.utils.jwt_auth import require_auth_header
from src.mcp.tools.providers.vllm_openai_provider import (
    OpenAICompatibleVisionProvider,
)


logger = logging.getLogger(__name__)
app = FastAPI(title="Vision API", version="1.0.0")


CONFIG_PATH = os.getenv(
    "VISION_CONFIG_PATH",
    os.path.join(os.getcwd(), "config", "config.json"),
)


def _resolve_env(value: Any) -> Any:
    """
    Substitui valores no formato ${VAR} por envs, mantendo o valor original
    como fallback.
    """
    if (
        isinstance(value, str)
        and value.startswith("${")
        and value.endswith("}")
    ):
        env_key = value[2:-1]
        return os.getenv(env_key, "")
    return value


def _load_config() -> Dict[str, Any]:
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data or {}
    except Exception as exc:
        logger.warning("Não foi possível carregar config.json: %s", exc)
        return {}


def _choose_api_key(cfg: Dict[str, Any]) -> str:
    """
    Seleciona a API key disponível: prioridade envs diretas,
    depois config VLLM.
    """
    direct_env = (
        os.getenv("ZHIPU_API_KEY")
        or os.getenv("OPENAI_API_KEY")
        or os.getenv("ALIBABA_API_KEY")
    )
    if direct_env:
        return direct_env

    vllm = cfg.get("VLLM", {})
    selected = cfg.get("selected_module", {}).get("VLLM")
    if selected and selected in vllm:
        candidate = _resolve_env(vllm[selected].get("api_key"))
        return candidate or ""
    return ""


def _extract_base_url(api_url: str) -> str:
    if not api_url:
        return ""
    marker = "/chat/completions"
    if marker in api_url:
        return api_url.split(marker)[0]
    return api_url


def get_provider() -> OpenAICompatibleVisionProvider:
    """
    Cria o provider OpenAI-compatível usando envs ou config.json
    (VLLM selecionado).
    """
    cfg = _load_config()
    vllm_cfg = cfg.get("VLLM", {})
    selected = os.getenv("VISION_PROVIDER") or cfg.get(
        "selected_module", {}
    ).get("VLLM")
    block = vllm_cfg.get(selected, {}) if selected else {}

    model = os.getenv("VISION_MODEL") or block.get("model") or "glm-4v"
    api_key = _choose_api_key(cfg)
    base_url = (
        os.getenv("VISION_BASE_URL")
        or _extract_base_url(block.get("api_url", ""))
        or "https://open.bigmodel.cn/api/paas/v4"
    )

    config: Dict[str, Any] = {
        "model": model,
        "base_url": base_url,
        "api_key": api_key,
    }
    return OpenAICompatibleVisionProvider(config)


def auth_dependency(
    authorization: Optional[str] = Header(None),
) -> Dict[str, Any]:
    """Dependência de autenticação JWT baseada no cabeçalho Authorization."""
    # Valida e lança HTTPException em caso de erro
    try:
        require_auth_header(authorization)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unauthorized: {e}",
        )


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


def _validate_and_b64(file: UploadFile) -> str:
    """Valida a imagem e retorna seu conteúdo em base64."""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Arquivo enviado não é uma imagem",
        )
    data = file.file.read()
    if not data:
        raise HTTPException(
            status_code=400,
            detail="Arquivo de imagem está vazio",
        )
    try:
        # Validar imagem abrindo com Pillow
        Image.open(BytesIO(data)).verify()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Imagem inválida ou corrompida",
        )
    return base64.b64encode(data).decode("utf-8")


@app.post("/api/vision/analyze")
def analyze(
    image: UploadFile = File(...),
    question: str = Form(...),
    context: Optional[str] = Form(None),
    _auth: Dict[str, Any] = Depends(auth_dependency),
    provider: OpenAICompatibleVisionProvider = Depends(get_provider),
) -> Dict[str, Any]:
    try:
        image_b64 = _validate_and_b64(image)
        result = provider.analyze_image(image_b64, question, context)
        return {"result": result}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erro no processamento de visão")
        raise HTTPException(status_code=500, detail=f"Erro interno: {e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api.vision_api_server:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=False,
    )
