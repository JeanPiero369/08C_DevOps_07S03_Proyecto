"""Pruebas de autorización del gateway (T-01, E-03, I-01, I-03).

Los microservicios se simulan con respx. La identidad siempre viene de
GET /auth/claims de ms-user, nunca de ids enviados por el cliente.
"""
import httpx
import respx

USERS = "http://localhost:8001"
QUICES = "http://localhost:8002/api/v1"
CLASSROOMS = "http://localhost:8003"
CHARACTERS = "http://localhost:8004"
AUTH = {"Authorization": "Bearer token-de-prueba"}

STUDENT_7 = {"id": 7, "email": "ana@kiwi.com", "role": "STUDENT"}
TEACHER_3 = {"id": 3, "email": "profe@kiwi.com", "role": "TEACHER"}


def _as(user, student_route_ok=True):
    """Simula el token de `user` en ms-user."""
    respx.get(f"{USERS}/auth/claims").mock(return_value=httpx.Response(200, json=user))
    respx.post(f"{USERS}/auth/validate-token").mock(return_value=httpx.Response(200))
    role_ok = 200 if user["role"] == "STUDENT" and student_route_ok else 403
    respx.post(f"{USERS}/auth/validate-token/student").mock(return_value=httpx.Response(role_ok))
    respx.post(f"{USERS}/auth/validate-token/teacher").mock(
        return_value=httpx.Response(200 if user["role"] == "TEACHER" else 403))


SUBMISSION = {"quiz_id": 1, "is_present": True, "questions": []}


# ───────────── T-01: IDOR en intentos y monedas ─────────────

@respx.mock
def test_quiz_submit_para_otro_estudiante_es_403_y_no_llama_a_servicios(client):
    _as(STUDENT_7)
    submit = respx.post(f"{QUICES}/quiz/submit_answers")
    coins = respx.post(url__regex=rf"{USERS}/student/\d+/add-coins/.*")
    res = client.post("/student/classroom/1/quiz-submit", json={**SUBMISSION, "student_id": 99}, headers=AUTH)
    assert res.status_code == 403
    assert not submit.called and not coins.called


@respx.mock
def test_quiz_submit_propio_se_procesa(client):
    _as(STUDENT_7)
    respx.post(f"{QUICES}/quiz/submit_answers").mock(
        return_value=httpx.Response(200, json={"obtained_points": 5}))
    respx.patch(f"{CLASSROOMS}/classrooms/1/student-quiz-points").mock(return_value=httpx.Response(200, json={}))
    coins = respx.post(f"{USERS}/student/7/add-coins/5").mock(return_value=httpx.Response(200))
    res = client.post("/student/classroom/1/quiz-submit", json={**SUBMISSION, "student_id": 7}, headers=AUTH)
    assert res.status_code == 201
    assert coins.called


@respx.mock
def test_quiz_list_de_otro_estudiante_es_403(client):
    _as(STUDENT_7)
    res = client.get("/student/classroom/1/student/99/quiz-list", headers=AUTH)
    assert res.status_code == 403


@respx.mock
def test_comprar_personaje_con_monedas_de_otro_es_403(client):
    _as(STUDENT_7)
    store = respx.post(f"{CHARACTERS}/store/buy")
    res = client.post("/characters/buy", json={"characterId": 1, "userId": 99}, headers=AUTH)
    assert res.status_code == 403
    assert not store.called


@respx.mock
def test_set_principal_de_otro_es_403(client):
    _as(STUDENT_7)
    res = client.patch("/characters/set-principal",
                       json={"userId": 99, "oldCharacterId": 1, "newCharacterId": 2}, headers=AUTH)
    assert res.status_code == 403


@respx.mock
def test_sin_token_es_401(client):
    respx.post(f"{USERS}/auth/validate-token").mock(return_value=httpx.Response(403))
    res = client.post("/characters/buy", json={"characterId": 1, "userId": 7})
    assert res.status_code == 401


# ───────────── E-03: autorización por rol ─────────────

@respx.mock
def test_estudiante_no_puede_crear_personajes(client):
    _as(STUDENT_7)
    create = respx.post(f"{CHARACTERS}/characters")
    res = client.post("/characters", json={"name": "x", "price": 1}, headers=AUTH)
    assert res.status_code == 403
    assert not create.called


@respx.mock
def test_docente_puede_crear_personajes(client):
    _as(TEACHER_3)
    respx.post(f"{CHARACTERS}/characters").mock(return_value=httpx.Response(201, json={"id": 5}))
    res = client.post("/characters", json={"name": "x", "price": 1}, headers=AUTH)
    assert res.status_code == 200
    assert res.json() == {"id": 5}


@respx.mock
def test_estudiante_no_ve_resultados_de_todo_el_quiz(client):
    _as(STUDENT_7)
    results = respx.get(f"{QUICES}/quiz/1/results")
    res = client.get("/quiz/1/results", headers=AUTH)
    assert res.status_code == 403
    assert not results.called


@respx.mock
def test_estudiante_no_ve_resultado_individual_de_otro(client):
    _as(STUDENT_7)
    res = client.get("/quiz/1/student/99/result", headers=AUTH)
    assert res.status_code == 403


# ───────────── I-03: el hash nunca sale del gateway ─────────────

@respx.mock
def test_perfil_no_expone_password_aunque_el_servicio_lo_envie(client):
    _as(STUDENT_7)
    respx.get(f"{USERS}/student/me").mock(return_value=httpx.Response(200, json={
        **STUDENT_7, "name": "Ana", "last_name": "Q", "password": "$2a$10$hashfalso"}))
    res = client.get("/student/me", headers=AUTH)
    assert res.status_code == 200
    assert "password" not in res.json()


# ───────────── I-01: CORS y errores ─────────────

def test_cors_rechaza_origen_no_permitido(client):
    res = client.options("/auth/login", headers={
        "Origin": "https://atacante.example", "Access-Control-Request-Method": "POST"})
    assert res.headers.get("access-control-allow-origin") != "https://atacante.example"


def test_cors_permite_el_frontend(client):
    res = client.options("/auth/login", headers={
        "Origin": "http://localhost:5174", "Access-Control-Request-Method": "POST"})
    assert res.headers.get("access-control-allow-origin") == "http://localhost:5174"


@respx.mock
def test_error_500_no_filtra_detalles_internos(client):
    respx.post(f"{USERS}/auth/login").mock(
        return_value=httpx.Response(500, text="org.postgresql.util.PSQLException at db:5432"))
    res = client.post("/auth/login", json={"email": "ana@kiwi.com", "password": "Clave123"})
    assert res.status_code == 500
    assert "PSQL" not in res.text and "5432" not in res.text


@respx.mock
def test_servicio_caido_no_expone_url_interna(client):
    respx.post(f"{USERS}/auth/login").mock(side_effect=httpx.ConnectError("sin conexión"))
    res = client.post("/auth/login", json={"email": "ana@kiwi.com", "password": "Clave123"})
    assert res.status_code == 503
    assert "localhost:8001" not in res.text


# ───────────── E-02: el código de invitación llega a ms-user ─────────────

@respx.mock
def test_registro_reenvia_codigo_de_invitacion(client):
    ruta = respx.post(f"{USERS}/auth/register").mock(return_value=httpx.Response(200, json={"token": "t"}))
    body = {"email": "profe@kiwi.com", "password": "Clave123", "role": "TEACHER", "invite_code": "abc"}
    assert client.post("/auth/register", json=body).status_code == 200
    assert b'"invite_code":"abc"' in ruta.calls.last.request.content.replace(b" ", b"")


@respx.mock
def test_registro_con_codigo_invalido_propaga_403(client):
    respx.post(f"{USERS}/auth/register").mock(
        return_value=httpx.Response(403, text="Código de invitación docente inválido"))
    body = {"email": "x@kiwi.com", "password": "Clave123", "role": "TEACHER", "invite_code": "malo"}
    assert client.post("/auth/register", json=body).status_code == 403
