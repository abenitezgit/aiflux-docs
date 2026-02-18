# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel
import os
import logging
import sys

# ⚙️ Configurar logging para mostrar en consola
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('server.log')
    ]
)

from app.core.database import engine
from app.core.config import settings
from app.models import * 
from app.routers import dashboard, auth, ai

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION, lifespan=lifespan)

# Asegurar que la carpeta static existe para evitar errores de montado
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates") 

# --- MANEJADOR DE ERRORES (Redirección al Login) ---
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    # Para otros errores, dejar que FastAPI lo maneje normalmente
    raise exc

# --- RUTAS ---
@app.get("/")
async def root():
    """Redirige la raíz al dashboard directamente"""
    return RedirectResponse(url="/dashboard")

app.include_router(dashboard.router)
app.include_router(auth.router)
app.include_router(ai.router)