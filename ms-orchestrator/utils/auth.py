from fastapi import Request, HTTPException
import httpx
import os

USERS_URL = os.getenv("USERS_URL", "http://localhost:8001")
        
async def _validate(request: Request, path: str) -> None:
    auth = request.headers.get("authorization")
    if not auth:
        # Antes se enviaba None como header -> TypeError -> 500
        raise HTTPException(status_code=401, detail="Token requerido")
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(f"{USERS_URL}{path}", headers={"Authorization": auth})
            res.raise_for_status()
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")


async def verify_token(request: Request):
    await _validate(request, "/auth/validate-token")


async def verify_token_role_teacher(request: Request):
    await _validate(request, "/auth/validate-token/teacher")


async def verify_token_role_student(request: Request):
    await _validate(request, "/auth/validate-token/student")


# ───────────── Identidad desde el token (T-01 / E-03) ─────────────
# El gateway nunca confía en ids de usuario que vengan del cliente (body o path):
# obtiene id y rol del JWT validado por ms-user y los compara.

async def get_current_user(request: Request) -> dict:
    """Devuelve {id, email, role} del token validado por ms-user; 401 si no es válido."""
    auth = request.headers.get("authorization")
    if not auth:
        raise HTTPException(status_code=401, detail="Token requerido")
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{USERS_URL}/auth/claims", headers={"Authorization": auth})
    if res.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return res.json()


def ensure_same_user(current_user: dict, user_id) -> None:
    """403 si el id indicado por el cliente no es el del token."""
    try:
        same = int(user_id) == int(current_user.get("id"))
    except (TypeError, ValueError):
        same = False
    if not same:
        raise HTTPException(status_code=403, detail="No puedes operar sobre otro usuario")


def ensure_role(current_user: dict, *roles: str) -> None:
    """403 si el rol del token no está entre los permitidos."""
    if str(current_user.get("role", "")).upper() not in {r.upper() for r in roles}:
        raise HTTPException(status_code=403, detail="Rol no autorizado para esta operación")
