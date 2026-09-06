"""
Smoke test do NeoBank: bate em todas as rotas GET registradas no Flask
e reporta quais quebram (500), sem validar o conteúdo da resposta —
só confirma que nada estourou erro de servidor.
"""
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture
def logged_client(client):
    """Faz login antes de testar rotas protegidas. Ajuste usuario/senha
    para um usuario de teste real que exista no seu banco de testes."""
    client.post("/api/login", json={"usuario": "teste", "senha": "123456"})
    return client


def get_all_get_routes():
    """Descobre automaticamente todas as rotas GET sem parametros de URL
    (ex: /api/dashboard, mas nao /api/conta/<id>)."""
    routes = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and "<" not in str(rule):
            routes.append(str(rule))
    return sorted(set(routes))


@pytest.mark.parametrize("route", get_all_get_routes())
def test_rota_nao_quebra_com_500(logged_client, route):
    """Bate em cada rota GET e falha se der 500 (erro interno)."""
    resp = logged_client.get(route)
    assert resp.status_code != 500, (
        f"Rota {route} quebrou com 500: "
        f"{resp.get_data(as_text=True)[:500]}"
    )


def test_health():
    """Teste direto do endpoint de health, sem precisar de login."""
    with app.test_client() as c:
        resp = c.get("/health")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "ok"
