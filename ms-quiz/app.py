from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

from api.v1.router import api_router
from db.database import init_db, drop_db
from db.models.quiz import *

app = FastAPI(
    title="Kiwi Quiz API",
    description="API para la generación y gestión de quizzes educativos",
    version="1.0.0"
)

# CORS
# I-01: lista blanca de orígenes (antes "*" con credenciales). ms-quiz solo recibe
# tráfico del gateway, por lo que en compose no necesita orígenes de navegador.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:5174").split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# API v1 (Las versiones se iran cambiando en base a los cambios que se hagan en la API)
# Esperemos que haya v2
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Inicializa la base de datos al arrancar la aplicación"""
    #await drop_db()
    await init_db()

@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint para verificar que la API está funcionando"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)
