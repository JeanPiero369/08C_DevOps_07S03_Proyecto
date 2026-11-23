import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from router import include_all_routers

load_dotenv()

logger = logging.getLogger("kiwi.gateway")

app = FastAPI()

# I-01: lista blanca de orígenes (antes "*" con credenciales). Separados por coma.
ALLOWED_ORIGINS = [
    o.strip()
    for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:5174").split(",")
    if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

GENERIC_ERROR = "Error interno del servidor. Inténtalo más tarde."


@app.exception_handler(HTTPException)
async def sanitize_server_errors(request: Request, exc: HTTPException):
    """I-01: los 5xx no exponen detalles internos (URLs, trazas, texto de otros servicios)."""
    if exc.status_code >= 500:
        logger.error("Error %s en %s %s: %s", exc.status_code, request.method, request.url.path, exc.detail)
        return JSONResponse(status_code=exc.status_code, content={"detail": GENERIC_ERROR})
    return await http_exception_handler(request, exc)


@app.exception_handler(Exception)
async def unhandled_errors(request: Request, exc: Exception):
    logger.exception("Error no controlado en %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": GENERIC_ERROR})


include_all_routers(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
