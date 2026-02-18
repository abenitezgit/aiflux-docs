from datetime import timedelta
from fastapi import APIRouter, Depends, Request, Response, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

# 1. ACTUALIZAR ESTA LÍNEA (Añadir los modelos faltantes)
from app.core.database import get_db, init_rls  # Añadimos init_rls
from app.core.config import settings
from app.core.auth import authenticate_user
from app.core.security import create_access_token, get_password_hash
from app.models import UsuarioDB, Categoria, Cuaderno, Tema # <--- Importar todos


router = APIRouter()
templates = Jinja2Templates(directory="templates")

# --- LOGIN ---
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("pages/login.html", {"request": request})

@router.post("/login")
async def login_action(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(session, email, password)
    if not user:
        return RedirectResponse(url="/login?error=1", status_code=status.HTTP_303_SEE_OTHER)
    
    # Crear Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    
    # Redirigir + Set Cookie
    resp = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    resp.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False # True si usas HTTPS en prod
    )
    return resp

# --- LOGOUT ---
@router.get("/logout")
async def logout():
    resp = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    resp.delete_cookie("access_token")
    return resp

# --- REGISTER ---
@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("pages/register.html", {"request": request})

@router.post("/register")
async def register_action(
    email: str = Form(...),
    password: str = Form(...),
    nombre: str = Form(...),
    session: AsyncSession = Depends(get_db)
):
    # Verificar si existe
    statement = select(UsuarioDB).where(UsuarioDB.email == email)
    result = await session.exec(statement)
    if result.first():
        return RedirectResponse(url="/register?error=exists", status_code=status.HTTP_303_SEE_OTHER)
    
    # Crear Usuario
    hashed_pwd = get_password_hash(password)
    new_user = UsuarioDB(email=email, hashed_password=hashed_pwd, nombre=nombre)
    session.add(new_user)
    
    # IMPORTANTE: Necesitamos el ID generado para el RLS
    await session.flush() 

    # 2. AXIOMA II.I: Inyectar RLS para poder crear la estructura inicial
    # Sin esto, las políticas de Postgres que ejecutaste antes bloquearían la inserción
    await init_rls(session, str(new_user.id))

    # Crear Estructura Maestra
    try:
        # Categoría General
        cat_general = Categoria(nombre="General", user_id=new_user.id, icono="folder")
        session.add(cat_general)
        await session.flush()

        # Cuaderno Inbox
        inbox = Cuaderno(nombre="Inbox", user_id=new_user.id, categoria_id=cat_general.id, tipo="cuaderno")
        session.add(inbox)
        await session.flush()

        # Tema Capturas Rápidas
        tema_capturas = Tema(nombre="Capturas Rápidas", user_id=new_user.id, cuaderno_id=inbox.id)
        session.add(tema_capturas)

        await session.commit()
    except Exception as e:
        await session.rollback()
        print(f"Error creando estructura inicial: {e}")
        return RedirectResponse(url="/register?error=structure", status_code=status.HTTP_303_SEE_OTHER)

    return RedirectResponse(url="/login?registered=1", status_code=status.HTTP_303_SEE_OTHER)