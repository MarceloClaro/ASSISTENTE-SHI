import io
import base64
from typing import Dict, Any, Optional

from fastapi.testclient import TestClient
from PIL import Image

from src.api.vision_api_server import app, get_provider, auth_dependency


class FakeProvider:
    def analyze_image(
        self,
        image_base64: str,
        question: str,
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        return {
            "provider": "fake",
            "question": question,
            "context": context,
            "image_len": len(image_base64),
            "text": "OK",
        }


def _make_png_bytes() -> bytes:
    img = Image.new("RGB", (8, 8), color=(255, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_health_ok():
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_analyze_requires_auth_header():
    client = TestClient(app)
    resp = client.post(
        "/api/vision/analyze",
        files={"image": ("test.png", _make_png_bytes(), "image/png")},
        data={"question": "o que é?"},
    )
    assert resp.status_code == 401


def test_analyze_with_fake_provider_and_auth_bypass(monkeypatch):
    # Sobrepõe dependências: provider e auth
    app.dependency_overrides[get_provider] = lambda: FakeProvider()
    app.dependency_overrides[auth_dependency] = lambda: {"ok": True}

    client = TestClient(app)
    png = _make_png_bytes()
    b64 = base64.b64encode(png).decode("utf-8")

    resp = client.post(
        "/api/vision/analyze",
        headers={"Authorization": "Bearer test"},
        files={"image": ("test.png", png, "image/png")},
        data={"question": "descreva", "context": "teste"},
    )

    assert resp.status_code == 200
    payload = resp.json()["result"]
    assert payload["provider"] == "fake"
    assert payload["question"] == "descreva"
    assert payload["context"] == "teste"
    assert payload["text"] == "OK"
    assert payload["image_len"] == len(b64)

    # Limpa overrides
    app.dependency_overrides.pop(get_provider, None)
    app.dependency_overrides.pop(auth_dependency, None)


if __name__ == "__main__":
    # Executa testes simples quando chamado diretamente
    test_health_ok()
    test_analyze_requires_auth_header()
    # Usa monkeypatch-like manual via overrides
    test_analyze_with_fake_provider_and_auth_bypass(monkeypatch=None)
    print("Testes de visão executados com sucesso.")
