# CONTEXTO DEL PROYECTO: proyecto-docs
Generado automáticamente para revisión de código.

## 📁 Estructura del Proyecto
```
    📄 requirements.txt
    📂 .docs/
        📄 1_ARQUITECTURA.md
        📄 0_REFERENCIA_LEGACY.md
        📄 2_ESTADO_ACTUAL.md
    📂 app/
        📄 models.py
        📄 __init__.py
        📄 main.py
        📂 routers/
        📂 core/
            📄 auth.py
            📄 config.py
            📄 database.py
            📄 security.py
        📂 models/
        📂 services/
    📂 templates/
        📂 layouts/
            📄 base.html
        📂 modules/
        📂 pages/
        📂 partials/
```

---

## 📄 Archivo: `app/__init__.py`
```py

```

---

## 📄 Archivo: `app/core/auth.py`
```py
from typing import Optional
from fastapi import Request, Depends, HTTPException, status
from jose import jwt, JWTError
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.core.config import settings
from app.core.database import get_db
from app.core.security import verify_password
from app.models import UsuarioDB

# Dependencia para obtener el usuario desde la Cookie
async def get_current_user(
    request: Request, 
    session: AsyncSession = Depends(get_db)
) -> Optional[UsuarioDB]:
    token = request.cookies.get("access_token")
    if not token:
        return None
    
    # Limpieza del token (Bearer ...)
    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
    except JWTError:
        return None

    # Buscar usuario en DB
    try:
        u_uuid = uuid.UUID(user_id)
        result = await session.exec(select(UsuarioDB).where(UsuarioDB.id == u_uuid))
        user = result.first()
        return user
    except (ValueError, Exception):
        return None

# Dependencia estricta (lanza error si no hay usuario)
async def get_authenticated_user(user: Optional[UsuarioDB] = Depends(get_current_user)):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Función de Login
async def authenticate_user(session: AsyncSession, email: str, password: str) -> Optional[UsuarioDB]:
    statement = select(UsuarioDB).where(UsuarioDB.email == email)
    result = await session.exec(statement)
    user = result.first()
    
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
```

---

## 📄 Archivo: `app/core/config.py`
```py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Docs.ai"
    VERSION: str = "2.0.0"
    
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 días

    # External
    SUPABASE_URL: str | None = None
    SUPABASE_KEY: str | None = None

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
```

---

## 📄 Archivo: `app/core/database.py`
```py
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from app.core.config import settings
from typing import AsyncGenerator

# 1. Ajuste de URL para Asyncpg
db_url = settings.DATABASE_URL
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif db_url and db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# 2. Motor Asíncrono
# statement_cache_size=0 es crítico para Supabase/PgBouncer
engine = create_async_engine(
    db_url,
    echo=False,
    future=True,
    connect_args={"statement_cache_size": 0}
)

# 3. Factoría de Sesiones
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# 4. Inyección de Seguridad (RLS)
async def init_rls(session: AsyncSession, user_id: str):
    """Inyecta el ID del usuario en la sesión para las políticas de seguridad de la DB"""
    if user_id:
        # Sanitización básica: asegurar que sea un UUID válido o string seguro
        await session.execute(text(f"SET LOCAL app.current_user_id = '{user_id}'"))

# 5. Dependencia para FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
```

---

## 📄 Archivo: `app/core/security.py`
```py
from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Configuración de Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
```

---

## 📄 Archivo: `app/main.py`
```py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel

from app.core.database import engine
from app.core.config import settings

# Importar modelos para que SQLModel los reconozca al crear tablas
from app.models import * 

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas al inicio
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# Montar estáticos (CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates") 

@app.get("/")
async def root(request: Request): # <--- Modificar root
    # Renderizamos el layout base
    return templates.TemplateResponse("layouts/base.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
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

# --- USUARIO ---
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

# --- CATEGORÍA (Biblioteca) ---
class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
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

# --- CUADERNO / PROYECTO ---
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
    
    # Campos específicos de Proyecto
    tipo: str = Field(default="cuaderno")  # 'cuaderno' | 'proyecto'
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
    cuaderno: Optional[Cuaderno] = Relationship(back_populates="tareas")

# --- TEMA ---
class Tema(SQLModel, table=True):
    __tablename__ = "temas"
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    user_id: uuid.UUID = Field(nullable=False, index=True)
    nombre: str
    orden: int = Field(default=0)
    cuaderno_id: uuid.UUID = Field(foreign_key="cuadernos.id")
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )
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
    user_id: uuid.UUID = Field(nullable=False, index=True)
    titulo: str
    contenido: Optional[str] = None # HTML / JSON
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
    user_id: uuid.UUID = Field(nullable=False, index=True)
    url: str
    nombre_original: Optional[str] = None
    tipo_archivo: Optional[str] = None
    anotacion_id: uuid.UUID = Field(foreign_key="anotaciones.id")
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )
    anotacion: Optional[Anotacion] = Relationship(back_populates="adjuntos")
```

---

## 📄 Archivo: `requirements.txt`
```txt
fastapi
uvicorn[standard]
pydantic
pydantic-settings
sqlmodel
asyncpg
python-dotenv
python-jose[cryptography]
passlib[bcrypt]
python-multipart
jinja2
supabase


```

---

## 📄 Archivo: `templates/layouts/base.html`
```html
<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Docs.ai</title>
    
    <!-- Tailwind CSS (CDN para desarrollo rápido) -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Configuración Tailwind (Colores Dark Mode exactos) -->
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        bgBase: '#0f111a', 
                        bgSidebar: '#161b22', 
                        bgList: '#1c2128', 
                        borderCol: '#30363d', 
                        accent: '#3b82f6'
                    },
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                    }
                }
            }
        }
    </script>

    <!-- Estilos Custom (Grid) -->
    <link rel="stylesheet" href="/static/css/styles.css">
    
    <!-- Fonts & Icons -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    
    <!-- HTMX & Alpine -->
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <script src="//unpkg.com/alpinejs" defer></script>
    
    <!-- Nuestra App Logic -->
    <script src="/static/js/app.js"></script>
</head>

<body class="bg-bgBase text-gray-300 h-screen w-screen overflow-hidden" x-data="layout()">

    <!-- EL GRID MAESTRO -->
    <div class="app-grid">
        
        <!-- COL 1: SIDEBAR -->
        <aside class="bg-bgSidebar border-r border-borderCol flex flex-col overflow-hidden relative">
            <div class="p-4 border-b border-borderCol">
                <h1 class="font-bold text-white tracking-wide">Docs.ai</h1>
            </div>
            <div class="p-4 text-xs text-gray-500">
                Sidebar Area
            </div>
            <!-- Bloque para inyección HTMX futuro -->
            <div id="sidebar-content" class="flex-1 overflow-y-auto"></div>
        </aside>

        <!-- RESIZER A -->
        <div class="resizer" @mousedown="startResize($event, 'sidebar')"></div>

        <!-- COL 2: LISTA -->
        <aside class="bg-bgList border-r border-borderCol flex flex-col overflow-hidden relative">
            <div class="p-4 border-b border-borderCol">
                <h2 class="font-semibold text-sm">Lista</h2>
            </div>
            <div class="p-4 text-xs text-gray-500">
                List Area
            </div>
            <!-- Bloque para inyección HTMX futuro -->
            <div id="list-content" class="flex-1 overflow-y-auto"></div>
        </aside>

        <!-- RESIZER B -->
        <div class="resizer" @mousedown="startResize($event, 'list')"></div>

        <!-- COL 3: MAIN (EDITOR + INSPECTOR) -->
        <main class="bg-bgBase flex flex-col overflow-hidden relative">
            <div class="p-4 border-b border-borderCol flex justify-between">
                <h2 class="font-semibold text-sm">Editor</h2>
                <span class="text-xs text-gray-500">Inspector Toggle</span>
            </div>
            <div class="flex-1 flex items-center justify-center text-gray-600">
                <div class="text-center">
                    <i class="fa-solid fa-layer-group text-4xl mb-4 opacity-20"></i>
                    <p>Grid Layout Activo</p>
                </div>
            </div>
        </main>

    </div>

</body>
</html>
```

---

