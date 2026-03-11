from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_generate_and_validate():
    payload = {
        "prompt": "创建一个电机控制 FB 输入 Start Stop Fault",
        "mode": "balanced",
        "model": "local",
    }
    generate_resp = client.post("/generate", json=payload)
    assert generate_resp.status_code == 200
    data = generate_resp.json()
    assert "FUNCTION_BLOCK" in data["scl_code"]
    assert data["validation"]["status"] in {"pass", "warning", "error"}

    validate_resp = client.post("/validate", json={"scl_code": data["scl_code"], "mode": "safe"})
    assert validate_resp.status_code == 200
