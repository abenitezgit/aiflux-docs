# CONTEXTO DEL PROYECTO: mi_documentacion
Generado automáticamente para revisión de código.

## 📁 Estructura del Proyecto
```
    📄 requirements.txt
    📄 .gitignore
    📄 .env
    📂 app/
        📄 auth.py
        📄 models.py
        📄 database.py
        📄 __init__.py
        📄 .env
        📄 main.py
        📄 dependencies.py
        📂 routers/
            📄 dashboard.py
            📄 editor.py
        📂 templates/
            📄 base_app.html
            📄 register.html
            📄 login.html
            📂 modules/
                📄 inspector_pane.html
                📄 sidebar_notebook.html
                📄 sidebar_dashboard.html
                📄 list_pane.html
                📄 placeholder_pane.html
                📄 cockpit_pane.html
            📂 partials/
                📄 lista_notas_evernote.html
                📄 lista_adjuntos.html
                📄 editor_pane.html
                📄 omnibar_results.html
                📂 modales/
                    📂 sidebar/
                        📄 manage_notebook.html
                        📄 edit_category.html
                        📄 create_category.html
                    📂 cockpit/
                        📄 quick_note.html
                        📄 create_task.html
                        📄 edit_task.html
                    📂 list/
                        📄 edit_topic.html
                        📄 create_topic.html
                    📂 global/
                        📄 security.html
                        📄 omnibar.html
                    📂 editor/
                        📄 move_note.html
    📂 docs/
        📄 POST_ANALISIS_REFLEXION.md
        📄 SOLUCION_POPOVERS_POSITIONING.md
        📄 TESTING_TOOLBAR_GUIA_INTERACTIVA.md
        📄 RESUMEN_CONVERSACION_COMPLETA.md
        📄 RESUMEN_EJECUTIVO.md
        📄 AGREGADO_SISTEMA_DEBUGGING.md
        📄 ANALISIS_BOTON_TAMAÑO_LETRA.md
        📄 OPTIMIZACION_CARGA_PARCIAL_NOTAS.md
        📄 FONT_FAMILY_TAMAÑO_REINCORPORADO.md
        📄 VERIFICACION_IMPLEMENTACION.md
        📄 SIMPLIFICACION_TOOLBAR_COMPLETADA.md
        📄 SOLUCION_RAPIDA_TOOLBAR.md
        📄 PLAN_REFACTORIZACION_CSS.md
        📄 IMPLEMENTACION_COMPLETA.md
        📄 INDICE_DOCUMENTACION.md
        📄 QUICK_SUMMARY_FONTS.md
        📄 contexto_telecom.md
        📄 PROBLEMA_ENCONTRADO_Y_SOLUCION.md
        📄 ANALISIS_PROFUNDO_TOOLBAR_ISSUES.md
        📄 RESUMEN_CORRECCIONES_TAMAÑO_LETRA.md
        📄 RESUMEN_VISUAL_HERENCIA.md
        📄 RESUMEN_SIMPLIFICACION_TOOLBAR.md
        📄 SOLUCION_FINAL_TOOLBAR.md
        📄 CHECKLIST_VALIDACION_OPTIMIZACION.md
        📄 GUIA_RAPIDA.md
        📄 VERIFICACION_RAPIDA_CAMBIOS.md
        📄 ANALISIS_HERENCIA_CSS_EDITOR.md
        📄 NOTAS_TECNICAS_HERENCIA_CSS.md
        📄 DEBUG_TOOLBAR_GUIA_PASO_A_PASO.md
```

---

## 📄 Archivo: `app/__init__.py`
```py

```

---

## 📄 Archivo: `app/auth.py`
```py
import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from pydantic import BaseModel
import bcrypt  # <--- USAMOS BCRYPT DIRECTO
from sqlmodel import select
import uuid 

# Importamos la DB y Modelos
from database import async_session_factory
from models import UsuarioDB

# Configuración Seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 

# Modelo Pydantic para el Token
class User(BaseModel):
    id: str
    email: str
    name: str

# --- UTILIDADES DE HASH (CORREGIDAS PARA PYTHON 3.13) ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica el password usando bcrypt nativo"""
    # bcrypt requiere bytes, no strings
    if isinstance(plain_password, str):
        plain_password_bytes = plain_password.encode('utf-8')
    else:
        plain_password_bytes = plain_password
        
    if isinstance(hashed_password, str):
        hashed_password_bytes = hashed_password.encode('utf-8')
    else:
        hashed_password_bytes = hashed_password
        
    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)

def get_password_hash(password: str) -> str:
    """Genera el hash usando bcrypt nativo"""
    if isinstance(password, str):
        password_bytes = password.encode('utf-8')
    else:
        password_bytes = password
        
    # Generar salt y hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Devolvemos string para guardar en Postgres
    return hashed.decode('utf-8')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- AUTENTICACIÓN ASÍNCRONA ---
async def authenticate_user(email: str, password: str) -> Optional[User]:
    async with async_session_factory() as session:
        statement = select(UsuarioDB).where(UsuarioDB.email == email)
        result = await session.exec(statement)
        user_db = result.first()
        
        if not user_db:
            return None
        
        # Usamos nuestra nueva función verify_password
        if not verify_password(password, user_db.hashed_password):
            return None
            
        return User(id=str(user_db.id), email=user_db.email, name=user_db.nombre)

# --- DEPENDENCIA ---
# --- EN AUTH.PY ---
async def get_current_user(request: Request) -> Optional[User]:
    token = request.cookies.get("access_token")
    if not token:
        return None
    
    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        user_id: str = payload.get("id")
        user_name: str = payload.get("name")
        
        # --- VALIDACIÓN ESTRICTA AÑADIDA ---
        if not user_email or not user_id:
            return None
            
        # Intentamos convertir a UUID. Si falla, el token es corrupto.
        try:
            uuid_obj = uuid.UUID(str(user_id))
        except ValueError:
            print(f"Token rechazado: ID no es UUID válido ({user_id})")
            return None
        # -----------------------------------
            
        return User(id=str(uuid_obj), email=user_email, name=user_name)
    except JWTError:
        return None

async def get_authenticated_user(user: Optional[User] = Depends(get_current_user)):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
```

---

## 📄 Archivo: `app/database.py`
```py
import os
from typing import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession # Importación correcta para .exec()
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

# 1. Configuración de la URL de Base de Datos
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# 2. Crear el Motor (Engine) Asíncrono
# FIX SUPABASE: connect_args={"statement_cache_size": 0} es OBLIGATORIO
# para evitar el error de "DuplicatePreparedStatementError" con PgBouncer.
engine = create_async_engine(
    DATABASE_URL, 
    echo=False, 
    future=True,
    connect_args={"statement_cache_size": 0} 
)

# 3. Factoría de Sesiones
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# 4. Función de Utilidad RLS (Row Level Security)
async def init_rls(session: AsyncSession, user_id: str):
    """
    Inyecta el ID del usuario en la sesión de Postgres.
    """
    if user_id:
        await session.execute(text(f"SET LOCAL app.current_user_id = '{user_id}'"))
    else:
        await session.execute(text("SET LOCAL app.current_user_id = ''"))

# 5. Dependencia Base
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
```

---

## 📄 Archivo: `app/dependencies.py`
```py

from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import async_session_factory, init_rls
from auth import get_current_user, User

# --- DEPENDENCIA MAESTRA RLS ---
# Cualquier ruta que use esta dependencia obtendrá una sesión de DB
# que YA TIENE el filtro de seguridad aplicado.
# El programador NO tiene que filtrar manualmente por user_id.

async def get_db_session(
    current_user: User = Depends(get_current_user)
) -> AsyncGenerator[AsyncSession, None]:
    
    # 1. Abrimos una conexión nueva
    async with async_session_factory() as session:
        try:
            # 2. Determinamos el ID para RLS
            user_id = current_user.id if current_user else ""
            
            # 3. INYECTAMOS LA SEGURIDAD (SET LOCAL app.current_user_id...)
            # Esto ocurre antes de cualquier consulta del router
            await init_rls(session, user_id)
            
            # 4. Entregamos la sesión segura al router
            yield session
            
        finally:
            # 5. Cerramos la conexión al terminar el request
            await session.close()
```

---

## 📄 Archivo: `app/main.py`
```py
# --- START OF FILE main.py ---

from fastapi import FastAPI, Request, Response, Depends, Form, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from sqlmodel import select, SQLModel
from sqlalchemy.ext.asyncio import AsyncSession
import json

# Imports Auth
from auth import (
    authenticate_user, 
    create_access_token, 
    get_password_hash
)
from models import UsuarioDB
from database import async_session_factory, engine

# Imports Routers
from routers import dashboard, editor

# --- LIFESPAN: Inicialización de Tablas ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # En producción, lo ideal es usar Alembic para migraciones.
    # Para este desarrollo, esto asegura que las tablas existan.
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield

app = FastAPI(title="Docs.ai Core", lifespan=lifespan)

# Si decides usar CSS propio en el futuro:
# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
templates.env.filters["tojson"] = json.dumps

# --- MANEJADOR DE ERRORES ---
@app.exception_handler(HTTPException)
async def unauthorized_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        # Si la petición viene de HTMX, hacemos una redirección especial
        if request.headers.get("HX-Request"):
            response = Response(status_code=status.HTTP_200_OK)
            response.headers["HX-Redirect"] = "/login"
            return response
        # Si es navegación normal, redirect estándar
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

# 1. Incluir Routers
app.include_router(dashboard.router)
app.include_router(editor.router)

# 2. Rutas de Autenticación

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_action(
    response: Response,
    email: str = Form(...), 
    password: str = Form(...)
):
    user = await authenticate_user(email, password) 
    if not user:
        return RedirectResponse(url="/login?error=1", status_code=status.HTTP_303_SEE_OTHER)
    
    access_token = create_access_token(data={"sub": user.email, "id": user.id, "name": user.name})
    
    resp = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    resp.set_cookie(
        key="access_token", 
        value=f"Bearer {access_token}", 
        httponly=True,
        max_age=60 * 60 * 24 * 7,
        samesite="lax"
    )
    return resp

@app.get("/logout")
async def logout():
    resp = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    resp.delete_cookie("access_token")
    return resp

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register_action(
    email: str = Form(...),
    password: str = Form(...),
    nombre: str = Form(...)
):
    async with async_session_factory() as session:
        # Verificar si existe
        existing = await session.exec(select(UsuarioDB).where(UsuarioDB.email == email))
        if existing.first():
            return RedirectResponse(url="/register?error=exists", status_code=303)
        
        # Crear Usuario
        hashed_pwd = get_password_hash(password)
        new_user = UsuarioDB(email=email, hashed_password=hashed_pwd, nombre=nombre)
        
        session.add(new_user)
        await session.commit()
        # Nota: El usuario se crea, pero no hace login automático. 
        # Lo enviamos al login con un mensaje de éxito.
        
    return RedirectResponse(url="/login?registered=1", status_code=303)

@app.get("/")
async def root():
    return RedirectResponse(url="/dashboard")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8020, reload=True)
```

---

## 📄 Archivo: `app/models.py`
```py
import uuid
from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, Column, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ARRAY
from sqlalchemy import text


class UsuarioDB(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    email: str = Field(unique=True, index=True)
    hashed_password: str
    nombre: str
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )

# --- CATEGORÍA ---
class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    # Indexamos user_id para velocidad en RLS
    user_id: uuid.UUID = Field(nullable=False, index=True)
    
    nombre: str
    icono: str = Field(default="folder")
    color: str = Field(default="#3b82f6")
    orden: int = Field(default=0)
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )

    # Relaciones
    cuadernos: List["Cuaderno"] = Relationship(
        back_populates="categoria",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


# --- CUADERNO ---
class Cuaderno(SQLModel, table=True):
    __tablename__ = "cuadernos"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    user_id: uuid.UUID = Field(nullable=False, index=True)
    
    nombre: str
    descripcion: Optional[str] = None
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )
    
    categoria_id: Optional[uuid.UUID] = Field(default=None, foreign_key="categorias.id")

    # Campos V2
    tipo: str = Field(default="cuaderno") 
    estado: str = Field(default="activo")
    fecha_limite: Optional[datetime] = None
    progreso: int = Field(default=0)

    # Relaciones
    categoria: Optional[Categoria] = Relationship(back_populates="cuadernos")
    
    temas: List["Tema"] = Relationship(
        back_populates="cuaderno",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    tareas: List["Tarea"] = Relationship(
        back_populates="cuaderno",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


# --- TAREA ---
class Tarea(SQLModel, table=True):
    __tablename__ = "tareas"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    user_id: uuid.UUID = Field(nullable=False, index=True)
    
    titulo: str
    hecho: bool = Field(default=False)
    
    cuaderno_id: Optional[uuid.UUID] = Field(default=None, foreign_key="cuadernos.id")
    fecha_objetivo: Optional[datetime] = None
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )

    # Relaciones
    cuaderno: Optional[Cuaderno] = Relationship(back_populates="tareas")


# --- TEMA ---
class Tema(SQLModel, table=True):
    __tablename__ = "temas"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    # AÑADIDO: Propiedad directa del usuario
    user_id: uuid.UUID = Field(nullable=False, index=True)
    
    nombre: str
    orden: int = Field(default=0)
    cuaderno_id: uuid.UUID = Field(foreign_key="cuadernos.id")
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )

    # Relaciones
    cuaderno: Optional[Cuaderno] = Relationship(back_populates="temas")
    
    anotaciones: List["Anotacion"] = Relationship(
        back_populates="tema",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


# --- ANOTACION ---
class Anotacion(SQLModel, table=True):
    __tablename__ = "anotaciones"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    # AÑADIDO: Propiedad directa del usuario
    user_id: uuid.UUID = Field(nullable=False, index=True)
    
    titulo: str
    contenido: Optional[str] = None
    
    tags: List[str] = Field(
        default=[], 
        sa_column=Column(ARRAY(String))
    )
    
    tema_id: uuid.UUID = Field(foreign_key="temas.id")
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )
    updated_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={
            "server_default": text("now()"),
            "onupdate": text("now()")
        }
    )

    # Relaciones
    tema: Optional[Tema] = Relationship(back_populates="anotaciones")
    
    adjuntos: List["Adjunto"] = Relationship(
        back_populates="anotacion",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


# --- ADJUNTO ---
class Adjunto(SQLModel, table=True):
    __tablename__ = "adjuntos"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    # AÑADIDO: Propiedad directa del usuario
    user_id: uuid.UUID = Field(nullable=False, index=True)
    
    url: str
    nombre_original: Optional[str] = None
    tipo_archivo: Optional[str] = None
    anotacion_id: uuid.UUID = Field(foreign_key="anotaciones.id")
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )

    # Relaciones
    anotacion: Optional[Anotacion] = Relationship(back_populates="adjuntos")
```

---

## 📄 Archivo: `app/routers/dashboard.py`
```py
import uuid
from datetime import datetime, date
from typing import Optional, Annotated

from fastapi import APIRouter, Depends, Form, Request, Header, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select, func, col, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

# Importamos nuestros módulos Core
from auth import get_authenticated_user, User
from dependencies import get_db_session
from models import Cuaderno, Categoria, Tarea, Anotacion, Tema

# Configuración
router = APIRouter()
templates = Jinja2Templates(directory="templates")

# --- HELPER: Contexto del Sidebar ---
async def get_sidebar_context(session: AsyncSession):
    stmt_cat = (
        select(Categoria)
        .order_by(Categoria.orden, Categoria.nombre)
        .options(
            selectinload(Categoria.cuadernos).selectinload(Cuaderno.temas) 
        )
    )
    categorias = (await session.exec(stmt_cat)).all()

    stmt_proj = (
        select(Cuaderno)
        .where(Cuaderno.tipo == "proyecto", Cuaderno.estado == "activo")
        .order_by(Cuaderno.fecha_limite)
    )
    proyectos = (await session.exec(stmt_proj)).all()

    return {
        "lista_categorias": categorias,
        "sidebar_proyectos": proyectos
    }


# ==========================================
# RUTAS DASHBOARD
# ==========================================

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    user: User = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db_session)
):
    stmt_p = (
        select(Cuaderno)
        .where(Cuaderno.tipo == 'proyecto', Cuaderno.estado == 'activo')
        .options(selectinload(Cuaderno.tareas))
        .order_by(Cuaderno.fecha_limite)
    )
    proyectos_raw = (await session.exec(stmt_p)).all()

    proyectos_data = []
    for p in proyectos_raw:
        total = len(p.tareas)
        completadas = len([t for t in p.tareas if t.hecho])
        porcentaje = int((completadas / total) * 100) if total > 0 else 0
        
        color_bar = "bg-accent"
        if porcentaje == 100: 
            color_bar = "bg-emerald-500"
        elif p.fecha_limite and p.fecha_limite.date() < date.today(): 
            color_bar = "bg-red-500"

        proyectos_data.append({
            'obj': p,
            'porcentaje': porcentaje,
            'total_tareas': total,
            'completadas': completadas,
            'color_bar': color_bar
        })

    stmt_t = (
        select(Tarea)
        .where(Tarea.hecho == False)
        .options(selectinload(Tarea.cuaderno))
        .order_by(Tarea.fecha_objetivo.asc().nullslast(), Tarea.created_at.desc())
        .limit(10)
    )
    agenda = (await session.exec(stmt_t)).all()

    total_notas = (await session.exec(select(func.count(Anotacion.id)))).one()
    
    stmt_hoy = select(func.count(Tarea.id)).where(
        Tarea.hecho == False,
        func.date(Tarea.fecha_objetivo) <= date.today()
    )
    tareas_hoy = (await session.exec(stmt_hoy)).one()

    stmt_rec = (
        select(Anotacion)
        .options(
            selectinload(Anotacion.tema).selectinload(Tema.cuaderno)
        )
        .order_by(desc(Anotacion.updated_at))
        .limit(5)
    )
    recientes = (await session.exec(stmt_rec)).all()

    sidebar_data = await get_sidebar_context(session)

    return templates.TemplateResponse("base_app.html", {
        "request": request,
        "user": user,
        "view_mode": "dashboard",
        "estanterias": sidebar_data["lista_categorias"],
        "recent_notes": recientes,
        "proyectos": proyectos_data,
        "agenda": agenda,
        "stats": {'total_notas': total_notas, 'tareas_hoy': tareas_hoy},
        "today": date.today(),
        **sidebar_data
    })

# ==========================================
# ACCIONES RÁPIDAS (TAREAS)
# ==========================================

@router.post("/tarea/crear")
async def crear_tarea(
    request: Request,
    response: Response,
    titulo: str = Form(...),
    fecha_objetivo: Optional[str] = Form(None),
    cuaderno_id: Optional[str] = Form(None),
    hx_request: Optional[str] = Header(None, alias="HX-Request"),
    user: User = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db_session)
):
    # user_id ya existía en Tarea, correcto.
    nueva_tarea = Tarea(titulo=titulo, user_id=uuid.UUID(user.id))
    
    if fecha_objetivo:
        try:
            nueva_tarea.fecha_objetivo = datetime.strptime(fecha_objetivo, '%Y-%m-%d')
        except ValueError:
            pass
            
    if cuaderno_id:
        c_uuid = uuid.UUID(cuaderno_id)
        c = await session.get(Cuaderno, c_uuid)
        if c:
            nueva_tarea.cuaderno_id = c_uuid
            
    session.add(nueva_tarea)
    await session.commit()
    
    if hx_request:
        response.headers["HX-Refresh"] = "true"
        return Response(status_code=200)
        
    return RedirectResponse(url="/dashboard", status_code=303)

@router.post("/tarea/toggle/{id}")
async def toggle_tarea(
    id: uuid.UUID,
    user: User = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db_session)
):
    tarea = await session.get(Tarea, id)
    if not tarea:
        return Response(status_code=404)
        
    tarea.hecho = not tarea.hecho
    session.add(tarea)
    await session.commit()
    return Response(content="")

# ==========================================
# ACCIÓN RÁPIDA (INBOX)
# ==========================================

@router.post("/quick_note")
async def quick_note(
    request: Request,
    response: Response,
    titulo: str = Form(None),
    contenido: str = Form(""),
    hx_request: Optional[str] = Header(None, alias="HX-Request"),
    user: User = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db_session)
):
    stmt_inbox = select(Cuaderno).where(func.lower(Cuaderno.nombre) == 'inbox')
    inbox = (await session.exec(stmt_inbox)).first()
    
    uid = uuid.UUID(user.id) # Preparamos UUID del usuario

    if not inbox:
        stmt_cat = select(Categoria).where(func.lower(Categoria.nombre) == 'general')
        cat = (await session.exec(stmt_cat)).first()
        
        if not cat:
            cat = Categoria(nombre="General", orden=0, user_id=uid)
            session.add(cat)
            await session.commit()
            await session.refresh(cat)
            
        inbox = Cuaderno(
            nombre="Inbox", 
            descripcion="Bandeja de entrada personal", 
            categoria_id=cat.id,
            user_id=uid
        )
        session.add(inbox)
        await session.commit()
        await session.refresh(inbox)
        
        # FIX: Añadido user_id a Tema
        tema = Tema(nombre="Notas Sueltas", cuaderno_id=inbox.id, user_id=uid)
        session.add(tema)
        await session.commit()

    stmt_tema = select(Tema).where(Tema.cuaderno_id == inbox.id)
    tema_inbox = (await session.exec(stmt_tema)).first()
    
    if not tema_inbox:
        # FIX: Añadido user_id a Tema
        tema_inbox = Tema(nombre="General", cuaderno_id=inbox.id, user_id=uid)
        session.add(tema_inbox)
        await session.commit()
        await session.refresh(tema_inbox)

    final_titulo = titulo.strip() if titulo else "Nota Rápida " + datetime.now().strftime("%H:%M")
    
    # FIX: Añadido user_id a Anotacion
    nueva = Anotacion(titulo=final_titulo, contenido=contenido, tema_id=tema_inbox.id, user_id=uid)
    session.add(nueva)
    await session.commit()
    
    if hx_request:
        response.headers["HX-Refresh"] = "true"
        return Response(status_code=200)
    
    return RedirectResponse(url="/dashboard", status_code=303)

@router.post("/categoria/editar/{id}")
async def editar_categoria(
    id: uuid.UUID,
    nombre: str = Form(...),
    icono: str = Form("folder"),
    session: AsyncSession = Depends(get_db_session)
):
    cat = await session.get(Categoria, id)
    if cat:
        cat.nombre = nombre
        cat.icono = icono
        session.add(cat)
        await session.commit()
        
    return RedirectResponse(url="/dashboard", status_code=303)

@router.post("/categoria/eliminar/{id}")
async def eliminar_categoria(
    id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session)
):
    # OJO: Por el cascade="all, delete-orphan" en models.py, 
    # esto borrará también los cuadernos y notas dentro.
    cat = await session.get(Categoria, id)
    if cat:
        await session.delete(cat)
        await session.commit()
        
    return RedirectResponse(url="/dashboard", status_code=303)

# --- AGREGAR AL FINAL DE routers/dashboard.py ---

@router.post("/tarea/editar/{id}")
async def editar_tarea(
    id: uuid.UUID,
    request: Request,
    titulo: str = Form(...),
    fecha_objetivo: Optional[str] = Form(None),
    cuaderno_id: Optional[str] = Form(None),
    session: AsyncSession = Depends(get_db_session)
):
    tarea = await session.get(Tarea, id)
    if not tarea:
        return Response(status_code=404)
    
    # 1. Actualizar Título
    tarea.titulo = titulo
    
    # 2. Actualizar Fecha
    if fecha_objetivo:
        try:
            tarea.fecha_objetivo = datetime.strptime(fecha_objetivo, '%Y-%m-%d')
        except ValueError:
            pass # Si falla el formato, ignoramos
    else:
        # Si llega vacío, ¿queremos borrar la fecha? 
        # En el HTML original parece que sí.
        # Descomenta la siguiente línea si quieres permitir quitar la fecha:
        # tarea.fecha_objetivo = None
        pass

    # 3. Actualizar Proyecto / Cuaderno
    if cuaderno_id and cuaderno_id.strip():
        tarea.cuaderno_id = uuid.UUID(cuaderno_id)
    else:
        tarea.cuaderno_id = None
        
    session.add(tarea)
    await session.commit()
    
    # Redireccionamos a la página desde donde se hizo la petición (Dashboard o Cuaderno)
    referer = request.headers.get("referer") or "/dashboard"
    return RedirectResponse(url=referer, status_code=303)
```

---

## 📄 Archivo: `app/routers/editor.py`
```py
import uuid
import os
import mimetypes
import re
from datetime import datetime, date
from typing import Optional, List

from fastapi import APIRouter, Depends, Form, Request, Header, Response, UploadFile, File, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select, col, or_, func, desc
from sqlalchemy.orm import selectinload
from supabase import create_client, Client
from sqlalchemy.ext.asyncio import AsyncSession

# Core Modules
from auth import get_authenticated_user, User
from dependencies import get_db_session
from models import Cuaderno, Categoria, Tarea, Anotacion, Tema, Adjunto
from database import async_session_factory, init_rls

# Configuración
router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Configuración Supabase (Storage)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Optional[Client] = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def limpiar_html(contenido_html: str | None) -> str:
    if not contenido_html:
        return "Sin contenido..." # Feedback visual mejor
    
    # TipTap usa <p> para párrafos. Añadimos espacio al cerrar p para que no se peguen las palabras.
    contenido_html = contenido_html.replace('</p>', ' ').replace('<br>', ' ')
    
    # Eliminar tags
    texto_limpio = re.sub('<[^<]+?>', '', contenido_html)
    
    # Colapsar espacios múltiples (ej: &nbsp; o saltos de línea convertidos a espacios)
    texto_limpio = " ".join(texto_limpio.split())
    
    if not texto_limpio:
        return "Sin contenido..."
        
    return texto_limpio[:160] + "..." if len(texto_limpio) > 160 else texto_limpio

# ==========================================
# 1. VISTA DE CUADERNO / PROYECTO
# ==========================================

# routers/editor.py

# ... (imports existentes) ...

# ==========================================
# 1. VISTA DE CUADERNO (Modo: notebook)
# ==========================================
@router.get("/cuaderno/{cuaderno_id}", response_class=HTMLResponse)
async def ver_cuaderno(
    request: Request,
    cuaderno_id: uuid.UUID,
    user: User = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db_session)
):
    # 1. Obtener Cuaderno con Relaciones
    stmt = (
        select(Cuaderno)
        .where(Cuaderno.id == cuaderno_id)
        .options(
            selectinload(Cuaderno.temas).selectinload(Tema.anotaciones),
            selectinload(Cuaderno.tareas)
        )
    )
    result = await session.exec(stmt)
    cuaderno = result.first()
    
    if not cuaderno:
        return RedirectResponse(url="/dashboard")

    # 2. Calcular Estadísticas (si es proyecto)
    stats_proyecto = None
    if cuaderno.tipo == 'proyecto':
        total = len(cuaderno.tareas)
        completadas = len([t for t in cuaderno.tareas if t.hecho])
        progreso = int((completadas / total) * 100) if total > 0 else 0
        
        dias_restantes = None
        if cuaderno.fecha_limite:
            delta = cuaderno.fecha_limite.date() - date.today()
            dias_restantes = delta.days
            
        stats_proyecto = {
            'progreso': progreso,
            'total': total,
            'completadas': completadas,
            'dias_restantes': dias_restantes,
            'tareas': sorted(cuaderno.tareas, key=lambda x: x.hecho) 
        }

    # 3. Cargar Categorías (Necesario para el Modal de Mover Nota en el layout base)
    stmt_cat = (
        select(Categoria)
        .order_by(Categoria.orden, Categoria.nombre)
        .options(
            selectinload(Categoria.cuadernos).selectinload(Cuaderno.temas) 
        )
    )
    categorias = (await session.exec(stmt_cat)).all()

    # 4. RENDERIZAR CON MODO 'NOTEBOOK'
    # Nota: Pasamos 'nota=None' explícitamente para que base_app cargue el placeholder
    return templates.TemplateResponse("base_app.html", {
        "request": request,
        "user": user,
        "view_mode": "notebook",       # <--- EL CORONEL MANDA ESTO
        "active_cuaderno": cuaderno,
        "project_stats": stats_proyecto,
        "lista_categorias": categorias,
        "nota": None                   # <--- IMPORTANTE
    })


# ==========================================
# NUEVA RUTA: VISTA DE NOTA (Modo: notebook_note)
# ==========================================
@router.get("/cuaderno/{cuaderno_id}/nota/{anotacion_id}", response_class=HTMLResponse)
async def ver_anotacion_completa(
    request: Request,
    cuaderno_id: uuid.UUID,
    anotacion_id: uuid.UUID,
    user: User = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db_session),
    hx_request: Optional[str] = Header(None)
):
    # 1. Obtener la Nota
    stmt_nota = (
        select(Anotacion)
        .where(Anotacion.id == anotacion_id)
        .options(
            selectinload(Anotacion.tema).selectinload(Tema.cuaderno),
            selectinload(Anotacion.adjuntos)
        )
    )
    nota = (await session.exec(stmt_nota)).first()
    
    if not nota:
        return RedirectResponse(url=f"/cuaderno/{cuaderno_id}")
    
    # 2. CARGA PARCIAL (HTMX): Solo devolvemos el editor
    if hx_request:
        stmt_cat = select(Categoria).order_by(Categoria.orden).options(selectinload(Categoria.cuadernos).selectinload(Cuaderno.temas))
        lista_categorias = (await session.exec(stmt_cat)).all()
        return templates.TemplateResponse("partials/editor_pane.html", {
            "request": request, "nota": nota, "adjuntos": nota.adjuntos, "lista_categorias": lista_categorias
        })

    # 3. CARGA COMPLETA: Recuperamos la lista de notas del mismo tema
    stmt_lista = (
        select(Anotacion)
        .where(Anotacion.tema_id == nota.tema_id)
        .options(selectinload(Anotacion.adjuntos))
        .order_by(desc(Anotacion.updated_at))
    )
    notas_db = (await session.exec(stmt_lista)).all()
    
    notas_procesadas = []
    for n in notas_db:
        notas_procesadas.append({
            'id': n.id,
            'titulo': n.titulo,
            'updated_at': n.updated_at,
            'tags': n.tags,
            'preview_contenido': limpiar_html(n.contenido),
            'adjuntos': n.adjuntos
        })

    # 4. Contexto del Sidebar (Cuaderno y Stats)
    stmt_cuaderno = select(Cuaderno).where(Cuaderno.id == cuaderno_id).options(selectinload(Cuaderno.temas).selectinload(Tema.anotaciones), selectinload(Cuaderno.tareas))
    cuaderno = (await session.exec(stmt_cuaderno)).first()
    
    stats_proyecto = None
    if cuaderno and cuaderno.tipo == 'proyecto':
        total = len(cuaderno.tareas)
        completadas = len([t for t in cuaderno.tareas if t.hecho])
        progreso = int((completadas / total) * 100) if total > 0 else 0
        dias_restantes = None
        if cuaderno.fecha_limite:
            delta = cuaderno.fecha_limite.date() - date.today()
            dias_restantes = delta.days
        stats_proyecto = {'progreso': progreso, 'dias_restantes': dias_restantes, 'tareas': sorted(cuaderno.tareas, key=lambda x: x.hecho)}
    
    # 5. Categorías para modales
    stmt_cat = select(Categoria).order_by(Categoria.orden).options(selectinload(Categoria.cuadernos).selectinload(Cuaderno.temas))
    categorias = (await session.exec(stmt_cat)).all()

    # 6. Renderizar Base
    return templates.TemplateResponse("base_app.html", {
        "request": request,
        "user": user,
        "view_mode": "notebook_note",
        "active_cuaderno": cuaderno,
        "project_stats": stats_proyecto,
        "lista_categorias": categorias,
        "nota": nota,
        "adjuntos": nota.adjuntos,
        "notas": notas_procesadas,  # <--- Esto rellena la lista
        "tema": nota.tema,
        "active_note_id": nota.id
    })
# ==========================================
# 2. HTMX PARTIALS (Listas y Editor)
# ==========================================

@router.get("/partial/lista_notas/{tema_id}", response_class=HTMLResponse)
async def partial_lista_notas(
    request: Request,
    tema_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session)
):
    tema = await session.get(Tema, tema_id)
    if not tema:
        return Response("Tema no encontrado", status_code=404)

    stmt = (
        select(Anotacion)
        .where(Anotacion.tema_id == tema_id)
        .options(selectinload(Anotacion.adjuntos))
        .order_by(desc(Anotacion.updated_at))
    )
    notas_db = (await session.exec(stmt)).all()
    
    notas_procesadas = []
    for n in notas_db:
        notas_procesadas.append({
            'id': n.id,
            'titulo': n.titulo,
            'updated_at': n.updated_at,
            'tags': n.tags,
            'preview_contenido': limpiar_html(n.contenido),
            'adjuntos': n.adjuntos
        })
    
    return templates.TemplateResponse("partials/lista_notas_evernote.html", {
        "request": request,
        "tema": tema,
        "notas": notas_procesadas
    })

@router.get("/partial/editor/{anotacion_id}", response_class=HTMLResponse)
async def partial_editor(
    request: Request,
    anotacion_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session)
):
    stmt = (
        select(Anotacion)
        .where(Anotacion.id == anotacion_id)
        .options(
            selectinload(Anotacion.tema).selectinload(Tema.cuaderno),
            selectinload(Anotacion.adjuntos)
        )
    )
    result = await session.exec(stmt)
    nota = result.first()
    if not nota:
        return Response("Nota no encontrada", status_code=404)

    # Consulta para el modal de mover nota (estructura de categorías/cuadernos/temas)
    stmt_cat = (
        select(Categoria)
        .order_by(Categoria.orden, Categoria.nombre)
        .options(
            selectinload(Categoria.cuadernos).selectinload(Cuaderno.temas)
        )
    )
    lista_categorias = (await session.exec(stmt_cat)).all()

    return templates.TemplateResponse("partials/editor_pane.html", {
        "request": request,
        "nota": nota,
        "adjuntos": nota.adjuntos if nota.adjuntos else [],
        "lista_categorias": lista_categorias
    })

@router.post("/nota/crear/{tema_id}", response_class=HTMLResponse)
async def crear_nota(
    request: Request,
    tema_id: uuid.UUID,
    user: User = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db_session)
):
    """Crea una nueva nota vacía y retorna el editor"""
    tema = await session.get(Tema, tema_id)
    if not tema:
        return Response("Tema no encontrado", status_code=404)
    
    # Crear nueva nota
    nueva_nota = Anotacion(
        titulo="Sin título",
        contenido="",
        tema_id=tema.id,
        user_id=uuid.UUID(user.id)
    )
    session.add(nueva_nota)
    await session.commit()
    await init_rls(session, user.id)
    await session.refresh(nueva_nota)
    
    # Cargar nota con relaciones
    stmt = (
        select(Anotacion)
        .where(Anotacion.id == nueva_nota.id)
        .options(
            selectinload(Anotacion.tema).selectinload(Tema.cuaderno),
            selectinload(Anotacion.adjuntos)
        )
    )
    nota_cargada = (await session.exec(stmt)).first()
    
    # Cargar categorías para el modal de mover
    stmt_cat = (
        select(Categoria)
        .order_by(Categoria.orden, Categoria.nombre)
        .options(
            selectinload(Categoria.cuadernos).selectinload(Cuaderno.temas)
        )
    )
    lista_categorias = (await session.exec(stmt_cat)).all()
    
    response = templates.TemplateResponse("partials/editor_pane.html", {
        "request": request,
        "nota": nota_cargada,
        "adjuntos": nota_cargada.adjuntos if nota_cargada.adjuntos else [],
        "lista_categorias": lista_categorias
    })
    
    # Trigger para actualizar la lista de notas
    response.headers["HX-Trigger"] = "updateNoteList"
    
    return response

@router.delete("/nota/eliminar/{anotacion_id}")
async def eliminar_nota(
    anotacion_id: uuid.UUID,
    user: User = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db_session)
):
    """Elimina una nota y todos sus adjuntos asociados"""
    # Buscar la nota con sus adjuntos cargados
    stmt = (
        select(Anotacion)
        .where(Anotacion.id == anotacion_id)
        .options(selectinload(Anotacion.adjuntos))
    )
    result = await session.exec(stmt)
    nota = result.first()
    
    if not nota:
        return JSONResponse(
            status_code=404,
            content={"error": "Nota no encontrada"}
        )
    
    # Verificar que la nota pertenece al usuario
    if str(nota.user_id) != user.id:
        return JSONResponse(
            status_code=403,
            content={"error": "No tienes permiso para eliminar esta nota"}
        )
    
    # Eliminar adjuntos de Supabase Storage si existen
    if nota.adjuntos and len(nota.adjuntos) > 0:
        for adjunto in nota.adjuntos:
            # Extraer el path del archivo desde la URL
            if adjunto.url and supabase:
                try:
                    # URL formato: https://.../storage/v1/object/public/docs_assets/user_id/filename
                    parts = adjunto.url.split('/docs_assets/')
                    if len(parts) > 1:
                        file_path = parts[1]
                        supabase.storage.from_("docs_assets").remove([file_path])
                except Exception as e:
                    print(f"Error eliminando archivo de storage: {e}")
    
    # Eliminar la nota (cascade eliminará los adjuntos de la BD)
    await session.delete(nota)
    await session.commit()
    
    return JSONResponse(
        status_code=200,
        content={"success": True, "message": "Nota eliminada correctamente"}
    )

@router.get("/partial/buscar_notas", response_class=HTMLResponse)
async def buscar_notas(
    request: Request,
    q: str = "",
    session: AsyncSession = Depends(get_db_session)
):
    query = q.strip()
    if not query:
        # Retorna vacío o una lista vacía usando la plantilla correcta
        return templates.TemplateResponse("partials/lista_notas_evernote.html", {
            "request": request, "tema": None, "notas": []
        })

    stmt = (
        select(Anotacion)
        .where(
            or_(
                col(Anotacion.titulo).ilike(f'%{query}%'),
                col(Anotacion.contenido).ilike(f'%{query}%')
            )
        )
        .order_by(desc(Anotacion.updated_at))
        .limit(50)
    )
    notas_db = (await session.exec(stmt)).all()

    # Clase simple para simular el objeto tema en la vista de búsqueda
    class FakeTema:
        id = "search"
        nombre = f'Resultados: "{query}"'
        cuaderno_id = "" # Evita error en url_for

    return templates.TemplateResponse("partials/lista_notas_evernote.html", {
        "request": request,
        "tema": FakeTema(),
        "notas": notas_db # Pasamos los objetos DB directos, el template evernote maneja atributos
    })

# ==========================================
# 3. OMNIBARRA (Búsqueda Global)
# ==========================================

@router.get("/partial/omnibar_search", response_class=HTMLResponse)
async def buscar_omnibar(
    request: Request,
    q: str = "",
    session: AsyncSession = Depends(get_db_session)
):
    query = q.strip()
    
    if not query: 
        return Response("")
    
    if query.startswith('/'):
        parts = query.split(' ', 1)
        command = parts[0].lower()
        argument = parts[1] if len(parts) > 1 else ""
        
        acciones = []
        
        if command in ['/tarea', '/todo', '/t']:
            titulo = argument if argument else "Nueva Tarea..."
            acciones.append({
                'tipo': 'comando',
                'icono': 'check',
                'titulo': f'Crear Tarea: "{titulo}"',
                'subtitulo': 'Presiona Enter para crear en Agenda',
                'hx_post': '/tarea/crear',
                'payload': {'titulo': titulo}
            })
            
        elif command in ['/nota', '/n']:
            titulo = argument if argument else "Nota Rápida..."
            acciones.append({
                'tipo': 'comando',
                'icono': 'feather',
                'titulo': f'Nota Rápida: "{titulo}"',
                'subtitulo': 'Guardar en Inbox',
                'hx_post': '/quick_note',
                'payload': {'titulo': titulo}
            })
            
        elif command in ['/proyecto', '/p']:
             nombre = argument if argument else "Nuevo Proyecto..."
             acciones.append({
                'tipo': 'modal',
                'modal_name': 'createNotebook',
                'icono': 'rocket',
                'titulo': f'Nuevo Proyecto: "{nombre}"',
                'subtitulo': 'Abrir configurador de proyecto'
            })

        return templates.TemplateResponse("partials/omnibar_results.html", {
            "request": request, 
            "resultados": None, 
            "acciones": acciones
        })

    stmt = (
        select(
            Anotacion.id, 
            Anotacion.titulo, 
            Tema.nombre.label('tema_nombre'), 
            Cuaderno.nombre.label('cuaderno_nombre')
        )
        .join(Tema, Anotacion.tema_id == Tema.id)
        .join(Cuaderno, Tema.cuaderno_id == Cuaderno.id)
        .where(
            or_(
                Anotacion.titulo.ilike(f'%{query}%'),
                Anotacion.contenido.ilike(f'%{query}%')
            )
        )
        .limit(8)
    )
    
    results = await session.exec(stmt)
    resultados_procesados = results.all() 
    
    return templates.TemplateResponse("partials/omnibar_results.html", {
        "request": request, 
        "resultados": resultados_procesados, 
        "acciones": None
    })

# ==========================================
# 4. CRUD CUADERNOS
# ==========================================

@router.post("/cuaderno/crear")
async def crear_cuaderno(
    nombre: str = Form(...),
    descripcion: Optional[str] = Form(None),
    categoria_id: Optional[str] = Form(None),
    tipo: str = Form("cuaderno"),
    fecha_limite: Optional[str] = Form(None),
    user: User = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db_session)
):
    nuevo = Cuaderno(
        nombre=nombre, 
        descripcion=descripcion, 
        tipo=tipo,
        user_id=uuid.UUID(user.id)
    )
    
    if categoria_id:
        nuevo.categoria_id = uuid.UUID(categoria_id)
    else:
        stmt = select(Categoria).where(Categoria.nombre == "General")
        cat_general = (await session.exec(stmt)).first()
        if cat_general: nuevo.categoria_id = cat_general.id
    
    if fecha_limite:
        try:
            nuevo.fecha_limite = datetime.strptime(fecha_limite, '%Y-%m-%d')
        except: pass
            
    session.add(nuevo)
    await session.commit()
    return RedirectResponse(url="/dashboard", status_code=303)

@router.post("/cuaderno/editar/{id}")
async def editar_cuaderno(
    id: uuid.UUID,
    nombre: str = Form(...),
    descripcion: Optional[str] = Form(None),
    categoria_id: Optional[str] = Form(None),
    tipo: str = Form("cuaderno"),
    fecha_limite: Optional[str] = Form(None),
    clear_date: Optional[str] = Form(None),
    session: AsyncSession = Depends(get_db_session)
):
    cuaderno = await session.get(Cuaderno, id)
    if not cuaderno: return Response(status_code=404)
    
    cuaderno.nombre = nombre
    cuaderno.descripcion = descripcion
    cuaderno.tipo = tipo
    
    if categoria_id:
        cuaderno.categoria_id = uuid.UUID(categoria_id)
        
    if fecha_limite:
        try:
            cuaderno.fecha_limite = datetime.strptime(fecha_limite, '%Y-%m-%d')
        except: pass
    elif clear_date:
        cuaderno.fecha_limite = None
        
    session.add(cuaderno)
    await session.commit()
    return RedirectResponse(url="/dashboard", status_code=303)

@router.post("/cuaderno/eliminar/{id}")
async def eliminar_cuaderno(id: uuid.UUID, session: AsyncSession = Depends(get_db_session)):
    cuaderno = await session.get(Cuaderno, id)
    if cuaderno:
        await session.delete(cuaderno)
        await session.commit()
    return RedirectResponse(url="/dashboard", status_code=303)

# ==========================================
# 5. CRUD TEMAS
# ==========================================

@router.post("/tema/crear/{cuaderno_id}")
async def crear_tema(
    cuaderno_id: uuid.UUID,
    request: Request,
    nombre: str = Form(...),
    user: User = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db_session)
):
    c = await session.get(Cuaderno, cuaderno_id)
    if c:
        count_stmt = select(func.count(Tema.id)).where(Tema.cuaderno_id == cuaderno_id)
        orden = (await session.exec(count_stmt)).one() + 1
        
        nuevo = Tema(
            nombre=nombre, 
            cuaderno_id=cuaderno_id, 
            orden=orden,
            user_id=uuid.UUID(user.id)
        )
        session.add(nuevo)
        await session.commit()
        
    referer = request.headers.get("referer") or "/dashboard"
    return RedirectResponse(url=referer, status_code=303)

@router.post("/tema/editar/{id}")
async def editar_tema(
    id: uuid.UUID,
    request: Request,
    nombre: str = Form(...),
    session: AsyncSession = Depends(get_db_session)
):
    t = await session.get(Tema, id)
    if t:
        t.nombre = nombre
        session.add(t)
        await session.commit()
    
    referer = request.headers.get("referer") or "/dashboard"
    return RedirectResponse(url=referer, status_code=303)

@router.post("/tema/eliminar/{id}")
async def eliminar_tema(
    id: uuid.UUID,
    request: Request,
    session: AsyncSession = Depends(get_db_session)
):
    t = await session.get(Tema, id)
    if t:
        await session.delete(t)
        await session.commit()
        
    referer = request.headers.get("referer") or "/dashboard"
    return RedirectResponse(url=referer, status_code=303)

# ==========================================
# 6. CRUD NOTAS
# ==========================================

@router.get("/anotacion/nueva/{tema_id}")
async def nueva_anotacion(
    request: Request,
    tema_id: uuid.UUID,
    hx_request: Optional[str] = Header(None, alias="HX-Request"),
    user: User = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db_session)
):
    tema = await session.get(Tema, tema_id)
    if not tema: return Response(status_code=404)
    
    nueva = Anotacion(
        titulo="", 
        contenido="", 
        tema_id=tema.id,
        user_id=uuid.UUID(user.id)
    )
    session.add(nueva)
    
    await session.flush()
    await session.refresh(nueva)
    
    if hx_request:
        stmt = (
            select(Anotacion)
            .where(Anotacion.id == nueva.id)
            .options(
                selectinload(Anotacion.tema).selectinload(Tema.cuaderno),
                selectinload(Anotacion.adjuntos)
            )
        )
        nota_cargada = (await session.exec(stmt)).first()
        
        response = templates.TemplateResponse("partials/editor_pane.html", {"request": request, "nota": nota_cargada})
        response.headers["HX-Trigger"] = "updateNoteList"
        
        await session.commit()
        return response
        
    await session.commit()
    return RedirectResponse(url="/dashboard", status_code=303)

@router.post("/anotacion/guardar/{anotacion_id}")
async def guardar_anotacion(
    anotacion_id: uuid.UUID,
    titulo: Optional[str] = Form(None),
    contenido: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    session: AsyncSession = Depends(get_db_session)
):
    nota = await session.get(Anotacion, anotacion_id)
    if not nota:
        return Response(status_code=404)
    
    if titulo is not None:
        nota.titulo = titulo
        
    nota.contenido = contenido if contenido is not None else ""
    
    if tags:
        nota.tags = [t.strip() for t in tags.split(',') if t.strip()]
    else:
        nota.tags = []
        
    session.add(nota)
    await session.commit()
    
    resp = Response(content="", status_code=200)
    resp.headers["HX-Trigger"] = "updateNoteList"
    return resp

@router.post("/anotacion/eliminar/{id}")
async def eliminar_anotacion(
    id: uuid.UUID,
    hx_request: Optional[str] = Header(None, alias="HX-Request"),
    session: AsyncSession = Depends(get_db_session)
):
    nota = await session.get(Anotacion, id)
    if nota:
        await session.delete(nota)
        await session.commit()
        
    if hx_request:
        empty_state = '''
        <div class="flex flex-col items-center justify-center h-full text-gray-600 space-y-4 fade-in">
            <i class="fa-solid fa-trash text-4xl opacity-20"></i>
            <p class="text-sm font-medium text-gray-500">Nota eliminada</p>
        </div>
        '''
        resp = Response(content=empty_state)
        resp.headers["HX-Trigger"] = "updateNoteList"
        return resp
        
    return RedirectResponse(url="/dashboard", status_code=303)

@router.post("/anotacion/mover")
async def mover_anotacion(
    anotacion_id: uuid.UUID = Form(...),
    tema_id: uuid.UUID = Form(...),
    session: AsyncSession = Depends(get_db_session)
):
    nota = await session.get(Anotacion, anotacion_id)
    destino = await session.get(Tema, tema_id)
    if nota and destino:
        nota.tema_id = destino.id
        session.add(nota)
        await session.commit()
    resp = Response(content="", status_code=200)
    resp.headers["HX-Trigger"] = "updateNoteList"
    return resp

# --- Reemplaza la sección final de app/routers/editor.py (desde donde empiezan los adjuntos) ---

# ==========================================
# 7. ADJUNTOS Y SUBIDAS (TipTap + HTMX)
# ==========================================

# Endpoint para imágenes "Inline" (arrastradas DENTRO del editor TipTap)
# TipTap espera una respuesta JSON con la URL.
# ==========================================
# ENDPOINT PARA IMÁGENES INLINE (TipTap)
# ==========================================
@router.post("/upload/image")
async def upload_image(
    file: UploadFile = File(...),
    user: User = Depends(get_authenticated_user)
):
    # Validar que sea imagen
    if not file.content_type.startswith("image/"):
         raise HTTPException(status_code=400, detail="Solo se permiten imágenes")
    
    if not supabase:
         raise HTTPException(status_code=500, detail="Error de configuración de Storage")

    # Generar nombre único
    ext = mimetypes.guess_extension(file.content_type) or ".png"
    filename = f"inline_{uuid.uuid4().hex}{ext}"
    
    try:
        content = await file.read()
        # Subir al bucket 'docs_assets'
        supabase.storage.from_("docs_assets").upload(filename, content, {
            "content-type": file.content_type
        })
        
        # Obtener URL Pública
        public_url = supabase.storage.from_("docs_assets").get_public_url(filename)
        
        # Retornar JSON exacto {"url": "..."}
        return JSONResponse({"url": public_url})
        
    except Exception as e:
        print(f"Error subiendo imagen inline: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Helper para renderizar la lista de adjuntos (HTMX)
async def render_lista_adjuntos(request: Request, nota_id: uuid.UUID, session: AsyncSession):
    print(f"[DEBUG][render_lista_adjuntos] Buscando nota con id: {nota_id}")
    try:
        # Consultar la nota con sus adjuntos
        stmt = select(Anotacion).where(Anotacion.id == nota_id).options(selectinload(Anotacion.adjuntos))
        result = await session.exec(stmt)
        nota = result.first()
        
        if not nota:
            print(f"[DEBUG][render_lista_adjuntos] Nota no encontrada para id: {nota_id}")
            return templates.TemplateResponse("partials/lista_adjuntos.html", {
                "request": request,
                "adjuntos": []
            })
        
        print(f"[DEBUG][render_lista_adjuntos] Nota encontrada. ID: {nota.id} | Adjuntos: {len(nota.adjuntos) if nota.adjuntos else 0}")
        
        # Debug de adjuntos
        if nota.adjuntos:
            for adj in nota.adjuntos:
                print(f"[DEBUG] Adjunto: id={adj.id} | nombre={adj.nombre_original} | url={adj.url}")
        
        return templates.TemplateResponse("partials/lista_adjuntos.html", {
            "request": request,
            "adjuntos": nota.adjuntos if nota.adjuntos else []
        })
        
    except Exception as e:
        print(f"[ERROR][render_lista_adjuntos] ERROR: {e}")
        import traceback
        traceback.print_exc()
        # Retornar lista vacía en caso de error
        return templates.TemplateResponse("partials/lista_adjuntos.html", {
            "request": request,
            "adjuntos": []
        })


# Endpoint para adjuntos (Archivos listados debajo de la nota) - Versión HTMX

@router.post("/adjunto/subir/{anotacion_id}")
async def subir_adjunto(
    request: Request,
    anotacion_id: uuid.UUID,
    file: UploadFile = File(...),
    user: User = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db_session)
):
    if not file or not supabase:
        return Response(content="Error de configuración o archivo", status_code=400)
    
    nota = await session.get(Anotacion, anotacion_id)
    if not nota: 
        return Response(status_code=404)

    try:
        ext = os.path.splitext(file.filename)[1]
        filename = f"att_{uuid.uuid4().hex}{ext}"
        file_bytes = await file.read()
        
        # Subir a Supabase Storage
        supabase.storage.from_('docs_assets').upload(filename, file_bytes, {"content-type": file.content_type})
        public_url = supabase.storage.from_('docs_assets').get_public_url(filename)
        
        # Crear el adjunto
        nuevo_adjunto = Adjunto(
            url=public_url,
            nombre_original=file.filename,
            tipo_archivo=file.content_type or 'application/octet-stream',
            anotacion_id=nota.id,
            user_id=uuid.UUID(user.id)
        )
        session.add(nuevo_adjunto)
        
        # Commit para guardar en la BD
        await session.commit()
        
        # IMPORTANTE: Restaurar RLS ANTES de hacer cualquier consulta
        await init_rls(session, user.id)
        
        # Ahora refrescar la nota para obtener los adjuntos actualizados
        await session.refresh(nota)
        
        # Renderizar lista actualizada
        return await render_lista_adjuntos(request, anotacion_id, session)

    except Exception as e:
        print(f"[ERROR] Error subiendo adjunto: {e}")
        import traceback
        traceback.print_exc()
        await session.rollback()
        return Response(content=f"Error: {str(e)}", status_code=500)


@router.post("/adjunto/eliminar/{id}")
async def eliminar_adjunto(
    request: Request,
    id: uuid.UUID,
    user: User = Depends(get_authenticated_user), # <--- AGREGAR ESTA DEPENDENCIA
    session: AsyncSession = Depends(get_db_session)
):
    adj = await session.get(Adjunto, id)
    if not adj:
        return Response(status_code=404)
        
    nota_id = adj.anotacion_id 
    
    # Opcional: Borrar de Supabase también
    await session.delete(adj)
    
    # 1. Commit (Borra RLS)
    await session.commit()
    
    # 2. Restaurar RLS
    await init_rls(session, user.id)
    
    return await render_lista_adjuntos(request, nota_id, session)

@router.post("/categoria/crear")
async def crear_categoria(
    nombre: str = Form(...),
    icono: str = Form("folder"),
    user: User = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_db_session)
):
    if nombre:
        count_stmt = select(func.count(Categoria.id)).where(Categoria.user_id == uuid.UUID(user.id))
        orden_actual = (await session.exec(count_stmt)).one() or 0
        
        nueva_cat = Categoria(
            nombre=nombre, 
            icono=icono, 
            orden=orden_actual, 
            user_id=uuid.UUID(user.id)
        )
        session.add(nueva_cat)
        await session.commit()
        
    return RedirectResponse(url="/dashboard", status_code=303)

@router.get("/partial/inspector/{anotacion_id}", response_class=HTMLResponse)
async def partial_inspector(
    request: Request,
    anotacion_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session)
):
    # Lógica idéntica a partial_editor pero para el panel derecho
    stmt = (
        select(Anotacion)
        .where(Anotacion.id == anotacion_id)
        .options(selectinload(Anotacion.adjuntos), selectinload(Anotacion.tema))
    )
    nota = (await session.exec(stmt)).first()
    
    if not nota:
        return Response("", status_code=200) # Retornar vacío si no hay nota

    return templates.TemplateResponse("modules/inspector_pane.html", {
        "request": request,
        "nota": nota,
        "adjuntos": nota.adjuntos
    })

# ==========================================
# NUEVO: ENDPOINT UNIFICADO PARA NOTAS
# ==========================================
@router.get("/api/note/{nota_id}/context")
async def get_note_context(
    nota_id: uuid.UUID,
    request: Request,
    session: AsyncSession = Depends(get_db_session)
):
    """
    Devuelve TODOS los componentes necesarios para mostrar una nota.
    Una sola request para actualizar editor + inspector + metadata.
    """
    # 1. Obtener nota con relaciones
    stmt = (
        select(Anotacion)
        .where(Anotacion.id == nota_id)
        .options(
            selectinload(Anotacion.tema).selectinload(Tema.cuaderno),
            selectinload(Anotacion.adjuntos)
        )
    )
    result = await session.exec(stmt)
    nota = result.first()
    
    if not nota:
        return JSONResponse(
            {"error": "Nota no encontrada"},
            status_code=404
        )
    
    # 2. Cargar estructura para el modal de mover (si es necesario)
    stmt_cat = (
        select(Categoria)
        .order_by(Categoria.orden, Categoria.nombre)
        .options(
            selectinload(Categoria.cuadernos).selectinload(Cuaderno.temas)
        )
    )
    categorias = (await session.exec(stmt_cat)).all()
    
    # 3. Renderizar componentes
    # Editor
    editor_html = templates.TemplateResponse(
        "partials/editor_pane.html",
        {
            "request": request,
            "nota": nota,
            "adjuntos": nota.adjuntos,
            "lista_categorias": categorias
        }
    ).body.decode('utf-8')
    
    # Inspector
    inspector_html = templates.TemplateResponse(
        "modules/inspector_pane.html",
        {
            "request": request,
            "nota": nota,
            "adjuntos": nota.adjuntos
        }
    ).body.decode('utf-8')
    
    # 4. Devolver TODO
    return JSONResponse({
        "success": True,
        "editor": editor_html,
        "inspector": inspector_html,
        "metadata": {
            "cuaderno_id": str(nota.tema.cuaderno_id),
            "tema_id": str(nota.tema_id),
            "nota_id": str(nota_id),
            "titulo": nota.titulo
        }
    })
```

---

## 📄 Archivo: `app/templates/base_app.html`
```html
<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cockpit | Docs.ai</title>
    
    <!-- STACK TECNOLÓGICO -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css" rel="stylesheet">
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>

    <!-- Nuestros nuevos scripts de estado -->
    <script src="/static/js/appState.js"></script>
    <script src="/static/js/noteNavigation.js"></script>

    <script src="//unpkg.com/alpinejs" defer></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>

    <!-- CONFIGURACIÓN TAILWIND -->
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: { sans: ['Inter', 'sans-serif'], mono: ['JetBrains Mono', 'monospace'] },
                    colors: {
                        bgBase: '#0f111a', bgSidebar: '#161b22', bgList: '#1c2128', bgEditor: '#191919',
                        borderCol: '#30363d', accent: '#3b82f6', accentHover: '#60a5fa', accentPurple: '#8b5cf6'
                    }
                }
            }
        }
    </script>
    
    <style>
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #58a6ff; }
        .htmx-swapping { opacity: 0; transition: opacity 0.3s ease-out; }
        [x-cloak] { display: none !important; }
        .resizer { width: 4px; background: transparent; cursor: col-resize; transition: background 0.2s; z-index: 50; flex-shrink: 0; }
        .resizer:hover, .resizer.active { background: #3b82f6; }
    </style>
</head>

<body class="bg-bgBase text-gray-300 h-screen w-screen overflow-hidden flex text-sm antialiased"
      x-data="appShell()"
      x-init="init()"
      @keydown.window.escape="closeAll()">

    <!-- ========================================== -->
    <!-- ZONA 1: PANEL IZQUIERDO (SIDEBAR)        -->
    <!-- ========================================== -->
    <aside x-show="sidebarOpen" 
           :style="`width: ${sidebarWidth}px`"
           class="flex flex-col flex-shrink-0 relative transition-all duration-75 ease-out"
           x-transition:enter="transition ease-out duration-200"
           x-transition:enter-start="-translate-x-full opacity-0"
           x-transition:enter-end="translate-x-0 opacity-100">
        
        <!-- Lógica Estricta de Sidebar -->
        {% if view_mode == 'dashboard' %}
            {% include 'modules/sidebar_dashboard.html' %}
        {% else %}
            <!-- Aplica para 'notebook' y 'notebook_note' -->
            {% include 'modules/sidebar_notebook.html' %}
        {% endif %}

    </aside>

    <!-- RESIZER A (Izquierda <-> Centro) -->
    <div class="resizer" @mousedown="startResize($event, 'sidebar')"></div>


    <!-- ========================================== -->
    <!-- ZONA 2: PANEL CENTRAL (LISTA)            -->
    <!-- ========================================== -->
    <!-- Solo se muestra si NO es dashboard -->
    {% if view_mode != 'dashboard' %}
    <div x-show="listOpen"
         :style="`width: ${listWidth}px`"
         class="flex flex-col flex-shrink-0 relative transition-all duration-75 ease-out"
         x-transition:enter="transition ease-out duration-200"
         x-transition:enter-start="-translate-x-10 opacity-0"
         x-transition:enter-end="translate-x-0 opacity-100">
         
         {% include 'modules/list_pane.html' %}
         
    </div>

    <!-- RESIZER B (Centro <-> Derecha) -->
    <div x-show="listOpen" class="resizer" @mousedown="startResize($event, 'list')"></div>
    {% endif %}


    <!-- ========================================== -->
    <!-- ZONA 3: PANEL DERECHO (MAIN AREA)        -->
    <!-- ========================================== -->
    <main class="flex-1 flex min-w-0 relative bg-bgEditor h-full overflow-hidden">
        
        <!-- GRUPO DE BOTONES FLOTANTES IZQUIERDA -->
        <div class="absolute top-3 left-3 z-30 flex gap-2" x-transition.opacity>
            <button x-show="!sidebarOpen" @click="sidebarOpen = true" class="w-8 h-8 flex items-center justify-center bg-[#161b22] border border-borderCol rounded-md text-gray-400 hover:text-white shadow-lg transition-colors hover:border-accent">
                <i class="fa-solid fa-bars"></i>
            </button>
            <button x-show="!listOpen && viewMode !== 'dashboard'" @click="listOpen = true" class="w-8 h-8 flex items-center justify-center bg-[#161b22] border border-borderCol rounded-md text-gray-400 hover:text-white shadow-lg transition-colors hover:border-accent">
                <i class="fa-solid fa-list-ul"></i>
            </button>
        </div>

        <!-- ID CRÍTICO: Aquí es donde HTMX inyecta contenido -->
        <div id="col-editor-content" class="flex-1 flex flex-col h-full relative min-w-0">
            <!-- Wrapper del Editor -->
            <div id="editor-pane" class="h-full flex-1">
                {% if view_mode == 'dashboard' %}
                    {% include 'modules/cockpit_pane.html' %}
                {% elif view_mode == 'notebook' %}
                    {% include 'modules/placeholder_pane.html' %}
                {% elif view_mode == 'notebook_note' %}
                    {% include 'partials/editor_pane.html' %}
                {% else %}
                    {% include 'modules/placeholder_pane.html' %}
                {% endif %}
            </div>
        </div>

        <!-- RESIZER C (Editor <-> Inspector) -->
        <div x-show="inspectorOpen" 
             class="resizer" 
             @mousedown="startResize($event, 'inspector')"
             style="cursor: col-resize;"
             x-cloak>
        </div>

        <!-- INSPECTOR: ESTRUCTURA PERMANENTE -->
        <!-- Quitamos el IF de Jinja del contenedor principal. Ahora siempre existe. -->
        <aside id="inspector-pane-wrapper"
               x-show="inspectorOpen"
               :style="`width: ${inspectorWidth}px`"
               class="flex flex-col flex-shrink-0 border-l border-borderCol bg-[#151515] transition-all duration-75 ease-out relative"
               x-transition:enter="transition ease-out duration-200"
               x-transition:enter-start="translate-x-10 opacity-0"
               x-transition:enter-end="translate-x-0 opacity-100"
               x-cloak>
            
                <!-- Contenedor interno donde HTMX inyectará los datos -->
                <div id="inspector-pane-content" class="h-full w-full">
                    {% if view_mode == 'notebook_note' %}
                        {% include 'modules/inspector_pane.html' %}
                    {% endif %}
                </div>
            
        </aside>

    </main>


    <!-- ========================================== -->
    <!-- CAPA DE MODALES                          -->
    <!-- ========================================== -->
    <!-- Se incluyen todos para estar disponibles -->
    {% include 'partials/modales/global/omnibar.html' %}
    {% include 'partials/modales/global/security.html' %}
    
    {% if view_mode == 'dashboard' %}
        {% include 'partials/modales/sidebar/create_category.html' %}
        {% include 'partials/modales/sidebar/edit_category.html' %}
        {% include 'partials/modales/cockpit/create_task.html' %}
        {% include 'partials/modales/cockpit/edit_task.html' %}
        {% include 'partials/modales/cockpit/quick_note.html' %}
    {% endif %}

    {% if view_mode in ['notebook', 'notebook_note'] %}
        {% include 'partials/modales/sidebar/manage_notebook.html' %}
        {% include 'partials/modales/list/create_topic.html' %}
        {% include 'partials/modales/list/edit_topic.html' %}
    {% endif %}

    {% if view_mode == 'notebook_note' %}
        {% include 'partials/modales/editor/move_note.html' %}
    {% endif %}


    <!-- ========================================== -->
    <!-- LÓGICA ALPINE (AppShell)                 -->
    <!-- ========================================== -->
    <script>
        function appShell(mode) {
            return {
                // Estado local sincronizado con AppState
                viewMode: 'dashboard',
                sidebarOpen: true,
                listOpen: false,
                inspectorOpen: false,
                activeNoteId: null,
                
                // Inicializar y sincronizar con AppState
                init() {
                    // Suscribirse a cambios globales
                    this.unsubscribe = AppState.subscribe((state) => {
                        this.viewMode = state.viewMode || 'dashboard';
                        this.activeNoteId = state.notaId;
                        
                        // Ajustar visibilidad de paneles según modo
                        if (this.viewMode === 'dashboard') {
                            this.listOpen = false;
                            this.inspectorOpen = false;
                        } else if (this.viewMode === 'notebook_note') {
                            this.listOpen = true;
                            this.inspectorOpen = true;
                        }
                        
                        console.log('🔄 Alpine sincronizado con AppState:', state);
                    });
            
                    // Configurar tamaños desde localStorage
                    this.sidebarWidth = parseInt(localStorage.getItem('sidebarWidth')) || 260;
                    this.listWidth = parseInt(localStorage.getItem('listWidth')) || 320;
                    this.inspectorWidth = parseInt(localStorage.getItem('inspectorWidth')) || 300;
                },

                startResize(event, panel) {
                    event.preventDefault();
                    this.isResizing = true;
                    const startX = event.clientX;
                    const startWidth = this[panel + 'Width'];
                    const doDrag = (e) => {
                        let newWidth = panel === 'inspector' ? startWidth - (e.clientX - startX) : startWidth + (e.clientX - startX);
                        if (newWidth < 150) newWidth = 150; if (newWidth > 600) newWidth = 600;
                        this[panel + 'Width'] = newWidth;
                    };
                    const stopDrag = () => {
                        this.isResizing = false;
                        localStorage.setItem(panel + 'Width', this[panel + 'Width']);
                        document.removeEventListener('mousemove', doDrag);
                        document.removeEventListener('mouseup', stopDrag);
                        event.target.classList.remove('active');
                        document.body.style.cursor = '';
                    };
                    document.addEventListener('mousemove', doDrag);
                    document.addEventListener('mouseup', stopDrag);
                    event.target.classList.add('active');
                    document.body.style.cursor = 'col-resize';
                },

                // Limpiar suscripción al destruir
                destroy() {
                    if (this.unsubscribe) {
                        this.unsubscribe();
                    }
                }
            }
        }
        
        window.toggleRightSidebar = function() {
            const root = document.querySelector('[x-data]');
            if (root) { Alpine.$data(root).inspectorOpen = !Alpine.$data(root).inspectorOpen; }
        };
        
        // Función para seleccionar tema/nota en la lista
        function selectTema(el) { 
            document.querySelectorAll('.tema-item').forEach(d => { 
                d.classList.remove('bg-borderCol', 'text-white'); 
                d.classList.add('text-gray-500'); 
            }); 
            el.classList.remove('text-gray-500'); 
            el.classList.add('bg-borderCol', 'text-white'); 
        }

        // Función mejorada para seleccionar tema
        function selectTema(temaElement) { 
            document.querySelectorAll('.tema-item').forEach(item => { 
                item.classList.remove('bg-borderCol', 'text-white', 'border-accent'); 
                item.classList.add('text-gray-500', 'border-transparent'); 
            }); 
            
            temaElement.classList.remove('text-gray-500', 'border-transparent'); 
            temaElement.classList.add('bg-borderCol', 'text-white', 'border-l-4', 'border-accent'); 
            
            // Actualizar AppState si existe
            if (window.AppState) {
                const temaId = temaElement.getAttribute('data-tema-id');
                if (temaId) {
                    AppState.set({ temaId: temaId });
                }
            }
        }
        
        // Scripts globales de HTMX se mantienen igual...
    </script>
</body>
</html>
```

---

## 📄 Archivo: `app/templates/login.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iniciar Sesión - Docs.ai</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body class="bg-slate-50 min-h-screen flex items-center justify-center p-4">

    <div class="w-full max-w-md bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-100">
        <!-- Header -->
        <div class="bg-blue-600 p-8 text-center">
            <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-white/20 mb-4 text-white">
                <i class="fa-solid fa-feather-pointed text-2xl"></i>
            </div>
            <h1 class="text-2xl font-bold text-white tracking-wide">Docs.ai</h1>
            <p class="text-blue-100 text-sm mt-1">Tu segundo cerebro digital</p>
        </div>

        <div class="p-8">
            <h2 class="text-xl font-semibold text-slate-800 text-center mb-6">Bienvenido de nuevo</h2>

            <!-- Alerta de ERROR (Credenciales inválidas) -->
            {% if request.query_params.get('error') == '1' %}
            <div class="mb-6 bg-red-50 border-l-4 border-red-500 p-4 rounded-r shadow-sm animate-pulse">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <i class="fa-solid fa-circle-xmark text-red-500"></i>
                    </div>
                    <div class="ml-3">
                        <p class="text-sm text-red-700 font-medium">Credenciales incorrectas</p>
                    </div>
                </div>
            </div>
            {% endif %}

            <!-- Alerta de ÉXITO (Registro completado) -->
            {% if request.query_params.get('registered') == '1' %}
            <div class="mb-6 bg-green-50 border-l-4 border-green-500 p-4 rounded-r shadow-sm">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <i class="fa-solid fa-circle-check text-green-500"></i>
                    </div>
                    <div class="ml-3">
                        <p class="text-sm text-green-700 font-medium">¡Cuenta creada! Inicia sesión ahora.</p>
                    </div>
                </div>
            </div>
            {% endif %}

            <!-- Formulario -->
            <form action="/login" method="POST" class="space-y-5">
                
                <!-- Email -->
                <div>
                    <label for="email" class="block text-sm font-medium text-slate-700 mb-1">Correo Electrónico</label>
                    <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <i class="fa-regular fa-envelope text-slate-400"></i>
                        </div>
                        <input type="email" name="email" id="email" required placeholder="tu@email.com"
                            class="pl-10 block w-full rounded-lg border-slate-300 border bg-slate-50 p-2.5 text-sm focus:ring-blue-500 focus:border-blue-500 transition-colors shadow-sm" />
                    </div>
                </div>

                <!-- Password -->
                <div>
                    <div class="flex justify-between items-center mb-1">
                        <label for="password" class="block text-sm font-medium text-slate-700">Contraseña</label>
                        <!-- Opcional: Link a recuperar pass -->
                        <a href="#" class="text-xs text-blue-600 hover:text-blue-500">¿Olvidaste tu contraseña?</a>
                    </div>
                    <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <i class="fa-solid fa-lock text-slate-400"></i>
                        </div>
                        <input type="password" name="password" id="password" required placeholder="••••••••"
                            class="pl-10 block w-full rounded-lg border-slate-300 border bg-slate-50 p-2.5 text-sm focus:ring-blue-500 focus:border-blue-500 transition-colors shadow-sm" />
                    </div>
                </div>

                <!-- Submit Button -->
                <button type="submit" 
                    class="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-slate-800 hover:bg-slate-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-500 transition-all transform hover:-translate-y-0.5">
                    Iniciar Sesión
                </button>
            </form>
        </div>

        <!-- Footer: Enlace al Registro -->
        <div class="bg-slate-50 px-8 py-4 border-t border-slate-100 text-center">
            <p class="text-sm text-slate-600">
                ¿No tienes una cuenta? 
                <a href="/register" class="font-medium text-blue-600 hover:text-blue-500 transition-colors">
                    Regístrate gratis
                </a>
            </p>
        </div>
    </div>

</body>
</html>
```

---

## 📄 Archivo: `app/templates/modules/cockpit_pane.html`
```html
<!-- modules/cockpit_pane.html -->
<!-- Panel Dashboard (Cockpit) -->
<div class="flex-1 overflow-y-auto bg-bgBase bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-[#1f2937] via-bgBase to-bgBase h-full w-full">
    <div class="max-w-7xl mx-auto p-8">
        
        <!-- HEADER COCKPIT -->
        <div class="flex items-center justify-between mb-8">
            <div>
                <h1 class="text-2xl font-bold text-white mb-1">Cockpit <span class="text-accent">.</span></h1>
                <p class="text-gray-500 text-sm">Resumen táctico del día.</p>
            </div>
            
            <div class="flex items-center gap-6">
                <!-- Stats de Tareas -->
                <div class="text-right hidden sm:block">
                    <p class="text-2xl font-bold text-white leading-none">{{ stats.tareas_hoy }}</p>
                    <p class="text-[9px] uppercase text-gray-500 font-bold tracking-wider">Tareas Pendientes</p>
                </div>
                
                <!-- Dropdown de Usuario -->
                <div class="relative" x-data="{ open: false }">
                    <button @click="open = !open" @click.outside="open = false" class="flex items-center gap-1 bg-[#161b22] border border-borderCol hover:border-accent rounded-full p-0.5 pr-2 transition-all shadow-sm group">
                        <img src="https://ui-avatars.com/api/?name={{ user.name }}&background=3b82f6&color=fff&size=64&bold=true"
                            class="w-8 h-8 rounded-full border border-black" alt="Avatar">
                        <i class="fa-solid fa-chevron-down text-[10px] text-gray-500"></i>
                    </button>

                    <div x-show="open"
                        x-transition.opacity
                        class="absolute top-full right-0 mt-2 w-48 bg-[#161b22] border border-borderCol rounded-xl shadow-2xl py-1 z-50 overflow-hidden"
                        style="display: none;">
                        <div class="px-4 py-3 border-b border-white/5">
                            <p class="text-xs text-gray-400">Conectado como</p>
                            <p class="text-sm font-bold text-white truncate">{{ user.email }}</p>
                        </div>
                        <a href="/logout" class="block px-4 py-2 text-xs text-red-400 hover:bg-white/5 transition-colors">
                            <i class="fa-solid fa-power-off mr-2"></i> Cerrar Sesión
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <!-- GRID PRINCIPAL -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
            <!-- COLUMNA 1: AGENDA -->
            <div class="lg:col-span-1 flex flex-col h-full">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-xs font-bold text-gray-400 uppercase tracking-widest flex gap-2 items-center"><i class="fa-solid fa-list-check"></i> Agenda</h3>
                    <button @click="currentModal='createTask'" class="text-accent hover:text-white text-xs"><i class="fa-solid fa-plus"></i></button>
                </div>
                
                <div class="bg-[#161b22] border border-borderCol rounded-xl flex-1 overflow-hidden flex flex-col h-[500px]">
                    {% if agenda %}
                    <div class="overflow-y-auto p-2 space-y-1 custom-scrollbar flex-1">
                        {% for tarea in agenda %}
                        <div class="group flex items-start gap-3 p-3 hover:bg-[#21262d] rounded-lg transition-colors border border-transparent hover:border-borderCol relative" id="tarea-{{tarea.id}}">
                            <input type="checkbox" hx-post="/tarea/toggle/{{tarea.id}}" hx-target="#tarea-{{tarea.id}}" hx-swap="outerHTML" class="mt-1 w-4 h-4 rounded border-gray-600 bg-bgBase text-accent focus:ring-0 cursor-pointer task-checkbox z-10">
                            
                            <div class="flex-1 min-w-0 cursor-pointer" 
                                @click="$dispatch('open-edit-task', {
                                    id: '{{tarea.id}}', 
                                    titulo: '{{tarea.titulo}}', 
                                    fecha: '{{ tarea.fecha_objetivo.strftime('%Y-%m-%d') if tarea.fecha_objetivo else '' }}',
                                    cuadernoId: '{{ tarea.cuaderno_id or '' }}'
                                })">
                                <p class="text-sm text-gray-300 group-hover:text-white font-medium leading-tight mb-1 transition-colors">{{ tarea.titulo }}</p>
                                <div class="flex items-center gap-2 text-[10px] text-gray-500">
                                    {% if tarea.fecha_objetivo %}
                                    <span class="{{ 'text-red-400 font-bold' if tarea.fecha_objetivo.date() < today else 'text-gray-500' }}">
                                        <i class="fa-regular fa-clock"></i> {{ tarea.fecha_objetivo.strftime('%d %b') }}
                                    </span>
                                    {% endif %}
                                    {% if tarea.cuaderno %}
                                    <span class="bg-[#30363d] px-1.5 rounded text-gray-400 truncate max-w-[100px]">{{ tarea.cuaderno.nombre }}</span>
                                    {% else %}
                                    <span class="text-gray-600 opacity-0 group-hover:opacity-100 transition-opacity"><i class="fa-solid fa-arrow-turn-up text-[9px] mr-1"></i>Asignar</span>
                                    {% endif %}
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                    {% else %}
                    <div class="flex-1 flex flex-col items-center justify-center text-gray-600 p-8">
                        <i class="fa-solid fa-check-circle text-4xl mb-2 opacity-20"></i>
                        <p class="text-xs">Todo despejado</p>
                    </div>
                    {% endif %}
                    <form action="/tarea/crear" method="POST" class="p-2 border-t border-borderCol bg-[#0d1117]">
                        <input type="text" name="titulo" placeholder="+ Añadir tarea rápida..." class="w-full bg-transparent text-xs text-white placeholder-gray-600 outline-none px-2 py-1">
                    </form>
                </div>
            </div>

            <!-- COLUMNA 2 y 3: PROYECTOS Y NOTAS -->
            <div class="lg:col-span-2">
                <h3 class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4 flex gap-2 items-center"><i class="fa-solid fa-rocket"></i> Proyectos Activos</h3>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {% for p in proyectos %}
                    <div onclick="window.location.href='{{ url_for('ver_cuaderno', cuaderno_id=p.obj.id) }}'" 
                         class="group bg-[#161b22] border border-borderCol rounded-xl p-5 hover:border-accent hover:shadow-lg transition-all cursor-pointer relative overflow-hidden h-32 flex flex-col justify-between">
                        
                        <div class="absolute top-0 left-0 h-1 {{ p.color_bar }}" style="width: {{ p.porcentaje }}%"></div>

                        <div>
                            <div class="flex justify-between items-start mb-1">
                                <h4 class="font-bold text-gray-200 group-hover:text-white text-base truncate pr-2">{{ p.obj.nombre }}</h4>
                                <span class="text-[10px] font-mono whitespace-nowrap {{ 'text-red-400' if p.color_bar == 'bg-red-500' else 'text-gray-500' }}">
                                    {{ p.obj.fecha_limite.strftime('%d %b') if p.obj.fecha_limite else '' }}
                                </span>
                            </div>
                            <p class="text-xs text-gray-500 line-clamp-1">{{ p.obj.descripcion or 'Sin descripción.' }}</p>
                        </div>
                        
                        <div class="flex items-center justify-between text-[10px] text-gray-500 pt-2 border-t border-white/5">
                            <div class="flex items-center gap-1">
                                <span class="text-white font-bold">{{ p.completadas }}/{{ p.total_tareas }}</span> tareas
                            </div>
                            <div class="flex items-center gap-1">
                                {{ p.porcentaje }}%
                            </div>
                        </div>
                    </div>
                    {% else %}
                    <div class="col-span-2 border border-dashed border-borderCol rounded-xl p-8 flex flex-col items-center justify-center text-gray-600">
                        <p class="text-sm mb-2">No hay proyectos activos.</p>
                        <button @click="currentModal='createNotebook'" class="text-accent text-xs hover:underline">Crear uno ahora</button>
                    </div>
                    {% endfor %}
                </div>

                <h3 class="text-xs font-bold text-gray-400 uppercase tracking-widest mt-8 mb-4 flex gap-2 items-center"><i class="fa-solid fa-clock-rotate-left"></i> Notas Recientes</h3>
                <div class="bg-[#161b22] border border-borderCol rounded-xl overflow-hidden divide-y divide-borderCol">
                <!-- En modules/cockpit_pane.html -->
                    {% for nota in recent_notes %}
                    <!-- CORRECCIÓN AQUÍ: Target y Evento para Inspector -->
                    <div hx-get="/partial/editor/{{ nota.id }}"
                         hx-target="#editor-pane"
                         hx-swap="innerHTML"
                         hx-push-url="/cuaderno/{{ nota.tema.cuaderno.id }}/nota/{{ nota.id }}"
                         hx-on::after-request="if(event.detail.successful) { htmx.ajax('GET', '/partial/inspector/{{ nota.id }}', {target: '#inspector-content'}); inspectorOpen = true; showList = false; }"
                         class="p-3 hover:bg-[#21262d] cursor-pointer flex items-center justify-between group transition-colors">
                        <div class="flex items-center gap-3">
                            <div class="w-8 h-8 rounded bg-[#0d1117] flex items-center justify-center text-gray-500 border border-borderCol">
                                <i class="fa-regular fa-file-lines"></i>
                            </div>
                            <div>
                                <p class="text-sm font-bold text-gray-300 group-hover:text-accent">{{ nota.titulo or 'Sin título' }}</p>
                                <p class="text-[10px] text-gray-500">{{ nota.tema.cuaderno.nombre }} / {{ nota.tema.nombre }}</p>
                            </div>
                        </div>
                        <span class="text-[10px] text-gray-600 font-mono">{{ nota.updated_at.strftime('%d/%m') }}</span>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>

        <!-- FOOTER: CATEGORÍAS -->
        <div class="border-t border-white/5 pt-8 mb-20">
            <h3 class="text-xs font-bold text-gray-500 uppercase tracking-widest mb-4">Biblioteca Completa</h3>
            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
                {% for estante in estanterias %}
                <div class="bg-[#161b22] p-3 rounded-lg border border-borderCol opacity-70 hover:opacity-100 transition-opacity">
                    <p class="text-[10px] uppercase font-bold text-gray-500 mb-2 flex items-center gap-2">
                        <i class="fa-solid fa-{{ estante.icono }}"></i> {{ estante.nombre }}
                    </p>
                    <ul class="space-y-1">
                        {% for c in estante.cuadernos[:3] %}
                        <li class="text-[11px] text-gray-400 truncate pl-1 border-l-2 border-transparent hover:border-accent hover:text-white cursor-pointer"
                            onclick="window.location.href='{{ url_for('ver_cuaderno', cuaderno_id=c.id) }}'">
                            {{ c.nombre }}
                        </li>
                        {% endfor %}
                        {% if estante.cuadernos|length > 3 %}
                        <li class="text-[9px] text-gray-600 italic pl-1">+{{ estante.cuadernos|length - 3 }} más</li>
                        {% endif %}
                    </ul>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
</div>
```

---

## 📄 Archivo: `app/templates/modules/inspector_pane.html`
```html
<!-- modules/inspector_pane.html -->
<!-- Panel Derecho: Inspector (TOC, Adjuntos, Info) -->
<aside id="inspector-pane" class="h-full w-full bg-[#151515] flex flex-col overflow-hidden border-l border-[#333]">
    <div class="flex-1 overflow-y-auto custom-scrollbar">
        
        <!-- SECCIÓN 1: TOC -->
        <div class="p-5 border-b border-[#2a2a2a]">
            <h4 class="text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-4">Tabla de Contenidos</h4>
            <div id="toc-container" class="space-y-1 text-xs text-gray-400">
                <!-- Se rellena vía JS desde el editor -->
            </div>
        </div>

        <!-- SECCIÓN 2: ADJUNTOS -->
        <div class="p-5 border-b border-[#2a2a2a]">
            <div class="flex items-center justify-between mb-4">
                <h4 class="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Adjuntos</h4>
                <button onclick="document.getElementById('file-upload').click()" class="text-gray-400 hover:text-white transition">
                    <i class="fa-solid fa-plus text-xs"></i>
                </button>
            </div>
            
            <div id="lista-adjuntos-wrapper" class="mb-4">
                {% if nota %}
                    {% include "partials/lista_adjuntos.html" with context %}
                {% endif %}
            </div>

            <form id="upload-form" 
                  hx-post="/adjunto/subir/{{ nota.id if nota else '' }}" 
                  hx-encoding="multipart/form-data"
                  hx-target="#lista-adjuntos-wrapper"
                  hx-indicator="#drop-zone-spinner">
                <input type="file" name="file" id="file-upload" class="hidden" onchange="htmx.trigger('#upload-form', 'submit')">
                <div id="drop-zone" class="border border-dashed border-[#333] bg-[#1a1a1a] rounded-lg p-6 text-center transition cursor-pointer group relative overflow-hidden hover:border-emerald-500 hover:bg-[#1f1f1f]" onclick="document.getElementById('file-upload').click()">
                    <div class="group-hover:scale-105 transition duration-300">
                        <i class="fa-solid fa-cloud-arrow-up text-xl text-gray-600 mb-2 group-hover:text-emerald-500 transition"></i>
                        <p class="text-[10px] text-gray-500">Arrastra archivos aquí</p>
                    </div>
                    <div id="drop-zone-spinner" class="htmx-indicator absolute inset-0 bg-[#1a1a1a] flex flex-col items-center justify-center">
                        <i class="fa-solid fa-circle-notch fa-spin text-emerald-500 text-lg mb-2"></i>
                    </div>
                </div>
            </form>
        </div>

        <!-- SECCIÓN 3: ACCIONES Y INFO -->
        <div class="p-5">
            <h4 class="text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-4">Acciones</h4>
            <button onclick="$dispatch('open-move-note', {id: '{{ nota.id }}', titulo: '{{ nota.titulo }}'})" class="flex items-center gap-3 text-gray-400 hover:text-white transition w-full text-left py-1 group">
                <i class="fa-solid fa-folder-tree text-gray-600 group-hover:text-emerald-500 transition w-4 text-center"></i>
                <span class="text-xs">Mover nota...</span>
            </button>
            
            <h4 class="text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-4 mt-8">Info</h4>
            <div class="text-xs space-y-3">
                <div>
                    <p class="text-gray-600 mb-0.5">Editado</p>
                    <p class="font-mono text-gray-400">{{ nota.updated_at.strftime('%d/%m/%Y %H:%M') if nota else '--' }}</p>
                </div>
                <div>
                    <p class="text-gray-600 mb-0.5">Ubicación</p>
                    <p class="text-gray-400 truncate">{{ nota.tema.nombre if nota else '--' }}</p>
                </div>
            </div>
        </div>
    </div>
</aside>
```

---

## 📄 Archivo: `app/templates/modules/list_pane.html`
```html
<!-- modules/list_pane.html -->
<!-- Panel Central: Lista de Notas -->
<div class="flex flex-col h-full w-full bg-bgList border-r border-borderCol">
    
    <!-- HEADER FIJO: Buscador y Controles -->
    <div class="h-14 flex items-center px-4 border-b border-borderCol gap-3 flex-shrink-0">
        
        <!-- 1. Buscador de Notas -->
        <div class="flex-1 relative group">
            <i class="fa-solid fa-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 text-xs group-focus-within:text-accent transition-colors"></i>
            <input type="text" 
                   name="q" 
                   class="w-full bg-[#0d1117] border border-borderCol rounded-md pl-8 pr-3 py-1.5 text-xs text-white focus:border-accent focus:outline-none focus:ring-1 focus:ring-accent transition-all placeholder-gray-600"
                   placeholder="Buscar en la lista..." 
                   hx-get="/partial/buscar_notas" 
                   hx-trigger="keyup changed delay:400ms, search" 
                   hx-target="#col-notes-content" 
                   autocomplete="off">
        </div>

        <!-- 2. Botón Cerrar Lista (Colapsar hacia la izquierda) -->
        <!-- Este botón interactúa con la variable 'listOpen' definida en base_app.html -->
        <button @click="listOpen = false" class="text-gray-500 hover:text-white hover:bg-white/5 p-1.5 rounded transition-colors" title="Ocultar lista">
            <i class="fa-solid fa-angles-left text-xs"></i>
        </button>
    </div>
    
    <!-- CONTENIDO DINÁMICO (HTMX Target) -->
    <div id="col-notes-content" class="flex-1 overflow-y-auto custom-scrollbar">
        
        {% if notas %}
            <!-- CASO 1: VENIMOS DEL SERVIDOR CON DATOS (Modo Note) -->
            <!-- Incluimos directamente el partial que ya diseñaste -->
            {% include 'partials/lista_notas_evernote.html' %}
        
        {% else %}
            <!-- CASO 2: ESTADO INICIAL (Modo Notebook vacío) -->
            <div class="flex flex-col items-center justify-center h-full text-gray-600 space-y-3 p-6 text-center opacity-60">
                <div class="w-12 h-12 rounded-full bg-[#161b22] border border-borderCol flex items-center justify-center">
                    <i class="fa-regular fa-folder-open text-xl"></i>
                </div>
                <div>
                    <p class="text-xs font-medium">Lista vacía</p>
                    <p class="text-[10px]">Selecciona un tema para ver sus notas.</p>
                </div>
            </div>
        {% endif %}

    </div>
</div>
```

---

## 📄 Archivo: `app/templates/modules/placeholder_pane.html`
```html
<!-- modules/placeholder_pane.html -->
<div class="flex flex-col items-center justify-center h-full text-gray-600 space-y-4 bg-bgEditor">
    <div class="w-20 h-20 rounded-full bg-[#161b22] border border-borderCol flex items-center justify-center mb-2 shadow-xl">
        <i class="fa-solid fa-pen-nib text-3xl opacity-40 text-accent"></i>
    </div>
    <div class="text-center">
        <p class="text-sm font-bold text-gray-400">Listo para escribir</p>
        <p class="text-xs text-gray-600 mt-1">Selecciona una nota de la lista o crea un tema nuevo.</p>
    </div>
</div>
```

---

## 📄 Archivo: `app/templates/modules/sidebar_dashboard.html`
```html
<!-- modules/sidebar_dashboard.html -->
<!-- Panel Izquierdo: Dashboard (Bibliotecas y Global) -->
<aside class="flex flex-col flex-shrink-0 bg-bgSidebar border-r border-borderCol select-none z-20 w-full h-full">
    
    <!-- HEADER COMÚN (Marca y Usuario) -->
    <div class="px-6 py-6 border-b border-white/5">
        <a href="/dashboard" class="flex items-center gap-3 group">
            <div class="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white shadow-lg shadow-blue-500/20 group-hover:scale-105 transition-transform">
                <i class="fa-solid fa-bolt"></i>
            </div>
            <div>
                <h1 class="font-bold text-lg tracking-tight text-white leading-tight">Docs.ai</h1>
                <p class="text-[11px] text-slate-400 font-medium uppercase tracking-wider flex items-center gap-1.5 mt-0.5">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                    {{ user.name }}
                </p>
            </div>
        </a>
    </div>

    <!-- CONTENIDO DASHBOARD -->
    <div class="flex-1 overflow-y-auto p-3 space-y-6 custom-scrollbar">
            
        <!-- ACCIONES RÁPIDAS -->
        <div class="grid grid-cols-2 gap-2">
            <button @click="currentModal='createTask'" class="flex items-center justify-center gap-2 px-2 py-2 text-gray-300 hover:text-white bg-[#21262d] rounded-lg text-xs transition-colors border border-borderCol hover:border-gray-500">
                <i class="fa-solid fa-check"></i> Tarea
            </button>
            <button @click="currentModal='quickNote'" class="flex items-center justify-center gap-2 px-2 py-2 text-gray-300 hover:text-white bg-[#21262d] rounded-lg text-xs transition-colors border border-borderCol hover:border-gray-500">
                <i class="fa-solid fa-feather"></i> Nota
            </button>
        </div>

        <!-- SECCIÓN 1: ENFOQUE -->
        {% if sidebar_proyectos %}
        <div>
            <div class="px-2 text-[9px] font-bold text-accent uppercase tracking-widest mb-2 flex items-center gap-2">
                <i class="fa-solid fa-crosshairs"></i> Enfoque
            </div>
            <div class="space-y-0.5">
                {% for proy in sidebar_proyectos %}
                <a href="{{ url_for('ver_cuaderno', cuaderno_id=proy.id) }}" class="flex items-center justify-between px-2 py-1.5 text-gray-300 hover:text-white hover:bg-[#21262d] rounded-md transition-colors cursor-pointer group ml-1 border-l-2 border-transparent hover:border-accent">
                    <div class="flex items-center gap-2 overflow-hidden flex-1">
                        <i class="fa-solid fa-rocket text-[10px] text-accent"></i>
                        <span class="font-medium truncate text-sm">{{ proy.nombre }}</span>
                    </div>
                </a>
                {% endfor %}
            </div>
        </div>
        {% endif %}

        <!-- SECCIÓN 2: BIBLIOTECA -->
        <div>
            <div class="flex items-center justify-between px-2 mb-2 mt-4">
                <div class="text-[9px] font-bold text-gray-500 uppercase tracking-widest flex items-center gap-2 opacity-70">
                    <i class="fa-solid fa-book"></i> Biblioteca
                </div>

                <button @click="currentModal = 'createCategory'" class="p-1 rounded-md text-gray-500 hover:text-white hover:bg-white/10 transition-colors duration-200 outline-none" title="Crear nueva biblioteca">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
                        <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
                        <line x1="12" y1="11" x2="12" y2="17"></line>
                        <line x1="9" y1="14" x2="15" y2="14"></line>
                    </svg>
                </button>
            </div>

            {% for cat in lista_categorias %}
            <div x-data="{ open: false }" class="mb-1 group/cat">
                <div class="flex items-center justify-between px-2 py-1 text-gray-500 hover:text-gray-300 rounded hover:bg-white/5 transition-colors select-none">
                    <div @click="open = !open" class="flex items-center gap-2 text-[11px] font-semibold uppercase tracking-wide flex-1 cursor-pointer">
                        <i class="fa-solid fa-{{ cat.icono or 'folder' }}"></i> {{ cat.nombre }}
                    </div>
                    <div class="flex items-center gap-2">
                        <button @click.stop="$dispatch('open-edit-category', {id: '{{cat.id}}', nombre: '{{cat.nombre}}', icono: '{{cat.icono}}'})" class="opacity-0 group-hover/cat:opacity-100 text-gray-600 hover:text-accentPurple transition-all" title="Editar Biblioteca">
                            <i class="fa-solid fa-gear text-[10px]"></i>
                        </button>
                        <i @click="open = !open" class="fa-solid fa-chevron-right text-[8px] transition-transform duration-200 cursor-pointer" :class="{'rotate-90': open}"></i>
                    </div>
                </div>

                <div x-show="open" x-collapse class="pl-2 mt-1 space-y-0.5 border-l border-borderCol ml-3">
                    {% for cuaderno in cat.cuadernos %}
                    <a href="{{ url_for('ver_cuaderno', cuaderno_id=cuaderno.id) }}" class="flex items-center justify-between px-2 py-1.5 text-gray-400 hover:text-white hover:bg-[#21262d] rounded-md transition-colors cursor-pointer group/item">
                        <span class="truncate text-xs">{{ cuaderno.nombre }}</span>
                        <div class="opacity-0 group-hover/item:opacity-100 transition-opacity">
                            <button @click.prevent="$dispatch('open-edit-notebook', {id: '{{cuaderno.id}}', nombre: '{{cuaderno.nombre}}', desc: '{{cuaderno.descripcion}}', tipo: '{{cuaderno.tipo}}', fecha: '{{cuaderno.fecha_limite}}', catId: '{{cuaderno.categoria_id}}'})" class="hover:text-accent"><i class="fa-solid fa-edit text-[10px]"></i></button>
                        </div>
                    </a>
                    {% else %}
                    <p class="text-[10px] text-gray-700 italic pl-2 py-1">Vacío</p>
                    {% endfor %}
                    <button @click="currentModal = 'createNotebook'" class="flex items-center gap-2 px-3 py-2 text-gray-500 hover:text-accent text-xs w-full text-left transition-colors mt-1 ml-1">
                        <i class="fa-solid fa-plus text-[10px]"></i> <span class="text-[11px]">Nuevo Cuaderno</span>
                    </button>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    <!-- No footer specific for dashboard in original, but space reserved -->
</aside>
```

---

## 📄 Archivo: `app/templates/modules/sidebar_notebook.html`
```html
<!-- modules/sidebar_notebook.html -->
<!-- Panel Izquierdo: Proyecto Activo (Temas y Navegación Local) -->
<aside class="flex flex-col flex-shrink-0 bg-bgSidebar border-r border-borderCol select-none z-20 w-full h-full">
    
    <!-- HEADER COMÚN (Marca y Usuario) - Se mantiene por consistencia visual -->
    <div class="px-6 py-6 border-b border-white/5">
        <a href="/dashboard" class="flex items-center gap-3 group">
            <div class="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white shadow-lg shadow-blue-500/20 group-hover:scale-105 transition-transform">
                <i class="fa-solid fa-bolt"></i>
            </div>
            <div>
                <h1 class="font-bold text-lg tracking-tight text-white leading-tight">Docs.ai</h1>
                <p class="text-[11px] text-slate-400 font-medium uppercase tracking-wider flex items-center gap-1.5 mt-0.5">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                    {{ user.name }}
                </p>
            </div>
        </a>
    </div>

    <!-- CONTENIDO PROYECTO/CUADERNO -->
    <div class="flex-1 overflow-y-auto p-3 space-y-6 custom-scrollbar">
            
        <!-- Botón Volver -->
        <a href="{{ url_for('dashboard') }}" class="flex items-center gap-2 px-2 py-2 text-gray-500 hover:text-accent mb-2 transition-colors group">
            <div class="w-6 h-6 rounded bg-[#21262d] flex items-center justify-center group-hover:bg-accent group-hover:text-white transition-colors">
                <i class="fa-solid fa-arrow-left text-[10px]"></i> 
            </div>
            <span class="text-xs font-bold uppercase tracking-wider">Dashboard</span>
        </a>

        <!-- Info del Cuaderno -->
        <div class="px-2 mb-6">
            <div class="flex items-center gap-2 mb-2">
                <span class="text-[9px] px-1.5 py-0.5 rounded {{ 'bg-accent/20 text-accent border border-accent/20' if active_cuaderno.tipo=='proyecto' else 'bg-gray-700 text-gray-300 border border-gray-600' }} uppercase font-bold tracking-widest">
                    {{ active_cuaderno.tipo }}
                </span>
                {% if project_stats and project_stats.dias_restantes is not none %}
                    <span class="text-[9px] px-1.5 py-0.5 rounded {{ 'bg-red-500/20 text-red-400 border border-red-500/20' if project_stats.dias_restantes < 3 else 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/20' }} font-mono">
                        <i class="fa-regular fa-clock mr-1"></i>{{ project_stats.dias_restantes }} días
                    </span>
                {% endif %}
            </div>
            
            <h2 class="text-xl font-bold text-white leading-tight mb-1">{{ active_cuaderno.nombre }}</h2>
            <p class="text-xs text-gray-500 line-clamp-3 leading-relaxed">{{ active_cuaderno.descripcion }}</p>
        </div>

        <!-- Stats del Proyecto (Solo si es proyecto) -->
        {% if active_cuaderno.tipo == 'proyecto' and project_stats %}
        <div class="mx-2 mb-6 p-3 bg-[#0d1117] rounded-lg border border-borderCol">
            <div class="flex justify-between items-end mb-1">
                <span class="text-[10px] font-bold text-gray-400 uppercase">Progreso</span>
                <span class="text-[10px] font-mono text-accent">{{ project_stats.progreso }}%</span>
            </div>
            <div class="h-1.5 w-full bg-[#21262d] rounded-full overflow-hidden mb-4">
                <div class="h-full bg-accent transition-all duration-500" style="width: {{ project_stats.progreso }}%"></div>
            </div>

            <div class="space-y-1.5 mb-2">
                {% for tarea in project_stats.tareas %}
                <div class="flex items-start gap-2 group/task" id="p-task-{{tarea.id}}">
                    <input type="checkbox" 
                           {{ 'checked' if tarea.hecho else '' }}
                           hx-post="/tarea/toggle/{{tarea.id}}" 
                           hx-target="#p-task-{{tarea.id}}" 
                           hx-swap="outerHTML" 
                           class="mt-0.5 w-3 h-3 rounded border-gray-600 bg-bgBase text-accent focus:ring-0 cursor-pointer task-checkbox opacity-70 hover:opacity-100">
                    <span class="text-[11px] leading-tight {{ 'line-through text-gray-600' if tarea.hecho else 'text-gray-300' }}">{{ tarea.titulo }}</span>
                </div>
                {% else %}
                <p class="text-[10px] text-gray-600 italic">No hay tareas definidas.</p>
                {% endfor %}
            </div>

            <button @click="currentModal='createTask'" class="w-full mt-2 py-1 text-[10px] text-gray-500 hover:text-white border border-dashed border-gray-700 hover:border-gray-500 rounded transition-colors">
                + Añadir Tarea
            </button>
        </div>
        {% endif %}

        <!-- Lista de Temas -->
        <div class="px-2 mb-1 text-[9px] font-bold text-gray-500 uppercase tracking-widest opacity-70">
            <i class="fa-solid fa-layer-group mr-1"></i> Temas & Notas
        </div>
        
        <div class="space-y-0.5">
            {% for tema in active_cuaderno.temas %}
            <!-- La clase safe-action evita que salte la alerta de 'cambios sin guardar' al cambiar de tema, si así se configura -->
            <div hx-get="{{ url_for('partial_lista_notas', tema_id=tema.id) }}"
                 hx-target="#col-notes-content"
                 hx-swap="innerHTML"
                 @click="selectTema($el); if(typeof toggleList !== 'undefined' && !listOpen) toggleList();"
                 class="tema-item flex items-center justify-between px-3 py-2 text-gray-400 hover:text-white hover:bg-[#21262d] rounded-md cursor-pointer transition-colors text-xs border-l-2 border-transparent hover:border-accent">
                <span class="truncate font-medium">{{ tema.nombre }}</span>
                <span class="text-[9px] bg-[#0d1117] px-1.5 rounded text-gray-500 border border-borderCol">{{ tema.anotaciones|length }}</span>
            </div>
            {% endfor %}
        </div>

        <button @click="$dispatch('open-create-topic', {id: '{{active_cuaderno.id}}'})" class="flex items-center gap-2 px-3 py-2 text-gray-500 hover:text-accent text-xs w-full text-left transition-colors mt-1 ml-1">
            <i class="fa-solid fa-plus text-[10px]"></i> <span class="text-[11px]">Nuevo tema</span>
        </button>
    </div>

    <!-- Footer Sidebar: Eliminar Cuaderno -->
    <div class="p-3 border-t border-borderCol flex gap-2">
        <button onclick="openDeleteModal('{{ url_for('eliminar_cuaderno', id=active_cuaderno.id) }}', 'body', 'Eliminar Cuaderno', 'Se perderán todos los temas.')" class="w-full flex items-center justify-center gap-2 bg-red-900/10 hover:bg-red-500 text-red-400 hover:text-white py-1.5 rounded border border-red-900/20 transition-all text-xs">
            <i class="fa-solid fa-trash"></i> Eliminar
        </button>
    </div>
</aside>
```

---

## 📄 Archivo: `app/templates/partials/editor_pane.html`
```html
<!-- app/templates/partials/editor_pane.html -->

<!-- PORTAL PARA POPOVERS (escapan de overflow-hidden) -->
<div id="popover-portal" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 9999;"></div>

<!-- 1. SCRIPT DE ANCLAJE - Ajusta el contenedor para el editor -->
<script>
    (function() {
        const parent = document.getElementById('editor-pane');
        if (parent) {
            // IMPORTANTE: No usar w-full, usar flex-1 para permitir expansión
            parent.className = 'relative h-full flex-1 bg-[#191919] overflow-hidden';
            parent.style.padding = '0';
        }
    })();
</script>

<style>
    /* Estilos TipTap Originales */
    .ProseMirror {
        outline: none !important;
        min-height: 100%;
        color: #d1d5db;
        font-family: 'Inter', sans-serif;
        line-height: 1.75;
        padding-bottom: 40vh;
    }
    
    .ProseMirror p.is-editor-empty:first-child::before {
        content: attr(data-placeholder);
        color: #525252;
        pointer-events: none;
        float: left;
        height: 0;
    }

    /* Tipografía */
    .ProseMirror h1 { font-size: 2.25em; font-weight: 800; color: #fff; margin-top: 1.2em; margin-bottom: 0.6em; line-height: 1.2; }
    .ProseMirror h2 { font-size: 1.75em; font-weight: 700; color: #f3f4f6; margin-top: 1.5em; margin-bottom: 0.5em; border-bottom: 1px solid #333; padding-bottom: 0.3em; }
    .ProseMirror ul { list-style-type: disc; padding-left: 1.5em; margin-bottom: 1em; }
    .ProseMirror ol { list-style-type: decimal; padding-left: 1.5em; margin-bottom: 1em; }
    .ProseMirror blockquote { border-left: 4px solid #10b981; padding-left: 1rem; color: #9ca3af; font-style: italic; margin: 1em 0; }
    .ProseMirror pre { background: #0d0d0d; border-radius: 0.5rem; color: #fff; padding: 0.75rem 1rem; border: 1px solid #333; overflow-x: auto; margin: 1em 0; }
    
    /* Imágenes */
    .ProseMirror img {
        transition: all 0.2s ease;
        border: 2px solid transparent;
        display: block;
    }
    .ProseMirror img.ProseMirror-selectednode {
        border-color: #10b981;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.2);
    }

    /* Scrollbar */
    .custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
    .custom-scrollbar::-webkit-scrollbar-track { background: #191919; }
    .custom-scrollbar::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
    .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #444; }

    /* Tablas */
    .ProseMirror table {
        border-collapse: collapse;
        table-layout: fixed;
        width: 100%;
        margin: 0;
        overflow: hidden;
    }
    .ProseMirror table td,
    .ProseMirror table th {
        min-width: 1em;
        border: 2px solid #333;
        padding: 3px 5px;
        vertical-align: top;
        box-sizing: border-box;
        position: relative;
    }
    .ProseMirror table th {
        font-weight: bold;
        text-align: left;
        background-color: #262626;
    }

    /* ESTILOS DE IMPRESIÓN ORIGINALES (Restaurados) */
    @media print {
        @page { margin: 1.5cm 1cm; size: auto portrait; }
        header, aside, #col-notes, #right-sidebar, #editor-toolbar, #image-bubble-menu { display: none !important; }
        html, body { background-color: white !important; color: black !important; margin: 0 !important; padding: 0 !important; overflow: visible !important; height: auto !important; }
        /* DEBUG: Removed problematic override that was collapsing flex layout */
        #editor-scroll-area { position: static !important; overflow: visible !important; height: auto !important; width: 100% !important; background-color: white !important; padding: 0 !important; margin: 0 !important; }
        #note-title { color: black !important; border: none !important; border-bottom: 2px solid black !important; font-size: 24pt !important; width: 100% !important; }
        .ProseMirror { color: black !important; background: white !important; min-height: auto !important; padding-bottom: 0 !important; margin-bottom: 0 !important; }
        .ProseMirror pre { background: #f3f4f6 !important; color: black !important; border: 1px solid #ccc !important; }
        .ProseMirror table td, .ProseMirror table th { border: 1px solid black !important; color: black !important; }
    }
</style>

<!-- ESTRUCTURA PRINCIPAL -->
<!-- ✅ PRINCIPIO DEL CORONEL: 
     No usar 'absolute inset-0' porque rompe el flexbox del layout padre.
     Este módulo debe fluir naturalmente dentro de #editor-pane.
-->
<div class="flex flex-col h-full w-full bg-[#191919] text-gray-300 overflow-hidden">

    <!-- HEADER -->
    <header class="h-14 shrink-0 flex items-center justify-between px-6 bg-[#191919] border-b border-[#333] z-20 relative">
        <div class="flex items-center gap-2 text-xs text-gray-500 font-mono overflow-hidden whitespace-nowrap">
            <span class="hover:text-gray-300 cursor-pointer transition flex items-center gap-1">
                <i class="fa-solid fa-book"></i> {{ nota.tema.cuaderno.nombre }}
            </span>
            <i class="fa-solid fa-chevron-right text-[10px] opacity-50"></i>
            <span class="hover:text-gray-300 cursor-pointer transition truncate">
                {{ nota.tema.nombre }}
            </span>
        </div>

        <div class="flex items-center gap-3 shrink-0">
            <!-- STATUS DE GUARDADO (Corregido para que funcione) -->
            <span id="save-status" class="text-xs text-gray-500 italic transition-opacity duration-500 opacity-0 hidden md:block">Guardado</span>
            
            <button 
                id="btn-guardar"
                class="bg-blue-600 hover:bg-blue-500 text-white px-4 py-1.5 rounded text-xs font-semibold shadow-lg shadow-blue-900/20 transition flex items-center gap-2"
                hx-post="/anotacion/guardar/{{ nota.id }}"
                hx-trigger="click, saveContent" 
                hx-include="#note-title, #contenido-hidden"
                hx-swap="none"
                onclick="showSaving()" 
            >
                <i class="fa-solid fa-floppy-disk"></i> <span class="hidden sm:inline">Guardar</span>
            </button>
            <button onclick="window.print()" class="text-gray-400 hover:text-white hover:bg-[#333] transition w-8 h-8 flex items-center justify-center rounded" title="Imprimir / PDF">
                <i class="fa-solid fa-print"></i>
            </button>
            <!-- ✅ PRINCIPIO DEL CORONEL: 
                 Botón toggle del inspector movido a base_app.html
                 El módulo editor NO debe controlar al módulo inspector
            -->
        </div>
    </header>

    <!-- EDITOR WORKSPACE -->
    <!-- ✅ PRINCIPIO DEL CORONEL:
         No crear contenedor flex horizontal aquí porque el Coronel (base_app.html)
         ya maneja el layout horizontal (editor + inspector).
         Este módulo solo renderiza el editor (flex-col vertical).
    -->
    <main class="flex-1 flex flex-col min-w-0 bg-[#191919] h-full relative overflow-hidden">
        
        <!-- TOOLBAR MEJORADO CON POPOVERS -->
        <div id="editor-toolbar" class="h-14 shrink-0 border-b border-[#333] flex items-center px-4 gap-3 bg-[#191919] z-10">
                
                <!-- HEADINGS DROPDOWN -->
                <div class="relative">
                    <button id="btn-headings" class="toolbar-btn-main flex items-center gap-1">
                        <span id="heading-display">H</span>
                        <i class="fa-solid fa-chevron-down text-[8px]"></i>
                    </button>
                </div>

                <div class="w-px h-5 bg-[#333]"></div>

                <!-- BOLD, ITALIC -->
                <button type="button" id="btn-bold" class="toolbar-btn" title="Bold"><i class="fa-solid fa-bold text-xs"></i></button>
                <button type="button" id="btn-italic" class="toolbar-btn" title="Italic"><i class="fa-solid fa-italic text-xs"></i></button>

                <!-- FONT FAMILY -->
                <div class="relative">
                    <button id="btn-font-family" class="toolbar-btn-main text-xs">
                        <span id="font-display">Inter</span>
                        <i class="fa-solid fa-chevron-down text-[8px]"></i>
                    </button>
                </div>

                <!-- FONT SIZE -->
                <div class="relative">
                    <button id="btn-font-size" class="toolbar-btn-main text-xs">
                        <span id="size-display">12</span>
                        <i class="fa-solid fa-chevron-down text-[8px]"></i>
                    </button>
                </div>

                <div class="w-px h-5 bg-[#333]"></div>

                <!-- LISTS DROPDOWN -->
                <div class="relative">
                    <button id="btn-lists" class="toolbar-btn-main">
                        <i id="list-icon" class="fa-solid fa-list-ul text-xs"></i>
                        <i class="fa-solid fa-chevron-down text-[8px]"></i>
                    </button>
                </div>

                <!-- ALIGNMENT DROPDOWN -->
                <div class="relative">
                    <button id="btn-align" class="toolbar-btn-main">
                        <i id="align-icon" class="fa-solid fa-align-left text-xs"></i>
                        <i class="fa-solid fa-chevron-down text-[8px]"></i>
                    </button>
                </div>

                <div class="w-px h-5 bg-[#333]"></div>

                <!-- CODE BLOCK -->
                <button type="button" id="btn-codeblock" class="toolbar-btn" title="Bloque de código"><i class="fa-solid fa-code text-xs"></i></button>

                <!-- QUOTE -->
                <button type="button" id="btn-blockquote" class="toolbar-btn" title="Cita"><i class="fa-solid fa-quote-right text-xs"></i></button>

                <!-- COLORS DROPDOWN -->
                <div class="relative">
                    <button id="btn-colors" class="toolbar-btn-main">
                        <i class="fa-solid fa-palette text-xs"></i>
                        <i class="fa-solid fa-chevron-down text-[8px]"></i>
                    </button>
                </div>

                <!-- CODE INLINE -->
                <button type="button" id="btn-code-inline" class="toolbar-btn" title="Código"><i class="fa-solid fa-brackets-curly text-xs"></i></button>

                <div class="w-px h-5 bg-[#333]"></div>

                <!-- UNDO/REDO -->
                <button type="button" id="btn-undo" class="toolbar-btn" title="Deshacer"><i class="fa-solid fa-rotate-left text-xs"></i></button>
                <button type="button" id="btn-redo" class="toolbar-btn" title="Rehacer"><i class="fa-solid fa-rotate-right text-xs"></i></button>
            </div>

            <!-- ESTILOS TOOLBAR MEJORADO -->
            <style>
                /* Botones principales con y sin dropdown */
                .toolbar-btn, .toolbar-btn-main {
                    height: 2rem;
                    padding: 0 0.5rem;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 0.25rem;
                    border-radius: 0.375rem;
                    color: #9ca3af;
                    background: transparent;
                    border: 1px solid transparent;
                    outline: none;
                    transition: all 0.2s ease;
                    font-size: 0.875rem;
                    font-weight: 500;
                    cursor: pointer;
                    white-space: nowrap;
                }

                .toolbar-btn:hover, .toolbar-btn-main:hover {
                    background: #2a2a2a;
                    color: #e5e7eb;
                    border-color: #444;
                }

                .toolbar-btn.active, .toolbar-btn-main.active {
                    background: #2563eb;
                    color: #fff;
                    border-color: #3b82f6;
                }

                /* Popovers con Popover API - En Portal para escapar overflow-hidden */
                [popover] {
                    background: #1a1a1a;
                    border: 1px solid #333;
                    border-radius: 0.5rem;
                    padding: 0.5rem;
                    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8);
                    inset: auto !important;
                    z-index: 10000 !important;
                    position: fixed !important;
                    top: auto !important;
                    left: auto !important;
                    right: auto !important;
                    bottom: auto !important;
                    margin: 0 !important;
                    pointer-events: auto;
                }

                [popover]::backdrop {
                    display: none;
                }

                /* Items dentro del popover */
                .popover-item, .popover-item-font, .popover-item-size {
                    display: flex;
                    align-items: center;
                    gap: 0.75rem;
                    width: 100%;
                    padding: 0.5rem 0.75rem;
                    border: none;
                    background: transparent;
                    color: #d1d5db;
                    border-radius: 0.375rem;
                    cursor: pointer;
                    transition: all 0.15s ease;
                    font-size: 0.875rem;
                    text-align: left;
                }

                .popover-item:hover, .popover-item-font:hover, .popover-item-size:hover {
                    background: #2a2a2a;
                    color: #fff;
                }

                .popover-item.active, .popover-item-font.active, .popover-item-size.active {
                    background: #2563eb;
                    color: #fff;
                }

                .popover-item span:last-child {
                    flex: 1;
                }

                .popover-item-font, .popover-item-size {
                    justify-content: space-between;
                }

                /* Para items que muestran opción activa con checkmark */
                .popover-item::after {
                    content: '';
                    width: 0.25rem;
                    height: 0.25rem;
                    border-radius: 50%;
                    background: currentColor;
                    opacity: 0;
                    transition: opacity 0.15s ease;
                    margin-left: auto;
                }

                .popover-item.active::after {
                    opacity: 1;
                }
            </style>

            <!-- SCROLL AREA -->
            <div class="flex-1 overflow-y-auto custom-scrollbar relative h-full bg-[#191919]" id="editor-scroll-area">
                <div class="max-w-4xl mx-auto px-8 pt-8 md:px-12 min-h-full bg-[#191919]">
                    
                    <!-- ETIQUETAS ELIMINADAS PARA EVITAR ERROR SERVER -->

                    <input type="text" 
                       id="note-title"
                       name="titulo" 
                       value="{{ nota.titulo }}" 
                       class="w-full bg-transparent text-4xl font-extrabold text-white placeholder-gray-700 border-none focus:ring-0 p-0 mb-6 leading-tight"
                       placeholder="Título de la nota"
                       hx-post="/anotacion/guardar/{{ nota.id }}" 
                       hx-trigger="keyup changed delay:1s" 
                       hx-include="#contenido-hidden"
                       autocomplete="off">
                    
                    <div id="tiptap-editor"></div>
                    <input type="hidden" name="contenido" id="contenido-hidden" value="">
                    <script id="contenido-json" type="application/json">{{ nota.contenido | tojson }}</script>
                </div>
            </div>
        </main>
        
</div>

<!-- ✅ PRINCIPIO DEL CORONEL:
     El inspector NO se renderiza en este partial.
     Es responsabilidad de base_app.html (el Coronel) decidir
     si mostrar el inspector y dónde colocarlo.
     Este módulo (editor) solo se preocupa del contenido del editor.
-->

<!-- Modal Mover (Original) -->
<dialog id="modal-mover" class="bg-[#191919] border border-[#333] text-gray-300 rounded-lg shadow-2xl backdrop:bg-black/60 p-0 w-full max-w-sm m-auto">
    <form method="post" hx-post="/anotacion/mover" hx-target="body" hx-swap="none" hx-on="htmx:afterOnLoad: closeMoveModal()">
        <div class="p-4 border-b border-[#333] flex justify-between items-center">
            <h3 class="font-bold text-sm text-gray-200">Mover nota</h3>
            <button type="button" class="text-gray-500 hover:text-white" onclick="document.getElementById('modal-mover').close()"><i class="fa-solid fa-xmark"></i></button>
        </div>
        <div class="p-4">
            <p class="text-xs text-gray-500 mb-3">Elige el nuevo destino:</p>
            <input type="hidden" name="anotacion_id" value="{{ nota.id }}">
            <select name="tema_id" class="w-full bg-[#111] border border-[#333] text-gray-300 text-xs rounded p-2.5 focus:border-emerald-500 focus:outline-none mb-4" required>
                <option value="" disabled selected>Selecciona un tema...</option>
                {% if lista_categorias %}
                    {% for cat in lista_categorias %}
                        <optgroup label="{{ cat.nombre }}">
                            {% for cuad in cat.cuadernos %}
                                {% for tema in cuad.temas %}
                                    <option value="{{ tema.id }}" {% if tema.id == nota.tema_id %}disabled{% endif %}>
                                        {{ cuad.nombre }} / {{ tema.nombre }}
                                    </option>
                                {% endfor %}
                            {% endfor %}
                        </optgroup>
                    {% endfor %}
                {% endif %}
            </select>
            <div class="flex justify-end gap-2">
                <button type="button" onclick="document.getElementById('modal-mover').close()" class="px-3 py-1.5 text-xs text-gray-400 hover:text-white">Cancelar</button>
                <button type="submit" class="px-3 py-1.5 text-xs bg-emerald-600 hover:bg-emerald-500 text-white rounded">Mover</button>
            </div>
        </div>
    </form>
</dialog>

<!-- MENÚ FLOTANTE -->
<div id="image-bubble-menu" class="flex items-center gap-1 bg-[#222] border border-[#444] rounded-lg shadow-xl p-1.5 z-50 transition-opacity duration-200" style="visibility: hidden;">
    <button id="img-align-left" class="p-1.5 text-gray-400 hover:text-white hover:bg-[#333] rounded" title="Alinear Izquierda"><i class="fa-solid fa-align-left text-xs"></i></button>
    <button id="img-align-center" class="p-1.5 text-gray-400 hover:text-white hover:bg-[#333] rounded" title="Centrar"><i class="fa-solid fa-align-center text-xs"></i></button>
    <button id="img-align-right" class="p-1.5 text-gray-400 hover:text-white hover:bg-[#333] rounded" title="Alinear Derecha"><i class="fa-solid fa-align-right text-xs"></i></button>
    <div class="w-px h-4 bg-[#444] mx-1"></div>
    <button id="img-size-small" class="p-1.5 text-gray-400 hover:text-white hover:bg-[#333] rounded font-mono text-[10px]" title="Pequeña">S</button>
    <button id="img-size-medium" class="p-1.5 text-gray-400 hover:text-white hover:bg-[#333] rounded font-mono text-[10px]" title="Mediana">M</button>
    <button id="img-size-large" class="p-1.5 text-gray-400 hover:text-white hover:bg-[#333] rounded font-mono text-[10px]" title="Grande">L</button>
</div>

<!-- SCRIPTS (Mantenidos modularizados para que funcionen las librerías, pero con lógica original) -->
<script>
    // Importar módulos ES6 de forma asíncrona
    (async () => {
        const { Editor } = await import('https://esm.sh/@tiptap/core@2.4.0');
        const StarterKit = (await import('https://esm.sh/@tiptap/starter-kit@2.4.0')).default;
        const Placeholder = (await import('https://esm.sh/@tiptap/extension-placeholder@2.4.0')).default;
        const TaskList = (await import('https://esm.sh/@tiptap/extension-task-list@2.4.0')).default;
        const TaskItem = (await import('https://esm.sh/@tiptap/extension-task-item@2.4.0')).default;
        const Underline = (await import('https://esm.sh/@tiptap/extension-underline@2.4.0')).default;
        const CodeBlockLowlight = (await import('https://esm.sh/@tiptap/extension-code-block-lowlight@2.4.0')).default;
        const Image = (await import('https://esm.sh/@tiptap/extension-image@2.4.0')).default;
        const BubbleMenu = (await import('https://esm.sh/@tiptap/extension-bubble-menu@2.4.0')).default;
        const Table = (await import('https://esm.sh/@tiptap/extension-table@2.4.0')).default;
        const TableCell = (await import('https://esm.sh/@tiptap/extension-table-cell@2.4.0')).default;
        const TableHeader = (await import('https://esm.sh/@tiptap/extension-table-header@2.4.0')).default;
        const TableRow = (await import('https://esm.sh/@tiptap/extension-table-row@2.4.0')).default;
        const TextAlign = (await import('https://esm.sh/@tiptap/extension-text-align@2.4.0')).default;
        const Color = (await import('https://esm.sh/@tiptap/extension-color@2.4.0')).default;
        const Highlight = (await import('https://esm.sh/@tiptap/extension-highlight@2.4.0')).default;
        const Code = (await import('https://esm.sh/@tiptap/extension-code@2.4.0')).default;
        const TextStyle = (await import('https://esm.sh/@tiptap/extension-text-style@2.4.0')).default;
        const FontFamily = (await import('https://esm.sh/@tiptap/extension-font-family@2.4.0')).default;
        
        // FontSize como Mark verdadero
        const FontSize = TextStyle.extend({
            name: 'fontSize',
            addOptions() {
                return { types: ['textStyle'] };
            },
            addAttributes() {
                return {
                    fontSize: {
                        default: null,
                        parseHTML: element => element.style.fontSize || null,
                        renderHTML: attributes => {
                            if (!attributes.fontSize) return {};
                            return { 
                                style: `font-size: ${attributes.fontSize}` 
                            };
                        },
                    },
                };
            },
            addCommands() {
                return {
                    setFontSize: (size) => ({ commands }) => {
                        return commands.setMark('fontSize', { fontSize: size });
                    },
                    unsetFontSize: () => ({ commands }) => {
                        return commands.unsetMark('fontSize');
                    },
                };
            },
        });
        
        const { common, createLowlight } = await import('https://esm.sh/lowlight@3.1.0');
        
        const lowlight = createLowlight(common);

    if (window.editor) window.editor.destroy();
    const content = JSON.parse(document.getElementById('contenido-json').textContent);
    let saveTimeout;

    // Extensión Imagen
    const CustomImage = Image.extend({
        addAttributes() {
            return {
                ...this.parent?.(),
                width: { default: 'auto', renderHTML: attrs => ({ style: `width: ${attrs.width} !important; max-width: 100%; height: auto;` }), parseHTML: el => el.style.width },
                class: { default: 'block mx-auto', renderHTML: attrs => ({ class: attrs.class }), parseHTML: el => el.getAttribute('class') }
            }
        }
    });

    // Subida Imagen (Con CSRF Fix)
    const uploadImage = async (file) => {
        const formData = new FormData();
        formData.append('file', file);
        try {
            const response = await fetch('/upload/image', { 
                method: 'POST', 
                body: formData,
                headers: { 'X-CSRFToken': '{{ csrf_token }}' }
            });
            if (!response.ok) throw new Error('Error en subida');
            const data = await response.json();
            return data.url;
        } catch (error) {
            console.error("Error:", error);
            return null;
        }
    };

    // TOC
    function updateTOC(editor) {
        const tocContainer = document.getElementById('toc-container');
        if (!tocContainer) return;
        
        const items = [];
        editor.state.doc.descendants((node, pos) => {
            if (node.type.name === 'heading') items.push({ level: node.attrs.level, text: node.textContent, pos: pos });
        });

        tocContainer.innerHTML = '';
        if (items.length === 0) {
            tocContainer.innerHTML = '<p class="pl-2 italic opacity-30 text-[10px]">Sin títulos...</p>';
        } else {
            items.forEach((item) => {
                const div = document.createElement('div');
                const paddingLeft = item.level === 1 ? 'pl-0' : (item.level === 2 ? 'pl-3' : 'pl-6');
                div.className = `cursor-pointer hover:text-white hover:bg-[#2a2a2a] py-1 rounded truncate transition text-[11px] ${paddingLeft} text-gray-400`;
                div.innerText = item.text || '(Sin texto)';
                div.onclick = (e) => {
                    e.preventDefault();
                    editor.chain().focus().setTextSelection(item.pos + 1).run();
                    const domEl = editor.view.nodeDOM(item.pos);
                    if(domEl) {
                        // Usa scrollIntoView con block: 'start' pero con un pequeño delay para asegurar el render
                        setTimeout(() => {
                            domEl.scrollIntoView({behavior: 'smooth', block: 'start'});
                        }, 0);
                    }
                };
                tocContainer.appendChild(div);
            });
        }
    }

    // Botones de imagen
    function setupImageControls(editor) {
        const setAttr = (attrs) => editor.chain().focus().updateAttributes('image', attrs).run();
        const bindBtn = (id, callback) => { const btn = document.getElementById(id); if(btn) btn.onclick = callback; };
        bindBtn('img-align-left', () => setAttr({ class: 'float-left mr-6 mb-2' }));
        bindBtn('img-align-center', () => setAttr({ class: 'block mx-auto' }));
        bindBtn('img-align-right', () => setAttr({ class: 'float-right ml-6 mb-2' }));
        bindBtn('img-size-small', () => setAttr({ width: '25%' }));
        bindBtn('img-size-medium', () => setAttr({ width: '50%' }));
        bindBtn('img-size-large', () => setAttr({ width: '100%' }));
    }

    // Inicializar Editor
    window.editor = new Editor({
        element: document.querySelector('#tiptap-editor'),
        extensions: [
            StarterKit.configure({ codeBlock: false }),
            Placeholder.configure({ placeholder: 'Escribe algo increíble...' }),
            TaskList, TaskItem.configure({ nested: true }),
            Underline, CodeBlockLowlight.configure({ lowlight }),
            CustomImage.configure({ inline: false, allowBase64: false }),
            BubbleMenu.configure({
                element: document.querySelector('#image-bubble-menu'),
                tippyOptions: { duration: 100, placement: 'top', interactive: true, zIndex: 99 },
                shouldShow: ({ editor }) => editor.isActive('image'),
            }),
            Table.configure({ resizable: true }), TableRow, TableHeader, TableCell,
            TextAlign.configure({ types: ['heading', 'paragraph'] }),
            Color,
            Highlight,
            Code,
            TextStyle,
            FontSize,
            FontFamily.configure({
                types: ['textStyle'],
            }),
        ],
        content: content,
        editorProps: {
            attributes: {
                class: 'focus:outline-none w-full min-w-full max-w-none prose-invert prose-img:rounded-lg prose-img:shadow-xl prose-table:border-collapse prose-td:border prose-td:border-gray-700 prose-td:p-2 prose-th:border prose-th:border-gray-700 prose-th:p-2 prose-th:bg-gray-800'
            },
            handlePaste: (view, event) => {
                // Prioridad 1: Imágenes
                const imageItems = Array.from(event.clipboardData.items || []).filter(item => item.type.indexOf('image') === 0);
                if (imageItems.length > 0) {
                    event.preventDefault();
                    imageItems.forEach(item => {
                        const file = item.getAsFile();
                        if (file) uploadImage(file).then(url => {
                            if (url) view.dispatch(view.state.tr.replaceSelectionWith(view.state.schema.nodes.image.create({ src: url })));
                        });
                    });
                    return true;
                }

                // Prioridad 2: HTML (Excel/Calc copia como HTML con tabla)
                const htmlItem = Array.from(event.clipboardData.items || []).find(item => item.type === 'text/html');
                if (htmlItem) {
                    htmlItem.getAsString((html) => {
                        // Detectar si contiene tabla
                        if (html.includes('<table') || html.includes('<TR') || html.includes('<tr')) {
                            event.preventDefault();
                            const parser = new DOMParser();
                            const doc = parser.parseFromString(html, 'text/html');
                            const table = doc.querySelector('table');
                            
                            if (table) {
                                // Convertir tabla HTML a estructura Tiptap
                                const rows = Array.from(table.querySelectorAll('tr'));
                                if (rows.length > 0) {
                                    const cells = rows[0].querySelectorAll('td, th').length;
                                    if (cells > 0) {
                                        // Insertar tabla
                                        view.dispatch(view.state.tr.replaceSelectionWith(
                                            view.state.schema.nodes.table.create(
                                                {},
                                                view.state.schema.nodes.tableRow.create(
                                                    {},
                                                    Array(cells).fill(null).map(() =>
                                                        view.state.schema.nodes.tableCell.create()
                                                    )
                                                )
                                            )
                                        ));
                                        return true;
                                    }
                                }
                            }
                        }
                    });
                }

                return false;
            }
        },
        onCreate({ editor }) {
            document.getElementById('contenido-hidden').value = editor.getHTML();
            updateTOC(editor);
            setupImageControls(editor);
            console.log('DEBUG: Editor onCreate - calling updateToolbarActive()');
            updateToolbarActive();
        },
        onUpdate: ({ editor }) => {
            // Mostrar "Editando..."
            const statusInfo = document.getElementById('save-status');
            if (statusInfo) {
                statusInfo.innerText = "Editando...";
                statusInfo.classList.remove('opacity-0');
            }
            document.getElementById('contenido-hidden').value = editor.getHTML();
            updateTOC(editor);
            console.log('DEBUG: Editor onUpdate - calling updateToolbarActive()');
            updateToolbarActive();
            // Debounce Trigger
            clearTimeout(saveTimeout);
            saveTimeout = setTimeout(() => {
                if (window.showSaving) window.showSaving();
                htmx.trigger('#btn-guardar', 'saveContent');
            }, 2000);
        }
    });

    // --- CREAR POPOVERS DINÁMICAMENTE EN EL BODY ---
    let menuReferences = {}; // Guardar referencias a los elementos dinámicos
    
    function createPopoverMenus() {
        const container = document.createElement('div');
        container.id = 'popover-menus-container';
        container.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 9999;';

        // HEADING MENU
        const headingMenu = document.createElement('div');
        headingMenu.id = 'heading-menu';
        headingMenu.innerHTML = `
            <button type="button" class="popover-item" data-heading="1">
                <span class="text-lg font-bold">H1</span>
                <span class="text-xs text-gray-500">Título</span>
            </button>
            <button type="button" class="popover-item" data-heading="2">
                <span class="text-base font-bold">H2</span>
                <span class="text-xs text-gray-500">Subtítulo</span>
            </button>
            <button type="button" class="popover-item" data-heading="3">
                <span class="text-sm font-bold">H3</span>
                <span class="text-xs text-gray-500">Sección</span>
            </button>
        `;
        headingMenu.style.cssText = 'position: fixed; background: #1a1a1a; border: 1px solid #333; border-radius: 0.5rem; padding: 0.5rem; box-shadow: 0 10px 40px rgba(0,0,0,0.8); display: none; pointer-events: auto; z-index: 10000;';

        // LISTS MENU
        const listsMenu = document.createElement('div');
        listsMenu.id = 'lists-menu';
        listsMenu.innerHTML = `
            <button type="button" class="popover-item" data-list="bullet">
                <i class="fa-solid fa-list-ul"></i>
                <span>Viñetas</span>
            </button>
            <button type="button" class="popover-item" data-list="ordered">
                <i class="fa-solid fa-list-ol"></i>
                <span>Numerada</span>
            </button>
            <button type="button" class="popover-item" data-list="task">
                <i class="fa-solid fa-square-check"></i>
                <span>Checklist</span>
            </button>
        `;
        listsMenu.style.cssText = 'position: fixed; background: #1a1a1a; border: 1px solid #333; border-radius: 0.5rem; padding: 0.5rem; box-shadow: 0 10px 40px rgba(0,0,0,0.8); display: none; pointer-events: auto; z-index: 10000;';

        // FONT FAMILY MENU
        const fontMenu = document.createElement('div');
        fontMenu.id = 'font-menu';
        fontMenu.innerHTML = `
            <button type="button" class="popover-item-font" data-font="Inter" style="font-family: 'Inter'">Inter</button>
            <button type="button" class="popover-item-font" data-font="Arial" style="font-family: Arial">Arial</button>
            <button type="button" class="popover-item-font" data-font="Georgia" style="font-family: Georgia">Georgia</button>
            <button type="button" class="popover-item-font" data-font="Courier" style="font-family: 'Courier New'">Courier New</button>
            <button type="button" class="popover-item-font" data-font="Verdana" style="font-family: Verdana">Verdana</button>
        `;
        fontMenu.style.cssText = 'position: fixed; background: #1a1a1a; border: 1px solid #333; border-radius: 0.5rem; padding: 0.5rem; box-shadow: 0 10px 40px rgba(0,0,0,0.8); display: none; pointer-events: auto; z-index: 10000; width: 160px;';

        // FONT SIZE MENU
        const sizeMenu = document.createElement('div');
        sizeMenu.id = 'size-menu';
        sizeMenu.innerHTML = `
            <button type="button" class="popover-item-size" data-size="10">10px</button>
            <button type="button" class="popover-item-size" data-size="12">12px</button>
            <button type="button" class="popover-item-size" data-size="14">14px</button>
            <button type="button" class="popover-item-size" data-size="16">16px</button>
            <button type="button" class="popover-item-size" data-size="18">18px</button>
            <button type="button" class="popover-item-size" data-size="20">20px</button>
            <button type="button" class="popover-item-size" data-size="24">24px</button>
        `;
        sizeMenu.style.cssText = 'position: fixed; background: #1a1a1a; border: 1px solid #333; border-radius: 0.5rem; padding: 0.5rem; box-shadow: 0 10px 40px rgba(0,0,0,0.8); display: none; pointer-events: auto; z-index: 10000;';

        // ALIGNMENT MENU
        const alignMenu = document.createElement('div');
        alignMenu.id = 'align-menu';
        alignMenu.innerHTML = `
            <button type="button" class="popover-item" data-align="left">
                <i class="fa-solid fa-align-left"></i>
                <span>Izquierda</span>
            </button>
            <button type="button" class="popover-item" data-align="center">
                <i class="fa-solid fa-align-center"></i>
                <span>Centro</span>
            </button>
            <button type="button" class="popover-item" data-align="right">
                <i class="fa-solid fa-align-right"></i>
                <span>Derecha</span>
            </button>
            <button type="button" class="popover-item" data-align="justify">
                <i class="fa-solid fa-align-justify"></i>
                <span>Justificado</span>
            </button>
        `;
        alignMenu.style.cssText = 'position: fixed; background: #1a1a1a; border: 1px solid #333; border-radius: 0.5rem; padding: 0.5rem; box-shadow: 0 10px 40px rgba(0,0,0,0.8); display: none; pointer-events: auto; z-index: 10000;';

        // COLORS MENU
        const colorsMenu = document.createElement('div');
        colorsMenu.id = 'colors-menu';
        colorsMenu.innerHTML = `
            <div style="padding: 0.5rem;">
                <label style="font-size: 0.75rem; color: #9ca3af; display: block; margin-bottom: 0.5rem;">Color de texto</label>
                <input type="color" id="btn-color" style="width: 100%; height: 2rem; cursor: pointer; border-radius: 0.375rem; border: 1px solid #444;" />
            </div>
            <div style="border-top: 1px solid #333;"></div>
            <div style="padding: 0.5rem;">
                <label style="font-size: 0.75rem; color: #9ca3af; display: block; margin-bottom: 0.5rem;">Color de fondo</label>
                <input type="color" id="btn-highlight" style="width: 100%; height: 2rem; cursor: pointer; border-radius: 0.375rem; border: 1px solid #444;" />
            </div>
        `;
        colorsMenu.style.cssText = 'position: fixed; background: #1a1a1a; border: 1px solid #333; border-radius: 0.5rem; padding: 0; box-shadow: 0 10px 40px rgba(0,0,0,0.8); display: none; pointer-events: auto; z-index: 10000; width: 192px;';

        container.appendChild(headingMenu);
        container.appendChild(fontMenu);
        container.appendChild(sizeMenu);
        container.appendChild(listsMenu);
        container.appendChild(alignMenu);
        container.appendChild(colorsMenu);

        document.body.appendChild(container);
        
        // Guardar referencias a los items de menú para actualización en tiempo real
        menuReferences = {
            headingItems: headingMenu.querySelectorAll('.popover-item'),
            fontItems: fontMenu.querySelectorAll('.popover-item-font'),
            sizeItems: sizeMenu.querySelectorAll('.popover-item-size'),
            listItems: listsMenu.querySelectorAll('.popover-item'),
            alignItems: alignMenu.querySelectorAll('.popover-item')
        };
    }

    // --- TOOLBAR MEJORADO CON POPOVER API ---
    function updateToolbarActive() {
        // Validación: menus deben estar creados
        if (!document.getElementById('heading-menu')) {
            console.log('DEBUG: heading-menu no encontrado');
            return;
        }
        
        // Validación: menuReferences debe tener headingItems
        if (!menuReferences || !menuReferences.headingItems) {
            console.log('DEBUG: menuReferences.headingItems no existe', menuReferences);
            return;
        }
        
        // 1. BOTONES SIMPLES (Bold, Italic, Code, Quote, Code Inline)
        updateButtonState('btn-bold', editor.isActive('bold'));
        updateButtonState('btn-italic', editor.isActive('italic'));
        updateButtonState('btn-codeblock', editor.isActive('codeBlock'));
        updateButtonState('btn-blockquote', editor.isActive('blockquote'));
        updateButtonState('btn-code-inline', editor.isActive('code'));
        
        // 2. HEADINGS - Display + Menu Items
        let headingDisplay = 'H';
        let headingActive = false;
        
        if (editor.isActive('heading', { level: 1 })) {
            headingDisplay = 'H1';
            headingActive = true;
            console.log('DEBUG: H1 detectado');
        } else if (editor.isActive('heading', { level: 2 })) {
            headingDisplay = 'H2';
            headingActive = true;
            console.log('DEBUG: H2 detectado');
        } else if (editor.isActive('heading', { level: 3 })) {
            headingDisplay = 'H3';
            headingActive = true;
            console.log('DEBUG: H3 detectado');
        } else {
            console.log('DEBUG: No heading detectado');
        }
        
        const headingDisplayEl = document.getElementById('heading-display');
        if (headingDisplayEl) {
            console.log('DEBUG: Actualizando heading-display a:', headingDisplay);
            headingDisplayEl.textContent = headingDisplay;
        } else {
            console.log('DEBUG: heading-display no encontrado');
        }
        updateButtonState('btn-headings', headingActive);
        
        // Update heading menu items
        if (menuReferences.headingItems) {
            menuReferences.headingItems.forEach(item => {
                const level = parseInt(item.dataset.heading);
                const isActive = editor.isActive('heading', { level });
                item.classList.toggle('active', isActive);
            });
        }
        
        // 3. LISTS - Icon + Button + Menu Items
        let listIcon = 'fa-list-ul';
        let listActive = false;
        
        if (editor.isActive('bulletList')) {
            listIcon = 'fa-list-ul';
            listActive = true;
        } else if (editor.isActive('orderedList')) {
            listIcon = 'fa-list-ol';
            listActive = true;
        } else if (editor.isActive('taskList')) {
            listIcon = 'fa-square-check';
            listActive = true;
        }
        
        const listIconEl = document.getElementById('list-icon');
        if (listIconEl) {
            listIconEl.className = `fa-solid ${listIcon} text-xs`;
        }
        updateButtonState('btn-lists', listActive);
        
        // Update list menu items
        if (menuReferences.listItems) {
            menuReferences.listItems.forEach(item => {
                const listType = item.dataset.list;
                let isActive = false;
                
                if (listType === 'bullet') isActive = editor.isActive('bulletList');
                else if (listType === 'ordered') isActive = editor.isActive('orderedList');
                else if (listType === 'task') isActive = editor.isActive('taskList');
                
                item.classList.toggle('active', isActive);
            });
        }
        
        // 4. ALIGNMENT - Icon + Button + Menu Items
        let alignIcon = 'fa-align-left';
        let alignActive = false;
        
        if (editor.isActive({ textAlign: 'center' })) {
            alignIcon = 'fa-align-center';
            alignActive = true;
        } else if (editor.isActive({ textAlign: 'right' })) {
            alignIcon = 'fa-align-right';
            alignActive = true;
        } else if (editor.isActive({ textAlign: 'justify' })) {
            alignIcon = 'fa-align-justify';
            alignActive = true;
        }
        
        const alignIconEl = document.getElementById('align-icon');
        if (alignIconEl) {
            alignIconEl.className = `fa-solid ${alignIcon} text-xs`;
        }
        updateButtonState('btn-align', alignActive);
        
        // Update alignment menu items
        if (menuReferences.alignItems) {
            menuReferences.alignItems.forEach(item => {
                const alignment = item.dataset.align;
                const isActive = editor.isActive({ textAlign: alignment });
                item.classList.toggle('active', isActive);
            });
        }
        
        // 5. FONT FAMILY - Display + Menu Items
        const currentFont = editor.getAttributes('textStyle')?.fontFamily || 'Inter';
        const fontDisplayEl = document.getElementById('font-display');
        if (fontDisplayEl) fontDisplayEl.textContent = currentFont;
        
        // Update font menu items
        if (menuReferences.fontItems) {
            menuReferences.fontItems.forEach(item => {
                const font = item.dataset.font;
                const isActive = editor.isActive('textStyle', { fontFamily: font });
                item.classList.toggle('active', isActive);
            });
        }
        
        // 6. FONT SIZE - Display + Menu Items
        let currentSize = '12';
        const fontSizeAttrs = editor.getAttributes('fontSize');
        if (fontSizeAttrs && fontSizeAttrs.fontSize) {
            currentSize = String(fontSizeAttrs.fontSize).replace('px', '');
        }
        const sizeDisplayEl = document.getElementById('size-display');
        if (sizeDisplayEl) sizeDisplayEl.textContent = currentSize;
        
        // Update size menu items
        if (menuReferences.sizeItems) {
            menuReferences.sizeItems.forEach(item => {
                const size = item.dataset.size + 'px';
                const isActive = editor.isActive('fontSize', { fontSize: size });
                item.classList.toggle('active', isActive);
            });
        }
    }
    
    // Helper function to update button active state
    function updateButtonState(id, active) {
        const el = document.getElementById(id);
        if (el) {
            el.classList.toggle('active', active);
        }
    }

    // Función para posicionar y mostrar menus
    function showMenu(buttonId, menuId) {
        const button = document.getElementById(buttonId);
        const menu = document.getElementById(menuId);
        
        if (!button || !menu) return;

        const btnRect = button.getBoundingClientRect();
        
        // Calcular posición base (debajo del botón)
        let top = btnRect.bottom + 8;
        let left = btnRect.left;
        
        // Aplicar posición
        menu.style.top = top + 'px';
        menu.style.left = left + 'px';
        menu.style.display = 'block';
        
        // Forzar reflow
        menu.offsetHeight;
        
        // Obtener medidas reales
        const menuRect = menu.getBoundingClientRect();
        
        // Ajustar si se sale por la derecha
        if (menuRect.right > window.innerWidth - 10) {
            left = window.innerWidth - menuRect.width - 10;
            menu.style.left = left + 'px';
        }
        
        // Ajustar si se sale por la izquierda
        if (left < 10) {
            menu.style.left = '10px';
        }
        
        // Ajustar si se sale por abajo (mostrar arriba)
        if (menuRect.bottom > window.innerHeight - 10) {
            top = btnRect.top - menuRect.height - 8;
            menu.style.top = top + 'px';
        }
    }

    function hideMenu(menuId) {
        const menu = document.getElementById(menuId);
        if (menu) menu.style.display = 'none';
    }

    // Cerrar menus al clickear afuera
    document.addEventListener('click', (e) => {
        const toolbar = document.getElementById('editor-toolbar');
        if (!toolbar || !toolbar.contains(e.target)) {
            document.querySelectorAll('[id$="-menu"]').forEach(menu => {
                if (menu.id.startsWith('popover')) return;
                menu.style.display = 'none';
            });
        }
    }, true);

    function setupToolbarActions(editor) {
        // Configurar botones para mostrar menus
        document.getElementById('btn-headings')?.addEventListener('click', () => showMenu('btn-headings', 'heading-menu'));
        document.getElementById('btn-font-family')?.addEventListener('click', () => showMenu('btn-font-family', 'font-menu'));
        document.getElementById('btn-font-size')?.addEventListener('click', () => showMenu('btn-font-size', 'size-menu'));
        document.getElementById('btn-lists')?.addEventListener('click', () => showMenu('btn-lists', 'lists-menu'));
        document.getElementById('btn-align')?.addEventListener('click', () => showMenu('btn-align', 'align-menu'));
        document.getElementById('btn-colors')?.addEventListener('click', () => showMenu('btn-colors', 'colors-menu'));

        // HEADINGS
        document.querySelectorAll('#heading-menu .popover-item').forEach(btn => {
            btn.onclick = () => {
                const level = parseInt(btn.dataset.heading);
                editor.chain().focus().toggleHeading({ level: level }).run();
                hideMenu('heading-menu');
                updateToolbarActive();
            };
        });

        // BOLD & ITALIC
        document.getElementById('btn-bold').onclick = () => {
            editor.chain().focus().toggleBold().run();
            updateToolbarActive();
        };
        document.getElementById('btn-italic').onclick = () => {
            editor.chain().focus().toggleItalic().run();
            updateToolbarActive();
        };

        // FONT FAMILY
        document.querySelectorAll('#font-menu .popover-item-font').forEach(btn => {
            btn.onclick = () => {
                const font = btn.dataset.font;
                editor.chain().focus().setFontFamily(font).run();
                hideMenu('font-menu');
                updateToolbarActive();
            };
        });

        // FONT SIZE (via custom setFontSize command)
        document.querySelectorAll('#size-menu .popover-item-size').forEach(btn => {
            btn.onclick = () => {
                const size = btn.dataset.size + 'px';
                editor.chain().focus().setFontSize(size).run();
                hideMenu('size-menu');
                updateToolbarActive();
            };
        });

        // LISTS
        document.querySelectorAll('#lists-menu .popover-item').forEach(btn => {
            btn.onclick = () => {
                const listType = btn.dataset.list;
                if (listType === 'bullet') editor.chain().focus().toggleBulletList().run();
                else if (listType === 'ordered') editor.chain().focus().toggleOrderedList().run();
                else if (listType === 'task') editor.chain().focus().toggleTaskList().run();
                hideMenu('lists-menu');
                updateToolbarActive();
            };
        });

        // ALIGNMENT
        document.querySelectorAll('#align-menu .popover-item').forEach(btn => {
            btn.onclick = () => {
                const align = btn.dataset.align;
                editor.chain().focus().setTextAlign(align).run();
                hideMenu('align-menu');
                updateToolbarActive();
            };
        });

        // CODE BLOCK & BLOCKQUOTE
        document.getElementById('btn-codeblock').onclick = () => {
            editor.chain().focus().toggleCodeBlock().run();
            updateToolbarActive();
        };
        document.getElementById('btn-blockquote').onclick = () => {
            editor.chain().focus().toggleBlockquote().run();
            updateToolbarActive();
        };

        // COLORS
        document.getElementById('btn-color').oninput = (e) => {
            editor.chain().focus().setColor(e.target.value).run();
        };
        document.getElementById('btn-highlight').oninput = (e) => {
            editor.chain().focus().setHighlight({ color: e.target.value }).run();
        };

        // CODE INLINE
        document.getElementById('btn-code-inline').onclick = () => {
            editor.chain().focus().toggleCode().run();
            updateToolbarActive();
        };

        // UNDO/REDO
        document.getElementById('btn-undo').onclick = () => {
            editor.chain().focus().undo().run();
            updateToolbarActive();
        };
        document.getElementById('btn-redo').onclick = () => {
            editor.chain().focus().redo().run();
            updateToolbarActive();
        };
    }

    window.editor.on('update', () => {
        console.log('DEBUG: Editor "update" event fired');
        updateToolbarActive();
    });
    window.editor.on('selectionUpdate', () => {
        console.log('DEBUG: Editor "selectionUpdate" event fired');
        updateToolbarActive();
    });
    createPopoverMenus();
    setupToolbarActions(window.editor);
    console.log('DEBUG: Initialization - menuReferences:', menuReferences);
    updateToolbarActive();

    // Funciones Globales
    window.showSaving = function() {
        const statusInfo = document.getElementById('save-status');
        if(statusInfo) { 
            statusInfo.innerText = "Guardando..."; 
            // Esperamos a que HTMX responda realmente, pero por UX simulamos el "Guardado" tras un instante
            // Lo ideal es usar htmx:afterRequest como en mi propuesta anterior, pero para ser fiel a tu código original:
            setTimeout(() => { statusInfo.innerText = "Guardado"; }, 1000); 
        }
    };

    // ✅ PRINCIPIO DEL CORONEL:
    // La función toggleRightSidebar() ya está definida en base_app.html
    // No duplicamos funcionalidad aquí.

    window.closeMoveModal = function() { document.getElementById('modal-mover').close(); };

    // Drag & Drop
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-upload');
    const uploadForm = document.getElementById('upload-form');
    if (dropZone) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(evt => { dropZone.addEventListener(evt, (e) => { e.preventDefault(); e.stopPropagation(); }, false); });
        dropZone.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length > 0) { fileInput.files = files; htmx.trigger(uploadForm, 'submit'); }
        }, false);
    }
    
    })
</script>

```

---

## 📄 Archivo: `app/templates/partials/lista_adjuntos.html`
```html
<!-- app/templates/partials/lista_adjuntos.html -->

<div id="lista-adjuntos" class="space-y-2 fade-in">
    {% if adjuntos and adjuntos|length > 0 %}
        {% for adjunto in adjuntos %}
        <div class="group flex items-center gap-3 p-2 rounded bg-[#2a2a2a] hover:bg-[#333] transition border border-transparent hover:border-[#444]">
            
            <!-- Icono según extensión (simplificado) -->
            <div class="shrink-0 text-gray-400">
                {% if 'image' in adjunto.tipo_archivo %}
                    <i class="fa-regular fa-image text-purple-400"></i>
                {% elif 'pdf' in adjunto.tipo_archivo %}
                    <i class="fa-regular fa-file-pdf text-red-400"></i>
                {% else %}
                    <i class="fa-regular fa-file text-blue-400"></i>
                {% endif %}
            </div>

            <!-- Nombre y Link -->
            <a href="{{ adjunto.url }}" target="_blank" class="flex-1 min-w-0">
                <p class="text-[11px] text-gray-300 truncate font-medium hover:underline hover:text-white" title="{{ adjunto.nombre_original }}">
                    {{ adjunto.nombre_original }}
                </p>
                <p class="text-[9px] text-gray-500 truncate">
                    {{ adjunto.created_at.strftime('%d %b %H:%M') }}
                </p>
            </a>

            <!-- Botón Eliminar -->
            <button 
                hx-post="/adjunto/eliminar/{{ adjunto.id }}"
                hx-target="#lista-adjuntos-wrapper"
                hx-confirm="¿Eliminar este archivo?"
                class="shrink-0 text-gray-600 hover:text-red-400 opacity-0 group-hover:opacity-100 transition p-1"
                title="Eliminar adjunto"
            >
                <i class="fa-solid fa-xmark"></i>
            </button>
        </div>
        {% endfor %}
    {% else %}
        <!-- Estado vacío (opcional, o dejarlo limpio) -->
        <p class="text-[10px] text-gray-600 text-center py-2 italic">Sin adjuntos</p>
    {% endif %}
</div>
```

---

## 📄 Archivo: `app/templates/partials/lista_notas_evernote.html`
```html
<!-- app/templates/partials/lista_notas_evernote.html -->

<!-- HEADER con función global añadida -->
<script>
    // Función global para inicializar el editor TipTap
    window.initTiptapEditor = function() {
        // Verificar si el editor ya existe y destruirlo
        if (window.editor) {
            window.editor.destroy();
            window.editor = null;
        }
        
        // Esperar un momento para que el DOM se actualice
        setTimeout(() => {
            const editorContainer = document.querySelector('#tiptap-editor');
            const contentJson = document.querySelector('#contenido-json');
            
            if (editorContainer && contentJson) {
                console.log('Inicializando editor TipTap...');
                // Forzar la ejecución del script del editor
                const scriptTags = document.querySelectorAll('script[src*="tiptap"], script[src*="lowlight"]');
                if (scriptTags.length > 0) {
                    // Los scripts ya están cargados, solo necesitamos ejecutar la inicialización
                    // Esto se hace automáticamente cuando se carga el partial
                }
            }
        }, 50);
    };
</script>

<!-- Header con buscador integrado (estilo Evernote) -->
<div class="bg-[#232326] border-b border-[#3A3A3D]">
    <!-- Barra de búsqueda -->
    <div class="px-3 py-2.5 flex items-center gap-2">
        <button class="text-gray-400 hover:text-white p-1.5 -ml-1 transition">
            <i class="fa-solid fa-chevron-left text-base"></i>
        </button>
        <div class="flex-1 relative">
            <i class="fa-solid fa-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 text-xs"></i>
            <input 
                type="text" 
                placeholder="Buscar..." 
                class="w-full pl-9 pr-3 py-1.5 rounded-md bg-[#3A3A3D] text-gray-200 text-sm placeholder-gray-500 focus:outline-none focus:bg-[#48484B] transition border-0"
            />
        </div>
    </div>
    
    <!-- Título de sección -->
    <div class="px-3 pb-3 pt-3">
        <div class="flex items-start justify-between mb-0.5">
            <h1 class="text-[19px] font-bold text-white leading-tight tracking-tight">
                {{ tema.nombre if tema else 'Personal' }}
            </h1>
            <div class="flex items-center gap-1 -mt-1">
                <!-- Botón Nuevo (CORREGIDO HTMX) -->
                <button 
                    hx-post="/nota/crear/{{ tema.id }}"
                    hx-target="#editor-pane"
                    hx-swap="innerHTML settle:0.5s"
                    hx-on:htmx:after-settle="initTiptapEditor()"
                    class="text-gray-300 hover:text-white hover:bg-[#3A3A3D] px-2.5 py-1.5 rounded-md text-sm font-medium flex items-center gap-1.5 transition"
                    title="Nueva nota"
                >
                    <i class="fa-solid fa-plus text-xs"></i>
                    <span class="text-[13px]">Nuevo</span>
                </button>
                
                <!-- Botón Filtros -->
                <div class="relative">
                    <button 
                        onclick="toggleFilterMenu(event)"
                        class="filter-menu-btn text-gray-400 hover:text-white p-1.5 rounded hover:bg-[#3A3A3D] transition"
                        title="Filtros"
                    >
                        <i class="fa-solid fa-sliders text-sm"></i>
                    </button>
                    <!-- Menú desplegable Filtros -->
                    <div id="filterMenu" class="hidden absolute right-0 mt-1 w-56 bg-[#2C2C2E] border border-[#3A3A3D] rounded-lg shadow-xl z-50 py-1">
                        <div class="px-3 py-2 text-xs text-gray-500 font-semibold">ORDENAR POR</div>
                        <button onclick="sortNotes('updated')" class="sort-updated w-full text-left px-3 py-2 text-sm text-gray-300 hover:bg-[#3A3A3D] flex items-center justify-between">
                            Última modificación <i class="fa-solid fa-check text-[#007AFF] text-xs"></i>
                        </button>
                        <button onclick="sortNotes('created')" class="sort-created w-full text-left px-3 py-2 text-sm text-gray-300 hover:bg-[#3A3A3D] flex items-center justify-between">
                            Fecha de creación <i class="fa-solid fa-check text-[#007AFF] text-xs hidden"></i>
                        </button>
                        <button onclick="sortNotes('title')" class="sort-title w-full text-left px-3 py-2 text-sm text-gray-300 hover:bg-[#3A3A3D] flex items-center justify-between">
                            Título <i class="fa-solid fa-check text-[#007AFF] text-xs hidden"></i>
                        </button>
                        <div class="border-t border-[#3A3A3D] my-1"></div>
                        <div class="px-3 py-2 text-xs text-gray-500 font-semibold">FILTRAR</div>
                        <button onclick="filterNotes('attachments')" class="filter-attachments w-full text-left px-3 py-2 text-sm text-gray-300 hover:bg-[#3A3A3D] flex items-center justify-between">
                            Con adjuntos <i class="fa-solid fa-check text-[#007AFF] text-xs hidden"></i>
                        </button>
                        <button onclick="filterNotes('reminders')" class="filter-reminders w-full text-left px-3 py-2 text-sm text-gray-300 hover:bg-[#3A3A3D] flex items-center justify-between">
                            Con recordatorios <i class="fa-solid fa-check text-[#007AFF] text-xs hidden"></i>
                        </button>
                        <button onclick="clearFilters()" class="w-full text-left px-3 py-2 text-sm text-gray-400 hover:bg-[#3A3A3D] border-t border-[#3A3A3D] mt-1">
                            Limpiar filtros
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <!-- ID AGREGADO AQUÍ PARA EVITAR ERRORES JS -->
        <p id="notes-counter" class="text-[12px] text-gray-500 font-normal">{{ notas|length }} notas</p>
    </div>
</div>

<!-- Lista de notas (estilo Evernote minimalista) -->
<div id="notesContainer" class="bg-[#232326] overflow-y-auto">
    {% if notas and notas|length > 0 %}
        {% for nota in notas %}
        
        <!-- ======================================================= -->
        <!-- AQUÍ ESTÁ EL CAMBIO CLAVE - HTMX CON SETTLE Y EVENTOS -->
        <!-- ======================================================= -->
        <div 
            hx-get="/partial/editor/{{ nota.id }}"
            hx-target="#editor-pane"
            hx-swap="innerHTML"
            hx-push-url="/cuaderno/{{ tema.cuaderno_id }}/nota/{{ nota.id }}"
            hx-indicator="#editor-pane"
            hx-on:htmx:before-request="showNoteLoading()"
            hx-on:htmx:after-request="
                if(event.detail.successful) {
                    // 1. Cargar inspector (CORREGIDO)
                    htmx.ajax('GET', '/partial/inspector/{{ nota.id }}', {
                        target: '#inspector-pane-content',
                        swap: 'innerHTML',
                        hxOnAfterSettle: 'handleNoteSelection(\'{{ nota.id }}\', \'{{ tema.cuaderno_id }}\')'
                    });
                    
                    // 2. Manejar selección visual
                    handleNoteSelection('{{ nota.id }}', '{{ tema.cuaderno_id }}');
                }
            "
            
            class="note-item flex items-start gap-3 px-3 py-3 border-b border-[#2C2C2E] cursor-pointer hover:bg-[#2C2C2E]/40 transition-colors duration-100 rounded-xl border-l-4 border-transparent"
            data-note-id="{{ nota.id }}"
            data-cuaderno-id="{{ tema.cuaderno_id }}"
            data-has-attachments="{{ 'true' if nota.adjuntos and nota.adjuntos|length > 0 else 'false' }}"
            onclick="handleNoteSelection('{{ nota.id }}', '{{ tema.cuaderno_id }}', event)"
        >
            <!-- Thumbnail/Icono -->
            <div class="note-thumbnail w-[42px] h-[42px] flex-shrink-0 rounded-md overflow-hidden flex items-center justify-center">
                {% set month_data = {
                    1: {'name': 'ENE', 'color': 'from-blue-500 to-blue-600'},
                    2: {'name': 'FEB', 'color': 'from-purple-500 to-purple-600'},
                    3: {'name': 'MAR', 'color': 'from-pink-500 to-pink-600'},
                    4: {'name': 'ABR', 'color': 'from-green-500 to-green-600'},
                    5: {'name': 'MAY', 'color': 'from-yellow-500 to-yellow-600'},
                    6: {'name': 'JUN', 'color': 'from-orange-500 to-orange-600'},
                    7: {'name': 'JUL', 'color': 'from-red-500 to-red-600'},
                    8: {'name': 'AGO', 'color': 'from-teal-500 to-teal-600'},
                    9: {'name': 'SEP', 'color': 'from-cyan-500 to-cyan-600'},
                    10: {'name': 'OCT', 'color': 'from-indigo-500 to-indigo-600'},
                    11: {'name': 'NOV', 'color': 'from-violet-500 to-violet-600'},
                    12: {'name': 'DIC', 'color': 'from-rose-500 to-rose-600'}
                } %}
                {% set nota_month = nota.updated_at.month %}
                {% set month_info = month_data[nota_month] %}
                
                <div class="w-full h-full rounded-full bg-gradient-to-br {{ month_info.color }} flex items-center justify-center">
                    <span class="text-white font-bold text-[8px] tracking-wide">{{ month_info.name }}</span>
                </div>
            </div>
            
            <!-- Contenido de la nota -->
            <div class="flex-1 min-w-0 pt-0.5">
                <h3 class="text-[14px] font-semibold text-white mb-1 line-clamp-2 leading-tight">
                    {{ nota.titulo if nota.titulo else "Sin título" }}
                </h3>
                <p class="text-[12px] text-gray-400 line-clamp-2 mb-1.5 leading-[1.4]">
                    {{ nota.preview_contenido if nota.preview_contenido else "..." }}
                </p>
                <div class="flex items-center gap-2.5 text-[11px] text-gray-500 font-normal">
                    <span>{{ nota.updated_at.strftime('%d %b %Y') }}</span>
                    {% if nota.tags and nota.tags|length > 0 %}
                        {% for tag in nota.tags[:2] %}
                        <span class="px-1.5 py-0.5 rounded-sm bg-[#3A3A3D] text-gray-400">
                            {{ tag }}
                        </span>
                        {% endfor %}
                    {% endif %}
                </div>
            </div>
            
            <!-- Botón eliminar (Mantenemos stopPropagation para que no dispare la navegación) -->
            <button 
                onclick="event.stopPropagation(); confirmDeleteNote('{{ nota.id }}', `{{ nota.titulo if nota.titulo else 'Sin título' }}`)"
                class="flex-shrink-0 text-gray-500 hover:text-red-400 p-2 rounded hover:bg-[#3A3A3D] transition"
                title="Eliminar nota"
            >
                <i class="fa-solid fa-trash text-sm"></i>
            </button>
        </div>
        {% endfor %}
    {% else %}
        <div class="flex flex-col items-center justify-center h-64 text-center px-6">
            <i class="fa-regular fa-file text-4xl text-gray-600 mb-3 opacity-30"></i>
            <p class="text-sm text-gray-500">No se encontraron notas</p>
        </div>
    {% endif %}
</div>

<style>
    /* Efecto de selección con borde azul estilo Evernote */
    .note-item.selected {
        background-color: rgba(0, 122, 255, 0.08) !important;
        border: 2px solid #007AFF !important;
        border-radius: 12px !important;
        padding: 10px; /* Compensar el borde de 2px */
    }
    
    /* Line clamp para preview */
    .line-clamp-2 {
        display: -webkit-box;
        -webkit-line-clamp: 2;
        line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
</style>

<script>
    function selectNote(element) {
        document.querySelectorAll('.note-item').forEach(el => {
            el.classList.remove('selected');
        });
        element.classList.add('selected');
    }
    
    // ========== FUNCIONES DE ORDENAMIENTO Y FILTROS ==========
    function sortNotes(sortBy) {
        const container = document.getElementById('notesContainer');
        const notesArray = Array.from(container.querySelectorAll('.note-item'));
        
        notesArray.sort((a, b) => {
            if (sortBy === 'updated') {
                const dateA = new Date(a.querySelector('.flex.items-center span').textContent);
                const dateB = new Date(b.querySelector('.flex.items-center span').textContent);
                return dateB - dateA;
            } else if (sortBy === 'created') {
                const dateA = new Date(a.querySelector('.flex.items-center span').textContent);
                const dateB = new Date(b.querySelector('.flex.items-center span').textContent);
                return dateB - dateA;
            } else if (sortBy === 'title') {
                const titleA = a.querySelector('h3').textContent.toLowerCase();
                const titleB = b.querySelector('h3').textContent.toLowerCase();
                return titleA.localeCompare(titleB);
            }
        });
        
        notesArray.forEach(note => container.appendChild(note));
        document.querySelectorAll('[class*="sort-"] .fa-check').forEach(check => check.classList.add('hidden'));
        document.querySelector(`.sort-${sortBy} .fa-check`).classList.remove('hidden');
        localStorage.setItem('notesSortBy', sortBy);
        closeAllMenus();
    }
    
    let activeFilters = new Set();
    
    function filterNotes(filterType) {
        const button = document.querySelector(`.filter-${filterType}`);
        const check = button.querySelector('.fa-check');
        
        if (activeFilters.has(filterType)) {
            activeFilters.delete(filterType);
            check.classList.add('hidden');
        } else {
            activeFilters.add(filterType);
            check.classList.remove('hidden');
        }
        applyFilters();
    }
    
    function applyFilters() {
        const notes = document.querySelectorAll('.note-item');
        notes.forEach(note => {
            let shouldShow = true;
            if (activeFilters.has('attachments')) {
                const hasAttachments = note.dataset.hasAttachments === 'true';
                if (!hasAttachments) shouldShow = false;
            }
            if (activeFilters.has('reminders')) {
                const hasReminders = note.dataset.hasReminders === 'true';
                if (!hasReminders) shouldShow = false;
            }
            if (shouldShow) {
                note.style.display = '';
            } else {
                note.style.display = 'none';
            }
        });
        localStorage.setItem('activeFilters', JSON.stringify([...activeFilters]));
    }
    
    function clearFilters() {
        activeFilters.clear();
        document.querySelectorAll('[class*="filter-"] .fa-check').forEach(check => {
            check.classList.add('hidden');
        });
        document.querySelectorAll('.note-item').forEach(note => {
            note.style.display = '';
        });
        localStorage.removeItem('activeFilters');
        closeAllMenus();
    }
    
    document.addEventListener('DOMContentLoaded', function() {
        const savedSort = localStorage.getItem('notesSortBy') || 'updated';
        if (savedSort !== 'updated') {
            sortNotes(savedSort);
        }
        const savedFilters = localStorage.getItem('activeFilters');
        if (savedFilters) {
            activeFilters = new Set(JSON.parse(savedFilters));
            activeFilters.forEach(filter => {
                document.querySelector(`.filter-${filter} .fa-check`).classList.remove('hidden');
            });
            applyFilters();
        }
    });
    
    // ========== FUNCIONES DE MENÚS ==========
    function toggleFilterMenu(event) {
        event.stopPropagation();
        const menu = document.getElementById('filterMenu');
        closeAllMenus();
        menu.classList.toggle('hidden');
    }
    
    function closeAllMenus() {
        document.querySelectorAll('[id$="Menu"]').forEach(menu => {
            if (!event || !menu.contains(event.target)) {
                menu.classList.add('hidden');
            }
        });
    }
    
    document.addEventListener('click', function(event) {
        if (!event.target.closest('.filter-menu-btn')) {
            closeAllMenus();
        }
    });
    
    // ========== FUNCIONES DE ELIMINAR NOTA (CORREGIDAS) ==========
    
    let noteToDelete = null;
    
    function confirmDeleteNote(noteId, noteTitle) {
        noteToDelete = noteId;
        document.getElementById('deleteNoteTitle').textContent = noteTitle;
        document.getElementById('deleteNoteModal').classList.remove('hidden');
    }
    
    function closeDeleteModal() {
        document.getElementById('deleteNoteModal').classList.add('hidden');
        noteToDelete = null;
    }
    
    async function deleteNote() {
        if (!noteToDelete) return;
        
        try {
            const response = await fetch(`/nota/eliminar/${noteToDelete}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                // 1. Remover la nota del DOM (Usando el selector HTMX)
                const noteElement = document.querySelector(`[hx-get="/partial/editor/${noteToDelete}"]`);
                if (noteElement) {
                    noteElement.remove();
                }
                
                // 2. Actualizar contador de notas (BLINDADO CON ID)
                const counterElement = document.getElementById('notes-counter');
                if (counterElement) {
                    const notesCount = document.querySelectorAll('.note-item').length;
                    counterElement.textContent = `${notesCount} notas`;
                }
                
                // 3. Limpiar el editor si la nota eliminada estaba abierta
                const editorPane = document.getElementById('editor-pane');
                // Verificamos si el editor actual tiene el ID de la nota borrada (opcional pero recomendable)
                // Para simplificar, si se borra, limpiamos el pane por seguridad visual
                if (editorPane) {
                    // Solo si quieres forzar el estado vacío:
                    // editorPane.innerHTML = '<div class="flex items-center justify-center h-full text-gray-500"><p>Selecciona una nota</p></div>';
                }
                
                // 4. CERRAR EL MODAL
                closeDeleteModal();
            } else {
                console.error("Respuesta del servidor no OK");
                alert('Error al eliminar la nota (Server Error)');
            }
        } catch (error) {
            console.error('Error en deleteNote:', error);
            // Si el error es de JS (como el del contador), al menos cerramos el modal
            closeDeleteModal();
            // alert('Ocurrió un error inesperado al eliminar');
        }
    }
</script>

<!-- Modal de confirmación para eliminar nota -->
<div id="deleteNoteModal" class="hidden fixed inset-0 bg-black/60 flex items-center justify-center z-[9999]" onclick="if(event.target === this) closeDeleteModal()">
    <div class="bg-[#2C2C2E] rounded-xl shadow-2xl w-full max-w-md mx-4 border border-[#3A3A3D]">
        <!-- Header -->
        <div class="px-6 py-4 border-b border-[#3A3A3D]">
            <h3 class="text-lg font-semibold text-white">Eliminar nota</h3>
        </div>
        
        <!-- Body -->
        <div class="px-6 py-4">
            <p class="text-gray-300 mb-2">¿Estás seguro de que deseas eliminar esta nota?</p>
            <p class="text-white font-medium" id="deleteNoteTitle"></p>
            <p class="text-gray-400 text-sm mt-3">Esta acción no se puede deshacer.</p>
        </div>
        
        <!-- Footer -->
        <div class="px-6 py-4 bg-[#232326] rounded-b-xl flex justify-end gap-3">
            <button 
                onclick="closeDeleteModal()"
                class="px-4 py-2 rounded-lg text-gray-300 hover:bg-[#3A3A3D] transition font-medium"
            >
                Cancelar
            </button>
            <button 
                onclick="deleteNote()"
                class="px-4 py-2 rounded-lg bg-red-500 hover:bg-red-600 text-white transition font-medium"
            >
                Eliminar
            </button>
        </div>
    </div>
</div>
```

---

## 📄 Archivo: `app/templates/partials/modales/cockpit/create_task.html`
```html
<div x-show="currentModal === 'createTask'" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm" style="display: none;">
    <div @click.outside="currentModal = null" class="bg-bgSidebar border border-borderCol w-96 rounded-lg shadow-2xl p-6">
        <h3 class="text-lg font-bold text-white mb-4"><i class="fa-solid fa-check text-accent mr-2"></i>Nueva Tarea</h3>
        <form action="{{ url_for('crear_tarea') }}" method="POST">
            <input type="text" name="titulo" placeholder="¿Qué hay que hacer?" required autofocus class="w-full bg-bgBase border border-borderCol rounded px-3 py-2 text-white focus:border-accent outline-none mb-3">
            
            <div class="grid grid-cols-2 gap-3 mb-4">
                <input type="date" name="fecha_objetivo" class="bg-bgBase border border-borderCol rounded px-3 py-2 text-gray-400 text-xs outline-none focus:border-accent">
                <select name="cuaderno_id" class="bg-bgBase border border-borderCol rounded px-3 py-2 text-gray-400 text-xs outline-none focus:border-accent">
                    <option value="">-- Sin proyecto --</option>
                    {% for cat in lista_categorias %}
                        <optgroup label="{{ cat.nombre }}">
                        {% for c in cat.cuadernos %}
                            <option value="{{ c.id }}">{{ c.nombre }}</option>
                        {% endfor %}
                        </optgroup>
                    {% endfor %}
                </select>
            </div>
            <div class="flex justify-end gap-2">
                <button type="button" @click="currentModal = null" class="px-4 py-2 text-xs text-gray-400 hover:text-white">Cancelar</button>
                <button type="submit" class="px-4 py-2 text-xs bg-accent text-white font-bold rounded hover:bg-white hover:text-black transition-colors">Añadir Tarea</button>
            </div>
        </form>
    </div>
</div>
```

---

## 📄 Archivo: `app/templates/partials/modales/cockpit/edit_task.html`
```html
<div x-data="{ tId: '', tTitulo: '', tFecha: '', tCuaderno: '' }"
     @open-edit-task.window="tId = $event.detail.id; tTitulo = $event.detail.titulo; tFecha = $event.detail.fecha; tCuaderno = $event.detail.cuadernoId; currentModal = 'editTask'"
     x-show="currentModal === 'editTask'" 
     class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm" style="display: none;">
    <div @click.outside="currentModal = null" class="bg-bgSidebar border border-borderCol w-96 rounded-lg shadow-2xl p-6">
        <h3 class="text-lg font-bold text-white mb-4">Editar Tarea</h3>
        
        <form :action="'/tarea/editar/' + tId" method="POST">
            <label class="block text-[10px] uppercase font-bold text-gray-500 mb-1">Título</label>
            <input type="text" name="titulo" x-model="tTitulo" required class="w-full bg-bgBase border border-borderCol rounded px-3 py-2 text-white focus:border-accent outline-none mb-3">
            
            <div class="grid grid-cols-2 gap-3 mb-4">
                <div>
                    <label class="block text-[10px] uppercase font-bold text-gray-500 mb-1">Fecha</label>
                    <input type="date" name="fecha_objetivo" x-model="tFecha" class="w-full bg-bgBase border border-borderCol rounded px-3 py-2 text-gray-400 text-xs outline-none focus:border-accent">
                </div>
                <div>
                    <label class="block text-[10px] uppercase font-bold text-gray-500 mb-1">Proyecto</label>
                    <select name="cuaderno_id" x-model="tCuaderno" class="w-full bg-bgBase border border-borderCol rounded px-3 py-2 text-gray-400 text-xs outline-none focus:border-accent">
                        <option value="">-- Sin asignar --</option>
                        {% for cat in lista_categorias %}
                            <optgroup label="{{ cat.nombre }}">
                            {% for c in cat.cuadernos %}
                                <option value="{{ c.id }}">{{ c.nombre }}</option>
                            {% endfor %}
                            </optgroup>
                        {% endfor %}
                    </select>
                </div>
            </div>
            
            <div class="flex justify-end gap-2">
                <button type="button" @click="currentModal = null" class="px-4 py-2 text-xs text-gray-400">Cancelar</button>
                <button type="submit" class="px-4 py-2 text-xs bg-accent text-white font-bold rounded">Guardar Cambios</button>
            </div>
        </form>
    </div>
</div>
```

---

## 📄 Archivo: `app/templates/partials/modales/cockpit/quick_note.html`
```html
<div x-show="currentModal === 'quickNote'" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm" style="display: none;">
    <div @click.outside="currentModal = null" class="bg-bgSidebar border border-borderCol w-[500px] rounded-lg shadow-2xl p-6">
        <h3 class="text-lg font-bold text-white mb-2"><i class="fa-solid fa-feather text-accentPurple mr-2"></i>Captura Rápida</h3>
        <p class="text-[10px] text-gray-500 mb-4">Se guardará en tu Inbox para procesar luego.</p>
        <form action="{{ url_for('quick_note') }}" method="POST">
            <input type="text" name="titulo" placeholder="Título..." class="w-full bg-transparent border-b border-borderCol py-2 text-white font-bold focus:border-accentPurple outline-none mb-3 text-sm">
            <textarea name="contenido" placeholder="Escribe aquí..." class="w-full bg-bgBase border border-borderCol rounded px-3 py-2 text-white mb-4 h-32 resize-none text-sm focus:border-accentPurple outline-none"></textarea>
            <div class="flex justify-end gap-2">
                <button type="button" @click="currentModal = null" class="px-4 py-2 text-xs text-gray-400 hover:text-white">Descartar</button>
                <button type="submit" class="px-4 py-2 text-xs bg-accentPurple text-white font-bold rounded hover:bg-white hover:text-black transition-colors">Guardar en Inbox</button>
            </div>
        </form>
    </div>
</div>
```

---

## 📄 Archivo: `app/templates/partials/modales/editor/move_note.html`
```html
<div x-data="{ noteId: '', noteTitle: '' }"
     @open-move-note.window="noteId = $event.detail.id; noteTitle = $event.detail.titulo; currentModal = 'moveNote'"
     x-show="currentModal === 'moveNote'" 
     class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm" style="display: none;">
    <div @click.outside="currentModal = null" class="bg-bgSidebar border border-borderCol w-96 rounded-lg shadow-2xl p-6">
        <h3 class="text-lg font-bold text-white mb-2">Mover Nota</h3>
        <p class="text-xs text-gray-500 mb-4">Mover "<span x-text="noteTitle" class="text-accent"></span>" a:</p>
        
        <form action="{{ url_for('mover_anotacion') }}" method="POST">
            <input type="hidden" name="anotacion_id" :value="noteId">
            
            <label class="block text-[10px] uppercase font-bold text-gray-500 mb-1">Cuaderno / Proyecto</label>
            <select name="tema_id" class="w-full bg-bgBase border border-borderCol rounded px-3 py-2 text-white focus:border-accent outline-none text-xs mb-4 custom-scrollbar h-40" size="5">
                {% for cat in lista_categorias %}
                    <optgroup label="{{ cat.nombre }}" class="text-gray-500 font-bold bg-[#161b22]">
                        {% for cuaderno in cat.cuadernos %}
                            <option disabled class="text-gray-400 font-bold bg-[#0d1117] pt-2">└── {{ cuaderno.nombre }}</option>
                            {% for tema in cuaderno.temas %}
                                <option value="{{ tema.id }}" class="text-white pl-6 bg-[#0d1117] py-1">⠀⠀⠀# {{ tema.nombre }}</option>
                            {% endfor %}
                        {% endfor %}
                    </optgroup>
                {% endfor %}
            </select>

            <div class="flex justify-end gap-2">
                <button type="button" @click="currentModal = null" class="px-4 py-2 text-xs text-gray-400 hover:text-white">Cancelar</button>
                <button type="submit" class="px-4 py-2 text-xs bg-accent text-white font-bold rounded">Mover</button>
            </div>
        </form>
    </div>
</div>
```

---

## 📄 Archivo: `app/templates/partials/modales/global/omnibar.html`
```html
<div x-show="openOmnibar" 
     x-transition.opacity 
     class="fixed inset-0 z-[100] bg-black/70 backdrop-blur-sm flex items-start justify-center pt-[15vh]"
     style="display: none;">
    
    <div @click.outside="openOmnibar = false" class="w-full max-w-2xl bg-[#161b22] border border-borderCol rounded-xl shadow-2xl overflow-hidden flex flex-col max-h-[60vh]">
        
        <div class="flex items-center px-4 py-3 border-b border-borderCol">
            <i class="fa-solid fa-magnifying-glass text-accent text-lg mr-3"></i>
            
            <input x-ref="omnibarInput"
                type="text" 
                name="q" 
                autocomplete="off"
                class="flex-1 bg-transparent text-lg text-white placeholder-gray-500 focus:outline-none"
                placeholder="Buscar nota, comando o tema..."
                hx-get="/partial/omnibar_search" 
                hx-trigger="keyup changed delay:200ms, search" 
                hx-target="#omnibar-results"
                @keydown.enter.prevent="selectFirstOmnibarItem($el)">
            
            <span class="text-xs text-gray-600 border border-borderCol px-2 py-0.5 rounded">ESC</span>
        </div>
        
        <div id="omnibar-results" class="flex-1 overflow-y-auto bg-bgBase">
            <div class="py-10 text-center text-gray-600">
                <p class="text-sm">Escribe para buscar...</p>
            </div>
        </div>
        
        <div class="bg-[#161b22] px-3 py-1.5 border-t border-borderCol flex justify-between items-center text-[10px] text-gray-500">
            <span><strong class="text-gray-400">Enter</strong> para seleccionar el primero</span>
            <span>Docs.ai Quick Switcher</span>
        </div>
    </div>
</div>
```

---

## 📄 Archivo: `app/templates/partials/modales/global/security.html`
```html
<!-- Modal Unsaved Changes -->
<div id="modalUnsaved" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 backdrop-blur-sm hidden opacity-0 transition-opacity duration-200">
    <div class="bg-bgSidebar border border-borderCol w-96 rounded-lg shadow-2xl p-6 transform scale-95 transition-transform duration-200" id="modalUnsavedContent">
        <div class="flex flex-col items-center text-center">
            <i class="fa-solid fa-triangle-exclamation text-yellow-500 text-3xl mb-3"></i>
            <h3 class="text-lg font-bold text-white mb-2">Cambios pendientes</h3>
            <p class="text-xs text-gray-400 mb-6">Si sales ahora perderás lo último que escribiste.</p>
            <div class="flex flex-col w-full gap-2">
                <button id="btnSaveAndLeave" class="w-full py-2 text-xs bg-accent text-white font-bold rounded hover:bg-accentHover transition-colors">Guardar y Salir</button>
                <button id="btnDiscard" class="w-full py-2 text-xs text-red-400 border border-red-900/50 hover:bg-red-900/20 rounded transition-colors">Descartar cambios</button>
                <button id="btnCancelUnsaved" class="w-full py-2 text-xs text-gray-500 hover:text-white transition-colors">Cancelar</button>
            </div>
        </div>
    </div>
</div>

<!-- Modal Delete Confirmation -->
<div id="modalDelete" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 backdrop-blur-sm hidden opacity-0 transition-opacity duration-200">
    <div class="bg-bgSidebar border border-borderCol w-96 rounded-lg shadow-2xl p-6 transform scale-95 transition-transform duration-200" id="modalDeleteContent">
        <div class="flex flex-col items-center text-center">
            <div class="w-12 h-12 rounded-full bg-red-900/20 flex items-center justify-center mb-4 border border-red-500/20">
                <i class="fa-solid fa-trash text-red-500"></i>
            </div>
            <h3 id="modalDelTitle" class="text-lg font-bold text-white mb-2">¿Eliminar?</h3>
            <p id="modalDelMsg" class="text-xs text-gray-400 mb-6">Esta acción es irreversible.</p>
            <div class="flex gap-3 w-full">
                <button onclick="hideDeleteModal()" class="flex-1 py-2 text-xs text-gray-400 hover:text-white border border-borderCol rounded transition-colors">Cancelar</button>
                <button id="btnConfirmDeleteAction" class="flex-1 py-2 text-xs bg-red-500/10 text-red-500 border border-red-500/50 hover:bg-red-500 hover:text-white font-bold rounded transition-colors">Eliminar</button>
            </div>
        </div>
    </div>
</div>
```

---

## 📄 Archivo: `app/templates/partials/modales/list/create_topic.html`
```html
<div x-data="{ notebookId: '' }"
     @open-create-topic.window="notebookId = $event.detail.id; currentModal = 'createTopic'"
     x-show="currentModal === 'createTopic'" 
     class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm" style="display: none;">
    <div @click.outside="currentModal = null" class="bg-bgSidebar border border-borderCol w-96 rounded-lg shadow-2xl p-6">
        <h3 class="text-lg font-bold text-white mb-4">Nuevo Tema</h3>
        <form :action="'/tema/crear/' + notebookId" method="POST">
            <input type="text" name="nombre" placeholder="Nombre del tema" required autofocus class="w-full bg-bgBase border border-borderCol rounded px-3 py-2 text-white focus:border-accent outline-none mb-4">
            <div class="flex justify-end gap-2">
                <button type="button" @click="currentModal = null" class="px-4 py-2 text-xs text-gray-400 hover:text-white">Cancelar</button>
                <button type="submit" class="px-4 py-2 text-xs bg-accent text-white font-bold rounded">Crear</button>
            </div>
        </form>
    </div>
</div>
```

---

## 📄 Archivo: `app/templates/partials/modales/list/edit_topic.html`
```html
<div x-data="{ id: '', nombre: '' }"
     @open-edit-topic.window="id = $event.detail.id; nombre = $event.detail.nombre; currentModal = 'editTopic'"
     x-show="currentModal === 'editTopic'" 
     class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm" style="display: none;">
    <div @click.outside="currentModal = null" class="bg-bgSidebar border border-borderCol w-96 rounded-lg shadow-2xl p-6">
        <h3 class="text-lg font-bold text-white mb-4">Renombrar Tema</h3>
        <form :action="'/tema/editar/' + id" method="POST">
            <input type="text" name="nombre" x-model="nombre" required class="w-full bg-bgBase border border-borderCol rounded px-3 py-2 text-white mb-4 focus:border-accent outline-none">
            <div class="flex justify-end gap-2">
                <button type="button" @click="currentModal = null" class="px-4 py-2 text-xs text-gray-400 hover:text-white">Cancelar</button>
                <button type="submit" class="px-4 py-2 text-xs bg-accent text-white font-bold rounded">Guardar</button>
            </div>
        </form>
    </div>
</div>
```

---

## 📄 Archivo: `app/templates/partials/modales/sidebar/create_category.html`
```html
<div x-show="currentModal === 'createCategory'" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm" style="display: none;">
    <div @click.outside="currentModal = null" class="bg-bgSidebar border border-borderCol w-80 rounded-xl shadow-2xl p-5">
        <h3 class="text-lg font-bold text-white mb-4"><i class="fa-solid fa-layer-group mr-2 text-accentPurple"></i>Nueva Biblioteca</h3>
        <form action="{{ url_for('crear_categoria') }}" method="POST">
            <label class="block text-[10px] uppercase font-bold text-gray-500 mb-1">Nombre</label>
            <input type="text" name="nombre" required autofocus class="w-full bg-bgBase border border-borderCol rounded px-3 py-2 text-white focus:border-accentPurple outline-none mb-4 text-xs">
            
            <label class="block text-[10px] uppercase font-bold text-gray-500 mb-1">Icono</label>
            <div class="grid grid-cols-5 gap-2 mb-6">
                {% for icon in ['folder', 'code', 'graduation-cap', 'briefcase', 'chess','inbox','chalkboard-teacher','school','microchip','film','music','tools','robot','industry','microscope'] %}
                <label class="cursor-pointer">
                    <input type="radio" name="icono" value="{{ icon }}" {{ 'checked' if icon=='folder' }} class="peer sr-only">
                    <div class="w-8 h-8 rounded bg-bgBase border border-borderCol flex items-center justify-center text-gray-500 peer-checked:bg-accentPurple peer-checked:text-white peer-checked:border-accentPurple transition-all">
                        <i class="fa-solid fa-{{ icon }}"></i>
                    </div>
                </label>
                {% endfor %}
            </div>

            <div class="flex justify-end gap-2">
                <button type="button" @click="currentModal = null" class="px-4 py-2 text-xs text-gray-400 hover:text-white">Cancelar</button>
                <button type="submit" class="px-4 py-2 text-xs bg-accentPurple text-white font-bold rounded hover:bg-white hover:text-black transition-colors">Crear</button>
            </div>
        </form>
    </div>
</div>
```

---

## 📄 Archivo: `app/templates/partials/modales/sidebar/edit_category.html`
```html
<div x-data="{ cId: '', cNombre: '', cIcono: 'folder' }"
    @open-edit-category.window="cId = $event.detail.id; cNombre = $event.detail.nombre; cIcono = $event.detail.icono; currentModal = 'editCategory'"
    x-show="currentModal === 'editCategory'"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm" style="display: none;">
    <div @click.outside="currentModal = null" class="bg-bgSidebar border border-borderCol w-80 rounded-xl shadow-2xl p-5">
        <h3 class="text-lg font-bold text-white mb-4">Editar Biblioteca</h3>

        <form :action="'/categoria/editar/' + cId" method="POST">
            <label class="block text-[10px] uppercase font-bold text-gray-500 mb-1">Nombre</label>
            <input type="text" name="nombre" x-model="cNombre" required class="w-full bg-bgBase border border-borderCol rounded px-3 py-2 text-white focus:border-accentPurple outline-none mb-4 text-xs">

            <label class="block text-[10px] uppercase font-bold text-gray-500 mb-1">Icono</label>
            <div class="grid grid-cols-5 gap-2 mb-6">
                {% for icon in ['folder', 'code', 'graduation-cap', 'briefcase', 'chess','inbox','chalkboard-teacher','school','microchip','film','music','tools','robot','industry','microscope'] %}
                <label class="cursor-pointer">
                    <input type="radio" name="icono" value="{{ icon }}" x-model="cIcono" class="peer sr-only">
                    <div class="w-8 h-8 rounded bg-bgBase border border-borderCol flex items-center justify-center text-gray-500 peer-checked:bg-accentPurple peer-checked:text-white peer-checked:border-accentPurple transition-all">
                        <i class="fa-solid fa-{{ icon }}"></i>
                    </div>
                </label>
                {% endfor %}
            </div>

            <div class="flex justify-between items-center pt-4 border-t border-white/5">
                <button type="button"
                        onclick="if(confirm('¡CUIDADO!\n\nSe eliminarán TODOS los cuadernos y notas dentro de esta biblioteca.\n\n¿Estás seguro?')) { document.getElementById('formDeleteCat').submit(); }"
                        class="text-xs text-red-500 hover:text-red-400 hover:underline flex items-center gap-1">
                    <i class="fa-solid fa-trash"></i> Eliminar
                </button>

                <div class="flex gap-2">
                    <button type="button" @click="currentModal = null" class="px-3 py-1.5 text-xs text-gray-400 hover:text-white">Cancelar</button>
                    <button type="submit" class="px-3 py-1.5 text-xs bg-accentPurple text-white font-bold rounded hover:bg-white hover:text-black transition-colors">Guardar</button>
                </div>
            </div>
        </form>
        <form id="formDeleteCat" :action="'/categoria/eliminar/' + cId" method="POST" class="hidden"></form>
    </div>
</div>
```

---

## 📄 Archivo: `app/templates/partials/modales/sidebar/manage_notebook.html`
```html
<div x-show="currentModal === 'createNotebook' || currentModal === 'editNotebook'" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm" style="display: none;">
    <div @click.outside="currentModal = null" class="bg-bgSidebar border border-borderCol w-96 rounded-lg shadow-2xl p-6" x-data="{ id: '', nombre: '', desc: '', tipo: 'cuaderno', fecha: '', catId: '' }" @open-edit-notebook.window="id=$event.detail.id; nombre=$event.detail.nombre; desc=$event.detail.desc; tipo=$event.detail.tipo; fecha=$event.detail.fecha; catId=$event.detail.catId; currentModal='editNotebook'">
        <h3 class="text-lg font-bold text-white mb-4" x-text="currentModal==='createNotebook'?'Nuevo Cuaderno':'Configurar Cuaderno'"></h3>
        <form :action="currentModal==='createNotebook' ? '{{ url_for('crear_cuaderno') }}' : '/cuaderno/editar/'+id" method="POST">
            <label class="block text-[10px] uppercase font-bold text-gray-500 mb-1">Nombre</label>
            <input type="text" name="nombre" x-model="nombre" required class="w-full bg-bgBase border border-borderCol rounded px-3 py-2 text-white focus:border-accent outline-none mb-3 text-xs">
            <div class="grid grid-cols-2 gap-3 mb-3">
                <div>
                    <label class="block text-[10px] uppercase font-bold text-gray-500 mb-1">Tipo</label>
                    <select name="tipo" x-model="tipo" class="w-full bg-bgBase border border-borderCol rounded px-3 py-2 text-white focus:border-accent outline-none text-xs">
                        <option value="cuaderno">Cuaderno</option>
                        <option value="proyecto">Proyecto</option>
                    </select>
                </div>
                <div>
                    <label class="block text-[10px] uppercase font-bold text-gray-500 mb-1">Biblioteca</label>
                    <select name="categoria_id" class="w-full bg-bgBase border border-borderCol rounded px-3 py-2 text-white focus:border-accent outline-none text-xs">
                        {% for cat in lista_categorias %}
                        <option value="{{ cat.id }}" :selected="catId == '{{cat.id}}'">{{ cat.nombre }}</option>
                        {% endfor %}
                    </select>
                </div>
            </div>
            <div x-show="tipo === 'proyecto'" class="mb-3">
                <label class="block text-[10px] uppercase font-bold text-gray-500 mb-1">Fecha Límite</label>
                <input type="date" name="fecha_limite" x-model="fecha" class="w-full bg-bgBase border border-borderCol rounded px-3 py-2 text-white focus:border-accent outline-none text-xs">
            </div>
            <label class="block text-[10px] uppercase font-bold text-gray-500 mb-1">Descripción</label>
            <textarea name="descripcion" x-model="desc" class="w-full bg-bgBase border border-borderCol rounded px-3 py-2 text-white focus:border-accent outline-none mb-4 text-xs h-16 resize-none"></textarea>
            <div class="flex justify-end gap-2">
                <button type="button" @click="currentModal = null" class="px-4 py-2 text-xs text-gray-400 hover:text-white">Cancelar</button>
                <button type="submit" class="px-4 py-2 text-xs bg-accent text-white font-bold rounded hover:bg-white hover:text-black transition-colors">Guardar</button>
            </div>
        </form>
    </div>
</div>
```

---

## 📄 Archivo: `app/templates/partials/omnibar_results.html`
```html
<!-- app/templates/partials/omnibar_results.html -->

<!-- COMANDOS TÁCTICOS -->
{% if acciones %}
    <div class="py-2">
        <p class="px-3 text-[10px] font-bold text-accent uppercase tracking-wider mb-2">Comandos</p>
        {% for accion in acciones %}
            
            {% if accion.tipo == 'comando' %}
            <button hx-post="{{ accion.hx_post }}" 
                    hx-vals='{{ accion.payload | tojson | safe }}'
                    hx-swap="none"
                    @click="openOmnibar = false"
                    {% if loop.first %}id="omnibar-first-item"{% endif %}
                    class="js-omnibar-item w-full text-left px-3 py-2 mx-2 rounded hover:bg-accent/10 hover:text-white group cursor-pointer transition-colors border border-transparent hover:border-accent/20 flex items-center gap-3 outline-none focus:bg-accent/10">
                <div class="w-8 h-8 rounded bg-[#21262d] flex items-center justify-center text-accent group-hover:bg-accent group-hover:text-white transition-colors">
                    <i class="fa-solid fa-{{ accion.icono }}"></i>
                </div>
                <div>
                    <span class="font-bold text-sm text-gray-200 group-hover:text-accent block">{{ accion.titulo }}</span>
                    <span class="text-[10px] text-gray-500">{{ accion.subtitulo }}</span>
                </div>
            </button>

            {% elif accion.tipo == 'modal' %}
            <button @click="currentModal = '{{ accion.modal_name }}'; openOmnibar = false;" 
                    {% if loop.first %}id="omnibar-first-item"{% endif %}
                    class="js-omnibar-item w-full text-left px-3 py-2 mx-2 rounded hover:bg-accent/10 hover:text-white group cursor-pointer transition-colors border border-transparent hover:border-accent/20 flex items-center gap-3 outline-none focus:bg-accent/10">
                <div class="w-8 h-8 rounded bg-[#21262d] flex items-center justify-center text-accentPurple group-hover:bg-accentPurple group-hover:text-white transition-colors">
                    <i class="fa-solid fa-{{ accion.icono }}"></i>
                </div>
                <div>
                    <span class="font-bold text-sm text-gray-200 group-hover:text-accentPurple block">{{ accion.titulo }}</span>
                    <span class="text-[10px] text-gray-500">{{ accion.subtitulo }}</span>
                </div>
            </button>
            {% endif %}

        {% endfor %}
    </div>
{% endif %}

<!-- RESULTADOS DE BÚSQUEDA -->
{% if resultados %}
    <div class="py-2 border-t border-white/5">
        <p class="px-3 text-[10px] font-bold text-gray-500 uppercase tracking-wider mb-2 mt-1">Notas Encontradas</p>
        {% for nota in resultados %}
        <!-- CORRECCIÓN AQUÍ: Target correcto y evento para Inspector -->
        <a href="#" 
           hx-get="/partial/editor/{{ nota.id }}"
           hx-target="#editor-pane"
           hx-swap="innerHTML"
           hx-on::after-request="if(event.detail.successful) { htmx.ajax('GET', '/partial/inspector/{{ nota.id }}', {target: '#inspector-content'}); inspectorOpen = true; showList = false; }"
           @click="openOmnibar = false;" 
           {% if loop.first and not acciones %}id="omnibar-first-item"{% endif %}
           class="js-omnibar-item block px-3 py-2 mx-2 rounded hover:bg-[#21262d] hover:text-white group cursor-pointer transition-colors border border-transparent hover:border-borderCol outline-none focus:bg-[#21262d]">
            
            <div class="flex justify-between items-center">
                <span class="font-bold text-sm text-gray-300 group-hover:text-white">{{ nota.titulo or 'Sin título' }}</span>
                <span class="text-[10px] text-gray-600 font-mono">
                    {{ nota.cuaderno_nombre }} / {{ nota.tema_nombre }}
                </span>
            </div>
        </a>
        {% endfor %}
    </div>
{% elif not acciones and not resultados %}
    <div class="py-8 text-center text-gray-600">
        <p class="text-xs">No se encontraron coincidencias.</p>
        <p class="text-[10px] mt-2 opacity-50">Prueba comandos como <span class="text-accent">/tarea</span> o <span class="text-accent">/nota</span></p>
    </div>
{% endif %}
```

---

## 📄 Archivo: `app/templates/register.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crear Cuenta - Docs.ai</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body class="bg-slate-50 min-h-screen flex items-center justify-center p-4">

    <div class="w-full max-w-md bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-100">
        <!-- Header -->
        <div class="bg-blue-600 p-8 text-center">
            <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-white/20 mb-4 text-white">
                <i class="fa-solid fa-feather-pointed text-2xl"></i>
            </div>
            <h1 class="text-2xl font-bold text-white tracking-wide">Docs.ai</h1>
            <p class="text-blue-100 text-sm mt-1">Tu segundo cerebro digital</p>
        </div>

        <div class="p-8">
            <h2 class="text-xl font-semibold text-slate-800 text-center mb-6">Crea tu cuenta</h2>

            <!-- Alerta de Error (Jinja2 Logic) -->
            {% if request.query_params.get('error') == 'exists' %}
            <div class="mb-6 bg-red-50 border-l-4 border-red-500 p-4 rounded-r shadow-sm">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <i class="fa-solid fa-circle-exclamation text-red-500"></i>
                    </div>
                    <div class="ml-3">
                        <p class="text-sm text-red-700">
                            Ese correo ya está registrado.
                            <a href="/login" class="font-bold underline hover:text-red-800">¿Iniciar sesión?</a>
                        </p>
                    </div>
                </div>
            </div>
            {% endif %}

            <!-- Formulario -->
            <form action="/register" method="POST" class="space-y-5">
                
                <!-- Nombre -->
                <div>
                    <label for="nombre" class="block text-sm font-medium text-slate-700 mb-1">Nombre Completo</label>
                    <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <i class="fa-regular fa-user text-slate-400"></i>
                        </div>
                        <input type="text" name="nombre" id="nombre" required placeholder="Ej: Andrés Benítez"
                            class="pl-10 block w-full rounded-lg border-slate-300 border bg-slate-50 p-2.5 text-sm focus:ring-blue-500 focus:border-blue-500 transition-colors shadow-sm" />
                    </div>
                </div>

                <!-- Email -->
                <div>
                    <label for="email" class="block text-sm font-medium text-slate-700 mb-1">Correo Electrónico</label>
                    <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <i class="fa-regular fa-envelope text-slate-400"></i>
                        </div>
                        <input type="email" name="email" id="email" required placeholder="usuario@empresa.com"
                            class="pl-10 block w-full rounded-lg border-slate-300 border bg-slate-50 p-2.5 text-sm focus:ring-blue-500 focus:border-blue-500 transition-colors shadow-sm" />
                    </div>
                </div>

                <!-- Password -->
                <div>
                    <label for="password" class="block text-sm font-medium text-slate-700 mb-1">Contraseña</label>
                    <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <i class="fa-solid fa-lock text-slate-400"></i>
                        </div>
                        <input type="password" name="password" id="password" required placeholder="••••••••"
                            class="pl-10 block w-full rounded-lg border-slate-300 border bg-slate-50 p-2.5 text-sm focus:ring-blue-500 focus:border-blue-500 transition-colors shadow-sm" />
                    </div>
                    <p class="mt-1 text-xs text-slate-400">Mínimo 6 caracteres recomendados.</p>
                </div>

                <!-- Submit Button -->
                <button type="submit" 
                    class="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all transform hover:-translate-y-0.5">
                    Registrarse y Comenzar
                </button>
            </form>
        </div>

        <!-- Footer -->
        <div class="bg-slate-50 px-8 py-4 border-t border-slate-100 text-center">
            <p class="text-sm text-slate-600">
                ¿Ya tienes una cuenta? 
                <a href="/login" class="font-medium text-blue-600 hover:text-blue-500 transition-colors">
                    Inicia sesión aquí
                </a>
            </p>
        </div>
    </div>

</body>
</html>
```

---

## 📄 Archivo: `requirements.txt`
```txt
fastapi
uvicorn
pydantic
python-dotenv
sqlmodel
sqlalchemy
supabase
python-jose[cryptography]
jinja2
# Corrección manual de librerías:
bcrypt
python-multipart
asyncpg
requests
```

---

