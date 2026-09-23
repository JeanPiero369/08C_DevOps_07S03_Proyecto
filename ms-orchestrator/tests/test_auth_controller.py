"""Pruebas unitarias del controlador /auth del orquestador.

El microservicio de usuarios se simula con respx: no se necesita
levantar ms-user ni la base de datos para ejecutar estas pruebas.
"""
import httpx
import respx

LOGIN_BODY = {"email": "ana@kiwi.com", "password": "Clave123"}


@respx.mock
def test_login_exitoso_devuelve_token(client, users_url):
    respx.post(f"{users_url}/auth/login").mock(
        return_value=httpx.Response(200, json={"token": "jwt-falso"})
    )
    res = client.post("/auth/login", json=LOGIN_BODY)
    assert res.status_code == 200
    assert res.json() == {"token": "jwt-falso"}


@respx.mock
def test_login_propaga_401_del_servicio_de_usuarios(client, users_url):
    respx.post(f"{users_url}/auth/login").mock(
        return_value=httpx.Response(401, text="Credenciales inválidas")
    )
    res = client.post("/auth/login", json=LOGIN_BODY)
    assert res.status_code == 401


@respx.mock
def test_login_devuelve_503_si_usuarios_no_responde(client, users_url):
    respx.post(f"{users_url}/auth/login").mock(
        side_effect=httpx.ConnectError("sin conexión")
    )
    res = client.post("/auth/login", json=LOGIN_BODY)
    assert res.status_code == 503


@respx.mock
def test_login_con_body_invalido_no_llama_al_servicio(client, users_url):
    ruta = respx.post(f"{users_url}/auth/login")
    res = client.post("/auth/login", json={"email": "malo", "password": "x"})
    assert res.status_code == 422
    assert not ruta.called


@respx.mock
def test_registro_exitoso_devuelve_token(client, users_url):
    respx.post(f"{users_url}/auth/register").mock(
        return_value=httpx.Response(200, json={"token": "jwt-nuevo"})
    )
    body = {"email": "nuevo@kiwi.com", "password": "Clave123", "role": "STUDENT"}
    res = client.post("/auth/register", json=body)
    assert res.status_code == 200
    assert res.json()["token"] == "jwt-nuevo"
