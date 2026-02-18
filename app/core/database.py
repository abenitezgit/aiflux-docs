from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from app.core.config import settings
from typing import AsyncGenerator
from supabase import create_client, Client
import os

SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_KEY = settings.SUPABASE_KEY

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


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
    pool_pre_ping=True,
    pool_recycle=300, # Recicla conexiones cada 5 min para evitar cierres de Supabase
    connect_args={
        "statement_cache_size": 0,
        "timeout": 60, # 60 segundos es generoso para el handshake SSL
    }
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